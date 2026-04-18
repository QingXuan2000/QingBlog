"""
GitHub Issues Blog Build
"""

import os
import json
import re
from datetime import datetime, timezone, timedelta
from typing import List, Optional, Tuple
import markdown
from bs4 import BeautifulSoup

# 配置


class Config:
    def __init__(self):
        self.WORKSPACE = os.getenv("GITHUB_WORKSPACE", "") + "/"
        self.BLOG_CONFIG_PATH = os.getenv("BLOG_CONFIG_PATH", "blogData/blogConfig.json")
        self.PAGES_CONFIG_PATH = os.getenv("PAGES_CONFIG_PATH", "blogData/pagesConfig.json")
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
        self.DISALLOW_PATHS = robots_cfg.get("disallowPaths", ["/.github/", "/.git/", "/blogData/"])
        self.SITEMAP_URL = robots_cfg.get("sitemapUrl")

        self.ISSUE_TITLE = os.getenv("ISSUE_TITLE", "")
        self.ISSUE_BODY = os.getenv("ISSUE_BODY") or "(无内容)"
        self.ISSUE_DATE = os.getenv("ISSUE_DATE", "")
        self.ISSUE_AUTHOR = os.getenv("ISSUE_AUTHOR", "")
        self.ISSUE_LABELS = json.loads(os.getenv("ISSUE_LABELS", "[]"))
        self.ISSUE_ID = os.getenv("ISSUE_ID", "")
        self.ISSUE_ACTION = os.getenv("ISSUE_ACTION", "opened")

        self._pages_config = pages_config

    def _load_json(self, path):
        full_path = os.path.join(self.WORKSPACE, path)
        if os.path.exists(full_path):
            with open(full_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    @property
    def pages_config(self):
        return self._pages_config

    def save_pages_config(self, config_data):
        full_path = os.path.join(self.WORKSPACE, self.PAGES_CONFIG_PATH)
        # 确保目录存在
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "w", encoding="utf-8") as f:
            json.dump(config_data, f, ensure_ascii=False, indent=4)


# 工具函数


def format_date(iso_date: str, offset: int = 8) -> str:
    dt = datetime.fromisoformat(iso_date.replace("Z", "+00:00"))
    return dt.astimezone(timezone(timedelta(hours=offset))).strftime(
        "%Y年%m月%d日 %H:%M"
    )


def truncate(text: str, max_len: int = 150) -> str:
    return text[:max_len] + "..." if len(text) > max_len else text


def get_link(target_id: str) -> str:
    return f"/article/{target_id}.html"


# HTML 处理器


class HTMLProcessor:
    def __init__(self, path: str) -> None:
        self.path = path
        with open(path, "r", encoding="utf-8") as f:
            self.html = f.read()

    def save(self) -> None:
        with open(self.path, "w", encoding="utf-8") as f:
            f.write(self.html)

    def find_card(self, issue_id: str) -> Optional[Tuple[int, int]]:
        link = get_link(issue_id)
        start = self.html.find(f'<a href="{link}">')
        if start != -1:
            li_start = self.html.rfind("<li>", 0, start)
            li_end = self.html.find("</li>", start)
            if li_end != -1:
                return li_start, li_end + 5
        return None

    def remove_card(self, issue_id: str) -> bool:
        pos = self.find_card(issue_id)
        if not pos:
            print(f"❌ 卡片不存在：{issue_id}")
            return False
        self.html = self.html[: pos[0]] + self.html[pos[1] :]
        print(f"✅ 卡片已删除：{issue_id}")
        return True

    @staticmethod
    def _gen_tags(labels: List[str]) -> str:
        return "".join(f'<div class="tag"><span>{l}</span></div>' for l in labels[:3])

    def _gen_card(self, title: str, date: str, content: str, issue_id: str, labels: List[str]) -> str:
        link, tags = get_link(issue_id), self._gen_tags(labels)
        return f"""<li><a href="{link}"><div class="card"><div class="card-header"><h2>{title}</h2></div><div class="divider"style="height:1px;width:100%;margin:1rem 0"></div><p>{content}</p><div class="divider"style="height:1px;width:100%;margin:1rem 0"></div><div class="card-footer"><div class="article-tag">{tags}</div><p>发布日期：{date}</p></div></div></a></li>"""

    def count_cards(self) -> int:
        """统计当前页面中的卡片数量"""
        return self.html.count('<li><a href="')

    def add_or_update(
        self,
        title: str,
        date: str,
        content: str,
        issue_id: str,
        labels: List[str],
        cfg: Config = None,
    ) -> bool:
        """
        添加或更新卡片，返回是否需要创建新页面
        """
        card = self._gen_card(title, date, content, issue_id, labels)
        pos = self.find_card(issue_id)

        if pos:
            # 更新现有卡片
            self.html = self.html[: pos[0]] + card + self.html[pos[1] :]
            print(f"✅ 卡片已更新：{title}")
            return False
        else:
            # 添加新卡片
            ul_start = self.html.find("<ul")
            ul_end = self.html.find("</ul>", ul_start)

            # 检查是否需要分页
            if cfg and self.count_cards() >= cfg.BLOG_ARTICLES_PER_PAGE:
                print(
                    f"❌ 当前页面卡片数量已达限制({cfg.BLOG_ARTICLES_PER_PAGE})，需要创建新页面"
                )
                return True

            # 添加卡片到当前页面
            self.html = self.html[:ul_end] + card + self.html[ul_end:]
            print(f"✅ 卡片已添加：{title}")
            return False


# 页面配置管理


class PagesConfigManager:
    def __init__(self, cfg: Config):
        self.cfg = cfg

    def update_max_article_page_num(self, total_pages: int) -> None:
        config = self.cfg.pages_config
        if "maxPageNum" not in config:
            config["maxPageNum"] = {}
        config["maxPageNum"]["maxArticlePageNum"] = total_pages
        self.cfg.save_pages_config(config)
        print(f"✅ pagesConfig.json 中 maxArticlePageNum 已更新为：{total_pages}")

    def update_tag_page_nums(self, tag_page_nums: dict) -> None:
        config = self.cfg.pages_config
        if "maxPageNum" not in config:
            config["maxPageNum"] = {}
        if "maxTagPageNums" not in config["maxPageNum"]:
            config["maxPageNum"]["maxTagPageNums"] = {}
        config["maxPageNum"]["maxTagPageNums"].update(tag_page_nums)
        self.cfg.save_pages_config(config)
        print(f"✅ pagesConfig.json 中 maxTagPageNums 已更新：{tag_page_nums}")

    def update_tags_article_total(self, tag: str, delta: int) -> None:
        config = self.cfg.pages_config
        if "tagsArtiAcleTotal" not in config:
            config["tagsArtiAcleTotal"] = {}
        current = config["tagsArtiAcleTotal"].get(tag, 0)
        new_total = max(0, current + delta)
        if new_total > 0:
            config["tagsArtiAcleTotal"][tag] = new_total
        else:
            if tag in config["tagsArtiAcleTotal"]:
                del config["tagsArtiAcleTotal"][tag]
        self.cfg.save_pages_config(config)
        print(f"✅ pagesConfig.json 中 {tag} 标签文章数已更新：{current} → {new_total}")

    def sync_tag_totals(self, tag_totals: dict) -> None:
        config = self.cfg.pages_config
        config["tagsArtiAcleTotal"] = tag_totals
        self.cfg.save_pages_config(config)
        print(f"✅ pagesConfig.json 中 tagsArtiAcleTotal 已同步：{tag_totals}")


# 分页管理


class PageManager:
    def __init__(self, workspace: str):
        self.workspace = workspace
        self.pages_dir = os.path.join(workspace, "pages")
        os.makedirs(self.pages_dir, exist_ok=True)

    def get_page_path(self, page_num: int) -> str:
        """获取页面路径"""
        if page_num == 1:
            return os.path.join(self.workspace, "index.html")
        else:
            return os.path.join(self.pages_dir, f"{page_num}.html")

    def create_page(self, page_num: int) -> str:
        """创建新页面"""
        path = self.get_page_path(page_num)

        # 创建基础页面结构
        with open(path, "w", encoding="utf-8") as f:
            f.write(
                f"""<!DOCTYPE html><html lang="zh-CN"><head><meta charset="UTF-8"/><meta name="viewport"content="width=device-width, initial-scale=1.0"/><meta name="color-scheme"content="light dark"><title></title><link rel="shortcut icon"href="/favicon.ico"type="image/x-icon"/></head><body><div id="card-list-wrapper"><ul id="card-list"></ul></div><link rel="stylesheet"href="/css/QBLOG.css"/><script src="/js/QBLOG.js"></script><link rel="stylesheet"href="/css/font-awesome.min.css"/><style>#card-list-wrapper{{border-top:none}}</style></body></html>"""
            )
        print(f"✅ 页面已创建：{path}")
        return path

    def get_next_page_num(self) -> int:
        """获取下一个页面编号"""
        page_num = 2
        while os.path.exists(self.get_page_path(page_num)):
            page_num += 1
        return page_num

    def get_total_pages(self) -> int:
        """获取总页面数"""
        page_num = 1
        while os.path.exists(self.get_page_path(page_num)):
            page_num += 1
        return page_num - 1

    def find_last_non_full_page(self, max_cards: int) -> int:
        """查找最后一个未满的页面编号，返回0表示没有，需要从首页开始"""
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
        """解析标签配置字符串为字典"""
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
        """构建标签配置字符串"""
        tag_entries = [f"'{tag}': {num}" for tag, num in tag_dict.items()]
        indent_str = " " * indent
        replacement = "{"
        for entry in tag_entries:
            replacement += f"\n{indent_str}{entry},"
        replacement = replacement.rstrip(",") + "\n}"
        return replacement

    @staticmethod
    def _update_tag_dict(existing_dict: dict, tag_updates: dict) -> dict:
        """更新标签字典，删除数量为0的标签"""
        new_dict = existing_dict.copy()
        for tag, num in tag_updates.items():
            if num > 0:
                new_dict[tag] = str(num)
            elif tag in new_dict:
                del new_dict[tag]
        return new_dict

    def update_max_page_num(self, total_pages: int, tag_page_nums: dict = None) -> None:
        """更新QBLOG.js中的maxArticlePageNum值和maxTagPageNums值"""

        js_path = os.path.join(self.workspace, "js", "QBLOG.js")
        if os.path.exists(js_path):
            with open(js_path, "r", encoding="utf-8") as f:
                content = f.read()

            content = re.sub(
                r"maxArticlePageNum: \d+,",
                f"maxArticlePageNum: {total_pages},",
                content,
            )

            if tag_page_nums:
                pattern = r"maxTagPageNums: \{([^\}]*)\}"
                match = re.search(pattern, content)
                if match:
                    existing_tags = match.group(1)
                    existing_tag_dict = self._parse_tag_dict(existing_tags)
                    new_tag_dict = self._update_tag_dict(
                        existing_tag_dict, tag_page_nums
                    )
                    replacement = "maxTagPageNums: " + self._build_tag_str(
                        new_tag_dict, 6
                    )
                    content = re.sub(pattern, replacement, content)

            content = re.sub(
                r"const maxArticlePageNum = \d+;",
                f"const maxArticlePageNum = {total_pages};",
                content,
            )

            if tag_page_nums:
                pattern = r"const maxTagPageNums = \{([^\}]*)\};"
                match = re.search(pattern, content)
                if match:
                    existing_tags = match.group(1)
                    existing_tag_dict = self._parse_tag_dict(existing_tags)
                    new_tag_dict = self._update_tag_dict(
                        existing_tag_dict, tag_page_nums
                    )
                    replacement = (
                        "const maxTagPageNums = "
                        + self._build_tag_str(new_tag_dict, 2)
                        + ";"
                    )
                    content = re.sub(pattern, replacement, content)
                else:
                    pattern = r"const maxArticlePageNum = \d+;"
                    tag_entries = [
                        f"'{tag}': {num}"
                        for tag, num in tag_page_nums.items()
                        if num > 0
                    ]
                    if tag_entries:
                        replacement = f"const maxArticlePageNum = {total_pages};\nconst maxTagPageNums = {{"
                        for entry in tag_entries:
                            replacement += f"\n  {entry},"
                        replacement = replacement.rstrip(",") + "\n};"
                        content = re.sub(pattern, replacement, content)

            with open(js_path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"✅ QBLOG.js 中 maxArticlePageNum 已更新为：{total_pages}")
            if tag_page_nums:
                print(f"✅ QBLOG.js 中 maxTagPageNums 已更新")



class TagManager:
    def __init__(self, workspace: str):
        self.tags_dir = os.path.join(workspace, "tags")

    def _get_tag_page_path(self, tag_name: str, page_num: int = 1) -> str:
        """获取标签页面路径"""
        if page_num == 1:
            return os.path.join(self.tags_dir, f"{tag_name}", "index.html")
        else:
            return os.path.join(self.tags_dir, f"{tag_name}", f"{page_num}.html")

    def _get_tag_dir(self, tag_name: str) -> str:
        """获取标签目录"""
        return os.path.join(self.tags_dir, tag_name)

    def create_page(self, name: str, page_num: int = 1) -> None:
        tag_dir = self._get_tag_dir(name)
        path = self._get_tag_page_path(name, page_num)
        if os.path.exists(path):
            print(f"❌ 标签页面已存在：{name} 第{page_num}页")
            return
        os.makedirs(tag_dir, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(
                f"""<!DOCTYPE html><html lang="zh-CN"><head><meta charset="UTF-8"><meta name="viewport"content="width=device-width, initial-scale=1.0"><title></title></head><body><div id="title"><h1>{name}</h1></div><div id="card-list-wrapper"><ul id="card-list"></ul></div><link rel="stylesheet"href="/css/QBLOG.css"><script src="/js/QBLOG.js"></script><link rel="stylesheet"href="/css/font-awesome.min.css"><style>#card-list-wrapper{{border-top:none}}</style></body></html>"""
            )
        print(f"✅ 标签页面已创建：{name} 第{page_num}页")

    def get_tag_page_count(self, tag_name: str) -> int:
        """获取标签页的总页数"""
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
        """同步标签页，返回各标签的总页数"""
        tag_page_nums = {}

        for label in target:
            if op == "add":
                self.create_page(label)
                # 查找是否是更新现有卡片
                found = False
                path = self._get_tag_page_path(label)
                if os.path.exists(path):
                    p = HTMLProcessor(path)
                    if p.find_card(issue_id):
                        p.add_or_update(
                            title, date, content, issue_id, all_labels, None
                        )
                        p.save()
                        print(f"✅ 卡片已更新：{issue_id}")
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
                        print(f"✅ 卡片已添加到标签页：{label} 第{page_num}页")
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
                print(f"✅ 卡片已从标签页删除：{label}")

            tag_page_nums[label] = self.get_tag_page_count(label)

        return tag_page_nums


# Markdown 处理


def escape_special_chars(md: str) -> str:
    """
    转义特殊字符，处理 -[空格] 后的内容
    将列表项中的特殊字符进行转义，避免被 Markdown 解析器误解析
    """
    lines = md.split("\n")
    result = []

    for line in lines:

        stripped = line.lstrip()
        indent = line[: len(line) - len(stripped)]

        if (
            stripped.startswith("- ")
            or stripped.startswith("* ")
            or stripped.startswith("+ ")
        ):
            marker = stripped[:2]
            content = stripped[2:]

            if (
                content.startswith("[ ] ")
                or content.startswith("[x] ")
                or content.startswith("[X] ")
            ):
                task_marker = content[:4]
                rest = content[4:]
                rest = rest.replace("[", "\\[").replace("]", "\\]")
                content = task_marker + rest
            else:
                content = content.replace("[", "\\[").replace("]", "\\]")

            if content.startswith(">"):
                content = "\\" + content

            line = indent + marker + content

        result.append(line)

    return "\n".join(result)


def md_to_html(md: str) -> str:
    md = escape_special_chars(md)
    extensions = [
        "extra",
        "toc",
        "sane_lists",
        "codehilite",
        "nl2br",
        "smarty",
        "admonition",
        "meta",
        "wikilinks",
        "legacy_attrs",
        "legacy_em",
        # pymdownx 扩展
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
        "pymdownx.progressbar",
        "pymdownx.striphtml",
        "pymdownx.tabbed",
        "pymdownx.arithmatex",
        "pymdownx.blocks.admonition",
        "pymdownx.blocks.details",
        "pymdownx.blocks.html",
        "pymdownx.blocks.tab",
        "pymdownx.snippets",
        "pymdownx.pathconverter",
    ]
    configs = {
        "codehilite": {
            "linenums": True,
            "css_class": "codehilite",
            "use_pygments": True,
        },
        "toc": {"permalink": " ?"},
        "pymdownx.highlight": {
            "linenums": True,
            "css_class": "codehilite",
            "use_pygments": True,
        },
        "pymdownx.superfences": {},
        "pymdownx.inlinehilite": {},
        "pymdownx.emoji": {},
        "pymdownx.tasklist": {"custom_checkbox": True, "clickable_checkbox": True},
        "pymdownx.betterem": {},
        "pymdownx.progressbar": {},
        "pymdownx.striphtml": {},
        "pymdownx.tabbed": {"alternate_style": True},
        "pymdownx.arithmatex": {"generic": True},
        "pymdownx.snippets": {},
        "pymdownx.pathconverter": {},
    }
    html = markdown.markdown(
        md, extensions=extensions, extension_configs=configs, output_format="html5"
    )

    soup = BeautifulSoup(html, "html.parser")
    for pre in soup.select("td.code pre"):
        copy_btn = BeautifulSoup(
            '<span class="copy-btn"><i class="fa fa-copy" aria-hidden="true"></i>&nbsp;Copy</span>',
            "html.parser",
        )
        pre.insert(0, copy_btn)
    for div in soup.select("div.codehilite"):
        code = div.find("code")
        if code:
            classes = code.get("class", [])
            lang = None
            for cls in classes:
                if cls.startswith("language-"):
                    lang = cls.replace("language-", "").capitalize()
                    break
            if lang:
                lang_label = BeautifulSoup(
                    f'<div class="code-lang-label">{lang}</div>',
                    "html.parser",
                )
                div.insert(0, lang_label)
    return str(soup)


# 文章管理


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
            print(f"❌ 文章文件不存在：{path}")
            return False
        os.remove(path)
        print(f"✅ 文章已删除：{path}")
        return True

    def extract_labels(self, issue_id: str) -> List[str]:
        path = self._path(issue_id)
        if not os.path.exists(path):
            return []
        with open(path, "r", encoding="utf-8") as f:
            return list(
                set(re.findall(r'<div class="tag"><span>(.*?)</span></div>', f.read()))
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
        tags = "".join(f'<div class="tag"><span>{l}</span></div>' for l in labels[:3])

        with open(self._path(issue_id), "w", encoding="utf-8") as f:
            f.write(
                f"""<!DOCTYPE html><html lang="zh-CN"><head><meta charset="UTF-8"/><meta name="viewport"content="width=device-width, initial-scale=1.0"/><title></title></head><body><div class="card-wrapper"><div class="card"><div class="card-header"><h1>{title}</h1><p>作者：{author}</p><p>发布日期：{date}</p></div><div class="divider"style="height:1px;width:100%;margin:1rem 0"></div><div class="card-content article-content">{md_to_html(content)}</div><div class="article-footer"><div class="article-tag"><span>文章标签：</span>{tags}</div></div></div></div><link rel="stylesheet"href="/css/blogArticle.css"><link rel="stylesheet"href="/css/QBLOG.css"/><script src="/js/QBLOG.js"></script><link rel="stylesheet"href="/css/font-awesome.min.css"/><script id="MathJax-script"async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script><script>window.MathJax={{tex:{{inlineMath:[['$','$'],['\\(','\\)']],displayMath:[['$$','$$'],['\\[','\\]']]}},svg:{{fontCache:'global'}}}};</script></body></html>"""
            )

        print(f"✅ 文章已{'更新' if is_update else '生成'}：{self._path(issue_id)}")


# 网站地图和Robots生成器


class SitemapGenerator:
    def __init__(self, workspace: str, cfg: Config):
        self.workspace = workspace
        self.cfg = cfg

    def scan_html_files(self, directory: str, exclude_dirs: List[str] = None) -> List[str]:
        """扫描目录下的HTML文件，返回相对路径列表"""
        if exclude_dirs is None:
            exclude_dirs = []
        
        html_files = []
        for root, dirs, files in os.walk(directory):
            # 排除指定目录
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
            
            for file in files:
                if file.endswith('.html'):
                    full_path = os.path.join(root, file)
                    rel_path = os.path.relpath(full_path, self.workspace)
                    # 转换为URL路径
                    url_path = '/' + rel_path.replace('\\', '/')
                    html_files.append(url_path)
        
        return sorted(html_files)

    def get_file_mod_time(self, file_path: str) -> str:
        """获取文件修改时间，返回ISO格式"""
        try:
            mtime = os.path.getmtime(file_path)
            return datetime.fromtimestamp(mtime).strftime('%Y-%m-%dT%H:%M:%S+08:00')
        except:
            return datetime.now().strftime('%Y-%m-%dT%H:%M:%S+08:00')

    def generate(self) -> None:
        """生成sitemap.xml"""
        print("\n❌ 开始生成 sitemap.xml...")
        
        urls = []
        
        # 添加静态页面
        static_pages = [
            '/',
            '/article/',
            '/tags/',
            '/data/',
            '/about/'
        ]
        for page in static_pages:
            full_path = os.path.join(self.workspace, page.lstrip('/'), 'index.html') if page != '/' else os.path.join(self.workspace, 'index.html')
            if os.path.exists(full_path):
                urls.append({
                    'loc': f"{self.cfg.SITE_URL}{page}",
                    'lastmod': self.get_file_mod_time(full_path),
                    'changefreq': 'daily',
                    'priority': '1.0' if page == '/' else '0.8'
                })

        # 添加文章分页页面
        pages_config = self.cfg.pages_config
        max_article_page = pages_config.get('maxPageNum', {}).get('maxArticlePageNum', 1)
        for i in range(2, max_article_page + 1):
            page_path = f'/pages/{i}.html'
            full_path = os.path.join(self.workspace, 'pages', f'{i}.html')
            if os.path.exists(full_path):
                urls.append({
                    'loc': f"{self.cfg.SITE_URL}{page_path}",
                    'lastmod': self.get_file_mod_time(full_path),
                    'changefreq': 'weekly',
                    'priority': '0.7'
                })

        # 添加标签页面
        max_tag_page_nums = pages_config.get('maxPageNum', {}).get('maxTagPageNums', {})
        for tag, page_count in max_tag_page_nums.items():
            for i in range(1, int(page_count) + 1):
                if i == 1:
                    tag_path = f'/tags/{tag}/'
                    full_path = os.path.join(self.workspace, 'tags', tag, 'index.html')
                else:
                    tag_path = f'/tags/{tag}/{i}.html'
                    full_path = os.path.join(self.workspace, 'tags', tag, f'{i}.html')
                
                if os.path.exists(full_path):
                    urls.append({
                        'loc': f"{self.cfg.SITE_URL}{tag_path}",
                        'lastmod': self.get_file_mod_time(full_path),
                        'changefreq': 'weekly',
                        'priority': '0.6'
                    })

        # 添加文章页面
        article_dir = os.path.join(self.workspace, 'article')
        if os.path.exists(article_dir):
            for file in os.listdir(article_dir):
                if file.endswith('.html'):
                    full_path = os.path.join(article_dir, file)
                    article_id = file.replace('.html', '')
                    urls.append({
                        'loc': f"{self.cfg.SITE_URL}/article/{article_id}.html",
                        'lastmod': self.get_file_mod_time(full_path),
                        'changefreq': 'monthly',
                        'priority': '0.9'
                    })

        # 生成XML
        xml_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
        xml_content += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        
        for url in urls:
            xml_content += '  <url>\n'
            xml_content += f"    <loc>{url['loc']}</loc>\n"
            xml_content += f"    <lastmod>{url['lastmod']}</lastmod>\n"
            xml_content += f"    <changefreq>{url['changefreq']}</changefreq>\n"
            xml_content += f"    <priority>{url['priority']}</priority>\n"
            xml_content += '  </url>\n'
        
        xml_content += '</urlset>\n'

        # 保存文件
        sitemap_path = os.path.join(self.workspace, 'sitemap.xml')
        with open(sitemap_path, 'w', encoding='utf-8') as f:
            f.write(xml_content)
        
        print(f"✅ sitemap.xml 已生成，共 {len(urls)} 个URL")


class RobotsGenerator:
    def __init__(self, workspace: str, cfg: Config):
        self.workspace = workspace
        self.cfg = cfg

    def generate(self) -> None:
        """生成robots.txt"""
        print("\n🤖 开始生成 robots.txt...")
        
        robots_content = f"# robots.txt for {self.cfg.SITE_URL}\n"
        robots_content += "# Generated automatically by check_issue.py\n\n"
        robots_content += "User-agent: *\n"
        
        for path in self.cfg.ALLOW_PATHS:
            robots_content += f"Allow: {path}\n"
        
        robots_content += "\n"
        
        for path in self.cfg.DISALLOW_PATHS:
            robots_content += f"Disallow: {path}\n"
        
        robots_content += f"\n# Sitemap\n"
        robots_content += f"Sitemap: {self.cfg.SITEMAP_URL}\n"

        # 保存文件
        robots_path = os.path.join(self.workspace, 'robots.txt')
        with open(robots_path, 'w', encoding='utf-8') as f:
            f.write(robots_content)
        
        print(f"✅ robots.txt 已生成")


# 主流程


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
        print(f"\n❌ 标题：{self.cfg.ISSUE_TITLE}\n❌ 内容：\n{self.cfg.ISSUE_BODY}")
        print(f"❌ 发布日期：{date}\n❌ 发布者：{self.cfg.ISSUE_AUTHOR}")
        print(
            f"⚠️ 标签：{', '.join(self.cfg.ISSUE_LABELS) if self.cfg.ISSUE_LABELS else '无'}"
        )
        print("=" * 50)

    def _update_indices(
        self, title: str, date: str, content: str, issue_id: str, labels: List[str]
    ) -> None:
        # 先检查首页
        idx = self.cfg.WORKSPACE + "index.html"
        p = HTMLProcessor(idx)
        pos = p.find_card(issue_id)

        is_update = False

        if pos:
            # 首页有这个卡片，直接更新
            is_update = True
            p.add_or_update(title, date, content, issue_id, labels, self.cfg)
            p.save()
        else:
            # 检查其他页面
            total_pages = self.page.get_total_pages()
            for page_num in range(2, total_pages + 1):
                page_path = self.page.get_page_path(page_num)
                if os.path.exists(page_path):
                    p_page = HTMLProcessor(page_path)
                    pos_page = p_page.find_card(issue_id)
                    if pos_page:

                        is_update = True
                        p_page.add_or_update(
                            title, date, content, issue_id, labels, self.cfg
                        )
                        p_page.save()
                        break

        # 如果是新卡片，找最后一个未满的页面添加
        if not is_update:
            # 查找最后一个未满的页面
            last_non_full_page = self.page.find_last_non_full_page(
                self.cfg.BLOG_ARTICLES_PER_PAGE
            )

            if last_non_full_page == 0:
                # 所有页面都满了，需要创建新页面
                next_page_num = self.page.get_next_page_num()
                new_page_path = self.page.create_page(next_page_num)

                # 在新页面中添加卡片
                p_new = HTMLProcessor(new_page_path)
                p_new.add_or_update(title, date, content, issue_id, labels, self.cfg)
                p_new.save()

                # 更新maxPageNum值
                self.pages_config_mgr.update_max_article_page_num(self.page.get_total_pages())

                print(f"✅ 卡片已添加到新页面：{new_page_path}")
            else:

                page_path = self.page.get_page_path(last_non_full_page)
                p_target = HTMLProcessor(page_path)
                p_target.add_or_update(title, date, content, issue_id, labels, self.cfg)
                p_target.save()
                print(f"✅ 卡片已添加到页面 {last_non_full_page}：{page_path}")

        # 更新文章列表页
        idx = self.cfg.WORKSPACE + "article/index.html"
        p = HTMLProcessor(idx)
        p.add_or_update(title, date, content, issue_id, labels, self.cfg)
        p.save()

    def handle_delete(self) -> None:
        print(f"\n⚠️ 删除文章：ID {self.cfg.ISSUE_ID}")
        old = self.article.extract_labels(self.cfg.ISSUE_ID)
        print(f"❌ 旧标签：{', '.join(old) if old else '无'}")

        self.article.delete(self.cfg.ISSUE_ID)

        # 从首页删除卡片
        idx = self.cfg.WORKSPACE + "index.html"
        p = HTMLProcessor(idx)
        p.remove_card(self.cfg.ISSUE_ID)
        p.save()

        # 从文章列表页删除卡片
        idx = self.cfg.WORKSPACE + "article/index.html"
        p = HTMLProcessor(idx)
        p.remove_card(self.cfg.ISSUE_ID)
        p.save()

        # 从所有分页页面删除卡片
        page_num = 2
        while os.path.exists(self.page.get_page_path(page_num)):
            idx = self.page.get_page_path(page_num)
            p = HTMLProcessor(idx)
            p.remove_card(self.cfg.ISSUE_ID)
            p.save()
            page_num += 1

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
            self.pages_config_mgr.update_max_article_page_num(self.page.get_total_pages())
            self.pages_config_mgr.update_tag_page_nums(tag_page_nums)
        print("=" * 50 + "\n✅ 删除操作完成")

    def handle_create_update(self) -> None:
        date = format_date(self.cfg.ISSUE_DATE, self.cfg.UTC_OFFSET)
        self._log()

        is_new = not self.article.exists(self.cfg.ISSUE_ID)
        old = [] if is_new else self.article.extract_labels(self.cfg.ISSUE_ID)
        if not is_new:
            print(f"❌ 旧标签：{', '.join(old) if old else '无'}")

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
                # 仅更新JSON，不再操作标签云页面
                for tag in self.cfg.ISSUE_LABELS:
                    self.pages_config_mgr.update_tags_article_total(tag, 1)
                self.pages_config_mgr.update_max_article_page_num(self.page.get_total_pages())
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
                # 仅更新JSON，不再操作标签云页面
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
                # 仅更新JSON，不再操作标签云页面
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

            # 更新标签页分页变量
            if tag_page_nums:
                self.pages_config_mgr.update_max_article_page_num(self.page.get_total_pages())
                self.pages_config_mgr.update_tag_page_nums(tag_page_nums)

    def run(self) -> None:
        if self.cfg.ISSUE_AUTHOR != self.cfg.TARGET_AUTHOR:
            print(
                f"✅ 跳过：作者不匹配 ({self.cfg.ISSUE_AUTHOR} != {self.cfg.TARGET_AUTHOR})"
            )
            return

        print(f"\n{'='*50}\n✅ Issue操作：{self.cfg.ISSUE_ACTION}\n{'='*50}")

        if self.cfg.ISSUE_ACTION == "deleted":
            self.handle_delete()
        else:
            self.handle_create_update()

        # 生成 sitemap.xml 和 robots.txt
        self.sitemap_gen.generate()
        self.robots_gen.generate()


if __name__ == "__main__":
    BlogGenerator().run()