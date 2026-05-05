<div align="center">
  <img src="img/logo.svg" alt="QingBlog Logo" width="120" height="120">
  <h1>QingBlog</h1>
  <p>一个基于 GitHub Issues 的自动化博客框架</p>

![License](https://img.shields.io/github/license/QingXuan2000/QingBlog?style=for-the-badge)
![GitHub stars](https://img.shields.io/github/stars/QingXuan2000/QingBlog?style=for-the-badge)
![GitHub issues](https://img.shields.io/github/issues/QingXuan2000/QingBlog?style=for-the-badge)
![GitHub Workflow](https://img.shields.io/github/actions/workflow/status/QingXuan2000/QingBlog/qingblog-build.yml?style=for-the-badge)

🌐 **在线演示**: [https://qingxuan2000.github.io/](https://qingxuan2000.github.io/)

📖 **QingBlog Wiki**: [https://github.com/QingXuan2000/QingBlog/wiki/](https://github.com/QingXuan2000/QingBlog/wiki/)

</div>

## 项目简介

QingBlog 是一个以 **GitHub Issues 作为内容源** 的静态博客方案：你在 Issue 里写作，GitHub Actions 会自动把内容渲染成文章页面并部署到 GitHub Pages。无需服务器与数据库，适合把写作与代码托管统一在同一套工作流里。

## 核心特性

- **一键部署**：GitHub Pages 免费托管，Actions 自动构建与提交
- **Issue 即文章**：创建/编辑/删除 Issue 后自动同步到站点
- **作者校验**：仅 `targetAuthor` 的 Issue 会被发布，避免被"投喂内容"
- **分页 + 标签**：首页/文章列表/标签页均支持分页，自动生成标签目录与统计
- **标签云 + 数据可视化**：标签云页与 ECharts 南丁格尔玫瑰图展示文章分布
- **词云**：关于页展示作者技能标签词云
- **代码复制**：文章代码块带一键复制按钮
- **Markdown 渲染**：代码高亮、任务列表、数学公式（MathJax admonition 等）
- **SEO**：自动生成 sitemap.xml / robots.txt
- **响应式布局**：适配桌面与移动端，侧边栏导航
- **主题切换**：多主题支持，可跟随系统主题偏好
- **加载动画**：可选的启动加载动画（SVG Logo 动画）
- **卡片滚动动画**：文章列表卡片滚动进入视口时渐入
- **动态页面标题**：页面可见性变化时自动切换标题文案
- **文章元信息**：文章页显示字数、阅读时间、最后更新时间
- **友情链接**：独立友情链接页面，通过 blogConfig 配置
- **404 页面**：自定义 404 错误页

## 技术栈

### 前端

- **HTML/CSS/JavaScript** - 静态页面与交互，ES6 Class 面向对象架构
- **Font Awesome** - 图标库
- **MathJax** - 公式渲染（客户端渲染，通过 tex-mml-chtml.js）
- **ECharts** - 数据可视化（南丁格尔玫瑰图 + 词云）

### 自动化

- **Python 3.12** - 构建脚本
- **GitHub Actions** - 触发构建、自动提交
- **Python-Markdown / PyMdown Extensions / Pygments / BeautifulSoup4** - Markdown 渲染与页面处理
- **GitHub Pages** - 部署托管

## 项目结构

```
QingBlog/
├── .github/
│   ├── workflows/
│   │   └── qingblog-build.yml         # GitHub Actions 工作流
│   └── scripts/
│       ├── static_blog_generator.py    # 核心构建脚本（Issue → 页面）
│       └── requirements.txt            # Python 依赖
│
├── blogData/                           # 博客配置目录
│   ├── blogConfig.json                 # 博客核心配置
│   ├── pagesConfig.json                # 分页与标签统计数据
│   └── themes.json                     # 主题配置
│
├── css/
│   ├── QBLOG.css                       # 主样式（主题变量、布局、组件）
│   ├── blogArticle.css                 # 文章页样式
│   └── font-awesome.min.css            # Font Awesome
│
├── js/
│   ├── QBLOG.js                        # 前端核心脚本（QingBlog 类）
│   ├── echarts.min.js                  # ECharts 图表库
│   ├── echarts-wordcloud.min.js        # ECharts 词云插件
│   └── tex-mml-chtml.js               # MathJax 渲染引擎
│
├── article/                            # 文章详情页
│   └── index.html                      # 文章列表页
│
├── tags/                               # 标签系统
│   └── index.html                      # 标签云页
│
├── pages/                              # 分页页面
│   └── .pagesDir
│
├── data/                               # 数据统计页
│   └── index.html
│
├── about/                              # 关于我
│   └── index.html
│
├── links/                              # 友情链接
│   └── index.html
│
├── fonts/                              # 字体文件
│   ├── 江城圆体/                       # 江城圆体字体（多字重 200W-700W）
│   ├── This-July.ttf
│   └── fontawesome-webfont.woff2
│
├── img/
│   ├── Avatar.png
│   └── logo.svg                        # 项目 Logo
│
├── index.html                          # 首页
├── 404.html                            # 自定义 404 页面
├── favicon.ico
├── LICENSE                             # GPL v3
└── README.md
```

## 快速开始

### 1. Fork + 开启 Pages

Fork 本仓库到你的账号下，然后在仓库 **Settings → Pages** 中把站点源设置为 **main 分支 / (root)**。

### 2. 允许工作流写入仓库

在 **Settings → Actions → General → Workflow permissions** 里选择 **Read and write permissions**，否则自动提交会失败。

### 3. 配置博客信息

编辑 `blogData/blogConfig.json`，主要字段：

| 字段 | 说明 |
|------|------|
| `blogInfo.blogName` | 博客名称 |
| `blogInfo.yearOfWriting` | 开始写作年份 |
| `blogInfo.repositoryName` | 仓库名（用于子路径部署） |
| `blogInfo.siteEstablishmentDate` | 建站日期（用于计算运行天数） |
| `author.targetAuthor` | 允许发布文章的 GitHub 用户名 |
| `author.introShort` | 标语（显示在侧边栏） |
| `author.introDetail` | 详细介绍（显示在关于页） |
| `author.socialMediaPlatform` | 社交平台链接 |
| `author.authorTags` | 技能标签（用于关于页词云） |
| `buildConfig.utcOffset` | 时区偏移，默认 8 |
| `buildConfig.articlesPerPage` | 每页文章数 |
| `buildConfig.showLoadingAnimation` | 是否显示加载动画 |
| `friendLinks` | 友情链接列表 |
| `robotsConfig` | SEO 配置（siteUrl，sitemapUrl 等） |

### 4. 配置主题（可选）

编辑 `blogData/themes.json`，可自定义 CSS 变量色板。页面右上角调色盘按钮可切换主题。

### 5. 发布文章

在你的仓库 **Issues** 新建 Issue（支持 Markdown）。工作流会在 `opened / edited / deleted / reopened` 时触发，自动构建并部署。

## 工作原理

```
创建/编辑/删除 Issue
        │
        ▼
  GitHub Actions 触发
        │
        ▼
  static_blog_generator.py
    ├── 校验作者 (targetAuthor)
    ├── Markdown → HTML（代码高亮、任务列表、公式等）
    ├── 生成文章页 article/{id}.html
    ├── 更新首页卡片 / 分页页 / 文章列表页
    ├── 同步标签系统（新增/更新/删除标签页）
    ├── 更新统计配置（文章数、字数、标签计数等）
    ├── 生成 sitemap.xml / robots.txt
    └── Git 自动提交并推送
        │
        ▼
  GitHub Pages 部署
```

## 本地运行（可选）

### 前置条件

- Python 3.12
- 安装依赖：

```bash
pip install -r .github/scripts/requirements.txt
```

### 运行脚本（PowerShell 示例）

```powershell
$env:ISSUE_TITLE="本地调试标题"
$env:ISSUE_BODY="# Hello QingBlog`n这是本地调试内容"
$env:ISSUE_DATE="2026-01-01T00:00:00Z"
$env:ISSUE_AUTHOR="你的GitHub名称"
$env:ISSUE_LABELS='["tag1","tag2"]'
$env:ISSUE_ID="1"
$env:ISSUE_ACTION="opened"
$env:BLOG_CONFIG_PATH="blogData/blogConfig.json"
$env:PAGES_CONFIG_PATH="blogData/pagesConfig.json"

python .github/scripts/static_blog_generator.py
```

> 若 `ISSUE_AUTHOR` 不等于 `author.targetAuthor`，脚本会跳过生成。

## Markdown 支持

通过 `Python-Markdown` + `PyMdown Extensions` 提供增强渲染：

- 标准 Markdown（标题、列表、链接、图片等）
- 代码块语法高亮（Pygments，带行号）
- 表格 / 脚注 / TOC / 任务列表（可点击）
- 数学公式（LaTeX，通过 MathJax 客户端渲染）
- Admonition / Details / Tabbed / Emoji / Magiclink 等扩展

## 标签系统

- **自动提取**：从 Issue 标签自动提取，每篇文章最多显示 3 个标签
- **独立标签页**：每个标签生成独立页面 `tags/{标签名}/`
- **标签分页**：标签文章超过每页限制时自动分页
- **智能计数**：新增/删除文章时自动增减标签计数，归零时自动移除
- **标签云**：`tags/index.html` 展示所有标签及其文章数

## 数据可视化

- **文章统计**：`data/` 页面展示南丁格尔玫瑰图（文章标签分布）
- **站点统计表**：展示文章总数、标签数、总字数、运行天数
- **个人词云**：`about/` 页面展示作者技能标签词云

## 前端架构

QingBlog 前端采用面向对象设计，核心 `QingBlog` 类（[js/QBLOG.js](js/QBLOG.js)）管理所有功能：

```javascript
class QingBlog {
  async init()                    // 初始化所有功能模块
  async loadConfigs()             // 加载 JSON 配置
  navigation(href)                // SPA 风格页面导航
  showAlert(color, message)       // 全局提示框

  // 功能模块
  initLoadingAnimation()          // 启动加载动画
  initThemeModal()                // 主题选择弹窗
  initSidebar()                   // 侧边栏导航
  initPagination()                 // 分页控件
  initBackToTop()                 // 回到顶部按钮
  initWebTitle()                  // 动态页面标题（可见性变化）
  initCopyButtons()               // 代码复制按钮
  initCardScrollAnimation()       // 卡片滚动渐入动画
  initLazyLoadImages()            // 图片懒加载
  initArticleData()               // 数据页 ECharts 图表
  initMeData()                    // 关于页词云
  initFriendLinks()               // 友情链接
  initArticleInfo()               // 文章更新时间
  addTagToPages()                 // 标签云渲染
}
```

可复用 `Modal` 类封装模态框通用逻辑（动画、遮罩、Escape 关闭、滚动锁定）。

## 安全说明

- 只有 `targetAuthor` 指定的用户创建的 Issue 才会被发布
- 建议将仓库设置为需要审核的 Fork 工作流

## Wiki 文档

完整 Wiki 文档在 [GitHub Wiki](https://github.com/QingXuan2000/QingBlog/wiki/)，涵盖安装、配置、开发、API、FAQ 等。

## 许可证

本项目采用 [GNU General Public License v3.0](LICENSE)。

## 作者

- **QingXuanJun** - [GitHub](https://github.com/QingXuan2000)

## 致谢

- [Font Awesome](https://fontawesome.com/) - 图标库
- [GitHub](https://github.com/) - 托管和 CI/CD
- [Python Markdown](https://python-markdown.github.io/) - Markdown 转换
- [ECharts](https://echarts.apache.org/) - 数据可视化
- [MathJax](https://www.mathjax.org/) - 公式渲染
