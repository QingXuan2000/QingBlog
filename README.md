<div align="center">
  <img src="img/logo.svg" alt="QingBlog Logo" width="120" height="120">
  <h1>QingBlog</h1>
  <p>一个基于 GitHub Issues 的自动化博客框架</p>

![License](https://img.shields.io/github/license/QingXuan2000/QingBlog?style=for-the-badge)
![GitHub stars](https://img.shields.io/github/stars/QingXuan2000/QingBlog?style=for-the-badge)
![GitHub issues](https://img.shields.io/github/issues/QingXuan2000/QingBlog?style=for-the-badge)
![GitHub Workflow](https://img.shields.io/github/actions/workflow/status/QingXuan2000/QingBlog/qingblog-build.yml?style=for-the-badge)

[![Star History Chart](https://api.star-history.com/svg?repos=QingXuan2000/QingBlog&type=Date)](https://star-history.com/#QingXuan2000/QingBlog&Date)

🌐 **在线演示**: [https://qingxuan2000.github.io/](https://qingxuan2000.github.io/)

📖 **QingBlog Wiki**: [https://github.com/QingXuan2000/QingBlog/wiki/](https://github.com/QingXuan2000/QingBlog/wiki/)

</div>

## 📖 项目简介

QingBlog 是一个以 **GitHub Issues 作为内容源** 的静态博客方案：你在 Issue 里写作，GitHub Actions 会自动把内容渲染成文章页面并部署到 GitHub Pages。无需服务器与数据库，适合把写作与代码托管统一在同一套工作流里。

## ✨ 核心特性

- 🚀 **一键部署**：GitHub Pages 免费托管，Actions 自动构建与提交
- 📝 **Issue 即文章**：创建/编辑/删除 Issue 后自动同步到站点
- 🔒 **作者校验**：仅 `targetAuthor` 的 Issue 会被发布，避免被“投喂内容”
- 📄 **分页 + 标签**：首页/文章列表/标签页均支持分页，自动生成标签目录与统计
- 💻 **写作体验**：Markdown 渲染、代码高亮、公式（MathJax）、基础 SEO（sitemap/robots）
- 🎨 **前端体验**：响应式布局、深浅主题切换与一套现代化 UI

## 🛠️ 技术栈

### 前端

- **HTML/CSS/JavaScript** - 静态页面与交互
- **Font Awesome** - 图标
- **MathJax** - 公式渲染
- **ECharts** - 数据可视化（可选）

### 自动化

- **Python 3.12** - 构建脚本
- **GitHub Actions** - 触发构建、自动提交
- **Python-Markdown / PyMdown Extensions / Pygments / BeautifulSoup4** - 渲染与页面处理
- **GitHub Pages** - 部署托管

## 📁 项目结构

```
QingBlog/
├── .github/
│   ├── workflows/
│   │   └── qingblog-build.yml    # GitHub Actions 工作流配置
│   └── scripts/
│       ├── static_blog_generator.py # 核心构建脚本（Issue → 页面）
│       └── requirements.txt         # Python 依赖
│
├── blogData/                     # 博客配置目录
│   ├── blogConfig.json           # 博客核心配置（作者信息、构建设置）
│   ├── pagesConfig.json          # 分页配置（页数、标签统计）
│   └── themes.json               # 主题配置
│
├── css/
│   ├── QBLOG.css                 # 主样式文件（主题变量、布局）
│   ├── blogArticle.css           # 文章页样式
│   └── font-awesome.min.css      # Font Awesome 压缩版
│
├── js/
│   ├── QBLOG.js                  # 前端交互脚本（QingBlog 类）
│   ├── echarts.min.js            # ECharts 图表库
│   └── echarts-wordcloud.min.js  # ECharts 词云插件
│
├── article/                      # 文章页面目录
│   └── index.html                # 文章列表页
│
├── tags/                         # 标签系统目录
│   └── index.html                # 标签云页面
│
├── pages/                        # 分页页面目录
│   └── .pagesDir                 # 分页标识文件
│
├── data/                         # 文章数据页面
│   └── index.html                # 数据可视化页面
│
├── about/                        # 关于我页面
│   └── index.html                # 个人介绍页面
│
├── fonts/                        # 字体文件
│   ├── 江城圆体/                # 江城圆体字体（多字重 200W-700W）
│   ├── This-July.ttf
│   └── fontawesome-webfont.woff2
│
├── img/                          # 图片资源
│   ├── Avatar.png
│   └── logo.svg                  # 项目 Logo
│
├── index.html                    # 首页
├── favicon.ico                   # 网站图标
├── LICENSE                       # GPL v3 许可证
└── README.md                     # 项目说明
```

## 🚀 快速开始

### 1) Fork + 开启 Pages

Fork 本仓库到你的账号下，然后在仓库 **Settings → Pages** 中把站点源设置为 **main 分支 /(root)**。

### 2) 允许工作流写入仓库

在 **Settings → Actions → General → Workflow permissions** 里选择 **Read and write permissions**，否则自动提交生成结果会失败。

### 3) 配置你的博客信息

编辑 `blogData/blogConfig.json`，通常你只需要关心这些字段：

- `blogInfo.blogName`: 博客名称（4 字英文为宜，与模板样式更匹配）
- `author.targetAuthor`: 允许发布文章的 GitHub 用户名（重要）
- `buildConfig.utcOffset`: 时区偏移（默认 `8`，北京时间）
- `buildConfig.articlesPerPage`: 每页文章数量
- `buildConfig.showLoadingAnimation`: 每次加载是否显示开启动画（默认 `true`）
- `robotsConfig.siteUrl` / `robotsConfig.sitemapUrl`: 用于 SEO（可选，但建议配置）

### 4) 发布文章

在你的仓库 **Issues** 新建 Issue（支持 Markdown）。工作流会在 `opened/edited/deleted/reopened` 时触发，生成页面并自动提交到仓库，Pages 随后完成部署。

## 🔧 工作原理

```
┌─────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  创建 Issue  │────▶│  GitHub Actions │────▶│ static_blog_generator.py │
│  或编辑     │     │  触发工作流      │     │   执行脚本       │
└─────────────┘     └─────────────────┘     └────────┬────────┘
                                                      │
            ┌────────────────────────────────────────┘
            ▼
   ┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
   │  验证作者身份    │────▶│ Markdown 转 HTML │────▶│ 生成文章页面    │
   │ (targetAuthor)  │     │  (含代码高亮)    │     │ article/{id}.html │
   └─────────────────┘     └─────────────────┘     └────────┬────────┘
                                                             │
   ┌─────────────────────────────────────────────────────────┘
   ▼
   ┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
   │  更新首页卡片    │────▶│  更新标签系统   │────▶│  更新JSON配置   │
   │  更新列表页     │     │  标签页/统计    │     │  pagesConfig.json│
   └─────────────────┘     └─────────────────┘     └────────┬────────┘
                                                             │
   ┌─────────────────────────────────────────────────────────┘
   ▼
   ┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
   │  生成SEO文件    │────▶│  Git自动提交    │────▶│ GitHub Pages 部署│
   │ sitemap.xml    │     │  更改到仓库      │     │  静态站点       │
   │ robots.txt     │     │                 │     │                │
   └─────────────────┘     └─────────────────┘     └─────────────────┘
```

### 详细流程

1. **触发**：Issue 被创建/编辑/删除/重新打开时触发工作流
2. **校验**：只处理作者为 `targetAuthor` 的 Issue
3. **渲染**：Markdown → HTML（含代码高亮等扩展能力）
4. **生成**：输出文章页、列表页、分页页、标签页及统计配置
5. **SEO**：生成 `sitemap.xml` 与 `robots.txt`（依赖 `robotsConfig`）
6. **提交**：自动提交生成结果并推送，Pages 完成部署

## 💻 本地运行（可选）

本项目默认通过 GitHub Actions 运行构建脚本；如果你想在本地调试生成逻辑，可以用环境变量模拟 Actions 传入的 Issue 信息。

### 前置条件

- 安装 Python 3.12（或与工作流一致的版本）
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

> 提示：若 `ISSUE_AUTHOR` 不等于 `blogData/blogConfig.json` 中的 `author.targetAuthor`，脚本可能会跳过生成（用于避免他人 Issue 被发布）。

## 📝 Markdown 支持

QingBlog 通过 `Python-Markdown` + `PyMdown Extensions` 提供增强的 Markdown 渲染能力（以写作友好为目标）：

- 标准 Markdown（标题、列表、链接、图片等）
- 代码块语法高亮（Pygments）
- 表格/脚注/目录（TOC）/任务列表
- 数学公式（LaTeX，MathJax）
- 常用扩展（如 admonition、details、tabbed 等，按需使用）

## 🏷️ 标签系统

QingBlog 拥有完善的智能标签系统，让文章分类管理更加便捷：

### 标签功能特性

- **自动标签提取**：从 Issue 标签自动提取，一篇文章最多显示 3 个标签
- **独立标签页面**：每个标签自动生成独立目录和页面 `tags/{标签名}/index.html`
- **标签页分页**：标签页同样支持分页功能，自动创建 `tags/{标签名}/{page}.html`
- **智能计数管理**：
  - 新增文章时自动增加标签计数
  - 删除文章时自动减少标签计数
  - 计数归零时自动移除标签
- **自动清理**：自动删除空标签页面和目录
- **双向同步**：文章更新时自动同步到相关标签页面
- **JSON 配置同步**：标签统计数据保存在 `pagesConfig.json` 中

### 使用方式

1. 创建 Issue 时添加 GitHub 标签
2. 系统自动生成标签页面和统计
3. 点击文章标签或访问标签云页面浏览同类型文章

## 🎨 自定义主题

主题配置位于 [`blogData/themes.json`](blogData/themes.json)，每个主题以中文命名，包含色板元数据和 CSS 变量：

```json
{
    "深色主题": {
        "swatch": {
            "primary": "#d3d3dc",
            "secondary": "rgba(20, 20, 20, 1)",
            "tertiary": "rgba(60, 60, 70, 1)"
        },
        "--primary-color": "#d3d3dc",
        "--text-color": "rgba(200, 200, 200, 1)",
        "--bg-color": "linear-gradient(180deg, rgba(20, 20, 20, 1), ...)",
        "--hero-bg-color": "rgba(10, 10, 10, 1)"
    },
    "浅色主题": {
        "swatch": { ... },
        ...
    }
}
```

- `swatch` 定义主题卡片的色块预览（三色），用于主题选择弹窗
- 其他字段为 CSS 自定义属性，加载时动态注入到 `:root`
- 可自行增删主题，页面右上角的调色盘按钮会打开主题选择弹窗，支持"跟随系统"、点选切换

## 📊 数据可视化

QingBlog 集成了 ECharts 数据可视化库，提供文章数据的可视化展示：

- 📈 **文章统计图表**：展示文章数量、标签分布等数据
- 🏷️ **标签云图**：词云形式展示热门标签

数据配置位于 [`blogData/blogConfig.json`](blogData/blogConfig.json) 的 `author.authorTags` 中。

## 🔍 前端架构

### QingBlog 类设计

QingBlog 采用面向对象编程设计，核心类包含：

```javascript
class QingBlog {
  // 静态配置
  static alertColors = { /* 弹窗颜色 */ };
  
  // 实例属性
  blogConfig = {};
  pagesConfig = {};
  themes = {};
  
  // 核心方法
  async init() { /* 初始化所有功能 */ }
  async loadConfigs() { /* 加载配置文件 */ }
  initThemeModal() { /* 主题选择弹窗（Modal + 卡片渲染） */ }
  initPagination() { /* 分页控件 */ }
  showAlert() { /* 弹窗提示 */ }
}
```

### 可复用 Modal 组件

模态框通用逻辑（动画、遮罩、Escape 关闭、滚动锁定）由独立 `Modal` 类封装，可传入不同的面板动画名复用：

```javascript
const modal = new Modal(overlayEl, panelEl, {
  panelShowAnim: "showThemeModalAnimation",
  panelHideAnim: "hideThemeModalAnimation"
});
modal.show();
modal.hide();
```

### 配置系统

前端通过 `_getBase()` 计算相对路径后异步加载 JSON 配置文件：

```javascript
async loadConfigs() {
  const base = this._getBase();
  this.blogConfig = await this.getConfig(`${base}/blogData/blogConfig.json`);
  this.pagesConfig = await this.getConfig(`${base}/blogData/pagesConfig.json`);
  this.themes = await this.getConfig(`${base}/blogData/themes.json`);
}
```

## 🛡️ 安全说明

- 只有 `targetAuthor` 指定的用户创建的 Issue 才会被发布
- 这防止了他人在你的博客上发表文章
- 建议将仓库设置为需要审核的 Fork 工作流

## 📚 Wiki 文档

QingBlog 提供了完整的 Wiki 文档，包含以下章节：

- 📖 [首页](https://github.com/QingXuan2000/QingBlog/wiki/) - Wiki 概览
- 🚀 [安装指南](https://github.com/QingXuan2000/QingBlog/wiki/Installation-Guide) - 快速上手教程
- ⚙️ [核心功能](https://github.com/QingXuan2000/QingBlog/wiki/Core-Features) - 功能详细介绍
- 🎨 [前端参考](https://github.com/QingXuan2000/QingBlog/wiki/Frontend-Reference) - 前端开发文档
- 🏗️ [技术架构](https://github.com/QingXuan2000/QingBlog/wiki/Technical-Architecture) - 架构设计说明
- 📦 [部署配置](https://github.com/QingXuan2000/QingBlog/wiki/Deployment-Configuration) - 部署相关配置
- ✅ [配置检查清单](https://github.com/QingXuan2000/QingBlog/wiki/Configuration-Checklist) - 配置验证清单
- 📖 [使用指南](https://github.com/QingXuan2000/QingBlog/wiki/Usage-Guide) - 日常使用教程
- 🔌 [API 文档](https://github.com/QingXuan2000/QingBlog/wiki/API-Documentation) - API 接口文档
- ❓ [常见问题](https://github.com/QingXuan2000/QingBlog/wiki/FAQ) - FAQ 问题解答
- 🤝 [贡献指南](https://github.com/QingXuan2000/QingBlog/wiki/Contributing-Guide) - 如何参与贡献
- 📝 [更新日志](https://github.com/QingXuan2000/QingBlog/wiki/Changelog) - 版本更新记录
- 📜 [许可证](https://github.com/QingXuan2000/QingBlog/wiki/License.md) - 许可证说明

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

详细的贡献指南请参阅 [贡献指南](https://github.com/QingXuan2000/QingBlog/wiki/Contributing-Guide)。

## 📄 许可证

本项目采用 [GNU General Public License v3.0](LICENSE) 许可证。

## 👨‍💻 作者

- **QingXuanJun** - [GitHub](https://github.com/QingXuan2000)

## 🌟 致谢

- [Font Awesome](https://fontawesome.com/) - 图标库
- [GitHub](https://github.com/) - 托管和 CI/CD 服务
- [Python Markdown](https://python-markdown.github.io/) - Markdown 转换库
- [ECharts](https://echarts.apache.org/) - 数据可视化库
