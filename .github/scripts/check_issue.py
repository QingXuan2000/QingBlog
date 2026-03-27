import os
import json
from datetime import datetime
import markdown

title = os.getenv("ISSUE_TITLE", "")
body = os.getenv("ISSUE_BODY", "") or "(无内容)"
date_str = os.getenv("ISSUE_DATE", "")
author = os.getenv("ISSUE_AUTHOR", "")
labels_json = os.getenv("ISSUE_LABELS", "[]")
target_author = os.getenv("TARGET_AUTHOR", "")
issue_id = os.getenv("ISSUE_ID", "")
workspace = os.getenv("GITHUB_WORKSPACE") + "/"

def add_card(file_path, title, time, content, id, labels):
    with open(file_path, 'r', encoding='utf-8') as f:
        html = f.read()

    date = time
    
    tags_html = ""
    if labels:
        for label in labels[:3]:
            tags_html += f'<div class="tag"><span>{label}</span></div>'

    card_link = f"../pages/{id}.html"
    if card_link in html:
        card_start = html.find(f'<a href="{card_link}">')
        card_end = html.find('</li>', card_start)
        card_end += 5
        new_card = f'''        <li>
            <a href="{card_link}">
                <div class="card">
                    <div class="card-header">
                        <h2>{title}</h2>
                    </div>
                    <div class="divider" style="height: 1px; width: 100%; margin: 1rem 0 1rem 0;"></div>
                    <p>{content}</p>
                    <div class="divider" style="height: 1px; width: 100%; margin: 1rem 0 1rem 0;"></div>
                    <div class="card-footer">
                        <div class="article-tag">
                            {tags_html}
                        </div>
                        <p>发布日期：{date}</p>
                    </div>
                </div>
            </a>
        </li>
'''
        html = html[:card_start] + new_card + html[card_end:]
        print(f"✅ 卡片已更新：{title}")
    else:
        card_list_start = html.find('class="card-list"')
        ul_start = html.rfind('<ul', 0, card_list_start)
        ul_end = html.find('</ul>', ul_start)
        card = f'''        <li>
            <a href="../pages/{id}.html">
                <div class="card">
                    <div class="card-header">
                        <h2>{title}</h2>
                    </div>
                    <div class="divider" style="height: 1px; width: 100%; margin: 1rem 0 1rem 0;"></div>
                    <p>{content}</p>
                    <div class="divider" style="height: 1px; width: 100%; margin: 1rem 0 1rem 0;"></div>
                    <div class="card-footer">
                        <div class="article-tag">
                            {tags_html}
                        </div>
                        <p>发布日期：{date}</p>
                    </div>
                </div>
            </a>
        </li>
'''
        new_html = html[:ul_end] + card + html[ul_end:]
        html = new_html
        print(f"✅ 卡片已添加：{title}")

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(html)

def md_to_html(md_text: str) -> str:
    extensions = [
        "extra", "toc", "sane_lists", "codehilite",
        "nl2br", "footnotes"
    ]
    
    extension_configs = {
        "codehilite": {"linenums": False, "css_class": "codehilite"}
    }

    html_text = markdown.markdown(
        md_text,
        extensions=extensions,
        extension_configs=extension_configs,
        output_format="html5"
    )
    return html_text

def generate_article_page(issue_id, title, author, publish_time, content, labels):
    try:
        date = datetime.strptime(publish_time, '%Y年%m月%d日 %H:%M:%S').strftime('%Y年%m月%d日 %H:%M')
    except:
        date = publish_time

    content_html = md_to_html(content)
    
    tags_html = ""
    if labels:
        for label in labels[:3]:
            tags_html += f'<div class="tag"><span>{label}</span></div>'

    article_template = f'''<!DOCTYPE html>
<html lang="zh-CN">

<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>QingBlog - {title}</title>

    <link rel="shortcut icon" href="../favicon.ico" type="image/x-icon" />

    <link rel="stylesheet" href="../css/font-awesome.css" />
    <link rel="stylesheet" href="../css/QBLOG.css" />
    <link rel="stylesheet" href="../css/blogArticle.css" />

    <script src="../js/QBLOG.js"></script>
</head>

<body>
    <div class="overlay"></div>

    <div id="sidebar">
        <div id="sidebar-close">
            <i class="fa fa-remove" aria-hidden="true"></i>
        </div>

        <div class="user-info">
            <img src="../img/logo.png" alt="Avatar" />
            <h1>QingXuanJun</h1>
        </div>

        <nav>
            <ul>
                <li>
                    <a href="../index.html"><i class="fa fa-home" aria-hidden="true"></i>&nbsp;首页</a>
                </li>

                <div class="divider" style="width: 100%; height: 1px;"></div>

                <li>
                    <a href="../pages.html"><i class="fa fa-book" aria-hidden="true"></i>&nbsp;文章</a>
                </li>

                <div class="divider" style="width: 100%; height: 1px;"></div>

                <li>
                    <a target="_blank" href="https://github.com/QingXuan2000"><i class="fa fa-github-square"
                            aria-hidden="true"></i>&nbsp;GitHub</a>
                </li>
            </ul>
        </nav>
    </div>

    <div id="alert">
        <div id="alert-message">
            <span></span>
        </div>
    </div>

    <header>
        <nav id="navbar">
            <img src="../img/logo.png" alt="Logo" class="logo" />
            <h1>QingBlog</h1>

            <div class="divider" style="width: 2px; margin: 0 0.5rem 0 1rem; border-radius: 100em;"></div>

            <ul>
                <li>
                    <a href="../index.html"><i class="fa fa-home" aria-hidden="true"></i>&nbsp;首页</a>
                </li>

                <li>
                    <a href="../pages.html"><i class="fa fa-book" aria-hidden="true"></i>&nbsp;文章</a>
                </li>

                <li>
                    <a target="_blank" href="https://github.com/QingXuan2000"><i class="fa fa-github-square"
                            aria-hidden="true"></i>&nbsp;GitHub</a>
                </li>
            </ul>

            <div id="search-container">
                <input id="search" type="search" placeholder="" />
                <label for="search"><i class="fa fa-search" aria-hidden="true"></i>&nbsp;搜索</label>
                <button onclick="find(document.getElementById('search').value)"><i class="fa fa-level-down"
                        aria-hidden="true"></i></button>
            </div>
        </nav>

        <div id="sidebar-toggle">
            <i class="fa fa-bars" aria-hidden="true"></i>
        </div>
    </header>

    <div class="card">
        <div class="card-header">
            <h1>{title}</h1>
            <p>作者：{author}</p>
            <p>发布日期：{date}</p>
        </div>

        <div class="divider" style="height: 1px; width: 100%; margin: 1rem 0 1rem 0;"></div>

        <div class="card-content">
            {content_html}
        </div>

        <div class="article-footer">
            <div class="article-tag">
                <span>文章标签：</span>
                {tags_html}
            </div>
        </div>
    </div>

    <div id="back-to-top">
        <i class="fa fa-chevron-up"></i>
    </div>

    <footer>
        <p>© 2025-2026 QingXuanJun & QingXuan2000. All rights reserved.</p>
    </footer>

    <!-- ------------------------------------------------------------ -->

    <link rel="stylesheet" href="../css/QBLOG.css" />
    <script src="../js/QBLOG.js"></script>

    <link rel="stylesheet" href="../css/font-awesome.min.css" />

    <!-- ------------------------------------------------------------ -->

    <style>
        .card-header {{
            display: flex;
            flex-direction: column;
            justify-content: center;
            gap: 10px;
        }}

        .card-header p {{
            justify-content: center;
        }}

        .card-content {{
            min-height: calc(100dvh - (var(--nav-height) + 26rem));
        }}
    </style>

    <!-- ------------------------------------------------------------ -->

</body>

</html>
'''

    pages_dir = os.path.join(workspace, "pages")
    os.makedirs(pages_dir, exist_ok=True)

    file_path = os.path.join(pages_dir, f"{issue_id}.html")
    
    if os.path.exists(file_path):
        # 更新现有文件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(article_template)
        print(f"✅ 文章已更新：{file_path}")
    else:
        # 创建新文件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(article_template)
        print(f"✅ 文章已生成：{file_path}")

def format_github_date_compact(iso_date: str) -> str:
    dt = datetime.fromisoformat(iso_date.replace("Z", "+00:00"))
    return dt.strftime("%Y年%m月%d日 %H:%M")

def main():
    labels = json.loads(labels_json)
    is_target_author = author == target_author
    formatted_date = format_github_date_compact(date_str)

    print(f"作者: {author}")
    print(f"标签: {labels}")
    print(f"目标作者: {target_author}")
    print(f"作者匹配: {is_target_author}")

    if is_target_author:
        print("\n" + "=" * 50)
        print("✅ Issue详细信息如下：")
        print("=" * 50)

        print(f"\n📌 标题：{title}")
        print(f"\n📝 内容：\n{body}")
        print(f"\n📅 发布日期：{formatted_date}")
        print(f"👤 发布者：{author}")
        print(f"🏷️  标签：{', '.join(labels) if labels else '无'}")
        print("=" * 50)

        generate_article_page(
            issue_id=issue_id,
            title=title,
            author=author,
            publish_time=formatted_date,
            content=body,
            labels=labels
        )

        add_card(
            workspace + 'index.html',
            title,
            formatted_date,
            body[:150] + "..." if len(body) > 150 else body,
            issue_id,
            labels=labels
        )

        add_card(
            workspace + 'pages.html',
            title,
            formatted_date,
            body[:150] + "..." if len(body) > 150 else body,
            issue_id,
            labels=labels
        )

    else:
        print("❌ 跳过生成")

if __name__ == "__main__":
    main()