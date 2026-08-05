#!/usr/bin/env python3
"""
语雀文档 CLI — fe-yuque-docs skill 唯一执行入口。

职责：
  - 通过 Cookie 认证访问语雀私有 API（企业版/团队子域）
  - 只读：读文档、搜索、列知识库、查目录
  - 写入类命令（write/create/title）保留在脚本内供维护，skill 层禁止使用

依赖：
  - 系统 curl（HTTP 请求）
  - credentials/cookie.txt（登录 Cookie）
  - credentials/config.json（自动识别的 base_url、可选 default_group）

退出码：
  - 0：成功
  - 1：一般错误（参数、业务逻辑）
  - 2：鉴权失败（AuthError，Cookie 过期或未配置）
"""

from __future__ import annotations

import argparse
import html
import json
import os
import random
import re
import string
import subprocess
import sys
import tempfile
from html.parser import HTMLParser
from pathlib import Path
from typing import Any
from urllib.parse import unquote, urlparse

# ---------------------------------------------------------------------------
# 路径与常量
# ---------------------------------------------------------------------------

# skill 包根目录（scripts/ 的上一级）
SKILL_ROOT = Path(__file__).resolve().parent.parent
COOKIE_FILE = SKILL_ROOT / "credentials" / "cookie.txt"
CONFIG_FILE = SKILL_ROOT / "credentials" / "config.json"

# 模拟浏览器 UA，避免部分 WAF 拦截
DEFAULT_UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
)

# 响应体中出现以下片段时，视为鉴权相关失败（辅助判断）
AUTH_ERROR_MARKERS = ("401", "Unauthorized", "未登录", "login", "Cookie may be expired")


class AuthError(Exception):
    """Cookie 无效、过期或 CSRF token 缺失时抛出；CLI 层映射为 exit code 2。"""


# ---------------------------------------------------------------------------
# 配置与 Cookie 持久化
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


def persist_base_url(base_url: str) -> None:
    """将识别到的语雀租户 base_url 持久化，供后续命令复用。"""
    cfg = read_config_file()
    cfg["base_url"] = base_url.rstrip("/")
    write_config_file(cfg)


def load_config() -> dict[str, str]:
    """
    加载运行配置，优先级：环境变量 > config.json > 默认值。

    字段：
      - base_url: 语雀租户根地址，如 https://team.yuque.com（不写死）
      - user_agent: HTTP User-Agent
      - default_group: 搜索全库时的默认团队 login（可选）
    """
    cfg: dict[str, str] = {
        "base_url": "",
        "user_agent": DEFAULT_UA,
        "default_group": "",
    }
    cfg.update(read_config_file())
    cfg["base_url"] = os.environ.get("YUQUE_BASE_URL", cfg["base_url"]).rstrip("/")
    cfg["user_agent"] = os.environ.get("YUQUE_USER_AGENT", cfg["user_agent"])
    return cfg


def load_cookie() -> str:
    """
    加载 Cookie，优先级：环境变量 YUQUE_COOKIE > credentials/cookie.txt。
    缺失时抛 AuthError。
    """
    if os.environ.get("YUQUE_COOKIE"):
        return os.environ["YUQUE_COOKIE"].strip()
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


def extract_ctoken(cookie: str) -> str:
    """从 Cookie 字符串提取 yuque_ctoken，用作 x-csrf-token 请求头。"""
    m = re.search(r"(?:^|;\s*)yuque_ctoken=([^;]+)", cookie)
    if not m:
        raise AuthError("Cookie 缺少 yuque_ctoken，请重新从浏览器复制完整 Cookie")
    return m.group(1)


# ---------------------------------------------------------------------------
# Lake 格式转换（Markdown ↔ 语雀 Lake HTML）
# 写入类命令使用；skill 只读场景主要用 lake_to_text 提取正文。
# ---------------------------------------------------------------------------


def uid() -> str:
    """生成语雀 Lake 节点用的随机 id（u + 7 位字母数字）。"""
    return "u" + "".join(random.choices(string.ascii_lowercase + string.digits, k=7))


def span(text: str, *, bold: bool = False, italic: bool = False, code: bool = False) -> str:
    """构造 Lake 内联 span 节点。"""
    sid = uid()
    cls = []
    if code:
        cls.append("ne-code")
    escaped = html.escape(text, quote=False)
    if bold:
        escaped = f"<strong>{escaped}</strong>"
    if italic:
        escaped = f"<em>{escaped}</em>"
    class_attr = f' class="{" ".join(cls)}"' if cls else ""
    return f'<span data-lake-id="{sid}" id="{sid}"{class_attr}>{escaped}</span>'


def paragraph(inner: str) -> str:
    """构造 Lake 段落节点。"""
    pid = uid()
    return f'<p data-lake-id="{pid}" id="{pid}">{inner}</p>'


def heading(level: int, text: str) -> str:
    """构造 Lake 标题节点（level 1-6）。"""
    hid = uid()
    return (
        f'<h{level} data-lake-id="{hid}" id="{hid}">'
        f'<span class="ne-text">{html.escape(text)}</span></h{level}>'
    )


def markdown_inline(text: str) -> str:
    """将行内 Markdown（代码、粗体、斜体、链接）转为 Lake HTML 片段。"""
    parts: list[str] = []
    pattern = re.compile(
        r"(`[^`]+`)|(\*\*[^*]+\*\*)|(\*[^*]+\*)|(\[[^\]]+\]\([^)]+\))"
    )
    pos = 0
    for m in pattern.finditer(text):
        if m.start() > pos:
            parts.append(span(text[pos : m.start()]))
        token = m.group(0)
        if token.startswith("`"):
            parts.append(span(token[1:-1], code=True))
        elif token.startswith("**"):
            parts.append(span(token[2:-2], bold=True))
        elif token.startswith("*"):
            parts.append(span(token[1:-1], italic=True))
        elif token.startswith("["):
            lm = re.match(r"\[([^\]]+)\]\(([^)]+)\)", token)
            if lm:
                label, href = lm.groups()
                aid = uid()
                parts.append(
                    f'<a href="{html.escape(href)}" data-lake-id="{aid}" id="{aid}">'
                    f'<span class="ne-text">{html.escape(label)}</span></a>'
                )
        pos = m.end()
    if pos < len(text):
        parts.append(span(text[pos:]))
    return "".join(parts) if parts else span(text)


def markdown_to_lake(md: str) -> str:
    """
    将 Markdown 转为语雀 Lake HTML 文档体。

    支持：标题、代码块、表格、无序/有序列表、段落。
    用于 write/create 子命令（skill 禁止调用）。
    """
    lines = md.replace("\r\n", "\n").split("\n")
    blocks: list[str] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        # ATX 标题
        hm = re.match(r"^(#{1,6})\s+(.+)$", line)
        if hm:
            blocks.append(heading(len(hm.group(1)), hm.group(2).strip()))
            i += 1
            continue
        # 围栏代码块
        if re.match(r"^```", line):
            lang = line[3:].strip()
            i += 1
            code_lines: list[str] = []
            while i < len(lines) and not lines[i].startswith("```"):
                code_lines.append(lines[i])
                i += 1
            i += 1
            code = html.escape("\n".join(code_lines))
            cid = uid()
            blocks.append(
                f'<pre data-lake-id="{cid}" id="{cid}"><code class="language-{html.escape(lang)}">{code}</code></pre>'
            )
            continue
        # Markdown 表格
        if line.strip().startswith("|") and "|" in line[1:]:
            table_lines = [line]
            i += 1
            while i < len(lines) and "|" in lines[i]:
                table_lines.append(lines[i])
                i += 1
            rows = [r.strip().strip("|").split("|") for r in table_lines]
            rows = [[c.strip() for c in r] for r in rows if any(c.strip() for c in r)]
            # 跳过分隔行 |---|---|
            if len(rows) >= 2 and re.match(r"^[-:|\s]+$", "|".join(rows[1])):
                rows.pop(1)
            tid = uid()
            trs = []
            for ri, row in enumerate(rows):
                tag = "th" if ri == 0 else "td"
                tds = "".join(f"<{tag}><p>{markdown_inline(c)}</p></{tag}>" for c in row)
                trs.append(f"<tr>{tds}</tr>")
            blocks.append(f'<table data-lake-id="{tid}" id="{tid}"><tbody>{"".join(trs)}</tbody></table>')
            continue
        # 无序列表
        if re.match(r"^[-*]\s+", line):
            items = []
            while i < len(lines) and re.match(r"^[-*]\s+", lines[i]):
                items.append(re.sub(r"^[-*]\s+", "", lines[i]).strip())
                i += 1
            lid = uid()
            lis = "".join(f'<li data-lake-id="{uid()}" id="{uid()}">{markdown_inline(it)}</li>' for it in items)
            blocks.append(f'<ul data-lake-id="{lid}" id="{lid}">{lis}</ul>')
            continue
        # 有序列表
        if re.match(r"^\d+\.\s+", line):
            items = []
            while i < len(lines) and re.match(r"^\d+\.\s+", lines[i]):
                items.append(re.sub(r"^\d+\.\s+", "", lines[i]).strip())
                i += 1
            lid = uid()
            lis = "".join(f'<li data-lake-id="{uid()}" id="{uid()}">{markdown_inline(it)}</li>' for it in items)
            blocks.append(f'<ol data-lake-id="{lid}" id="{lid}">{lis}</ol>')
            continue
        # 普通段落（合并连续非空行）
        para_lines = [line]
        i += 1
        while i < len(lines) and lines[i].strip() and not re.match(r"^(#{1,6}\s|[-*]\s|\d+\.\s|```|\|)", lines[i]):
            para_lines.append(lines[i])
            i += 1
        blocks.append(paragraph(markdown_inline(" ".join(p.strip() for p in para_lines))))
    body = "".join(blocks) or paragraph(span(""))
    return f'<!doctype lake><meta name="doc-version" content="1" />{body}'


class LakeTextExtractor(HTMLParser):
    """
    从语雀 Lake HTML 提取纯文本/Markdown 风格正文。

    用于 read 子命令：API 返回的 content/body 为 Lake 格式，需转为可读文本。
    """

    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []
        self.skip = False  # script/style 内跳过
        self.in_a = False
        self.href = ""

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attrs_dict = dict(attrs)
        if tag in ("script", "style"):
            self.skip = True
        if tag == "br":
            self.parts.append("\n")
        if tag in ("p", "div", "tr", "section", "blockquote"):
            self.parts.append("\n")
        if tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self.parts.append("\n" + "#" * int(tag[1]) + " ")
        if tag == "li":
            self.parts.append("\n- ")
        if tag in ("td", "th"):
            self.parts.append(" | ")
        if tag == "img":
            self.parts.append(f"[图片:{attrs_dict.get('alt') or '图片'}]")
        if tag == "a":
            self.in_a = True
            self.href = attrs_dict.get("href") or ""
        # 语雀卡片（画板、附件等）占位
        if tag == "card":
            name = attrs_dict.get("name") or ""
            value = attrs_dict.get("value") or ""
            useful = ""
            if value.startswith("data:"):
                try:
                    payload = unquote(value[5:])
                    data = json.loads(payload)
                    useful = str(data.get("src") or data.get("url") or data)[:200]
                except Exception:
                    useful = unquote(value[5:])[:200]
            self.parts.append(f"\n[[{name}:{useful}]]\n")

    def handle_endtag(self, tag: str) -> None:
        if tag in ("script", "style"):
            self.skip = False
        if tag in ("p", "div", "h1", "h2", "h3", "h4", "h5", "h6", "li", "tr", "table", "section", "blockquote"):
            self.parts.append("\n")
        if tag == "a" and self.in_a:
            if self.href and not self.href.startswith("javascript"):
                self.parts.append(f"({self.href})")
            self.in_a = False

    def handle_data(self, data: str) -> None:
        if self.skip:
            return
        if data.strip():
            self.parts.append(data)


def lake_to_text(content: str) -> str:
    """Lake HTML → 纯文本，压缩多余空行。"""
    parser = LakeTextExtractor()
    parser.feed(content)
    text = "".join(parser.parts)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return re.sub(r"[ \t]+\n", "\n", text).strip()


# ---------------------------------------------------------------------------
# URL 解析
# ---------------------------------------------------------------------------


def parse_yuque_url(url: str) -> tuple[str, list[str]]:
    """
    解析语雀 URL。

    返回：
      - base: https://{tenant}.yuque.com
      - parts: 路径段，如 [group, book] 或 [group, book, doc]
    """
    parsed = urlparse(url)
    if not parsed.scheme or not parsed.netloc:
        raise SystemExit(f"无效的语雀 URL: {url}")
    if "yuque.com" not in parsed.netloc:
        raise SystemExit(f"URL 不是语雀域名: {url}")
    base = f"{parsed.scheme}://{parsed.netloc}"
    parts = [p for p in parsed.path.split("/") if p]
    return base, parts


def is_yuque_host(netloc: str) -> bool:
    """判断 host 是否为语雀域名（含 www.yuque.com 与企业子域）。"""
    return netloc == "yuque.com" or netloc.endswith(".yuque.com")


# ---------------------------------------------------------------------------
# 语雀 API 客户端
# ---------------------------------------------------------------------------


class YuqueClient:
    """
    语雀 HTTP 客户端。

    所有请求经 curl 发出，携带 Cookie + x-csrf-token。
    base_url 可从用户 URL 自动识别并持久化，不写死租户地址。
    """

    def __init__(self, cookie: str, base_url: str | None = None, user_agent: str = DEFAULT_UA) -> None:
        self.cookie = cookie
        self.ctoken = extract_ctoken(cookie)
        self.base_url = (base_url if base_url is not None else load_config()["base_url"]).rstrip("/")
        self.user_agent = user_agent

    def apply_base_from_url(self, url: str) -> str:
        """
        从任意语雀链接提取租户 base_url 并更新实例（有变化则写入 config.json）。
        """
        parsed = urlparse(url)
        if not parsed.scheme or not parsed.netloc or not is_yuque_host(parsed.netloc):
            raise SystemExit(f"无效的语雀 URL，无法识别 base_url: {url}")
        base = f"{parsed.scheme}://{parsed.netloc}".rstrip("/")
        if base != self.base_url:
            self.base_url = base
            persist_base_url(base)
        return self.base_url

    def require_base_url(self) -> str:
        """确保 base_url 已设置，否则提示用户先提供语雀链接。"""
        if not self.base_url:
            raise SystemExit(
                "尚未识别语雀 base_url。请先对任意语雀文档/知识库 URL 执行 read/info/toc，"
                "或运行 cookie --check --url <语雀链接> 自动识别并保存。"
            )
        return self.base_url

    def _curl(
        self,
        method: str,
        url: str,
        *,
        referer: str | None = None,
        body: dict[str, Any] | None = None,
        accept: str = "application/json",
    ) -> str:
        """
        底层 HTTP 请求（curl 子进程）。

        响应写入临时文件再读取，避免大正文撑爆内存。
        """
        with tempfile.NamedTemporaryFile(delete=False, suffix=".yuque") as tmp:
            out_path = tmp.name
        try:
            cmd = [
                "curl", "-sS", "--http1.1", "--max-time", "120", "-X", method, "-o", out_path,
                "-H", f"Cookie: {self.cookie}",
                "-H", f"User-Agent: {self.user_agent}",
                "-H", f"Accept: {accept}",
                "-H", "X-Requested-With: XMLHttpRequest",
                "-H", f"x-csrf-token: {self.ctoken}",
            ]
            if referer:
                cmd.extend(["-H", f"Referer: {referer}"])
            if body is not None:
                cmd.extend(["-H", "Content-Type: application/json", "-d", json.dumps(body, ensure_ascii=False)])
            cmd.append(url)
            proc = subprocess.run(cmd, capture_output=True, text=True, timeout=130)
            raw = Path(out_path).read_text(encoding="utf-8", errors="ignore")
            if proc.returncode != 0:
                raise AuthError(f"请求失败 ({proc.returncode}): {proc.stderr.strip() or raw[:200]}")
            # 语雀反爬：返回「浏览器版本过低」页面
            if any(m in raw for m in ("当前浏览器版本过低", "module-error")) and accept == "text/html":
                raise AuthError("页面返回浏览器拦截，请检查 Cookie 是否有效")
            return raw
        finally:
            Path(out_path).unlink(missing_ok=True)

    def _request(
        self,
        method: str,
        path: str,
        *,
        referer: str | None = None,
        body: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """
        调用语雀 JSON API。

        path 可为相对路径（拼 base_url）或完整 URL。
        401/403 → AuthError；404/422 → SystemExit。
        """
        if not path.startswith("http"):
            self.require_base_url()
        url = path if path.startswith("http") else f"{self.base_url}{path}"
        raw = self._curl(method, url, referer=referer, body=body)
        # HTML 响应通常表示被重定向到登录页
        if raw.strip().startswith("<"):
            raise AuthError("Cookie 可能已过期，请用户提供新 Cookie 并更新 credentials/cookie.txt")
        try:
            result = json.loads(raw)
        except json.JSONDecodeError as e:
            raise AuthError(f"API 返回非 JSON，Cookie 可能已过期: {raw[:200]}") from e
        if isinstance(result, dict) and result.get("status") in (401, 403):
            raise AuthError(f"Cookie 已过期或无权限 ({result.get('status')}): {result.get('message')}")
        if isinstance(result, dict) and result.get("status") in (404, 422):
            raise SystemExit(f"API error {result.get('status')}: {result.get('message') or result}")
        return result

    def fetch_app_data(self, page_url: str) -> dict[str, Any]:
        """从语雀页面 HTML 内嵌的 decodeURIComponent 数据块提取 JSON（SSR 数据）。"""
        html_text = self._curl("GET", page_url, accept="text/html")
        m = re.search(r'decodeURIComponent\("(%[^"]{50,})"\)', html_text)
        if not m:
            raise AuthError("无法解析页面，Cookie 可能已过期或 URL 无效")
        return json.loads(unquote(m.group(1)))

    def resolve_book(self, book_url: str) -> dict[str, Any]:
        """
        解析知识库 URL → book_id、slug、page_url 等元信息。

        URL 格式：https://{tenant}.yuque.com/{group}/{book}
        """
        _base, parts = parse_yuque_url(book_url)
        if len(parts) < 2:
            raise SystemExit(f"知识库 URL 需为 /{{group}}/{{book}}: {book_url}")
        self.apply_base_from_url(book_url)
        group_login, book_slug = parts[0], parts[1]
        page_url = f"{self.base_url}/{group_login}/{book_slug}"
        group = self._request("GET", f"/api/groups/{group_login}", referer=f"{self.base_url}/")["data"]
        books = self._request(
            "GET", f"/api/groups/{group['id']}/books?limit=100", referer=f"{self.base_url}/"
        ).get("data", [])
        book = next((b for b in books if b.get("slug") == book_slug), None)
        if not book:
            raise SystemExit(f"未找到知识库 slug={book_slug}，请检查 URL 或权限")
        return {
            "page_url": page_url,
            "group_login": group_login,
            "book_id": book["id"],
            "book_slug": book["slug"],
            "book_name": book["name"],
        }

    def resolve_doc(self, doc_url: str) -> dict[str, Any]:
        """
        解析文档 URL → doc_id、book_id、title 等元信息。

        URL 格式：https://{tenant}.yuque.com/{group}/{book}/{doc}
        """
        _base, parts = parse_yuque_url(doc_url)
        if len(parts) < 3:
            raise SystemExit(f"文档 URL 需为 /{{group}}/{{book}}/{{doc}}: {doc_url}")
        self.apply_base_from_url(doc_url)
        group_login, book_slug, doc_slug = parts[0], parts[1], parts[2]
        page_url = f"{self.base_url}/{group_login}/{book_slug}/{doc_slug}"
        book = self.resolve_book(f"{self.base_url}/{group_login}/{book_slug}")
        doc = self._request(
            "GET",
            f"/api/docs/{doc_slug}?book_id={book['book_id']}",
            referer=page_url,
        )["data"]
        return {
            "page_url": page_url,
            "group_login": group_login,
            "book_id": book["book_id"],
            "book_name": book["book_name"],
            "book_slug": book_slug,
            "doc_id": doc["id"],
            "doc_slug": doc["slug"],
            "title": doc["title"],
            "url": page_url,
        }

    def get_doc(self, doc_id: int, book_id: int, referer: str) -> dict[str, Any]:
        """按 doc_id 获取文档详情（含 Lake 正文）。"""
        return self._request("GET", f"/api/docs/{doc_id}?book_id={book_id}", referer=referer)["data"]

    def create_doc(self, book_id: int, title: str, body: str, referer: str) -> dict[str, Any]:
        """新建文档（skill 禁止调用）。"""
        payload = {"book_id": book_id, "title": title, "format": "lake", "body": body}
        return self._request("POST", "/api/docs", referer=referer, body=payload)["data"]

    def update_doc(self, doc_id: int, book_id: int, referer: str, **fields: Any) -> dict[str, Any]:
        """更新文档字段（skill 禁止调用）。"""
        payload = {"book_id": book_id, **fields}
        return self._request("PUT", f"/api/docs/{doc_id}", referer=referer, body=payload)["data"]

    def list_books(self, group_login: str) -> list[dict[str, Any]]:
        """列出团队下所有知识库。"""
        self.require_base_url()
        group = self._request("GET", f"/api/groups/{group_login}", referer=f"{self.base_url}/")["data"]
        result = self._request("GET", f"/api/groups/{group['id']}/books?limit=100", referer=f"{self.base_url}/")
        return result.get("data", [])

    def list_docs(self, book_id: int, *, offset: int = 0, limit: int = 100) -> list[dict[str, Any]]:
        """分页列出知识库内文档。"""
        result = self._request(
            "GET",
            f"/api/books/{book_id}/docs?offset={offset}&limit={limit}",
            referer=f"{self.base_url}/",
        )
        return result.get("data", [])

    def get_toc(self, book_id: int, referer: str) -> list[dict[str, Any]]:
        """获取知识库目录树（TOC）。"""
        result = self._request("GET", f"/api/books/{book_id}/toc", referer=referer)
        data = result.get("data", {})
        toc = data.get("toc", []) if isinstance(data, dict) else []
        return toc if isinstance(toc, list) else []

    def find_toc_node(
        self,
        book_id: int,
        referer: str,
        *,
        doc_slug: str | None = None,
        doc_url: str | None = None,
    ) -> dict[str, Any] | None:
        """在 TOC 中按 doc_slug 或 doc_url 查找节点（create 挂载目录用）。"""
        if doc_url:
            _, parts = parse_yuque_url(doc_url.split("#")[0])
            doc_slug = parts[2] if len(parts) >= 3 else None
        if not doc_slug:
            return None
        for item in self.get_toc(book_id, referer):
            if item.get("url") == doc_slug or str(item.get("doc_id")) == doc_slug:
                return item
        return None

    def try_place_in_toc(
        self,
        book_id: int,
        doc_id: int,
        *,
        after_uuid: str,
        referer: str,
        action_mode: str = "sibling",
    ) -> tuple[bool, str]:
        """
        尝试将文档挂载到目录（best-effort）。

        企业版语雀常返回 404，此时返回 (False, 提示信息) 而非抛错。
        """
        payload = {
            "action": "appendNode",
            "action_mode": action_mode,
            "target_uuid": after_uuid,
            "type": "DOC",
            "doc_id": doc_id,
        }
        try:
            self._request("PUT", f"/api/books/{book_id}/toc", referer=referer, body=payload)
            node = next((n for n in self.get_toc(book_id, referer) if n.get("doc_id") == doc_id), None)
            if node and node.get("parent_uuid"):
                return True, "已自动挂载到目录"
            return False, "目录 API 不可用，文档已创建但未出现在目标目录"
        except SystemExit as e:
            msg = str(e)
            if "404" in msg:
                return False, "企业版语雀不支持目录自动挂载 API（PUT /toc 返回 404）"
            raise
        except AuthError:
            raise
        except Exception as e:
            return False, f"目录挂载失败: {e}"

    def search_docs(
        self,
        query: str,
        *,
        book_id: int | None = None,
        book: dict[str, Any] | None = None,
        group_login: str | None = None,
    ) -> list[dict[str, Any]]:
        """
        关键词搜索文档。

        语雀无全局 search API，实现为遍历文档列表，在 title/description/slug 中匹配。
        可限定单库（book/book_id）或整个团队（group_login / default_group）。
        """
        q = query.lower()
        hits: list[dict[str, Any]] = []

        def match_doc(doc: dict[str, Any], book: dict[str, Any] | None = None) -> bool:
            hay = " ".join(
                str(doc.get(k) or "")
                for k in ("title", "description", "slug")
            ).lower()
            return q in hay

        def enrich(doc: dict[str, Any], book: dict[str, Any]) -> dict[str, Any]:
            group = (
                book.get("group_login")
                or (book.get("namespace", "").split("/")[0] if book.get("namespace") else None)
                or group_login
            )
            slug = doc.get("slug")
            book_slug = book.get("slug") or book.get("book_slug")
            url = f"{self.base_url}/{group}/{book_slug}/{slug}" if group and book_slug and slug else None
            return {
                "title": doc.get("title"),
                "description": (doc.get("description") or "")[:120],
                "book_name": book.get("name"),
                "book_id": book.get("id"),
                "doc_id": doc.get("id"),
                "slug": slug,
                "url": url,
                "updated_at": doc.get("content_updated_at") or doc.get("updated_at"),
            }

        # 单库搜索
        if book is not None:
            for doc in self.list_docs(book["book_id"], limit=200):
                if match_doc(doc, book):
                    hits.append(enrich(doc, book))
            return hits

        if book_id is not None:
            book_meta: dict[str, Any] = {"id": book_id, "slug": "", "name": "", "namespace": ""}
            for doc in self.list_docs(book_id, limit=200):
                if match_doc(doc):
                    hits.append(enrich(doc, book_meta))
            return hits

        # 团队内全库搜索
        books: list[dict[str, Any]] = []
        if group_login:
            books = self.list_books(group_login)
        else:
            default_group = load_config()["default_group"]
            if not default_group:
                raise SystemExit(
                    "搜索全库需提供 --group、--book-url 或 --book-id；"
                    "或在 credentials/config.json 中配置 default_group"
                )
            books = self.list_books(default_group)

        for book_item in books:
            book_item["group_login"] = group_login or load_config()["default_group"]
            for doc in self.list_docs(book_item["id"], limit=200):
                if match_doc(doc, book_item):
                    hits.append(enrich(doc, book_item))
        return hits


def get_client() -> YuqueClient:
    """工厂：加载配置与 Cookie，返回已初始化的客户端。"""
    cfg = load_config()
    return YuqueClient(load_cookie(), base_url=cfg["base_url"], user_agent=cfg["user_agent"])


# ---------------------------------------------------------------------------
# CLI 子命令（skill 允许：cookie/read/search/books/toc/info）
# skill 禁止：write/create/title
# ---------------------------------------------------------------------------


def cmd_cookie(args: argparse.Namespace) -> None:
    """
    cookie 子命令：
      --set '...'     保存 Cookie
      --check         校验 Cookie + 可选 --url 识别 base_url
      --url <链接>    仅识别并保存 base_url
      （无参）        打印 cookie 文件路径
    """
    if args.set:
        save_cookie(args.set)
        print(json.dumps({"ok": True, "cookie_file": str(COOKIE_FILE)}, ensure_ascii=False))
    elif args.check:
        try:
            client = get_client()
            if args.url:
                client.apply_base_from_url(args.url)
            client.require_base_url()
            me = client._request("GET", "/api/mine", referer=client.base_url + "/")
            name = me.get("data", {}).get("publicName") or me.get("data", {}).get("login")
            print(
                json.dumps(
                    {
                        "ok": True,
                        "user": name,
                        "base_url": client.base_url,
                        "cookie_file": str(COOKIE_FILE),
                    },
                    ensure_ascii=False,
                )
            )
        except AuthError as e:
            print(json.dumps({"ok": False, "error": str(e)}, ensure_ascii=False))
            sys.exit(1)
    elif args.url:
        client = get_client()
        client.apply_base_from_url(args.url)
        print(
            json.dumps(
                {
                    "ok": True,
                    "base_url": client.base_url,
                    "config_file": str(CONFIG_FILE),
                },
                ensure_ascii=False,
            )
        )
    else:
        print(str(COOKIE_FILE))


def cmd_info(args: argparse.Namespace) -> None:
    """解析文档 URL，输出 doc_id / book_id 等 JSON。"""
    print(json.dumps(get_client().resolve_doc(args.url), ensure_ascii=False, indent=2))


def cmd_read(args: argparse.Namespace) -> None:
    """
    读取文档正文。

    --format text（默认）：Markdown 风格标题 + 正文
    --format json：元信息 + text + 原始 Lake HTML
    --format markdown：仅正文
    """
    client = get_client()
    meta = client.resolve_doc(args.url)
    doc = client.get_doc(meta["doc_id"], meta["book_id"], meta["page_url"])
    content = doc.get("content") or doc.get("body") or ""
    text = lake_to_text(content) if content else ""
    if args.format == "json":
        print(json.dumps({**meta, "text": text, "content_html": content, "description": doc.get("description")}, ensure_ascii=False, indent=2))
    elif args.format == "markdown":
        print(text)
    else:
        print(f"# {doc.get('title') or meta['title']}\n\n{text}")


def cmd_title(args: argparse.Namespace) -> None:
    """更新文档标题（skill 禁止）。"""
    client = get_client()
    meta = client.resolve_doc(args.url)
    updated = client.update_doc(meta["doc_id"], meta["book_id"], meta["page_url"], title=args.title)
    print(json.dumps({"title": updated["title"], "url": meta["page_url"]}, ensure_ascii=False, indent=2))


def cmd_write(args: argparse.Namespace) -> None:
    """写入文档正文（skill 禁止）。"""
    client = get_client()
    meta = client.resolve_doc(args.url)
    raw = Path(args.file).read_text(encoding="utf-8")
    body = markdown_to_lake(raw) if args.markdown or args.file.endswith(".md") else raw
    fields: dict[str, Any] = {"body": body, "format": "lake"}
    if args.title:
        fields["title"] = args.title
    updated = client.update_doc(meta["doc_id"], meta["book_id"], meta["page_url"], **fields)
    print(json.dumps({"title": updated["title"], "url": meta["page_url"], "updated_at": updated["updated_at"]}, ensure_ascii=False, indent=2))


def cmd_create(args: argparse.Namespace) -> None:
    """在知识库中新建文档（skill 禁止）。"""
    client = get_client()
    book = client.resolve_book(args.book_url)
    raw = Path(args.file).read_text(encoding="utf-8")
    body = markdown_to_lake(raw) if args.markdown or args.file.endswith(".md") else raw
    created = client.create_doc(book["book_id"], args.title, body, book["page_url"])
    url = f"{client.base_url}/{book['group_login']}/{book['book_slug']}/{created['slug']}"

    result: dict[str, Any] = {
        "title": created["title"],
        "url": url,
        "doc_id": created["id"],
        "book_name": book["book_name"],
        "toc_placed": False,
        "toc_message": None,
        "manual_toc_hint": None,
    }

    # 可选：参考文档同级挂载到 TOC
    if args.after_url:
        ref = client.resolve_doc(args.after_url.split("#")[0])
        if ref["book_id"] != book["book_id"]:
            raise SystemExit("参考文档与目标知识库不一致")
        node = client.find_toc_node(book["book_id"], book["page_url"], doc_slug=ref["doc_slug"])
        if not node:
            result["toc_message"] = f"未在目录中找到参考文档「{ref['title']}」"
        else:
            placed, msg = client.try_place_in_toc(
                book["book_id"], created["id"], after_uuid=node["uuid"], referer=book["page_url"]
            )
            result["toc_placed"] = placed
            result["toc_message"] = msg
            parent_uuid = node.get("parent_uuid")
            if parent_uuid:
                toc = client.get_toc(book["book_id"], book["page_url"])
                parent = next((n for n in toc if n.get("uuid") == parent_uuid), None)
                parent_title = parent.get("title") if parent else "目标目录"
            else:
                parent_title = "知识库根目录"
            if not placed:
                result["manual_toc_hint"] = (
                    f"请在语雀侧边栏打开「{parent_title}」，将新文档「{created['title']}」"
                    f"拖到「{ref['title']}」同级位置。文档链接：{url}"
                )

    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_toc(args: argparse.Namespace) -> None:
    """输出知识库目录树。"""
    client = get_client()
    book = client.resolve_book(args.book_url)
    toc = client.get_toc(book["book_id"], book["page_url"])
    if args.format == "json":
        print(json.dumps(toc, ensure_ascii=False, indent=2))
        return
    for item in toc:
        indent = "  " * max(0, int(item.get("level", 0)))
        slug = item.get("url", "")
        title = item.get("title", "")
        print(f"{indent}- {title} ({slug})")


def cmd_books(args: argparse.Namespace) -> None:
    """列出团队下所有知识库。"""
    client = get_client()
    if args.url:
        client.apply_base_from_url(args.url)
    client.require_base_url()
    group = args.group
    if not group:
        raise SystemExit("请提供 --group（团队 login，URL 中 /{group}/{book} 的第一段）")
    books = client.list_books(group)
    out = [
        {
            "id": b["id"],
            "name": b["name"],
            "slug": b["slug"],
            "url": f"{client.base_url}/{group}/{b['slug']}",
            "items_count": b.get("items_count"),
        }
        for b in books
    ]
    print(json.dumps(out, ensure_ascii=False, indent=2))


def cmd_search(args: argparse.Namespace) -> None:
    """按关键词搜索文档，输出 JSON 数组。"""
    client = get_client()
    book = None
    book_id = args.book_id
    if args.book_url:
        book = client.resolve_book(args.book_url)
        book_id = book["book_id"]
    hits = client.search_docs(args.query, book_id=book_id, book=book, group_login=args.group)
    print(json.dumps(hits, ensure_ascii=False, indent=2))


def main() -> None:
    """CLI 入口：解析子命令并分发；AuthError 统一 exit 2。"""
    parser = argparse.ArgumentParser(description="Yuque docs skill CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    p_cookie = sub.add_parser("cookie", help="Check or save cookie")
    p_cookie.add_argument("--check", action="store_true")
    p_cookie.add_argument("--set", help="Save cookie string to credentials/cookie.txt")
    p_cookie.add_argument(
        "--url",
        help="从语雀链接自动识别 base_url（可单独使用，或与 --check 联用）",
    )
    p_cookie.set_defaults(func=cmd_cookie)

    p_info = sub.add_parser("info", help="Resolve doc URL")
    p_info.add_argument("url")
    p_info.set_defaults(func=cmd_info)

    p_read = sub.add_parser("read", help="Read document")
    p_read.add_argument("url")
    p_read.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    p_read.set_defaults(func=cmd_read)

    p_title = sub.add_parser("title", help="Update title")
    p_title.add_argument("url")
    p_title.add_argument("title")
    p_title.set_defaults(func=cmd_title)

    p_write = sub.add_parser("write", help="Write Markdown/lake body to existing doc")
    p_write.add_argument("url")
    p_write.add_argument("--file", required=True)
    p_write.add_argument("--title")
    p_write.add_argument("--markdown", action="store_true", help="Force Markdown conversion")
    p_write.set_defaults(func=cmd_write)

    p_create = sub.add_parser("create", help="Create new doc in a book")
    p_create.add_argument("--book-url", required=True)
    p_create.add_argument("--title", required=True)
    p_create.add_argument("--file", required=True)
    p_create.add_argument("--markdown", action="store_true")
    p_create.add_argument("--after-url", help="参考文档 URL，新建文档与其平级（同目录下）")
    p_create.set_defaults(func=cmd_create)

    p_toc = sub.add_parser("toc", help="List book TOC")
    p_toc.add_argument("--book-url", required=True)
    p_toc.add_argument("--format", choices=["text", "json"], default="text")
    p_toc.set_defaults(func=cmd_toc)

    p_books = sub.add_parser("books", help="List books in a group")
    p_books.add_argument("--group", help="Group login，即 URL /{group}/{book} 的第一段")
    p_books.add_argument("--url", help="任意语雀链接，用于自动识别 base_url")
    p_books.set_defaults(func=cmd_books)

    p_search = sub.add_parser("search", help="Search docs by keyword in title/description")
    p_search.add_argument("query")
    p_search.add_argument("--book-url")
    p_search.add_argument("--book-id", type=int)
    p_search.add_argument("--group", help="Search all books in group")
    p_search.set_defaults(func=cmd_search)

    args = parser.parse_args()
    try:
        args.func(args)
    except AuthError as e:
        print(json.dumps({"ok": False, "auth_error": True, "message": str(e)}, ensure_ascii=False), file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
