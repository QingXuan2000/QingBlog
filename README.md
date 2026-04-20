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

QingBlog 是一个创新的博客框架，它将 GitHub Issues 作为内容管理系统，通过 GitHub Actions 自动将 Issue 转换为精美的博客文章页面。无需服务器、无需数据库，只需创建 Issue 即可发布博客。内置丰富的 Markdown 支持、分页系统、标签管理和现代化 UI 设计。

## ✨ 核心特性

- 🚀 **零成本部署**：利用 GitHub Pages 免费托管
- 📝 **Issue 即文章**：在 GitHub Issues 中写作，自动同步到博客
- 🔄 **自动化流程**：创建/编辑 Issue 后自动构建部署
- 📄 **智能分页系统**：首页、文章列表页、标签页均支持分页
- 🎨 **现代化设计**：渐变背景、毛玻璃效果、卡片式布局
- 🌓 **深色/浅色主题**：支持一键切换主题，自动适配系统偏好
- 📱 **响应式设计**：适配桌面和移动设备，侧边栏导航
- 🏷️ **标签系统**：自动提取 Issue 标签，生成独立标签页面
- 💻 **代码高亮**：支持代码块语法高亮和复制功能
- 🔒 **作者验证**：仅指定作者的 Issue 才会被发布
- ✨ **动态标题**：页面动态切换标题，检测用户离开/返回
- 🎬 **加载动画**：炫酷的 SVG 加载动画
- ⬆️ **返回顶部**：一键返回顶部功能
- 🎯 **右键菜单**：自定义右键菜单（复制、刷新）
- 📐 **数学公式**：支持 LaTeX 数学公式渲染
- 🎭 **弹窗提示**：友好的操作反馈弹窗
- 📊 **数据可视化**：文章数据可视化展示（ECharts）
- 🔧 **JSON 配置系统**：灵活的 JSON 配置文件管理
- 🤖 **SEO 优化**：自动生成 sitemap.xml 和 robots.txt

## 🛠️ 技术栈

### 前端

- **HTML5** - 语义化页面结构
- **CSS3** - 渐变、动画、毛玻璃效果
- **JavaScript (ES6+)** - 面向对象编程，QingBlog 类架构设计
- **Font Awesome** - 矢量图标库
- **MathJax** - 数学公式渲染
- **ECharts** - 数据可视化图表库
- **中文字体** - 江城圆体、阿里妈妈方圆体、得意黑等

### 自动化

- **Python 3.12** - 核心处理脚本
- **GitHub Actions** - CI/CD 工作流
- **Python-Markdown** - Markdown 渲染
- **PyMdown Extensions** - Markdown 增强扩展
- **Pygments** - 代码高亮
- **Beautiful Soup 4** - HTML 处理
- **GitHub Pages** - 静态站点托管

## 📁 项目结构

```
QingBlog/
├── .github/
│   ├── workflows/
│   │   └── qingblog-build.yml    # GitHub Actions 工作流配置
│   └── scripts/
│       ├── check_issue.py        # 核心处理脚本
│       └── requirements.txt      # Python 依赖
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

### 1. Fork 项目

Fork 本仓库到你的 GitHub 账号下。

### 2. 配置 GitHub Pages

1. 进入仓库 **Settings** → **Pages**
2. **Source** 选择 **Deploy from a branch**
3. **Branch** 选择 **main** 分支，文件夹选择 **/(root)**
4. 点击 **Save**

### 3. 启用 GitHub Actions

1. 进入仓库 **Actions** 标签页
2. 点击 **I understand my workflows, go ahead and enable them** 按钮
3. 确保工作流已启用，否则自动构建将无法运行

### 4. 配置工作流权限

1. 进入仓库 **Settings** → **Actions** → **General**
2. 找到 **Workflow permissions**
3. 选择 **Read and write permissions**
4. 点击 **Save**

### 5. 修改博客配置

编辑 [`blogData/blogConfig.json`](blogData/blogConfig.json) 配置文件：

```json
{
    "blogInfo": {
        "blogName": "博客名称（4字英文）",
        "yearOfWriting": 2025,
        "currentYear": 2026
    },
    "author": {
        "targetAuthor": "你的GitHub名称",
        "introShort": "标语",
        "introDetail": "自我介绍",
        "socialMediaPlatform": {
            "GitHub": {
                "icon": "<i class=\"fa fa-github\" aria-hidden=\"true\"></i>",
                "url": "https://github.com/QingXuan2000"
            },
            "社交平台设置（格式如上，此处填写名字）": {
                "icon": "图标",
                "url": "链接"
            }
        },
        "authorTags": {
            "HTML": 65,
            "CSS": 60,
            "JavaScript": 40,
            "个人标签设置（格式如上，数字为占比）": 0
        }
    },
    "buildConfig": {
        "utcOffset": 8,
        "articlesPerPage": 20
    },
    "robotsConfig": {
        "siteUrl": "网站主域名",
        "allowPaths": ["/"],
        "disallowPaths": ["/blogData/"],
        "sitemapUrl": "Sitemap完整URL"
    }
}
```

**配置说明**：
- `targetAuthor`: 指定允许发布博客的 GitHub 用户名
- `utcOffset`: 时区偏移（默认东八区北京时间）
- `articlesPerPage`: 每页文章数量（默认 20）
- `robotsConfig`: SEO 配置，包括站点 URL、允许/禁止路径、站点地图 URL
- `socialMediaPlatform`: 社交媒体平台配置，可配置多个社交平台
- `authorTags`: 作者个人标签配置，数字表示占比（用于数据可视化页面）

> **时区说明**：`utcOffset` 用于将 GitHub 的 UTC 时间转换为本地时间显示，默认为 `8`（东八区）。如需其他时区，请修改为对应偏移值，如 `-5`（美东）、`0`（伦敦）等。

### 6. 发布第一篇文章

1. 打开你 Fork 的仓库
2. 进入 **Issues** 标签页
3. 点击 **New issue**
4. 填写标题和内容（支持 Markdown）
5. 添加标签（可选，最多显示3个）
6. 点击 **Submit new issue**

等待几秒后，GitHub Actions 会自动构建并部署，你的文章就会出现在博客中了！

## 🔧 工作原理

```
┌─────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  创建 Issue  │────▶│  GitHub Actions │────▶│ check_issue.py  │
│  或编辑     │     │  触发工作流      │     │   执行脚本       │
└─────────────┘     └─────────────────┘     └────────┬────────┘
                                                      │
            ┌────────────────────────────────────────┘
            ▼
   ┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
   │  验证作者身份    │────▶│ Markdown 转 HTML │────▶│ 生成文章页面    │
   │ (TARGET_AUTHOR) │     │  (含代码高亮)    │     │ article/{id}.html │
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

1. **触发**：当 Issue 被创建、编辑、删除或重新打开时，GitHub Actions 自动触发
2. **验证**：脚本检查 Issue 作者是否匹配 `targetAuthor`
3. **时区转换**：根据 `utcOffset` 将 UTC 时间转换为本地时间
4. **转换**：使用 Python-Markdown + PyMdown Extensions 将 Markdown 转换为 HTML，支持：
   - 表格、脚注、目录
   - 代码高亮（带复制按钮）
   - 自动换行
   - 任务列表
   - Emoji 表情
   - 数学公式（LaTeX）
   - 标签页、警告框等高级特性
5. **生成**：创建文章页面 `article/{id}.html`
6. **分页管理**：
   - 在 `index.html` 和 `article/index.html` 中添加/更新文章卡片
   - 当文章数量超过 `articlesPerPage` 时自动创建新的分页页面 `pages/{page}.html`
   - 更新 JSON 配置文件和 JS 文件中的分页数据
7. **标签处理**：
   - 自动为每个标签创建独立目录和页面 `tags/{标签名}/index.html`
   - 标签页也支持分页，自动创建 `tags/{标签名}/{page}.html`
   - 更新 `pagesConfig.json` 中的标签文章统计
   - 将文章同步到对应的标签页面
   - 自动删除空标签页面和目录
8. **SEO 优化**：
   - 自动生成 `sitemap.xml` 包含所有页面链接
   - 生成 `robots.txt` 配置搜索引擎爬取规则
9. **部署**：自动提交更改，GitHub Pages 自动部署

## 📝 Markdown 支持

QingBlog 支持极其丰富的 Markdown 语法，通过 PyMdown Extensions 提供强大的增强功能：

- ✅ 标准 Markdown 语法（标题、列表、链接、图片等）
- ✅ 代码块（支持复制按钮、语法高亮）
- ✅ 表格
- ✅ 任务列表（可点击复选框）
- ✅ 脚注
- ✅ 目录（TOC）
- ✅ Emoji 表情支持
- ✅ 数学公式（LaTeX，通过 MathJax 渲染）
- ✅ 高亮文本（使用 `==文本==` 语法）
- ✅ 删除线（使用 `~~文本~~` 语法）
- ✅ 上标/下标
- ✅ 进度条
- ✅ 标签页（Tabbed）内容
- ✅ 警告框/提示框（Admonition）
- ✅ 详情折叠框（Details）
- ✅ 魔法链接（自动识别 URL、邮箱等）
- ✅ 按键样式（Keyboard）
- ✅ 代码行内高亮

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

主题配置位于 [`blogData/themes.json`](blogData/themes.json) 中，前端通过 QingBlog 类动态加载：

```javascript
class QingBlog {
  static themes = {
    dark: {
      '--primary-color': '#d9d9deb8',
      '--text-color': 'rgba(200, 200, 200, 1)',
      '--bg-color': 'linear-gradient(180deg, rgba(20, 20, 20, 1), ...)',
      '--hero-bg-color': 'rgba(10, 10, 10, 1)',
      // ... 更多变量
    },
    light: {
      '--primary-color': '#2c2c2db8',
      '--text-color': 'rgba(44, 44, 44, 1)',
      '--bg-color': 'linear-gradient(180deg, rgba(233, 233, 237, 1), ...)',
      '--hero-bg-color': 'rgba(217, 218, 220, 1)',
      // ... 更多变量
    }
  }
}
```

用户可以通过页面右上角的按钮切换深色/浅色主题。

## 📊 数据可视化

QingBlog 集成了 ECharts 数据可视化库，提供文章数据的可视化展示：

- 📈 **文章统计图表**：展示文章数量、标签分布等数据
- 🏷️ **标签云图**：词云形式展示热门标签
- 📅 **时间轴图表**：文章发布时间分布

数据配置位于 [`blogData/blogConfig.json`](blogData/blogConfig.json) 的 `author.authorTags` 中。

## 🔍 前端架构

### QingBlog 类设计

QingBlog 采用面向对象编程设计，核心类包含：

```javascript
class QingBlog {
  // 静态配置
  static themes = { /* 主题配置 */ };
  static alertColors = { /* 弹窗颜色 */ };
  
  // 实例属性
  blogConfig = {};
  pagesConfig = {};
  themes = {};
  
  // 核心方法
  async init() { /* 初始化所有功能 */ }
  async loadConfigs() { /* 加载配置文件 */ }
  toggleTheme() { /* 主题切换 */ }
  initPagination() { /* 分页控件 */ }
  showAlert() { /* 弹窗提示 */ }
}
```

### 配置系统

前端通过异步加载 JSON 配置文件：

```javascript
async loadConfigs() {
  this.blogConfig = await this.getConfig("/blogData/blogConfig.json");
  this.pagesConfig = await this.getConfig("/blogData/pagesConfig.json");
  this.themes = await this.getConfig("/blogData/themes.json");
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
