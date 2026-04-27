from __future__ import annotations

"""
QingBlog 静态站点生成脚本（GitHub Issues → HTML）

该脚本由 GitHub Actions 在 Issue 生命周期事件触发时运行，通过环境变量获取 Issue 信息，
并同步更新：
- `article/{id}.html` 文章详情页
- `index.html` / `pages/{n}.html` 首页与分页列表
- `article/index.html` 文章列表页
- `tags/{tag}/...` 标签页
- `sitemap.xml` / `robots.txt` SEO 文件
"""

import json
import os
import re
from datetime import datetime, timedelta, timezone
from typing import Dict, Iterable, List, Optional, Tuple

import markdown
from bs4 import BeautifulSoup

# =============================================================================
# 常量与模板
# =============================================================================

CARD_LI_PREFIX = "<li>"
CARD_LI_SUFFIX = "</li>"

LIST_PAGE_TEMPLATE = (
    "<!DOCTYPE html><html lang=\"zh-CN\"><head><meta charset=\"UTF-8\"/>"
    "<meta name=\"viewport\"content=\"width=device-width, initial-scale=1.0\"/>"
    "<meta name=\"color-scheme\"content=\"light dark\"><title></title>"
    "<meta name=\"description\"content=\"QingBlog - 文章列表\"/>"
    "<link rel=\"shortcut icon\"href=\"/favicon.ico\"type=\"image/x-icon\"/>"
    "<link rel=\"stylesheet\"href=\"/css/QBLOG.css\"/>"
    "<link rel=\"stylesheet\"href=\"/css/font-awesome.min.css\"/>"
    "<style>.card-list{border-top:none}</style>"
    "</head><body><header id=\"title\"><h1></h1></header>"
    "<main class=\"card-list\"><ul class=\"card-list__items\"></ul></main>"
    "<script src=\"/js/QBLOG.js\"></script></body></html>"
)

TAG_PAGE_TEMPLATE = (
    "<!DOCTYPE html><html lang=\"zh-CN\"><head><meta charset=\"UTF-8\"/>"
    "<meta name=\"viewport\"content=\"width=device-width, initial-scale=1.0\"/>"
    "<meta name=\"color-scheme\"content=\"light dark\"><title></title>"
    "<meta name=\"description\"content=\"QingBlog - {tag} 标签下的文章\"/>"
    "<link rel=\"shortcut icon\"href=\"/favicon.ico\"type=\"image/x-icon\"/>"
    "<link rel=\"stylesheet\"href=\"/css/QBLOG.css\">"
    "<link rel=\"stylesheet\"href=\"/css/font-awesome.min.css\">"
    "<style>.card-list{border-top:none}</style>"
    "</head><body><header id=\"title\"><h1>{tag}</h1></header>"
    "<main class=\"card-list\"><ul class=\"card-list__items\"></ul></main>"
    "<script src=\"/js/QBLOG.js\"></script></body></html>"
)

ARTICLE_PAGE_TEMPLATE = (
    "<!DOCTYPE html><html lang=\"zh-CN\"><head><meta charset=\"UTF-8\"/>"
    "<meta name=\"viewport\"content=\"width=device-width, initial-scale=1.0\"/>"
    "<meta name=\"color-scheme\"content=\"light dark\">"
    "<meta name=\"description\"content=\"{title} - QingBlog\"/>"
    "<link rel=\"shortcut icon\"href=\"/favicon.ico\"type=\"image/x-icon\"/>"
    "<title></title>"
    "<link rel=\"stylesheet\"href=\"/css/blogArticle.css\">"
    "<link rel=\"stylesheet\"href=\"/css/QBLOG.css\"/>"
    "<link rel=\"stylesheet\"href=\"/css/font-awesome.min.css\"/>"
    "</head><body><main class=\"card__wrapper\"><article class=\"card\">"
    "<header class=\"card__header\"><h1>{title}</h1><p>作者：{author}</p>"
    "<p>发布日期：<time datetime=\"{date}\">{date}</time></p></header>"
    "<div class=\"divider\"style=\"height:1px;width:100%;margin:1rem 0\"></div>"
    "<div class=\"card__content article-content\">{content_html}</div>"
    "<footer class=\"article-footer\">"
    "<nav class=\"article-tag\" aria-label=\"文章标签\">"
    "<span class=\"article-tag__label\">文章标签：</span>"
    "<ul class=\"article-tag__list\">{tags_html}</ul>"
    "</nav>"
    "</footer></article></main>"
    "<script src=\"/js/QBLOG.js\"></script>"
    "<script>\n"
    "window.MathJax = {\n"
    "  tex: {\n"
    "    inlineMath: [['$','$'],['\\\\(','\\\\)']],\n"
    "    displayMath: [['$$','$$'],['\\\\[','\\\\]']]\n"
    "  },\n"
    "  chtml: { fontCache: 'global' }\n"
    "};\n"
    "</script>\n"
    "<script id=\"MathJax-script\" src=\"https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js\"></script>\n"
    "</body></html>"
)

MD_EXTENSIONS = [
    "extra",
    "toc",
    "sane_lists",
    "codehilite",
    "admonition",
    "meta",
    "pymdownx.highlight",
    "pymdownx.superfences",
    "pymdownx.inlinehilite",
    "pymdownx.details",
    "pymdownx.emoji",
    "pymdownx.tasklist",
    "pymdownx.magiclink",
    "pymdownx.keys",
    "pymdownx.mark",
    "pymdownx.tilde",
    "pymdownx.caret",
    "pymdownx.betterem",
    "pymdownx.saneheaders",
    "pymdownx.arithmatex",
]

MD_EXTENSION_CONFIGS = {
    "codehilite": {"linenums": True, "css_class": "codehilite", "use_pygments": True},
    "toc": {"permalink": "&nbsp;&para;"},
    "pymdownx.highlight": {
        "linenums": True,
        "css_class": "codehilite",
        "use_pygments": True,
        "guess_lang": False,
    },
    "pymdownx.tasklist": {"custom_checkbox": True, "clickable_checkbox": True},
    "pymdownx.arithmatex": {"generic": True},
}

COPY_BUTTON_HTML = (
    "<button type=\"button\" class=\"article-content__copy-btn\" aria-label=\"复制代码\">"
    "<i class=\"fa fa-copy\" aria-hidden=\"true\"></i>&nbsp;Copy</button>"
)


# =============================================================================
# I/O 工具函数
# =============================================================================

def _read_text(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def _write_text(path: str, content: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


# =============================================================================
# 配置
# =============================================================================
#
# 负责加载环境变量、博客配置、页面配置等全局参数。
class Config:
    def __init__(self):
        self.WORKSPACE = os.getenv("GITHUB_WORKSPACE", "") + "/"
        self.BLOG_CONFIG_PATH = os.getenv(
            "BLOG_CONFIG_PATH", "blogData/blogConfig.json"
        )
        self.PAGES_CONFIG_PATH = os.getenv(
            "PAGES_CONFIG_PATH", "blogData/pagesConfig.json"
        )
        self._load_configs()

    def _load_configs(self):
        blog_config = self._load_json(self.BLOG_CONFIG_PATH)
        pages_config = self._load_json(self.PAGES_CONFIG_PATH)

        build_cfg = blog_config.get("buildConfig", {})
        self.UTC_OFFSET = build_cfg.get("utcOffset", 8)
        self.BLOG_ARTICLES_PER_PAGE = build_cfg.get("articlesPerPage", 20)

        author_cfg = blog_config.get("author", {})
        self.TARGET_AUTHOR = author_cfg.get("targetAuthor", "")

        robots_cfg = blog_config.get("robotsConfig", {})
        self.SITE_URL = robots_cfg.get("siteUrl")
        self.ALLOW_PATHS = robots_cfg.get("allowPaths", ["/"])
        self.DISALLOW_PATHS = robots_cfg.get(
            "disallowPaths", ["/.github/", "/.git/", "/blogData/"]
        )
        self.SITEMAP_URL = robots_cfg.get("sitemapUrl")

        self.ISSUE_TITLE = os.getenv("ISSUE_TITLE", "")
        self.ISSUE_BODY = os.getenv("ISSUE_BODY") or "(无内容)"
        self.ISSUE_DATE = os.getenv("ISSUE_DATE", "")
        self.ISSUE_AUTHOR = os.getenv("ISSUE_AUTHOR", "")
        self.ISSUE_LABELS = json.loads(os.getenv("ISSUE_LABELS", "[]"))
        self.ISSUE_ID = os.getenv("ISSUE_ID", "")
        self.ISSUE_ACTION = os.getenv("ISSUE_ACTION", "opened")

        self._pages_config = pages_config

    def _load_json(self, path: str) -> dict:
        full_path = os.path.join(self.WORKSPACE, path)
        if os.path.exists(full_path):
            with open(full_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    @property
    def pages_config(self) -> dict:
        return self._pages_config

    def save_pages_config(self, config_data: dict) -> None:
        full_path = os.path.join(self.WORKSPACE, self.PAGES_CONFIG_PATH)
        _write_text(full_path, json.dumps(config_data, ensure_ascii=False, indent=4))


# =============================================================================
# 通用工具
# =============================================================================

# 将 ISO 时间转为指定时区的中文格式时间
def format_date(iso_date: str, offset: int = 8) -> str:
    dt = datetime.fromisoformat(iso_date.replace("Z", "+00:00"))
    return dt.astimezone(timezone(timedelta(hours=offset))).strftime(
        "%Y年%m月%d日 %H:%M"
    )


# 文本截断：用于列表页卡片摘要
def truncate(text: str, max_len: int = 150) -> str:
    return text[:max_len] + "..." if len(text) > max_len else text


# 生成文章链接（列表页卡片跳转）
def get_link(target_id: str) -> str:
    return f"/article/{target_id}.html"


# =============================================================================
# 列表页 HTML 操作（首页 / 文章列表 / 分页 / 标签页）
# =============================================================================

# 对列表页 HTML 进行卡片增删改查
class HTMLProcessor:
    def __init__(self, path: str) -> None:
        self.path = path
        self.html = _read_text(path)

    def save(self) -> None:
        _write_text(self.path, self.html)

    def find_card(self, issue_id: str) -> Optional[Tuple[int, int]]:
        link = get_link(issue_id)
        start = self.html.find(f'<a href="{link}">')
        if start != -1:
            li_start = self.html.rfind(CARD_LI_PREFIX, 0, start)
            li_end = self.html.find(CARD_LI_SUFFIX, start)
            if li_end != -1:
                return li_start, li_end + 5
        return None

    def remove_card(self, issue_id: str) -> bool:
        pos = self.find_card(issue_id)
        if not pos:
            print(f"[错误] 卡片不存在：{issue_id}")
            return False
        self.html = self.html[: pos[0]] + self.html[pos[1] :]
        print(f"[成功] 卡片已删除：{issue_id}")
        return True

    @staticmethod
    def _gen_tags(labels: List[str]) -> str:
        items = []
        for l in labels[:3]:
            href = f"/tags/{l}/"
            items.append(
                "<li class=\"article-tag__list-item\">"
                f"<a class=\"article-tag__item\" href=\"{href}\">"
                f"<span>{l}</span>"
                "</a>"
                "</li>"
            )
        return "".join(items)

    def _gen_card(
        self, title: str, date: str, content: str, issue_id: str, labels: List[str]
    ) -> str:
        link, tags = get_link(issue_id), self._gen_tags(labels)
        return (
            f"<li><article class=\"card\"><a href=\"{link}\">"
            f"<header class=\"card__header\"><h2>{title}</h2></header>"
            "<div class=\"divider\"style=\"height:1px;width:100%;margin:1rem 0\"></div>"
            f"<p>{content}</p>"
            "<div class=\"divider\"style=\"height:1px;width:100%;margin:1rem 0\"></div>"
            "<footer class=\"card__footer\">"
            "<nav class=\"article-tag\" aria-label=\"文章标签\">"
            "<ul class=\"article-tag__list\">"
            f"{tags}"
            "</ul>"
            "</nav>"
            f"<p>发布日期：<time datetime=\"{date}\">{date}</time></p></footer>"
            "</a></article></li>"
        )

    def count_cards(self) -> int:
        # 兼容历史结构 <li><a ...> 与当前结构 <li><article ...><a ...>
        count_article = self.html.count('<article class="card">')
        count_legacy = self.html.count('<li><a href="')
        return max(count_article, count_legacy)

    def add_or_update(
        self,
        title: str,
        date: str,
        content: str,
        issue_id: str,
        labels: List[str],
        cfg: Optional[Config] = None,
    ) -> bool:
        card = self._gen_card(title, date, content, issue_id, labels)
        pos = self.find_card(issue_id)

        if pos:
            self.html = self.html[: pos[0]] + card + self.html[pos[1] :]
            print(f"[成功] 卡片已更新：{title}")
            return False
        else:
            if cfg and self.count_cards() >= cfg.BLOG_ARTICLES_PER_PAGE:
                print(
                    f"[提示] 当前页面卡片数量已达限制({cfg.BLOG_ARTICLES_PER_PAGE})，需要创建新页面"
                )
                return True

            ul_start = self.html.find("<ul")
            ul_tag_end = self.html.find(">", ul_start)
            self.html = (
                self.html[: ul_tag_end + 1] + card + self.html[ul_tag_end + 1 :]
            )
            print(f"[成功] 卡片已添加：{title}")
            return False


# =============================================================================
# pagesConfig.json 管理
# =============================================================================
#
# 负责维护页数、标签文章统计等运行态数据。
class PagesConfigManager:
    def __init__(self, cfg: Config):
        self.cfg = cfg

    def update_max_article_page_num(self, total_pages: int) -> None:
        config = self.cfg.pages_config
        if "maxPageNum" not in config:
            config["maxPageNum"] = {}
        config["maxPageNum"]["maxArticlePageNum"] = total_pages
        self.cfg.save_pages_config(config)
        print(f"[成功] pagesConfig.json 中 maxArticlePageNum 已更新为：{total_pages}")

    def update_tag_page_nums(self, tag_page_nums: Dict[str, int]) -> None:
        config = self.cfg.pages_config
        if "maxPageNum" not in config:
            config["maxPageNum"] = {}
        if "maxTagPageNums" not in config["maxPageNum"]:
            config["maxPageNum"]["maxTagPageNums"] = {}
        config["maxPageNum"]["maxTagPageNums"].update(tag_page_nums)
        self.cfg.save_pages_config(config)
        print(f"[成功] pagesConfig.json 中 maxTagPageNums 已更新：{tag_page_nums}")

    def update_tags_article_total(self, tag: str, delta: int) -> None:
        config = self.cfg.pages_config
        if "tagsArticleTotal" not in config:
            config["tagsArticleTotal"] = {}
        current = config["tagsArticleTotal"].get(tag, 0)
        new_total = max(0, current + delta)
        if new_total > 0:
            config["tagsArticleTotal"][tag] = new_total
        else:
            if tag in config["tagsArticleTotal"]:
                del config["tagsArticleTotal"][tag]
        self.cfg.save_pages_config(config)
        print(
            f"[成功] pagesConfig.json 中 {tag} 标签文章数已更新：{current} → {new_total}"
        )

    def sync_tag_totals(self, tag_totals: Dict[str, int]) -> None:
        config = self.cfg.pages_config
        config["tagsArticleTotal"] = tag_totals
        self.cfg.save_pages_config(config)
        print(f"[成功] pagesConfig.json 中 tagsArticleTotal 已同步：{tag_totals}")


# =============================================================================
# 列表分页管理（pages/）
# =============================================================================
class PageManager:
    def __init__(self, workspace: str):
        self.workspace = workspace
        self.pages_dir = os.path.join(workspace, "pages")
        os.makedirs(self.pages_dir, exist_ok=True)

    def get_page_path(self, page_num: int) -> str:
        if page_num == 1:
            return os.path.join(self.workspace, "index.html")
        else:
            return os.path.join(self.pages_dir, f"{page_num}.html")

    def create_page(self, page_num: int) -> str:
        path = self.get_page_path(page_num)
        _write_text(path, LIST_PAGE_TEMPLATE)
        print(f"[成功] 页面已创建：{path}")
        return path

    def get_next_page_num(self) -> int:
        page_num = 2
        while os.path.exists(self.get_page_path(page_num)):
            page_num += 1
        return page_num

    def get_total_pages(self) -> int:
        page_num = 1
        while os.path.exists(self.get_page_path(page_num)):
            page_num += 1
        return page_num - 1

    def find_last_non_full_page(self, max_cards: int) -> int:
        total_pages = self.get_total_pages()
        for page_num in range(total_pages, 0, -1):
            path = self.get_page_path(page_num)
            if os.path.exists(path):
                p = HTMLProcessor(path)
                card_count = p.count_cards()
                if card_count < max_cards:
                    return page_num
        return 0

    @staticmethod
    def _parse_tag_dict(existing_tags_str: str) -> dict:
        tag_dict = {}
        tag_lines = existing_tags_str.strip().split("\n")
        for line in tag_lines:
            line = line.strip().rstrip(",")
            if line:
                parts = line.split(":")
                if len(parts) == 2:
                    tag = parts[0].strip().strip("'\"")
                    num = parts[1].strip()
                    tag_dict[tag] = num
        return tag_dict

    @staticmethod
    def _build_tag_str(tag_dict: dict, indent: int = 2) -> str:
        tag_entries = [f"'{tag}': {num}" for tag, num in tag_dict.items()]
        indent_str = " " * indent
        replacement = "{"
        for entry in tag_entries:
            replacement += f"\n{indent_str}{entry},"
        replacement = replacement.rstrip(",") + "\n}"
        return replacement

    @staticmethod
    def _update_tag_dict(existing_dict: dict, tag_updates: dict) -> dict:
        new_dict = existing_dict.copy()
        for tag, num in tag_updates.items():
            if num > 0:
                new_dict[tag] = str(num)
            elif tag in new_dict:
                del new_dict[tag]
        return new_dict


# =============================================================================
# 标签页管理（tags/）
# =============================================================================
class TagManager:
    def __init__(self, workspace: str):
        self.tags_dir = os.path.join(workspace, "tags")

    def _get_tag_page_path(self, tag_name: str, page_num: int = 1) -> str:
        if page_num == 1:
            return os.path.join(self.tags_dir, f"{tag_name}", "index.html")
        else:
            return os.path.join(self.tags_dir, f"{tag_name}", f"{page_num}.html")

    def _get_tag_dir(self, tag_name: str) -> str:
        return os.path.join(self.tags_dir, tag_name)

    def create_page(self, name: str, page_num: int = 1) -> None:
        tag_dir = self._get_tag_dir(name)
        path = self._get_tag_page_path(name, page_num)
        if os.path.exists(path):
            print(f"[提示] 标签页面已存在：{name} 第{page_num}页")
            return
        os.makedirs(tag_dir, exist_ok=True)
        _write_text(path, TAG_PAGE_TEMPLATE.format(tag=name))
        print(f"[成功] 标签页面已创建：{name} 第{page_num}页")

    def get_tag_page_count(self, tag_name: str) -> int:
        page_num = 1
        while os.path.exists(self._get_tag_page_path(tag_name, page_num)):
            page_num += 1
        return page_num - 1

    def sync(
        self,
        issue_id: str,
        title: str,
        date: str,
        content: str,
        target: List[str],
        all_labels: List[str],
        op: str = "add",
        max_cards: int = 20,
    ) -> dict:
        tag_page_nums = {}
        for label in target:
            if op == "add":
                self.create_page(label)
                found = False
                path = self._get_tag_page_path(label)
                if os.path.exists(path):
                    p = HTMLProcessor(path)
                    if p.find_card(issue_id):
                        p.add_or_update(
                            title, date, content, issue_id, all_labels, None
                        )
                        p.save()
                        print(f"[成功] 卡片已更新：{issue_id}")
                        found = True
                if found:
                    continue

                page_num = 1
                while True:
                    path = self._get_tag_page_path(label, page_num)
                    if not os.path.exists(path):
                        self.create_page(label, page_num)
                        path = self._get_tag_page_path(label, page_num)

                    p = HTMLProcessor(path)
                    if p.count_cards() < max_cards:
                        p.add_or_update(
                            title, date, content, issue_id, all_labels, None
                        )
                        p.save()
                        print(f"[成功] 卡片已添加到标签页：{label} 第{page_num}页")
                        break
                    else:
                        page_num += 1

            elif op == "remove":
                page_num = 1
                while os.path.exists(self._get_tag_page_path(label, page_num)):
                    path = self._get_tag_page_path(label, page_num)
                    p = HTMLProcessor(path)
                    p.remove_card(issue_id)
                    p.save()
                    page_num += 1
                print(f"[成功] 卡片已从标签页删除：{label}")

            tag_page_nums[label] = self.get_tag_page_count(label)
        return tag_page_nums


# =============================================================================
# Markdown 渲染
# =============================================================================

# 转义 Markdown 中特殊字符，避免解析异常
def escape_special_chars(md: str) -> str:
    block_pat = re.compile(r'\\\[[\s\S]*?\\\]')
    inline_pat = re.compile(r'\\\([\s\S]*?\\\)')
    store = {}
    idx = 0

    def save(m):
        nonlocal idx
        k = f"__FML{idx}__"
        store[k] = m.group(0)
        idx += 1
        return k

    md = block_pat.sub(save, md)
    md = inline_pat.sub(save, md)

    lines = md.split("\n")
    result = []
    for line in lines:
        stripped = line.lstrip()
        indent = line[: len(line) - len(stripped)]
        if stripped.startswith(("- ", "* ", "+ ")):
            marker = stripped[:2]
            content = stripped[2:]
            if content.startswith(("[ ] ", "[x] ", "[X] ")):
                task_marker = content[:4]
                rest = content[4:].replace("[", "\\[").replace("]", "\\]")
                content = task_marker + rest
            else:
                content = content.replace("[", "\\[").replace("]", "\\]")
            if content.startswith(">"):
                content = "\\" + content
            line = indent + marker + content
        result.append(line)
    md = "\n".join(result)

    for k, v in store.items():
        md = md.replace(k, v)
    return md


# Markdown 转 HTML（代码高亮 / 任务列表 / 数学公式等扩展）
def md_to_html(md: str) -> str:
    md = escape_special_chars(md)
    html = markdown.markdown(
        md,
        extensions=MD_EXTENSIONS,
        extension_configs=MD_EXTENSION_CONFIGS,
        output_format="html5",
    )
    soup = BeautifulSoup(html, "html.parser")
    for pre in soup.select("td.code pre"):
        copy_btn = BeautifulSoup(COPY_BUTTON_HTML, "html.parser")
        pre.insert(0, copy_btn)
    return str(soup)


# =============================================================================
# 文章详情页（article/）
# =============================================================================

# 生成、删除、查询文章详情页
class ArticleManager:
    def __init__(self, workspace: str, cfg: Config = None):
        self.pages_dir = os.path.join(workspace, "article")
        self.cfg = cfg
        os.makedirs(self.pages_dir, exist_ok=True)

    def _path(self, issue_id: str) -> str:
        return os.path.join(self.pages_dir, f"{issue_id}.html")

    def exists(self, issue_id: str) -> bool:
        return os.path.exists(self._path(issue_id))

    def delete(self, issue_id: str) -> bool:
        path = self._path(issue_id)
        if not os.path.exists(path):
            print(f"[错误] 文章文件不存在：{path}")
            return False
        os.remove(path)
        print(f"[成功] 文章已删除：{path}")
        return True

    def extract_labels(self, issue_id: str) -> List[str]:
        path = self._path(issue_id)
        if not os.path.exists(path):
            return []
        with open(path, "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f.read(), "html.parser")
            return list(
                {
                    span.get_text(strip=True)
                    for span in soup.select(".article-tag__item span")
                    if span.get_text(strip=True)
                }
            )

    def generate(
        self,
        issue_id: str,
        title: str,
        author: str,
        date: str,
        content: str,
        labels: List[str],
    ) -> None:
        try:
            date = datetime.strptime(date, "%Y年%m月%d日 %H:%M:%S").strftime(
                "%Y年%m月%d日 %H:%M"
            )
        except ValueError:
            pass
        is_update = self.exists(issue_id)
        tags = HTMLProcessor._gen_tags(labels)
        html = ARTICLE_PAGE_TEMPLATE.format(
            title=title,
            author=author,
            date=date,
            content_html=md_to_html(content),
            tags_html=tags,
        )
        _write_text(self._path(issue_id), html)
        print(f"[成功] 文章已{'更新' if is_update else '生成'}：{self._path(issue_id)}")


# =============================================================================
# SEO（sitemap.xml / robots.txt）
# =============================================================================

# 自动生成网站地图 sitemap.xml
class SitemapGenerator:
    def __init__(self, workspace: str, cfg: Config):
        self.workspace = workspace
        self.cfg = cfg

    def scan_html_files(
        self, directory: str, exclude_dirs: Optional[List[str]] = None
    ) -> List[str]:
        if exclude_dirs is None:
            exclude_dirs = []
        html_files = []
        for root, dirs, files in os.walk(directory):
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
            for file in files:
                if file.endswith(".html"):
                    full_path = os.path.join(root, file)
                    rel_path = os.path.relpath(full_path, self.workspace)
                    url_path = "/" + rel_path.replace("\\", "/")
                    html_files.append(url_path)
        return sorted(html_files)

    def get_file_mod_time(self, file_path: str) -> str:
        try:
            mtime = os.path.getmtime(file_path)
            return datetime.fromtimestamp(mtime).strftime("%Y-%m-%dT%H:%M:%S+08:00")
        except:
            return datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00")

    def generate(self) -> None:
        print("\n[信息] 开始生成 sitemap.xml...")
        urls = []
        static_pages = ["/", "/article/", "/tags/", "/data/", "/about/"]
        for page in static_pages:
            full_path = (
                os.path.join(self.workspace, page.lstrip("/"), "index.html")
                if page != "/"
                else os.path.join(self.workspace, "index.html")
            )
            if os.path.exists(full_path):
                urls.append(
                    {
                        "loc": f"{self.cfg.SITE_URL}{page}",
                        "lastmod": self.get_file_mod_time(full_path),
                        "changefreq": "daily",
                        "priority": "1.0" if page == "/" else "0.8",
                    }
                )
        pages_config = self.cfg.pages_config
        max_article_page = pages_config.get("maxPageNum", {}).get(
            "maxArticlePageNum", 1
        )
        for i in range(2, max_article_page + 1):
            page_path = f"/pages/{i}.html"
            full_path = os.path.join(self.workspace, "pages", f"{i}.html")
            if os.path.exists(full_path):
                urls.append(
                    {
                        "loc": f"{self.cfg.SITE_URL}{page_path}",
                        "lastmod": self.get_file_mod_time(full_path),
                        "changefreq": "weekly",
                        "priority": "0.7",
                    }
                )
        max_tag_page_nums = pages_config.get("maxPageNum", {}).get("maxTagPageNums", {})
        for tag, page_count in max_tag_page_nums.items():
            for i in range(1, int(page_count) + 1):
                if i == 1:
                    tag_path = f"/tags/{tag}/"
                    full_path = os.path.join(self.workspace, "tags", tag, "index.html")
                else:
                    tag_path = f"/tags/{tag}/{i}.html"
                    full_path = os.path.join(self.workspace, "tags", tag, f"{i}.html")
                if os.path.exists(full_path):
                    urls.append(
                        {
                            "loc": f"{self.cfg.SITE_URL}{tag_path}",
                            "lastmod": self.get_file_mod_time(full_path),
                            "changefreq": "weekly",
                            "priority": "0.6",
                        }
                    )
        article_dir = os.path.join(self.workspace, "article")
        if os.path.exists(article_dir):
            for file in os.listdir(article_dir):
                if file.endswith(".html"):
                    full_path = os.path.join(article_dir, file)
                    article_id = file.replace(".html", "")
                    urls.append(
                        {
                            "loc": f"{self.cfg.SITE_URL}/article/{article_id}.html",
                            "lastmod": self.get_file_mod_time(full_path),
                            "changefreq": "monthly",
                            "priority": "0.9",
                        }
                    )
        xml_content = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        for url in urls:
            xml_content += f'  <url>\n    <loc>{url["loc"]}</loc>\n    <lastmod>{url["lastmod"]}</lastmod>\n    <changefreq>{url["changefreq"]}</changefreq>\n    <priority>{url["priority"]}</priority>\n  </url>\n'
        xml_content += "</urlset>\n"
        sitemap_path = os.path.join(self.workspace, "sitemap.xml")
        _write_text(sitemap_path, xml_content)
        print(f"[成功] sitemap.xml 已生成，共 {len(urls)} 个URL")


# 生成 robots.txt
class RobotsGenerator:
    def __init__(self, workspace: str, cfg: Config):
        self.workspace = workspace
        self.cfg = cfg

    def generate(self) -> None:
        print("\n[信息] 开始生成 robots.txt...")
        generator_name = os.path.basename(__file__)
        robots_content = (
            f"# robots.txt for {self.cfg.SITE_URL}\n"
            f"# Generated automatically by {generator_name}\n\n"
            "User-agent: *\n"
        )
        for path in self.cfg.ALLOW_PATHS:
            robots_content += f"Allow: {path}\n"
        robots_content += "\n"
        for path in self.cfg.DISALLOW_PATHS:
            robots_content += f"Disallow: {path}\n"
        robots_content += f"\n# Sitemap\nSitemap: {self.cfg.SITEMAP_URL}\n"
        robots_path = os.path.join(self.workspace, "robots.txt")
        _write_text(robots_path, robots_content)
        print(f"[成功] robots.txt 已生成")


# =============================================================================
# 主流程调度
# =============================================================================
class BlogGenerator:
    def __init__(self):
        self.cfg = Config()
        self.article = ArticleManager(self.cfg.WORKSPACE, self.cfg)
        self.tag = TagManager(self.cfg.WORKSPACE)
        self.page = PageManager(self.cfg.WORKSPACE)
        self.pages_config_mgr = PagesConfigManager(self.cfg)
        self.sitemap_gen = SitemapGenerator(self.cfg.WORKSPACE, self.cfg)
        self.robots_gen = RobotsGenerator(self.cfg.WORKSPACE, self.cfg)

    def _log(self) -> None:
        date = format_date(self.cfg.ISSUE_DATE, self.cfg.UTC_OFFSET)
        body_len = len(self.cfg.ISSUE_BODY or "")
        print(f"\n[信息] 标题：{self.cfg.ISSUE_TITLE}\n[信息] 内容：<已隐藏>（长度：{body_len}）")
        print(f"[信息] 发布日期：{date}\n[信息] 发布者：{self.cfg.ISSUE_AUTHOR}")
        print(
            f"[信息] 标签：{', '.join(self.cfg.ISSUE_LABELS) if self.cfg.ISSUE_LABELS else '无'}"
        )
        print("=" * 50)

    def _iter_existing_page_paths(self) -> Iterable[str]:
        """遍历现有列表页路径：`index.html` + `pages/2..N`。"""
        yield os.path.join(self.cfg.WORKSPACE, "index.html")
        page_num = 2
        while os.path.exists(self.page.get_page_path(page_num)):
            yield self.page.get_page_path(page_num)
            page_num += 1

    def _try_update_card_in_pages(
        self,
        title: str,
        date: str,
        content: str,
        issue_id: str,
        labels: List[str],
    ) -> bool:
        """若卡片已存在于任意列表页则更新之；更新成功返回 True。"""
        for path in self._iter_existing_page_paths():
            if not os.path.exists(path):
                continue
            p = HTMLProcessor(path)
            if p.find_card(issue_id):
                p.add_or_update(title, date, content, issue_id, labels, self.cfg)
                p.save()
                return True
        return False

    def _remove_card_from_all_pages(self, issue_id: str) -> None:
        for path in self._iter_existing_page_paths():
            if not os.path.exists(path):
                continue
            p = HTMLProcessor(path)
            p.remove_card(issue_id)
            p.save()

    def _update_indices(
        self, title: str, date: str, content: str, issue_id: str, labels: List[str]
    ) -> None:
        is_update = self._try_update_card_in_pages(
            title, date, content, issue_id, labels
        )
        if not is_update:
            last_non_full_page = self.page.find_last_non_full_page(
                self.cfg.BLOG_ARTICLES_PER_PAGE
            )
            if last_non_full_page == 0:
                next_page_num = self.page.get_next_page_num()
                new_page_path = self.page.create_page(next_page_num)
                p_new = HTMLProcessor(new_page_path)
                p_new.add_or_update(title, date, content, issue_id, labels, self.cfg)
                p_new.save()
                self.pages_config_mgr.update_max_article_page_num(
                    self.page.get_total_pages()
                )
                print(f"[成功] 卡片已添加到新页面：{new_page_path}")
            else:
                page_path = self.page.get_page_path(last_non_full_page)
                p_target = HTMLProcessor(page_path)
                p_target.add_or_update(title, date, content, issue_id, labels, self.cfg)
                p_target.save()
                print(f"[成功] 卡片已添加到页面 {last_non_full_page}：{page_path}")
        idx = os.path.join(self.cfg.WORKSPACE, "article", "index.html")
        p = HTMLProcessor(idx)
        p.add_or_update(title, date, content, issue_id, labels, self.cfg)
        p.save()

    def handle_delete(self) -> None:
        print(f"\n[操作] 删除文章：ID {self.cfg.ISSUE_ID}")
        old = self.article.extract_labels(self.cfg.ISSUE_ID)
        print(f"[信息] 旧标签：{', '.join(old) if old else '无'}")
        self.article.delete(self.cfg.ISSUE_ID)
        self._remove_card_from_all_pages(self.cfg.ISSUE_ID)
        idx = os.path.join(self.cfg.WORKSPACE, "article", "index.html")
        p = HTMLProcessor(idx)
        p.remove_card(self.cfg.ISSUE_ID)
        p.save()
        if old:
            tag_page_nums = self.tag.sync(
                self.cfg.ISSUE_ID,
                "",
                "",
                "",
                old,
                [],
                "remove",
                self.cfg.BLOG_ARTICLES_PER_PAGE,
            )
            for tag in old:
                self.pages_config_mgr.update_tags_article_total(tag, -1)
            self.pages_config_mgr.update_max_article_page_num(
                self.page.get_total_pages()
            )
            self.pages_config_mgr.update_tag_page_nums(tag_page_nums)
        print("=" * 50 + "\n[成功] 删除操作完成")

    def handle_create_update(self) -> None:
        date = format_date(self.cfg.ISSUE_DATE, self.cfg.UTC_OFFSET)
        self._log()
        is_new = not self.article.exists(self.cfg.ISSUE_ID)
        old = [] if is_new else self.article.extract_labels(self.cfg.ISSUE_ID)
        if not is_new:
            print(f"[信息] 旧标签：{', '.join(old) if old else '无'}")
        self.article.generate(
            self.cfg.ISSUE_ID,
            self.cfg.ISSUE_TITLE,
            self.cfg.ISSUE_AUTHOR,
            date,
            self.cfg.ISSUE_BODY,
            self.cfg.ISSUE_LABELS,
        )
        self._update_indices(
            self.cfg.ISSUE_TITLE,
            date,
            truncate(self.cfg.ISSUE_BODY),
            self.cfg.ISSUE_ID,
            self.cfg.ISSUE_LABELS,
        )

        if is_new:
            if self.cfg.ISSUE_LABELS:
                tag_page_nums = self.tag.sync(
                    self.cfg.ISSUE_ID,
                    self.cfg.ISSUE_TITLE,
                    date,
                    truncate(self.cfg.ISSUE_BODY),
                    self.cfg.ISSUE_LABELS,
                    self.cfg.ISSUE_LABELS,
                    max_cards=self.cfg.BLOG_ARTICLES_PER_PAGE,
                )
                for tag in self.cfg.ISSUE_LABELS:
                    self.pages_config_mgr.update_tags_article_total(tag, 1)
                self.pages_config_mgr.update_max_article_page_num(
                    self.page.get_total_pages()
                )
                self.pages_config_mgr.update_tag_page_nums(tag_page_nums)
        else:
            to_add = [l for l in self.cfg.ISSUE_LABELS if l not in old]
            to_remove = [l for l in old if l not in self.cfg.ISSUE_LABELS]
            to_keep = [l for l in self.cfg.ISSUE_LABELS if l in old]
            tag_page_nums = {}
            if to_remove:
                remove_nums = self.tag.sync(
                    self.cfg.ISSUE_ID,
                    "",
                    "",
                    "",
                    to_remove,
                    [],
                    "remove",
                    self.cfg.BLOG_ARTICLES_PER_PAGE,
                )
                for tag in to_remove:
                    self.pages_config_mgr.update_tags_article_total(tag, -1)
                tag_page_nums.update(remove_nums)
            if to_add:
                add_nums = self.tag.sync(
                    self.cfg.ISSUE_ID,
                    self.cfg.ISSUE_TITLE,
                    date,
                    truncate(self.cfg.ISSUE_BODY),
                    to_add,
                    self.cfg.ISSUE_LABELS,
                    max_cards=self.cfg.BLOG_ARTICLES_PER_PAGE,
                )
                for tag in to_add:
                    self.pages_config_mgr.update_tags_article_total(tag, 1)
                tag_page_nums.update(add_nums)
            if to_keep:
                keep_nums = self.tag.sync(
                    self.cfg.ISSUE_ID,
                    self.cfg.ISSUE_TITLE,
                    date,
                    truncate(self.cfg.ISSUE_BODY),
                    to_keep,
                    self.cfg.ISSUE_LABELS,
                    max_cards=self.cfg.BLOG_ARTICLES_PER_PAGE,
                )
                tag_page_nums.update(keep_nums)
            if tag_page_nums:
                self.pages_config_mgr.update_max_article_page_num(
                    self.page.get_total_pages()
                )
                self.pages_config_mgr.update_tag_page_nums(tag_page_nums)

    def run(self) -> None:
        if self.cfg.ISSUE_AUTHOR != self.cfg.TARGET_AUTHOR:
            print(
                f"[跳过] 作者不匹配 ({self.cfg.ISSUE_AUTHOR} != {self.cfg.TARGET_AUTHOR})"
            )
            return
        print(f"\n{'='*50}\n[操作] Issue操作：{self.cfg.ISSUE_ACTION}\n{'='*50}")
        if self.cfg.ISSUE_ACTION == "deleted":
            self.handle_delete()
        else:
            self.handle_create_update()
        self.sitemap_gen.generate()
        self.robots_gen.generate()


# =============================================================================
# 程序入口
# =============================================================================
if __name__ == "__main__":
    BlogGenerator().run()
