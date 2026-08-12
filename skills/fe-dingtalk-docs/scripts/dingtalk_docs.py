#!/usr/bin/env python3
"""
钉钉文档 CLI — fe-dingtalk-docs skill 唯一执行入口。

职责：
  - 通过 Cookie 认证读取 alidocs.dingtalk.com 页面
  - 只读：解析链接、读取页面 HTML、提取标题/正文/内嵌 JSON 文本
  - 不提供任何新建、更新、删除、移动、写表格、改权限命令

退出码：
  - 0：成功
  - 1：一般错误（参数、解析、业务逻辑）
  - 2：鉴权失败（Cookie 过期或未配置）
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
from html import unescape
from html.parser import HTMLParser
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, quote, unquote, urlencode, urljoin, urlparse, urlunparse


# ---------------------------------------------------------------------------
# 路径与常量
# ---------------------------------------------------------------------------

SKILL_ROOT = Path(__file__).resolve().parent.parent
COOKIE_FILE = SKILL_ROOT / "credentials" / "cookie.txt"
CONFIG_FILE = SKILL_ROOT / "credentials" / "config.json"

DEFAULT_UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
)

AUTH_ERROR_MARKERS = (
    "login.dingtalk.com",
    "passport.dingtalk.com",
    "请先登录",
    "登录钉钉",
    "无权限",
    "access denied",
    "Access Denied",
)

TEXT_KEYS = {
    "title",
    "name",
    "text",
    "content",
    "body",
    "description",
    "summary",
    "markdown",
    "plainText",
    "plain_text",
}

FOLLOW_PATH_KEYWORDS = ("/note/", "/edit/", "/doc/", "/docs/", "/i/nodes/")
SHELL_TEXT_MARKERS = (
    "钉钉文档",
    "DingTalk",
    "加载中",
    "请稍候",
    "enable JavaScript",
)


class AuthError(Exception):
    """Cookie 无效、过期或当前账号无权限时抛出；CLI 层映射为 exit code 2。"""


# ---------------------------------------------------------------------------
# Cookie 与配置
# ---------------------------------------------------------------------------


def read_config_file() -> dict[str, str]:
    """读取 credentials/config.json，不存在则返回空 dict。"""
    if CONFIG_FILE.exists():
        data = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
        return {str(k): str(v) for k, v in data.items()}
    return {}


def write_config_file(cfg: dict[str, str]) -> None:
    """写入 credentials/config.json（UTF-8，缩进 2）。"""
    CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
    CONFIG_FILE.write_text(
        json.dumps(cfg, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def load_config() -> dict[str, str]:
    """加载运行配置，优先级：环境变量 > config.json > 默认值。"""
    cfg: dict[str, str] = {
        "base_url": "https://alidocs.dingtalk.com",
        "user_agent": DEFAULT_UA,
    }
    cfg.update(read_config_file())
    cfg["base_url"] = os.environ.get("DINGTALK_DOCS_BASE_URL", cfg["base_url"]).rstrip("/")
    cfg["user_agent"] = os.environ.get("DINGTALK_DOCS_USER_AGENT", cfg["user_agent"])
    return cfg


def load_cookie() -> str:
    """加载 Cookie，优先级：环境变量 DINGTALK_DOCS_COOKIE > credentials/cookie.txt。"""
    if os.environ.get("DINGTALK_DOCS_COOKIE"):
        return os.environ["DINGTALK_DOCS_COOKIE"].strip()
    if COOKIE_FILE.exists():
        return COOKIE_FILE.read_text(encoding="utf-8").strip()
    raise AuthError(
        f"Cookie 未配置。请将浏览器 Cookie 写入 {COOKIE_FILE}，"
        "或在对话中粘贴 Cookie 后由 AI 更新 credentials/cookie.txt"
    )


def save_cookie(cookie: str) -> None:
    """保存 Cookie 到文件，权限设为 600（仅当前用户可读）。"""
    COOKIE_FILE.parent.mkdir(parents=True, exist_ok=True)
    COOKIE_FILE.write_text(cookie.strip(), encoding="utf-8")
    os.chmod(COOKIE_FILE, 0o600)


# ---------------------------------------------------------------------------
# URL 解析
# ---------------------------------------------------------------------------


def require_alidocs_url(url: str) -> None:
    """校验 URL 必须来自 alidocs.dingtalk.com。"""
    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https") or parsed.netloc != "alidocs.dingtalk.com":
        raise SystemExit(f"URL 不是钉钉文档域名: {url}")


def parse_iframe_query(query: dict[str, list[str]]) -> dict[str, str]:
    """解析 iframeQuery 中二次编码的参数。"""
    iframe_values = query.get("iframeQuery") or []
    if not iframe_values:
        return {}
    iframe_query = parse_qs(unquote(iframe_values[0]), keep_blank_values=True)
    return {k: v[0] for k, v in iframe_query.items() if v}


def normalize_url(url: str) -> str:
    """保留读取必需参数，移除 IM/埋点类参数，生成更干净的 URL。"""
    parsed = urlparse(url)
    query = parse_qs(parsed.query, keep_blank_values=True)
    keep_keys = {"corpId", "iframeQuery", "sideCollapsed"}
    clean_query = {
        key: values
        for key, values in query.items()
        if key in keep_keys or key in {"sheetId", "viewId"}
    }
    return urlunparse(
        (
            parsed.scheme,
            parsed.netloc,
            parsed.path,
            "",
            urlencode(clean_query, doseq=True, quote_via=quote),
            "",
        )
    )


def normalize_candidate_url(url: str) -> str:
    """标准化候选读取 URL，去掉 fragment 并保留原查询。"""
    parsed = urlparse(url)
    return urlunparse((parsed.scheme, parsed.netloc, parsed.path, "", parsed.query, ""))


def parse_dingtalk_url(url: str) -> dict[str, str]:
    """解析钉钉文档 URL，提取 node_id、corpId、sheetId、viewId 等字段。"""
    require_alidocs_url(url)
    parsed = urlparse(url)
    parts = [p for p in parsed.path.split("/") if p]
    if len(parts) < 3 or parts[0] != "i" or parts[1] not in {"nodes", "note"}:
        raise SystemExit(f"暂只支持 /i/nodes/{{nodeId}} 或 /i/note/{{nodeId}} 链接: {url}")

    query = parse_qs(parsed.query, keep_blank_values=True)
    iframe = parse_iframe_query(query)
    result = {
        "node_id": parts[2],
        "corp_id": (query.get("corpId") or [""])[0],
        "sheet_id": (query.get("sheetId") or [iframe.get("sheetId", "")])[0],
        "view_id": (query.get("viewId") or [iframe.get("viewId", "")])[0],
        "iframe_entrance": iframe.get("entrance", ""),
        "source": iframe.get("source", ""),
        "clean_url": normalize_url(url),
        "url": url,
    }
    return result


def make_note_edit_candidates(info: dict[str, str]) -> list[str]:
    """基于 node_id 构造常见 note/edit 只读候选页面。"""
    node_id = info["node_id"]
    query: dict[str, list[str]] = {}
    if info.get("corp_id"):
        query["corpId"] = [info["corp_id"]]
    encoded_query = urlencode(query, doseq=True, quote_via=quote)
    suffix = f"?{encoded_query}" if encoded_query else ""
    return [
        f"https://alidocs.dingtalk.com/i/note/{node_id}{suffix}",
        f"https://alidocs.dingtalk.com/i/note/{node_id}/edit{suffix}",
        f"https://alidocs.dingtalk.com/i/nodes/{node_id}/edit{suffix}",
    ]


# ---------------------------------------------------------------------------
# HTML / JSON 文本提取
# ---------------------------------------------------------------------------


class VisibleTextExtractor(HTMLParser):
    """从 HTML 中提取可见文本，跳过 script/style/svg。"""

    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []
        self.skip_depth = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in ("script", "style", "svg", "noscript"):
            self.skip_depth += 1
            return
        if tag in ("p", "div", "section", "article", "tr", "li", "h1", "h2", "h3", "h4"):
            self.parts.append("\n")
        if tag == "br":
            self.parts.append("\n")

    def handle_endtag(self, tag: str) -> None:
        if tag in ("script", "style", "svg", "noscript") and self.skip_depth:
            self.skip_depth -= 1
            return
        if tag in ("p", "div", "section", "article", "tr", "li", "h1", "h2", "h3", "h4"):
            self.parts.append("\n")

    def handle_data(self, data: str) -> None:
        if self.skip_depth:
            return
        text = unescape(data).strip()
        if text:
            self.parts.append(text)


def compact_text(text: str, *, limit: int = 30000) -> str:
    """压缩空白字符并限制最大长度，避免输出过大。"""
    text = unescape(text)
    text = re.sub(r"[ \t\r\f\v]+", " ", text)
    text = re.sub(r"\n\s*\n\s*\n+", "\n\n", text)
    text = "\n".join(line.strip() for line in text.splitlines())
    text = re.sub(r"\n{3,}", "\n\n", text).strip()
    if len(text) > limit:
        return text[:limit] + "\n\n[内容过长，已截断]"
    return text


def html_to_text(html_text: str) -> str:
    """HTML → 可见文本。"""
    parser = VisibleTextExtractor()
    parser.feed(html_text)
    return compact_text("\n".join(parser.parts))


def extract_title(html_text: str) -> str:
    """从 title / og:title / JSON 片段中提取页面标题。"""
    patterns = (
        r'<meta[^>]+property=["\']og:title["\'][^>]+content=["\']([^"\']+)["\']',
        r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+property=["\']og:title["\']',
        r"<title[^>]*>(.*?)</title>",
        r'"title"\s*:\s*"([^"]{1,200})"',
        r'"name"\s*:\s*"([^"]{1,200})"',
    )
    for pattern in patterns:
        match = re.search(pattern, html_text, re.IGNORECASE | re.DOTALL)
        if match:
            title = compact_text(match.group(1), limit=300)
            title = re.sub(r"\s*[-|]\s*钉钉文档.*$", "", title)
            if title:
                return title
    return ""


def iter_json_candidates(html_text: str) -> list[Any]:
    """从页面脚本中提取常见内嵌 JSON 候选。"""
    candidates: list[Any] = []

    next_match = re.search(
        r'<script[^>]+id=["\']__NEXT_DATA__["\'][^>]*>(.*?)</script>',
        html_text,
        re.DOTALL,
    )
    if next_match:
        try:
            candidates.append(json.loads(unescape(next_match.group(1))))
        except json.JSONDecodeError:
            pass

    for pattern in (
        r"window\.__INITIAL_STATE__\s*=\s*({.*?})\s*</script>",
        r"window\.g_initialProps\s*=\s*({.*?})\s*</script>",
        r"window\.__APP_DATA__\s*=\s*({.*?})\s*</script>",
    ):
        for match in re.finditer(pattern, html_text, re.DOTALL):
            raw = match.group(1).strip()
            try:
                candidates.append(json.loads(raw))
            except json.JSONDecodeError:
                continue

    return candidates


def collect_text_from_json(data: Any, *, max_items: int = 400) -> list[str]:
    """递归提取 JSON 中常见正文/标题字段。"""
    results: list[str] = []

    def walk(value: Any, key: str = "") -> None:
        if len(results) >= max_items:
            return
        if isinstance(value, dict):
            for child_key, child_value in value.items():
                walk(child_value, str(child_key))
            return
        if isinstance(value, list):
            for item in value:
                walk(item, key)
            return
        if not isinstance(value, str):
            return

        text = compact_text(value, limit=4000)
        if not text or len(text) < 2:
            return
        if key in TEXT_KEYS or ("\n" in text and len(text) > 20):
            results.append(text)

    walk(data)
    return results


def dedupe_lines(items: list[str]) -> list[str]:
    """按内容去重，保留顺序。"""
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        normalized = re.sub(r"\s+", " ", item).strip()
        if not normalized or normalized in seen:
            continue
        seen.add(normalized)
        result.append(item)
    return result


def extract_document(html_text: str) -> dict[str, Any]:
    """从 HTML 中提取标题、正文和内嵌 JSON 文本。"""
    title = extract_title(html_text)
    visible_text = html_to_text(html_text)
    json_texts: list[str] = []
    for candidate in iter_json_candidates(html_text):
        json_texts.extend(collect_text_from_json(candidate))

    content_items = dedupe_lines(json_texts + ([visible_text] if visible_text else []))
    content = compact_text("\n\n".join(content_items))
    if title and content.startswith(title):
        content = content[len(title) :].strip()
    return {
        "title": title,
        "content": content,
        "content_length": len(content),
        "json_blocks": len(json_texts),
        "has_visible_text": bool(visible_text),
    }


def score_document(doc: dict[str, Any]) -> int:
    """给提取结果打分，优先选择更像正文而不是知识库外壳的页面。"""
    content = str(doc.get("content") or "")
    if not content:
        return 0
    score = len(content)
    marker_hits = sum(1 for marker in SHELL_TEXT_MARKERS if marker in content)
    if marker_hits and len(content) < 1000:
        score -= marker_hits * 500
    if doc.get("json_blocks"):
        score += int(doc["json_blocks"]) * 200
    if re.search(r"(^|\n)#{1,6}\s|\n[-*]\s|\n\d+\.\s", content):
        score += 300
    return max(score, 0)


def extract_follow_urls(html_text: str, base_url: str, node_id: str) -> list[str]:
    """从页面 HTML/脚本中发现 note/edit 等只读候选链接。"""
    urls: list[str] = []

    for match in re.finditer(r'(?:href|src)=["\']([^"\']+)["\']', html_text, re.IGNORECASE):
        urls.append(urljoin(base_url, unescape(match.group(1))))

    for match in re.finditer(r'https?:\\?/\\?/alidocs\.dingtalk\.com[^"\'\\<>\s]+', html_text):
        raw = match.group(0).replace("\\/", "/")
        urls.append(unescape(raw))

    for match in re.finditer(r'(["\'])(/[^"\']*(?:note|edit|nodes)[^"\']*)\1', html_text):
        urls.append(urljoin(base_url, unescape(match.group(2)).replace("\\/", "/")))

    normalized: list[str] = []
    seen: set[str] = set()
    for url in urls:
        parsed = urlparse(url)
        if parsed.netloc != "alidocs.dingtalk.com":
            continue
        if node_id not in url:
            continue
        if not any(keyword in parsed.path for keyword in FOLLOW_PATH_KEYWORDS):
            continue
        clean = normalize_candidate_url(url)
        if clean in seen:
            continue
        seen.add(clean)
        normalized.append(clean)

    return normalized


# ---------------------------------------------------------------------------
# HTTP 客户端
# ---------------------------------------------------------------------------


class DingTalkDocsClient:
    """钉钉文档只读 HTTP 客户端。"""

    def __init__(self, cookie: str, user_agent: str = DEFAULT_UA) -> None:
        self.cookie = cookie
        self.user_agent = user_agent

    def fetch_page(self, url: str) -> str:
        """使用 Cookie 读取钉钉文档页面 HTML。"""
        require_alidocs_url(url)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".dingtalk-docs") as tmp:
            out_path = tmp.name
        try:
            cmd = [
                "curl",
                "-sS",
                "--http1.1",
                "--max-time",
                "120",
                "-L",
                "-o",
                out_path,
                "-H",
                f"Cookie: {self.cookie}",
                "-H",
                f"User-Agent: {self.user_agent}",
                "-H",
                "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "-H",
                f"Referer: {url}",
                url,
            ]
            proc = subprocess.run(cmd, capture_output=True, text=True, timeout=130)
            raw = Path(out_path).read_text(encoding="utf-8", errors="ignore")
            if proc.returncode != 0:
                raise AuthError(f"请求失败 ({proc.returncode}): {proc.stderr.strip() or raw[:200]}")
            if any(marker in raw for marker in AUTH_ERROR_MARKERS):
                raise AuthError("Cookie 可能已过期，或当前账号无权访问该钉钉文档")
            return raw
        finally:
            Path(out_path).unlink(missing_ok=True)

    def read_candidate(self, url: str) -> dict[str, Any]:
        """读取单个候选页面，返回提取结果与来源 URL。"""
        html_text = self.fetch_page(url)
        doc = extract_document(html_text)
        doc["source_url"] = normalize_candidate_url(url)
        doc["score"] = score_document(doc)
        doc["follow_urls"] = extract_follow_urls(html_text, url, parse_dingtalk_url(url)["node_id"])
        return doc

    def read(self, url: str) -> dict[str, Any]:
        """读取钉钉文档页面，并跟随 note/edit 只读候选页提取正文。"""
        info = parse_dingtalk_url(url)
        base_url = info["clean_url"] or url
        candidate_urls = [base_url, *make_note_edit_candidates(info)]
        candidates: list[dict[str, Any]] = []
        errors: list[dict[str, str]] = []
        seen: set[str] = set()
        index = 0

        while index < len(candidate_urls) and len(seen) < 12:
            candidate_url = normalize_candidate_url(candidate_urls[index])
            index += 1
            if candidate_url in seen:
                continue
            seen.add(candidate_url)
            try:
                candidate = self.read_candidate(candidate_url)
                candidates.append(candidate)
                for follow_url in candidate.get("follow_urls", []):
                    if follow_url not in seen and follow_url not in candidate_urls:
                        candidate_urls.append(follow_url)
            except AuthError:
                raise
            except Exception as exc:  # noqa: BLE001 - 候选页失败不应阻断其他候选
                errors.append({"url": candidate_url, "message": str(exc)})

        doc = max(candidates, key=score_document, default={})
        fallback_title = next((c.get("title") for c in candidates if c.get("title")), "")
        if doc and not doc.get("title"):
            doc["title"] = fallback_title

        return {
            "ok": True,
            **info,
            **doc,
            "followed_urls": [c["source_url"] for c in candidates if c.get("source_url")],
            "candidate_errors": errors,
            "note": (
                "已尝试原始 node 页面、常见 note/edit 子页面及页面内发现的只读候选链接；"
                "若 content 仍为空或仅有页面壳，说明正文可能由未暴露在 SSR/HTML 中的运行时只读接口加载，"
                "请补充 Network 中加载正文的 GET/只读请求样本。"
                if not doc.get("content")
                else ""
            ),
        }


# ---------------------------------------------------------------------------
# 输出与命令
# ---------------------------------------------------------------------------


def print_json(data: Any) -> None:
    """打印 JSON，保持中文可读。"""
    print(json.dumps(data, ensure_ascii=False, indent=2))


def cmd_cookie(args: argparse.Namespace) -> None:
    """保存或检查 Cookie。"""
    if args.set:
        save_cookie(args.set)
        print_json({"ok": True, "message": "Cookie 已保存", "path": str(COOKIE_FILE)})
        return

    if args.check:
        cookie = load_cookie()
        if args.url:
            client = DingTalkDocsClient(cookie, load_config()["user_agent"])
            html_text = client.fetch_page(args.url)
            print_json(
                {
                    "ok": True,
                    "url": args.url,
                    "title": extract_title(html_text),
                    "message": "Cookie 可用于读取该页面",
                }
            )
        else:
            print_json({"ok": True, "message": "Cookie 文件存在；建议加 --url 检查实际访问权限"})
        return

    raise SystemExit("请使用 cookie --set <Cookie> 或 cookie --check [--url <链接>]")


def cmd_info(args: argparse.Namespace) -> None:
    """解析钉钉文档 URL。"""
    print_json(parse_dingtalk_url(args.url))


def cmd_read(args: argparse.Namespace) -> None:
    """读取钉钉文档。"""
    cookie = load_cookie()
    client = DingTalkDocsClient(cookie, load_config()["user_agent"])
    result = client.read(args.url)
    if args.format == "json":
        print_json(result)
        return

    print(f"# {result.get('title') or result['node_id']}")
    print()
    print(f"链接：{result['clean_url']}")
    if result.get("corp_id"):
        print(f"corpId：{result['corp_id']}")
    if result.get("sheet_id"):
        print(f"sheetId：{result['sheet_id']}")
    if result.get("view_id"):
        print(f"viewId：{result['view_id']}")
    print()
    content = result.get("content") or ""
    if content:
        print(content)
    else:
        print(result.get("note") or "未提取到正文。")


def build_parser() -> argparse.ArgumentParser:
    """构造 CLI 参数解析器。"""
    parser = argparse.ArgumentParser(description="DingTalk Docs readonly skill CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    cookie = sub.add_parser("cookie", help="Check or save cookie")
    cookie.add_argument("--set", metavar="COOKIE", help="Save browser Cookie")
    cookie.add_argument("--check", action="store_true", help="Check Cookie")
    cookie.add_argument("--url", help="DingTalk Docs URL for real access check")
    cookie.set_defaults(func=cmd_cookie)

    info = sub.add_parser("info", help="Resolve DingTalk Docs URL")
    info.add_argument("url")
    info.set_defaults(func=cmd_info)

    read = sub.add_parser("read", help="Read DingTalk document page")
    read.add_argument("url")
    read.add_argument("--format", choices=("text", "json"), default="text")
    read.set_defaults(func=cmd_read)

    return parser


def main() -> int:
    """CLI 入口。"""
    parser = build_parser()
    args = parser.parse_args()
    try:
        args.func(args)
        return 0
    except AuthError as exc:
        print_json({"ok": False, "error": "auth_error", "message": str(exc)})
        return 2
    except SystemExit as exc:
        if isinstance(exc.code, int):
            return exc.code
        print_json({"ok": False, "error": "error", "message": str(exc)})
        return 1
    except Exception as exc:  # noqa: BLE001 - CLI 需要稳定输出错误 JSON
        print_json({"ok": False, "error": exc.__class__.__name__, "message": str(exc)})
        return 1


if __name__ == "__main__":
    sys.exit(main())
