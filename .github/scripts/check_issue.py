"""
GitHub Issues 博客生成器

功能：监听 GitHub Issues 事件，自动生成静态博客页面
支持操作：创建、更新、删除文章，标签管理
"""

import os
import json
import re
from datetime import datetime, timezone, timedelta
from typing import List, Optional, Tuple
import markdown
from bs4 import BeautifulSoup


# ==================== 配置 ====================

class Config:
    ISSUE_TITLE = os.getenv("ISSUE_TITLE", "")
    ISSUE_BODY = os.getenv("ISSUE_BODY") or "(无内容)"
    ISSUE_DATE = os.getenv("ISSUE_DATE", "")
    ISSUE_AUTHOR = os.getenv("ISSUE_AUTHOR", "")
    ISSUE_LABELS = json.loads(os.getenv("ISSUE_LABELS", "[]"))
    TARGET_AUTHOR = os.getenv("TARGET_AUTHOR", "")
    ISSUE_ID = os.getenv("ISSUE_ID", "")
    ISSUE_ACTION = os.getenv("ISSUE_ACTION", "opened")
    WORKSPACE = os.getenv("GITHUB_WORKSPACE", "") + "/"
    UTC_OFFSET = int(os.getenv("UTC_OFFSET", "8"))


# ==================== 工具函数 ====================

def format_date(iso_date: str, offset: int = 8) -> str:
    dt = datetime.fromisoformat(iso_date.replace("Z", "+00:00"))
    return dt.astimezone(timezone(timedelta(hours=offset))).strftime("%Y年%m月%d日 %H:%M")

def truncate(text: str, max_len: int = 150) -> str:
    return text[:max_len] + "..." if len(text) > max_len else text

def get_link(file_path: str, target_id: str) -> str:
    path = file_path.replace('\\', '/')
    if 'tags/' in path: return f"../pages/{target_id}.html"
    if 'pages/' in path and 'index.html' in path: return f"./{target_id}.html"
    return f"./pages/{target_id}.html"


# ==================== HTML 处理器 ====================

class HTMLProcessor:
    def __init__(self, path: str):
        self.path = path
        with open(path, 'r', encoding='utf-8') as f:
            self.html = f.read()
    
    def save(self) -> None:
        with open(self.path, 'w', encoding='utf-8') as f:
            f.write(self.html)
    
    def _find_card(self, issue_id: str) -> Optional[Tuple[int, int]]:
        link = get_link(self.path, issue_id)
        for pattern in [link, f"../pages/{issue_id}.html", f"./pages/{issue_id}.html", f"./{issue_id}.html"]:
            start = self.html.find(f'<a href="{pattern}">')
            if start != -1:
                li_start = self.html.rfind('<li>', 0, start)
                li_end = self.html.find('</li>', start)
                if li_end != -1:
                    return (li_start, li_end + 5)
        return None
    
    def remove_card(self, issue_id: str) -> bool:
        pos = self._find_card(issue_id)
        if not pos:
            print(f"ℹ️ 卡片不存在：{issue_id}")
            return False
        self.html = self.html[:pos[0]] + self.html[pos[1]:]
        print(f"✅ 卡片已删除：{issue_id}")
        return True
    
    def _gen_tags(self, labels: List[str]) -> str:
        return ''.join(f'<div class="tag"><span>{l}</span></div>' for l in labels[:3])
    
    def _gen_card(self, title: str, date: str, content: str, issue_id: str, labels: List[str]) -> str:
        link, tags = get_link(self.path, issue_id), self._gen_tags(labels)
        return f'''<li><a href="{link}"><div class="card"><div class="card-header"><h2>{title}</h2></div>
<div class="divider" style="height:1px;width:100%;margin:1rem 0"></div><p>{content}</p>
<div class="divider" style="height:1px;width:100%;margin:1rem 0"></div>
<div class="card-footer"><div class="article-tag">{tags}</div><p>发布日期：{date}</p></div></div></a></li>'''
    
    def add_or_update(self, title: str, date: str, content: str, issue_id: str, labels: List[str]) -> None:
        card = self._gen_card(title, date, content, issue_id, labels)
        pos = self._find_card(issue_id)
        if pos:
            self.html = self.html[:pos[0]] + card + self.html[pos[1]:]
            print(f"✅ 卡片已更新：{title}")
        else:
            ul_start = self.html.find('<ul')
            ul_end = self.html.find('</ul>', ul_start)
            self.html = self.html[:ul_end] + card + self.html[ul_end:]
            print(f"✅ 卡片已添加：{title}")


# ==================== 标签管理 ====================

class TagManager:
    def __init__(self, workspace: str):
        self.tags_dir = os.path.join(workspace, "tags")
    
    def _tag_path(self, name: str) -> str:
        return os.path.join(self.tags_dir, f"{name}.html")
    
    def create_page(self, name: str) -> None:
        path = self._tag_path(name)
        if os.path.exists(path):
            print(f"ℹ️ 标签页面已存在：{name}")
            return
        os.makedirs(self.tags_dir, exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(f'''<!DOCTYPE html><html lang="zh-CN"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0"><title></title></head>
<body><div id="title"><h1>{name}</h1></div><div id="card-list-box"><ul id="card-list"></ul></div>
<footer><p>© 2025-2026 QingXuanJun & QingXuan2000. All rights reserved.</p></footer>
<link rel="stylesheet" href="../css/QBLOG.css"><script src="../js/QBLOG.js"></script>
<link rel="stylesheet" href="../css/font-awesome.min.css"><style>#card-list-box{{border-top:none}}</style></body></html>''')
        print(f"✅ 标签页面已创建：{name}")
    
    def update_cloud(self, tags: List[str], inc: bool = True) -> None:
        path = os.path.join(self.tags_dir, "index.html")
        if not os.path.exists(path):
            print(f"⚠️ 标签云文件不存在")
            return
        with open(path, 'r', encoding='utf-8') as f:
            html = f.read()
        for tag in tags:
            html = self._update_tag(html, tag, inc)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)
    
    def _update_tag(self, html: str, tag: str, inc: bool) -> str:
        pattern = f'<a href="./{tag}.html" class="tag-item">'
        if pattern not in html:
            if not inc: return html
            # 添加新标签
            pos = html.find('</ul>', html.find('<ul class="tag-cloud">'))
            return html[:pos] + f'<li><a href="./{tag}.html" class="tag-item"><span class="tag-name">{tag}</span><span class="tag-count">1</span></a></li>' + html[pos:]
        
        start, end = html.find(pattern), html.find('</a>', html.find(pattern))
        tag_html = html[start:end]
        count = int(re.search(r'<span class="tag-count">(\d+)</span>', tag_html).group(1))
        new_count = count + (1 if inc else -1)
        
        if new_count <= 0:
            li_start = html.rfind('<li>', 0, start)
            li_end = html.find('</li>', end)
            print(f"✅ 标签已移除：{tag}")
            return html[:li_start] + html[li_end + 5:]
        
        print(f"✅ 标签计数已更新：{tag} ({count} → {new_count})")
        return html[:start] + tag_html.replace(f'>{count}<', f'>{new_count}<') + html[end:]
    
    def sync(self, issue_id: str, title: str, date: str, content: str, 
             target: List[str], all_labels: List[str], op: str = "add") -> None:
        for label in target:
            path = self._tag_path(label)
            if op == "add":
                self.create_page(label)
                p = HTMLProcessor(path)
                p.add_or_update(title, date, content, issue_id, all_labels)
                p.save()
                print(f"✅ 卡片已添加到标签页：{label}")
            elif op == "remove" and os.path.exists(path):
                p = HTMLProcessor(path)
                p.remove_card(issue_id)
                p.save()
                print(f"✅ 卡片已从标签页删除：{label}")


# ==================== Markdown 处理 ====================

def escape_special_chars(md: str) -> str:
    """
    转义特殊字符，处理 -[空格] 后的内容
    将列表项中的特殊字符进行转义，避免被 Markdown 解析器误解析
    """
    lines = md.split('\n')
    result = []
    
    for line in lines:
        # 匹配列表项：以 - 或 * 或 + 开头，后跟空格
        stripped = line.lstrip()
        indent = line[:len(line) - len(stripped)]
        
        if stripped.startswith('- ') or stripped.startswith('* ') or stripped.startswith('+ '):
            # 提取列表标记后的内容
            marker = stripped[:2]
            content = stripped[2:]
            
            # 转义内容中的特殊字符
            # 转义 [ ] 任务列表语法（如果不在开头）
            if content.startswith('[ ] ') or content.startswith('[x] ') or content.startswith('[X] '):
                # 保留任务列表语法，但转义后面的内容
                task_marker = content[:4]
                rest = content[4:]
                # 转义 rest 中的特殊字符
                rest = rest.replace('[', '\\[').replace(']', '\\]')
                content = task_marker + rest
            else:
                # 转义所有 [ 和 ]
                content = content.replace('[', '\\[').replace(']', '\\]')
            
            # 转义其他可能被误解析的字符
            # 转义行首的 > 避免被解析为引用
            if content.startswith('>'):
                content = '\\' + content
            
            line = indent + marker + content
        
        result.append(line)
    
    return '\n'.join(result)


def md_to_html(md: str) -> str:
    # 先进行字符转义
    md = escape_special_chars(md)
    extensions = [
        "extra", "toc", "sane_lists", "codehilite", "nl2br", "smarty",
        "admonition", "meta", "wikilinks", "legacy_attrs", "legacy_em",
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
        "codehilite": {"linenums": True, "css_class": "codehilite", "use_pygments": True},
        "toc": {"permalink": " ¶"},
        "pymdownx.highlight": {"linenums": True, "css_class": "codehilite", "use_pygments": True},
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
    html = markdown.markdown(md, extensions=extensions, extension_configs=configs, output_format="html5")

    soup = BeautifulSoup(html, 'html.parser')
    for pre in soup.select('td.code pre'):
        copy_btn = BeautifulSoup('<span class="copy-btn"><i class="fa fa-copy" aria-hidden="true"></i>&nbsp;Copy</span>', 'html.parser')
        pre.insert(0, copy_btn)
    return str(soup)


# ==================== 文章管理 ====================

class ArticleManager:
    def __init__(self, workspace: str):
        self.pages_dir = os.path.join(workspace, "pages")
        os.makedirs(self.pages_dir, exist_ok=True)
    
    def _path(self, issue_id: str) -> str:
        return os.path.join(self.pages_dir, f"{issue_id}.html")
    
    def exists(self, issue_id: str) -> bool:
        return os.path.exists(self._path(issue_id))
    
    def delete(self, issue_id: str) -> bool:
        path = self._path(issue_id)
        if not os.path.exists(path):
            print(f"ℹ️ 文章文件不存在：{path}")
            return False
        os.remove(path)
        print(f"✅ 文章已删除：{path}")
        return True
    
    def extract_labels(self, issue_id: str) -> List[str]:
        path = self._path(issue_id)
        if not os.path.exists(path):
            return []
        with open(path, 'r', encoding='utf-8') as f:
            return list(set(re.findall(r'<div class="tag"><span>(.*?)</span></div>', f.read())))
    
    def generate(self, issue_id: str, title: str, author: str, date: str, content: str, labels: List[str]) -> None:
        try:
            date = datetime.strptime(date, '%Y年%m月%d日 %H:%M:%S').strftime('%Y年%m月%d日 %H:%M')
        except ValueError:
            pass
        
        is_update = self.exists(issue_id)
        tags = ''.join(f'<div class="tag"><span>{l}</span></div>' for l in labels[:3])
        
        with open(self._path(issue_id), 'w', encoding='utf-8') as f:
            f.write(f'''<!DOCTYPE html><html lang="zh-CN"><head><meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" /><title></title></head>
<body><div class="card-box"><div class="card"><div class="card-header"><h1>{title}</h1>
<p>作者：{author}</p><p>发布日期：{date}</p></div>
<div class="divider" style="height:1px;width:100%;margin:1rem 0"></div>
<div class="card-content article-content">{md_to_html(content)}</div>
<div class="article-footer"><div class="article-tag"><span>文章标签：</span>{tags}</div></div></div></div>
<footer><p>© 2025-2026 QingXuanJun & QingXuan2000. All rights reserved.</p></footer>
<link rel="stylesheet" href="../css/blogArticle.css"><link rel="stylesheet" href="../css/QBLOG.css" />
<script src="../js/QBLOG.js"></script><link rel="stylesheet" href="../css/font-awesome.min.css" />
<script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
<script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
<script>window.MathJax = {{ tex: {{ inlineMath: [['$', '$'], ['\\\\(', '\\\\)']], displayMath: [['$$', '$$'], ['\\\\[', '\\\\]']] }}, svg: {{ fontCache: 'global' }} }};</script>
</body></html>''')
        
        print(f"✅ 文章已{'更新' if is_update else '生成'}：{self._path(issue_id)}")


# ==================== 主流程 ====================

class BlogGenerator:
    def __init__(self):
        self.cfg = Config()
        self.article = ArticleManager(self.cfg.WORKSPACE)
        self.tag = TagManager(self.cfg.WORKSPACE)
    
    def _log(self) -> None:
        date = format_date(self.cfg.ISSUE_DATE, self.cfg.UTC_OFFSET)
        print(f"\n📌 标题：{self.cfg.ISSUE_TITLE}\n📝 内容：\n{self.cfg.ISSUE_BODY}")
        print(f"📅 发布日期：{date}\n👤 发布者：{self.cfg.ISSUE_AUTHOR}")
        print(f"🏷️ 标签：{', '.join(self.cfg.ISSUE_LABELS) if self.cfg.ISSUE_LABELS else '无'}")
        print("=" * 50)
    
    def _update_indices(self, title: str, date: str, content: str, issue_id: str, labels: List[str]) -> None:
        for idx in [self.cfg.WORKSPACE + 'index.html', self.cfg.WORKSPACE + 'pages/index.html']:
            p = HTMLProcessor(idx)
            p.add_or_update(title, date, content, issue_id, labels)
            p.save()
    
    def handle_delete(self) -> None:
        print(f"\n🗑️ 删除文章：ID {self.cfg.ISSUE_ID}")
        old = self.article.extract_labels(self.cfg.ISSUE_ID)
        print(f"📌 旧标签：{', '.join(old) if old else '无'}")
        
        self.article.delete(self.cfg.ISSUE_ID)
        
        for idx in [self.cfg.WORKSPACE + 'index.html', self.cfg.WORKSPACE + 'pages/index.html']:
            p = HTMLProcessor(idx)
            p.remove_card(self.cfg.ISSUE_ID)
            p.save()
        
        if old:
            self.tag.sync(self.cfg.ISSUE_ID, "", "", "", old, [], "remove")
            self.tag.update_cloud(old, False)
        print("=" * 50 + "\n✅ 删除操作完成")
    
    def handle_create_update(self) -> None:
        date = format_date(self.cfg.ISSUE_DATE, self.cfg.UTC_OFFSET)
        self._log()
        
        is_new = not self.article.exists(self.cfg.ISSUE_ID)
        old = [] if is_new else self.article.extract_labels(self.cfg.ISSUE_ID)
        if not is_new:
            print(f"📌 旧标签：{', '.join(old) if old else '无'}")
        
        self.article.generate(self.cfg.ISSUE_ID, self.cfg.ISSUE_TITLE, self.cfg.ISSUE_AUTHOR, 
                           date, self.cfg.ISSUE_BODY, self.cfg.ISSUE_LABELS)
        self._update_indices(self.cfg.ISSUE_TITLE, date, truncate(self.cfg.ISSUE_BODY), 
                            self.cfg.ISSUE_ID, self.cfg.ISSUE_LABELS)
        
        if is_new:
            if self.cfg.ISSUE_LABELS:
                self.tag.sync(self.cfg.ISSUE_ID, self.cfg.ISSUE_TITLE, date, 
                             truncate(self.cfg.ISSUE_BODY), self.cfg.ISSUE_LABELS, self.cfg.ISSUE_LABELS)
                self.tag.update_cloud(self.cfg.ISSUE_LABELS, True)
        else:
            to_add = [l for l in self.cfg.ISSUE_LABELS if l not in old]
            to_remove = [l for l in old if l not in self.cfg.ISSUE_LABELS]
            to_keep = [l for l in self.cfg.ISSUE_LABELS if l in old]
            
            if to_remove:
                self.tag.sync(self.cfg.ISSUE_ID, "", "", "", to_remove, [], "remove")
                self.tag.update_cloud(to_remove, False)
            if to_add:
                self.tag.sync(self.cfg.ISSUE_ID, self.cfg.ISSUE_TITLE, date, 
                             truncate(self.cfg.ISSUE_BODY), to_add, self.cfg.ISSUE_LABELS)
                self.tag.update_cloud(to_add, True)
            if to_keep:
                self.tag.sync(self.cfg.ISSUE_ID, self.cfg.ISSUE_TITLE, date, 
                             truncate(self.cfg.ISSUE_BODY), to_keep, self.cfg.ISSUE_LABELS)
    
    def run(self) -> None:
        if self.cfg.ISSUE_AUTHOR != self.cfg.TARGET_AUTHOR:
            print(f"❌ 跳过：作者不匹配 ({self.cfg.ISSUE_AUTHOR} != {self.cfg.TARGET_AUTHOR})")
            return
        
        print(f"\n{'='*50}\n✅ Issue操作：{self.cfg.ISSUE_ACTION}\n{'='*50}")
        
        if self.cfg.ISSUE_ACTION == "deleted":
            self.handle_delete()
        else:
            self.handle_create_update()


if __name__ == "__main__":
    BlogGenerator().run()