# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

QingBlog is a **static blog generator** that uses GitHub Issues as its CMS. When an Issue is created, edited, or deleted, a GitHub Actions workflow triggers a Python script that converts the Issue's Markdown body into static HTML pages, then auto-commits them back to the repo for deployment via GitHub Pages. No server, no database, no build tools — the entire pipeline is one Python script and one workflow.

## Commands

**Local build simulation (PowerShell):**
```powershell
$env:ISSUE_TITLE="测试标题"
$env:ISSUE_BODY="# Hello`n这是内容"
$env:ISSUE_DATE="2026-01-01T00:00:00Z"
$env:ISSUE_AUTHOR="你的GitHub名称"
$env:ISSUE_LABELS='["tag1","tag2"]'
$env:ISSUE_ID="1"
$env:ISSUE_ACTION="opened"
$env:BLOG_CONFIG_PATH="blogData/blogConfig.json"
$env:PAGES_CONFIG_PATH="blogData/pagesConfig.json"
python .github/scripts/static_blog_generator.py
```

**Install Python dependencies (once):**
```bash
pip install -r .github/scripts/requirements.txt
```

There are no other build/lint/test commands — this repo has no package manager, no bundler, and no test suite.

## Architecture

### Build pipeline (`.github/scripts/static_blog_generator.py`)

A ~1000-line self-contained Python 3.12 script. It receives Issue data via environment variables (set by the Actions workflow) and produces all static HTML. The script uses `markdown` + `pymdown-extensions` for Markdown → HTML conversion and `BeautifulSoup4` for DOM manipulation on list pages.

Key classes and their responsibilities:
- **`Config`** — reads all env vars and JSON configs; validates the Issue author against `targetAuthor` (non-matching authors are silently skipped)
- **`HTMLProcessor`** — inserts/removes/updates `<li class="card-list__item">` cards in the list pages (`index.html`, `pages/{n}.html`, `article/index.html`, tag pages)
- **`PagesConfigManager`** — maintains `blogData/pagesConfig.json` (max page numbers, per-tag article counts)
- **`PageManager`** — creates/deletes paginated list pages under `pages/`
- **`TagManager`** — manages tag directories and pages under `tags/{tag}/`, handles tag lifecycle (create on first use, delete when count reaches zero)
- **`ArticleManager`** — generates/deletes `article/{id}.html`
- **`SitemapGenerator` / `RobotsGenerator`** — write `sitemap.xml` and `robots.txt` to root
- **`BlogGenerator`** — top-level orchestrator; `run()` dispatches to `handle_create_update()` or `handle_delete()`

The Markdown → HTML conversion uses Pygments for code highlighting (with line numbers), injects a "Copy" button into every code block via BeautifulSoup, and article pages include an inline MathJax 3 config + CDN script for LaTeX rendering.

### GitHub Actions workflow (`.github/workflows/qingblog-build.yml`)

Triggered on `issues` events (`opened`, `edited`, `deleted`, `reopened`). Steps: checkout → setup Python 3.12 → pip install → run the generator script → auto-commit changes via `stefanzweifel/git-auto-commit-action@v5` with `--force-with-lease` push.

### Frontend (`js/QBLOG.js`)

A single vanilla JS class `QingBlog` (~930 lines). On page load, it:
1. Fetches `blogData/blogConfig.json`, `blogData/pagesConfig.json`, and `blogData/themes.json`
2. Dynamically injects nav bar, footer, sidebar, loading animation, and pagination controls into the DOM
3. Initializes theme toggling (dark/light via CSS custom properties from `themes.json`), back-to-top button, context menus, copy buttons on code blocks, and lazy image loading
4. On the `/data/` page: renders an ECharts pie chart of tag distribution
5. On the `/about/` page: renders an ECharts word cloud of author skill tags

All HTML pages (`index.html`, `article/index.html`, `tags/index.html`, `data/index.html`, `about/index.html`) are minimal shells — the `QingBlog` class populates them at runtime.

### CSS

- **`css/QBLOG.css`** — CSS custom properties for theming (overridden by JS from `themes.json`), main layout, nav, sidebar, cards, footer, pagination, responsive breakpoints (1024px, 640px)
- **`css/blogArticle.css`** — article content typography and styling: code blocks (terminal-style with CSS-generated line numbers), Pygments syntax highlighting classes, admonitions, task lists, tables, footnotes, progress bars

### Configuration files

- **`blogData/blogConfig.json`** — blog name, author info (including `targetAuthor` for verification), social media links, author skill tags (for word cloud), build settings (`utcOffset`, `articlesPerPage`), robots config
- **`blogData/pagesConfig.json`** — auto-maintained by the Python script; tracks `maxArticlePageNum` and per-tag article counts (`tagsArticleTotal`). Do not edit manually.
- **`blogData/themes.json`** — two themes (`dark`, `light`), each with 13 CSS custom properties that get applied to `:root` at runtime

### Pages and directories

- **`pages/`** — paginated article list pages (`1.html`, `2.html`, ...), managed by `PageManager`
- **`article/`** — individual article detail pages (`{issue_number}.html`), plus `index.html` for the full article list
- **`tags/`** — per-tag directories with paginated listing pages, managed by `TagManager`
- **`data/`**, **`about/`** — static pages with ECharts visualizations

## Key behaviors to preserve

- **Author gating**: the Python script silently skips Issues whose author doesn't match `blogConfig.author.targetAuthor`. This is a security feature, not a bug.
- **Force-with-lease push**: the workflow uses `--force-with-lease` because the script amends previous commits during Issue edits. Do not change this to a regular push.
- **No manual edits to `pagesConfig.json`**: it's the script's runtime state; manual changes will be overwritten.
- **HTML pages are templates**: the Python script uses hardcoded HTML string templates (e.g., `LIST_PAGE_TEMPLATE`, `ARTICLE_PAGE_TEMPLATE`) with `str.format()` substitution. Changes to page structure must be made in both the Python templates AND the static HTML shells.
