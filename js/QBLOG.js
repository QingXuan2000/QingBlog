/**
 * ==================================================
 * QingBlog 博客前端核心脚本
 * ==================================================
 */

class QingBlog {
  // ========== 静态常量配置 ==========
  static blogLogoSvg = `<svg class="loading__graphic-svg" width="620" height="620" viewBox="0 0 620 620" fill="none" xmlns="http://www.w3.org/2000/svg">
    <circle class="loading__logo-circle" cx="310" cy="310" r="250" />
    <circle class="loading__logo-circle" cx="310" cy="310" r="300" />
    <path class="loading__logo-path" d="M315 70L315 550" />
    <line class="loading__logo-path" x1="124" y1="213" x2="264" y2="213" />
    <line class="loading__logo-path" x1="104" y1="310" x2="284" y2="310" />
    <line class="loading__logo-path" x1="124" y1="407" x2="264" y2="407" />
    <line class="loading__logo-path" x1="365" y1="115" x2="365" y2="245" />
    <line class="loading__logo-path" x1="365" y1="286" x2="365" y2="386" />
    <line class="loading__logo-path" x1="365" y1="427" x2="365" y2="507" />
    <line class="loading__logo-path" x1="423" y1="490" x2="423" y2="380" />
    <line class="loading__logo-path" x1="474" y1="440" x2="474" y2="330" />
    <line class="loading__logo-path" x1="423" y1="345" x2="423" y2="255" />
    <line class="loading__logo-path" x1="423" y1="220" x2="423" y2="140" />
    <line class="loading__logo-path" x1="474" y1="285" x2="474" y2="205" />
  </svg>`;

  static alertColors = {
    green: { background: "rgba(34, 197, 94, 0.3)", border: "1px solid rgba(34, 197, 94, 0.4)", boxShadow: "0 0 20px rgba(34, 197, 94, 0.2), inset 0 0 10px rgba(34, 197, 94, 0.05)" },
    red: { background: "rgba(239, 68, 68, 0.3)", border: "1px solid rgba(239, 68, 68, 0.4)", boxShadow: "0 0 20px rgba(239, 68, 68, 0.2), inset 0 0 10px rgba(239, 68, 68, 0.05)" },
    orange: { background: "rgba(249, 115, 22, 0.3)", border: "1px solid rgba(249, 115, 22, 0.4)", boxShadow: "0 0 20px rgba(249, 115, 22, 0.2), inset 0 0 10px rgba(249, 115, 22, 0.05)" },
    yellow: { background: "rgba(234, 179, 8, 0.3)", border: "1px solid rgba(234, 179, 8, 0.4)", boxShadow: "0 0 20px rgba(234, 179, 8, 0.2), inset 0 0 10px rgba(234, 179, 8, 0.05)" }
  };

  // ========== 实例属性 ==========
  constructor() {
    this.eventCleanPool = []; // 清理任务池
    this.blogConfig = null;   // 博客配置
    this.pagesConfig = null;  // 分页配置
    this.themes = null;       // 主题配置
    this.root = document.documentElement; // HTML根元素
    this.body = document.body; // body元素
  }

  // ========== 公共初始化入口 ==========
  async init() {
    try {
      // 加载核心配置
      await this.loadConfigs();

      // 渲染公共组件
      this.dynamicComponentBox();

      // 初始化各个功能模块
      this.initLoadingAnimation();
      this.setNavHeightVariable();
      this.initThemeModal();
      this.initBackToTop();
      this.initSidebar();
      this.initWebTitle();
      this.initCopyButtons();
      this.initHeaderBackground();
      this.initTagManager();
      this.initPagination();
      this.initCardScrollAnimation();
      this.initLazyLoadImages();
      this.initArticleData();
      this.addTagToPages();
      this.initMeData();
      this.addAboutCard();
      this.initFriendLinks();
      this.initFriendLinks();

      // 绑定窗口resize事件
      window.addEventListener("resize", this.debounceSetNavHeight);
      this.addCleanTask(() => window.removeEventListener("resize", this.debounceSetNavHeight));

      // 绑定页面卸载清理事件
      window.addEventListener("beforeunload", () => this.cleanAll());

    } catch (error) {
      console.error("博客初始化失败：", error);
    }
  }

  // ========== 配置加载 ==========
  _getBase() {
    const path = window.location.pathname;
    const cleaned = path.replace(/\/$/, "");
    const parts = cleaned.split("/").filter(Boolean);
    const last = parts[parts.length - 1];
    const depth = last && last.includes(".") ? parts.length - 1 : parts.length;
    return depth > 0 ? "../".repeat(depth) : "./";
  }

  async loadConfigs() {
    const base = this._getBase();
    this.blogConfig = await this.getConfig(`${base}/blogData/blogConfig.json`);
    this.pagesConfig = await this.getConfig(`${base}/blogData/pagesConfig.json`);
    this.themes = await this.getConfig(`${base}/blogData/themes.json`);

    // 防抖导航栏高度更新
    this.debounceSetNavHeight = this.debounce(() => this.setNavHeightVariable());
  }

  async getConfig(url) {
    try {
      const response = await fetch(url);
      if (!response.ok) throw new Error(`请求${url}失败，状态码：${response.status}`);
      return await response.json();
    } catch (error) {
      console.error("配置获取失败：", error);
      throw error;
    }
  }

  // ========== 清理任务管理 ==========
  addCleanTask(task) {
    this.eventCleanPool.push(task);
  }

  cleanAll() {
    this.eventCleanPool.forEach(task => {
      try { task(); } catch (e) { console.error("清理任务执行失败：", e); }
    });
  }

  // ========== 工具函数 ==========
  resizeLogo(width, height) {
    return QingBlog.blogLogoSvg.replace('width="620" height="620"', `width="${width}" height="${height}"`);
  }

  debounce(fn, delay = 50) {
    let timer = null;
    return (...args) => {
      clearTimeout(timer);
      timer = setTimeout(() => fn.apply(this, args), delay);
    };
  }

  throttle(fn, delay = 50) {
    let lastTime = 0;
    return (...args) => {
      const now = Date.now();
      if (now - lastTime >= delay) {
        lastTime = now;
        fn.apply(this, args);
      }
    };
  }

  // ========== 提示框功能 ==========
  playAlertAnimation() {
    const alertMessage = document.getElementById("alert-message");
    if (!alertMessage) return;
    alertMessage.style.animation = "none";
    void alertMessage.offsetHeight;
    alertMessage.style.animation = "alertAnimation 2.2s normal forwards";
  }

  showAlert(color, message) {
    const alertMessage = document.getElementById("alert-message");
    if (!alertMessage) return;
    const textSpan = alertMessage.querySelector("span");
    if (textSpan) textSpan.innerHTML = message;
    const style = QingBlog.alertColors[color];
    if (style) {
      Object.assign(alertMessage.style, style);
      this.playAlertAnimation();
    }
  }

  // ========== 导航栏高度 ==========
  setNavHeightVariable() {
    const nav = document.getElementById("navbar");
    if (nav) {
      const height = nav.offsetHeight;
      this.root.style.setProperty("--nav-height", `${height}px`);
      return height;
    }
    return 0;
  }

  // ========== 公共组件渲染 ==========
  dynamicComponentBox() {
    const pathSegments = window.location.pathname.split("/").filter(Boolean);
    const pageName = pathSegments[0];
    const needPaginationPages = ["", "index.html", "article", "pages", "tags"];

    // 构建社交链接
    const socialMediaPlatform = Object.entries(this.blogConfig.author.socialMediaPlatform)
      .map(([_, config]) => `<li><a href="${config.url}" target="_blank" class="social-link">${config.icon}</a></li>`)
      .join("");

    // 版权文本
    const copyrightText = `&copy; ${this.blogConfig.blogInfo.yearOfWriting}-${this.blogConfig.blogInfo.currentYear} ${this.blogConfig.author.targetAuthor}. All rights reserved.`;

    // 头部组件
    const componentBoxHeader = `
      <div class="loading" role="status" aria-label="页面加载中">
          <div class="loading__graphic">${QingBlog.blogLogoSvg}</div>
          <div class="loading__bar"></div>
          <div class="loading__bar"></div>
      </div>
      <div id="alert" role="alert" aria-live="polite">
          <div id="alert-message"><span></span></div>
      </div>
      <div class="overlay" aria-hidden="true"></div>
      <button id="back-to-top" aria-label="返回顶部"><i class="fa fa-angle-up" aria-hidden="true"></i></button>
      <button id="back-to-top" aria-label="返回顶部"><i class="fa fa-angle-up" aria-hidden="true"></i></button>
      <header id="page-header">
          <nav id="navbar" aria-label="主导航">
              ${this.resizeLogo(35, 35)}
              <div id="navbar-title" aria-label="博客名称">${this.blogConfig.blogInfo.blogName}</div>
              <div class="divider" style="width: 2px; margin: 0 0.5rem 0 1rem; border-radius: 100em;" aria-hidden="true"></div>
              <ul>
                  <li><a href="#" onclick="window.qingBlogInstance.navigation('/')"><i class="fa fa-home" aria-hidden="true"></i>&nbsp;首页</a></li>
                  <li><a href="#" onclick="window.qingBlogInstance.navigation('/article/')"><i class="fa fa-book" aria-hidden="true"></i>&nbsp;文章</a></li>
                  <li><a href="#" onclick="window.qingBlogInstance.navigation('/tags/')"><i class="fa fa-tags" aria-hidden="true"></i>&nbsp;标签</a></li>
                  <li><a href="#" onclick="window.qingBlogInstance.navigation('/data/')"><i class="fa fa-database" aria-hidden="true"></i>&nbsp;文章数据</a></li>
                  <li><a href="#" onclick="window.qingBlogInstance.navigation('/about/')"><i class="fa fa-user-circle-o" aria-hidden="true"></i>&nbsp;关于我</a></li>
                  <li><a href="#" onclick="window.qingBlogInstance.navigation('/links/')"><i class="fa fa-link" aria-hidden="true"></i>&nbsp;友情链接</a></li>
                  <li><a href="#" onclick="window.qingBlogInstance.navigation('/links/')"><i class="fa fa-link" aria-hidden="true"></i>&nbsp;友情链接</a></li>
              </ul>
          </nav>
          <button id="theme-toggle" aria-label="选择主题"><i class="fa fa-paint-brush"></i></button>
          <button id="sidebar-toggle" aria-label="打开侧边栏"><i class="fa fa-bars" aria-hidden="true"></i></button>
      </header>
      <aside id="sidebar" aria-label="侧边栏导航">
          <div id="sidebar-header" class="sidebar__header">
              <div class="sidebar__logo">${this.resizeLogo(35, 35)}</div>
              <div class="sidebar__title">${this.blogConfig.blogInfo.blogName}</div>
              <button id="sidebar-close" aria-label="关闭侧边栏"><i class="fa fa-remove" aria-hidden="true"></i></button>
          </div>
          <div class="sidebar__header-divider divider" style="width: 100%; height: 1px;" aria-hidden="true"></div>
          <div id="sidebar-content" class="sidebar__content">
              <div class="sidebar__user-info">
                  <img id="sidebar-avatar" src="${base}img/Avatar.png" alt="作者头像" />
                  <h2 id="user-name" class="sidebar__user-name">${this.blogConfig.author.targetAuthor}</h2>
                  <p class="sidebar__motto">${this.blogConfig.author.introShort}</p>
              </div>
              <nav aria-label="侧边栏导航">
                  <ul>
                      <li><a href="#" onclick="window.qingBlogInstance.navigation('/')"><i class="fa fa-home" aria-hidden="true"></i>&nbsp;首页</a></li>
                      <li class="sidebar__nav-divider" role="separator"><div class="sidebar__header-divider divider" style="width: 100%; height: 1px;" aria-hidden="true"></div></li>
                      <li><a href="#" onclick="window.qingBlogInstance.navigation('/article/')"><i class="fa fa-book" aria-hidden="true"></i>&nbsp;文章</a></li>
                      <li class="sidebar__nav-divider" role="separator"><div class="sidebar__header-divider divider" style="width: 100%; height: 1px;" aria-hidden="true"></div></li>
                      <li><a href="#" onclick="window.qingBlogInstance.navigation('/tags/')"><i class="fa fa-tags" aria-hidden="true"></i>&nbsp;标签</a></li>
                      <li class="sidebar__nav-divider" role="separator"><div class="sidebar__header-divider divider" style="width: 100%; height: 1px;" aria-hidden="true"></div></li>
                      <li><a href="#" onclick="window.qingBlogInstance.navigation('/data/')"><i class="fa fa-database" aria-hidden="true"></i>&nbsp;文章数据</a></li>
                      <li class="sidebar__nav-divider" role="separator"><div class="sidebar__header-divider divider" style="width: 100%; height: 1px;" aria-hidden="true"></div></li>
                      <li><a href="#" onclick="window.qingBlogInstance.navigation('/about/')"><i class="fa fa-user-circle-o" aria-hidden="true"></i>&nbsp;关于我</a></li>
                      <li class="sidebar__nav-divider" role="separator"><div class="sidebar__header-divider divider" style="width: 100%; height: 1px;" aria-hidden="true"></div></li>
                      <li><a href="#" onclick="window.qingBlogInstance.navigation('/links/')"><i class="fa fa-link" aria-hidden="true"></i>&nbsp;友情链接</a></li>
                      <li class="sidebar__nav-divider" role="separator"><div class="sidebar__header-divider divider" style="width: 100%; height: 1px;" aria-hidden="true"></div></li>
                      <li><a href="#" onclick="window.qingBlogInstance.navigation('/links/')"><i class="fa fa-link" aria-hidden="true"></i>&nbsp;友情链接</a></li>
                  </ul>
              </nav>
              <div class="sidebar__social">
                  <h3 class="sidebar__social-title">关注我</h3>
                  <ul class="social-links">${socialMediaPlatform}</ul>
              </div>
          </div>
          <div id="sidebar-footer" class="sidebar__footer">
              <div class="sidebar__header-divider divider" style="width: 100%; height: 1px; margin-bottom: 1rem;" aria-hidden="true"></div>
              <p>${copyrightText}</p>
          </div>
      </aside>
      <!-- 主题选择弹窗 -->
      <div class="theme-modal-overlay" id="theme-modal-overlay" aria-hidden="true"></div>
      <div id="theme-modal" aria-label="选择主题" role="dialog" aria-modal="true">
          <div id="theme-modal-header">
              <h2><i class="fa fa-paint-brush"></i>&nbsp;&nbsp;选择主题</h2>
              <button id="theme-modal-close" aria-label="关闭主题选择">
                  <i class="fa fa-remove" aria-hidden="true"></i>
              </button>
          </div>
          <div class="theme-modal__divider" aria-hidden="true"></div>
          <div id="theme-modal-grid"></div>
      </div>
    `;

    // 页脚组件
    const componentBoxFooter = `
    <footer class="footer">
      <div class="footer__content">
        <div class="footer__section footer__brand">
          ${this.resizeLogo(50, 50)}
          <h2>${this.blogConfig.blogInfo.blogName}</h2>
          <p>${this.blogConfig.author.introShort}</p>
        </div>
        <nav class="footer__section footer__links" aria-label="页脚导航">
          <h3>快速链接</h3>
          <ul>
            <li><a href="#" onclick="window.qingBlogInstance.navigation('/')"><i class="fa fa-home"></i>&nbsp;首页</a></li>
            <li><a href="#" onclick="window.qingBlogInstance.navigation('/article/')"><i class="fa fa-book"></i>&nbsp;文章</a></li>
            <li><a href="#" onclick="window.qingBlogInstance.navigation('/tags/')"><i class="fa fa-tags"></i>&nbsp;标签</a></li>
            <li><a href="#" onclick="window.qingBlogInstance.navigation('/data/')"><i class="fa fa-database" aria-hidden="true"></i>&nbsp;文章数据</a></li>
            <li><a href="#" onclick="window.qingBlogInstance.navigation('/about/')"><i class="fa fa-user-circle-o" aria-hidden="true"></i>&nbsp;关于我</a></li>
            <li><a href="#" onclick="window.qingBlogInstance.navigation('/links/')"><i class="fa fa-link" aria-hidden="true"></i>&nbsp;友情链接</a></li>
            <li><a href="#" onclick="window.qingBlogInstance.navigation('/links/')"><i class="fa fa-link" aria-hidden="true"></i>&nbsp;友情链接</a></li>
          </ul>
        </nav>
        <div class="footer__section footer__social">
          <h3>关注我</h3>
          <ul class="social-links">${socialMediaPlatform}</ul>
        </div>
      </div>
      <div class="footer__bottom">
        <div class="divider" style="width: 100%; height: 1px; margin: 1rem 0;" aria-hidden="true"></div>
        <p>${copyrightText}</p>
        <p class="footer__powered">Powered by Love and Coffee</p>
      </div>
    </footer>
    `;

    // 分页组件
    const paginationControls = `
    <nav id="pagination-controls-wrapper" aria-label="分页导航">
        <div id="pagination-controls">
            <button type="button" id="prev-trigger" aria-label="上一页">
                <i class="fa fa-arrow-left" aria-hidden="true"></i>
                <span>上一页</span>
            </button>
            <div id="input-page-num-wrapper">
                <span id="page-num" aria-live="polite"></span>
                <input id="input-page-num" type="text" placeholder="输入页码" aria-label="输入页码">
                <button type="button" id="go-to-page-btn" aria-label="跳转到指定页">
                    <i class="fa fa-level-down" aria-hidden="true"></i>
                </button>
            </div>
            <button type="button" id="next-trigger" aria-label="下一页">
                <span>下一页</span>
                <i class="fa fa-arrow-right" aria-hidden="true"></i>
            </button>
        </div>
    </nav>
    `;

    // 渲染组件
    this.body.insertAdjacentHTML("afterbegin", componentBoxHeader);
    if (needPaginationPages.includes(pageName || "")) {
      this.body.insertAdjacentHTML("beforeend", paginationControls);
    }
    this.body.insertAdjacentHTML("beforeend", componentBoxFooter);

    // 设置首页标题
    const heroCenterText = document.getElementById("hero-center-text");
    if (heroCenterText) heroCenterText.innerHTML = this.blogConfig.blogInfo.blogName;
  }

  // ========== 加载动画 ==========
  initLoadingAnimation() {
    const loadingContainer = document.querySelector(".loading");
    if (!loadingContainer) return;

    // URL参数 ?skipLoading=true 时跳过动画（页面间跳转）
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.has("skipLoading")) {
      loadingContainer.style.display = "none";
      // 清除 URL 参数，保持地址栏整洁
      history.replaceState(null, "", window.location.pathname + window.location.hash);
      return;
    }

    const showAlways = this.blogConfig?.buildConfig?.showLoadingAnimation;

    // showLoadingAnimation = false：直接隐藏，从不显示动画
    if (showAlways === false) {
      loadingContainer.style.display = "none";
      return;
    }

    // showLoadingAnimation = true：每次加载都显示动画
    if (showAlways === true) {
      this._playLoadingAnimation(loadingContainer);
      return;
    }

    // 未配置时向后兼容：仅首次访问显示动画
    const firstLoading = localStorage.getItem("firstLoading") || "true";
    if (firstLoading !== "false") {
      this._playLoadingAnimation(loadingContainer);
      localStorage.setItem("firstLoading", "false");
    } else {
      loadingContainer.style.display = "none";
    }
  }

  _playLoadingAnimation(loadingContainer) {
    const qingBlogIcon = document.querySelector(".loading__graphic");
    const loadingDivs = document.querySelectorAll(".loading__bar");
    this.body.style.overflow = "hidden";

    const hideTimer = setTimeout(() => {
      loadingDivs.forEach((div, index) => {
        div.style.animation = (index + 1) % 2 === 0 ? "loadingRightAnimation 1.5s ease-out forwards" : "loadingLeftAnimation 1.5s ease-out forwards";
      });
      qingBlogIcon.style.animation = "hideOverlayAnimation 0.5s ease-in-out forwards";
    }, 1600);

    const removeTimer = setTimeout(() => {
      loadingContainer.style.display = "none";
      this.body.style.overflow = "auto";
    }, 3000);

    this.addCleanTask(() => {
      clearTimeout(hideTimer);
      clearTimeout(removeTimer);
    });
  }

  // ========== 主题切换 ==========
  initThemeModal() {
    const toggleBtn = document.getElementById("theme-toggle");
    const systemThemeMedia = window.matchMedia("(prefers-color-scheme: dark)");
    const overlay = document.getElementById("theme-modal-overlay");
    const modal = document.getElementById("theme-modal");
    const closeBtn = document.getElementById("theme-modal-close");
    const grid = document.getElementById("theme-modal-grid");

    if (!toggleBtn || !overlay || !modal || !closeBtn || !grid) return;

    const themeModal = new Modal(overlay, modal);

    const getValidTheme = (theme) => {
      if (theme && this.themes[theme]) return theme;
      return (systemThemeMedia.matches && this.themes["深色主题"]) ? "深色主题" : "浅色主题";
    };

    const applyTheme = (theme) => {
      Object.entries(this.themes[theme]).forEach(([key, value]) => {
        if (key === "swatch") return;
        this.root.style.setProperty(key, value);
      });
    };

    const setTheme = (theme) => {
      applyTheme(theme);
      localStorage.setItem("theme", theme);
      const cards = grid.querySelectorAll(".theme-card");
      cards.forEach((card) => {
        card.classList.toggle("theme-card--active", card.dataset.theme === theme);
      });
    };

    const initTheme = () => {
      const savedTheme = localStorage.getItem("theme");
      applyTheme(getValidTheme(savedTheme));
    };

    const handleSystemThemeChange = (e) => {
      if (!localStorage.getItem("theme")) {
        setTheme(e.matches ? "深色主题" : "浅色主题");
      }
    };

    const refreshCardHighlight = () => {
      const isSystem = !localStorage.getItem("theme");
      const currentTheme = isSystem ? null : getValidTheme(localStorage.getItem("theme"));
      const cards = grid.querySelectorAll(".theme-card");
      cards.forEach((card) => {
        if (isSystem) {
          card.classList.toggle("theme-card--active", card.dataset.theme === "system");
        } else {
          card.classList.toggle("theme-card--active", card.dataset.theme === currentTheme);
        }
      });
    };

    // 模态框开关
    const showModal = () => {
      const sidebar = document.getElementById("sidebar");
      if (sidebar && sidebar.style.display === "flex") {
        document.querySelector(".overlay")?.click();
      }
      refreshCardHighlight();
      themeModal.show();
    };

    const hideModal = () => themeModal.hide();

    // 渲染主题卡片
    const renderThemeCards = () => {
      const isSystem = !localStorage.getItem("theme");

      const systemCard = `
        <div class="theme-card${isSystem ? " theme-card--active" : ""}" data-theme="system" role="button" tabindex="0" aria-label="跟随系统">
          <div class="theme-card__swatch theme-card__swatch--system" aria-hidden="true">
            <i class="fa fa-desktop" aria-hidden="true"></i>
          </div>
          <span class="theme-card__name">跟随系统</span>
          <div class="theme-card__status" aria-hidden="true"><i class="fa fa-check"></i></div>
        </div>
      `;

      const cardsHtml = Object.entries(this.themes).map(([key, theme]) => {
        const swatchPrimary = theme.swatch?.primary || "transparent";
        const swatchSecondary = theme.swatch?.secondary || "transparent";
        const swatchTertiary = theme.swatch?.tertiary || "transparent";
        const isActive = !isSystem && key === getValidTheme(localStorage.getItem("theme"));

        return `
          <div class="theme-card${isActive ? " theme-card--active" : ""}" data-theme="${key}" role="button" tabindex="0" aria-label="切换到${key}">
            <div class="theme-card__swatch" aria-hidden="true">
              <div class="theme-card__swatch-primary" style="background: ${swatchPrimary};"></div>
              <div class="theme-card__swatch-secondary" style="background: ${swatchSecondary};"></div>
              <div class="theme-card__swatch-tertiary" style="background: ${swatchTertiary};"></div>
            </div>
            <span class="theme-card__name">${key}</span>
            <div class="theme-card__status" aria-hidden="true"><i class="fa fa-check"></i></div>
          </div>
        `;
      }).join("");

      grid.innerHTML = systemCard + cardsHtml;

      grid.addEventListener("click", (e) => {
        const card = e.target.closest(".theme-card");
        if (!card) return;
        const theme = card.dataset.theme;
        if (!theme) return;

        if (theme === "system") {
          localStorage.removeItem("theme");
          applyTheme(getValidTheme(null));
          hideModal();
          this.showAlert("green", '<i class="fa fa-laptop"></i>&nbsp;已跟随系统主题');
        } else {
          if (!this.themes[theme]) return;
          setTheme(theme);
          hideModal();
          this.showAlert("green", `<i class="fa fa-check-circle-o"></i>&nbsp;已切换到${theme}！`);
        }
      });
    };

    // --- 初始化 ---
    initTheme();
    renderThemeCards();

    systemThemeMedia.addEventListener("change", handleSystemThemeChange);
    this.addCleanTask(() => systemThemeMedia.removeEventListener("change", handleSystemThemeChange));

    toggleBtn.addEventListener("click", showModal);
    closeBtn.addEventListener("click", hideModal);
  }

  // ========== 回到顶部 ==========
  initBackToTop() {
    const backToTopBtn = document.getElementById("back-to-top");
    if (!backToTopBtn) return;

    backToTopBtn.addEventListener("click", () => {
      this.showAlert("green", "<i class=\"fa fa-hand-pointer-o\" aria-hidden=\"true\"></i>&nbsp;Go! Go! Go! 正在返回顶部！");
      window.scrollTo({ top: 0, behavior: "smooth" });
    });

    const handleScroll = () => {
      backToTopBtn.style.visibility = window.scrollY > 0 ? "visible" : "hidden";
    };

    window.addEventListener("scroll", handleScroll);
    handleScroll();
    this.addCleanTask(() => window.removeEventListener("scroll", handleScroll));
  }

  // ========== 侧边栏 ==========
  initSidebar() {
    const overlay = document.querySelector(".overlay");
    const sidebar = document.getElementById("sidebar");
    const sidebarToggle = document.getElementById("sidebar-toggle");
    const sidebarClose = document.getElementById("sidebar-close");
    if (!overlay || !sidebar || !sidebarToggle || !sidebarClose) return;

    const showSidebar = () => {
      sidebar.style.animation = "none";
      overlay.style.animation = "none";
      void overlay.offsetHeight;
      sidebar.style.animation = "showSidebarAnimation 0.5s forwards";
      overlay.style.animation = "showOverlayAnimation 0.5s forwards";
      overlay.style.display = "block";
      sidebar.style.display = "flex";
      this.body.style.overflow = "hidden";
    };

    const hideSidebar = () => {
      sidebar.style.animation = "none";
      overlay.style.animation = "none";
      void overlay.offsetHeight;
      sidebar.style.animation = "hideSidebarAnimation 0.5s forwards";
      overlay.style.animation = "hideOverlayAnimation 0.5s forwards";
      setTimeout(() => {
        overlay.style.display = "none";
        this.body.style.overflow = "auto";
      }, 500);
    };

    overlay.addEventListener("click", hideSidebar);
    sidebar.addEventListener("click", (e) => e.stopPropagation());
    sidebarToggle.addEventListener("click", showSidebar);
    sidebarClose.addEventListener("click", hideSidebar);
  }

  // ========== 网页标题 ==========
  initWebTitle() {
    const blogName = this.blogConfig.blogInfo.blogName;
    const webTitleNormalList = [
      `${blogName} | 记录代码与生活`,
      `${blogName} | 技术成长分享站`,
      `${blogName} | 0和1里的小世界`,
      `${blogName} | 程序员的日常碎碎念`,
      `${blogName} | 探索技术，记录成长`
    ];
    const webTitleAwayList = [
      `${blogName} | 等你回来继续逛呀~`,
      `${blogName} | 页面已后台待命`,
      `${blogName} | 别走远，我在这儿等你`,
      `${blogName} | 正在后台加载想念模式`,
      `${blogName} | 快回来，代码还没写完呢`
    ];
    const webTitleWelcomeList = [
      `${blogName} | 欢迎回来！继续探索~`,
      `${blogName} | 好久不见，欢迎回家`,
      `${blogName} | 你终于回来啦！`,
      `${blogName} | 回来啦？我们接着逛`,
      `${blogName} | 欢迎回来，灵感已就位`
    ];

    const webTitleSwitchInterval = 5000;
    let webTitleIntervalId = null;

    const getRandomTitle = (list) => list[Math.floor(Math.random() * list.length)];

    const switchWebTitle = (list) => {
      clearInterval(webTitleIntervalId);
      document.title = getRandomTitle(list);
      webTitleIntervalId = setInterval(() => {
        document.title = getRandomTitle(list);
      }, webTitleSwitchInterval);
    };

    this.addCleanTask(() => clearInterval(webTitleIntervalId));

    document.addEventListener("visibilitychange", () => {
      if (document.hidden) {
        switchWebTitle(webTitleAwayList);
      } else {
        switchWebTitle(webTitleWelcomeList);
        setTimeout(() => switchWebTitle(webTitleNormalList), webTitleSwitchInterval);
      }
    });

    switchWebTitle(webTitleNormalList);
  }

  // ========== 代码复制 ==========
  initCopyButtons() {
    document.addEventListener("click", async (e) => {
      const copyBtn = e.target.closest(".article-content__copy-btn");
      if (!copyBtn) return;

      try {
        const code = copyBtn.parentElement.querySelector("code")?.textContent;
        if (!code) return this.showAlert("orange", "<i class=\"fa fa-warning\" aria-hidden=\"true\"></i>&nbsp;未找到可复制的代码内容！");
        await navigator.clipboard.writeText(code);
        this.showAlert("green", "<i class=\"fa fa-check-square-o\" aria-hidden=\"true\"></i>&nbsp;复制成功！");
      } catch (error) {
        console.error("复制失败：", error);
        this.showAlert("red", "<i class=\"fa fa-times-circle-o\" aria-hidden=\"true\"></i>&nbsp;复制失败，请重试！");
      }
    });
  }

  // ========== 导航栏背景 ==========
  initHeaderBackground() {
    const heroDiv = document.querySelector(".hero");
    if (!heroDiv) return;
    const header = document.getElementById("page-header");

    const handleScroll = this.throttle(() => {
      const navHeight = this.setNavHeightVariable();
      header.style.background = window.scrollY > (navHeight * 2) ? "none" : "var(--hero-bg-color)";
    });

    handleScroll();

    window.addEventListener("scroll", handleScroll);
    this.addCleanTask(() => window.removeEventListener("scroll", handleScroll));
  }

  // ========== 标签管理 ==========
  initTagManager() {
    document.addEventListener("click", (e) => {
      const tagElement = e.target.closest(".article-tag__item");
      if (tagElement) {
        e.preventDefault();
        const tagText = tagElement.querySelector("span")?.textContent;
        if (tagText) this.navigateToTagPage(tagText);
      }
    });
  }

  addTagToPages() {
    if (!document.getElementById("tags-wrapper")) return;

    const tagCloud = document.querySelector(".tag-cloud");

    const tagList = [];

    Object.entries(this.pagesConfig.tagsArticleTotal).forEach(([tagName, tagInArticleTotal]) => {
      tagList.push(`
        <li>
          <a href="#" onclick="window.qingBlogInstance.navigation('/tags/${tagName}/')" class="tag-cloud__item">
            <span class="tag-cloud__name">${tagName}</span>
            <span class="tag-cloud__count">${tagInArticleTotal}</span>
          </a>
        </li>`)
    })

    tagCloud.innerHTML = tagList.join("");
  }

  navigateToTagPage(tagText) {
    this.navigation(`/tags/${encodeURIComponent(tagText)}/`);
  }

  // ========== 分页 ==========
  initPagination() {
    const prevTrigger = document.getElementById("prev-trigger");
    const nextTrigger = document.getElementById("next-trigger");
    const goToPageBtn = document.getElementById("go-to-page-btn");
    const pageNum = document.getElementById("page-num");
    const inputPageNum = document.getElementById("input-page-num");
    if (!prevTrigger || !nextTrigger || !pageNum) return;

    const path = window.location.pathname;
    const isTagPage = path.startsWith("/tags/");
    let current = 1;
    let maxPageNum = this.pagesConfig.maxPageNum.maxArticlePageNum;
    let tagName = '';

    if (isTagPage) {
      const pathParts = path.split("/").filter(Boolean);
      if (pathParts.length > 1) {
        tagName = decodeURIComponent(pathParts[1]);
        if (pathParts.length > 2) {
          const pagePart = pathParts[2].replace(".html", "");
          const pageVal = parseInt(pagePart, 10);
          current = !Number.isNaN(pageVal) && pageVal > 0 ? pageVal : 1;
        }
        maxPageNum = this.pagesConfig.maxPageNum.maxTagPageNums[tagName] || 1;
      }
    } else {
      if (path.includes("/pages/")) {
        const parts = path.split("/pages/");
        if (parts.length > 1) {
          const pagePart = parts[1].replace(".html", "");
          const pageVal = parseInt(pagePart, 10);
          current = !Number.isNaN(pageVal) && pageVal > 0 ? pageVal : 1;
        }
      }
    }

    const goToPage = (page) => {
      this.navigation(isTagPage
        ? (page === 1 ? `/tags/${encodeURIComponent(tagName)}/` : `/tags/${encodeURIComponent(tagName)}/${page}.html`)
        : (page === 1 ? `/` : `/pages/${page}.html`));
    };

    const updatePageDisplay = () => {
      pageNum.textContent = `${current} / ${maxPageNum}`;
    };

    updatePageDisplay();

    prevTrigger.addEventListener("click", () => {
      if (current <= 1) return this.showAlert("red", "<i class=\"fa fa-warning\" aria-hidden=\"true\"></i>&nbsp;已经到第一页了！");
      goToPage(current - 1);
    });

    nextTrigger.addEventListener("click", () => {
      if (current >= maxPageNum) return this.showAlert("red", "<i class=\"fa fa-warning\" aria-hidden=\"true\"></i>&nbsp;已经到最后一页了！");
      goToPage(current + 1);
    });

    goToPageBtn?.addEventListener("click", () => {
      if (!inputPageNum) return;
      const target = parseInt(inputPageNum.value.trim(), 10);
      if (Number.isNaN(target)) return this.showAlert("red", "<i class=\"fa fa-warning\" aria-hidden=\"true\"></i>&nbsp;请输入有效的页码！");
      if (target < 1 || target > maxPageNum) return this.showAlert("red", "<i class=\"fa fa-warning\" aria-hidden=\"true\"></i>&nbsp;页码超出范围！");
      goToPage(target);
    });

    inputPageNum?.addEventListener("keypress", (e) => {
      if (e.key === "Enter") goToPageBtn?.click();
    });

    if (current <= 1) {
      prevTrigger.classList.add("disabled");
      prevTrigger.style.cursor = "not-allowed";
    }
    if (current >= maxPageNum) {
      nextTrigger.classList.add("disabled");
      nextTrigger.style.cursor = "not-allowed";
    }
  }

  // ========== 卡片动画 ==========
  initCardScrollAnimation() {
    const cards = document.querySelectorAll('.card');
    if (!cards.length) return;

    if (location.pathname.includes('/article')) {
      cards.forEach(c => c.classList.add('card--visible'));
      return;
    }

    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (!entry.isIntersecting) return;
        entry.target.classList.add('card--visible');
        observer.unobserve(entry.target);
      });
    });

    cards.forEach(card => observer.observe(card));
    this.addCleanTask(() => observer.disconnect());
  }

  // ========== 图片懒加载 ==========
  initLazyLoadImages() {
    document.querySelectorAll('img:not([loading])').forEach(img => img.loading = 'lazy');
  }

  // ========== 文章数据图表生成 ==========
  initArticleData() {
    const chartDoms = document.querySelectorAll(".data-chart__pie");
    if (!chartDoms.length) return;

    if (typeof echarts === 'undefined') {
      console.warn('Echarts 未加载！');
      return;
    }

    const roseData = [];
    Object.entries(this.pagesConfig.tagsArticleTotal).forEach(([name, value]) => {
      roseData.push({ name, value });
    });

    const option = {
      tooltip: {
        trigger: 'item',
        backgroundColor: 'rgba(20, 20, 20, 0.7)',
        textStyle: { color: '#fff' },
        borderRadius: 10,
        fontFamily: '江城圆体, 阿里妈妈方圆体, sans-serif',
        formatter: '{b}: {c} 篇文章'
      },
      legend: {
        orient: 'horizontal',
        left: 'center',
        bottom: 'bottom'
      },
      series: [
        {
          type: 'pie',
          radius: ['20%', '60%'],
          center: ['50%', '45%'],
          padAngle: 4,
          itemStyle: {
            borderRadius: 16,
            borderColor: 'rgba(255,255,255,0.2)',
            borderWidth: 2,
            opacity: 0.8
          },
          label: {
            show: true,
            fontSize: 14,
            formatter: '{b} {d} %'
          },
          emphasis: {
            scale: true,
            scaleSize: 15
          },
          data: roseData
        }
      ]
    };

    chartDoms.forEach((chartDom) => {
      const chart = echarts.init(chartDom);
      chart.setOption(option);

      const resizeObserver = this.debounce(() => chart.resize());
      window.addEventListener('resize', resizeObserver);
      this.addCleanTask(() => {
        window.removeEventListener('resize', resizeObserver);
        chart.dispose();
      });
    });
  }

  // ========== 关于图表生成 ==========
  initMeData() {
    const chartDoms = document.querySelectorAll(".about-card__chart");
    if (!chartDoms.length) return;

    if (typeof echarts === 'undefined') {
      console.warn('Echarts 未加载！');
      return;
    }

    const roseData = [];
    Object.entries(this.blogConfig.author.authorTags).forEach(([name, value]) => {
      roseData.push({ name, value });
    });

    const colorList = [
      '#7C3AED', '#A78BFA', '#C4B5FD',
      '#0EA5E9', '#38BDF8', '#7DD3FC',
      '#14B8A6', '#5EEAD4', '#99F6E4',
      '#F59E0B', '#FCD34D', '#FDE68A'
    ];

    const option = {
      tooltip: {
        backgroundColor: 'rgba(20, 20, 20, 0.7)',
        textStyle: { color: '#fff', fontSize: 14 },
        padding: [6, 10],
        borderRadius: 6
      },
      series: [
        {
          type: 'wordCloud',
          shape: 'rect',
          gridSize: 10,
          sizeRange: [16, 48],
          rotationRange: [0, 0],
          textStyle: {
            color() {
              return colorList[Math.floor(Math.random() * colorList.length)];
            },
            fontWeight: 'bold',
            fontFamily: '江城圆体, 阿里妈妈方圆体, sans-serif'
          },
          emphasis: {
            textStyle: {
              shadowBlur: 10,
              shadowColor: '#fff'
            }
          },
          data: roseData,
        },
      ],
    };

    chartDoms.forEach((chartDom) => {
      const chart = echarts.init(chartDom);
      chart.setOption(option);

      const resizeObserver = this.debounce(() => chart.resize());
      window.addEventListener('resize', resizeObserver);
      this.addCleanTask(() => {
        window.removeEventListener('resize', resizeObserver);
        chart.dispose();
      });
    });
  }

  addAboutCard() {
    const cards = document.querySelectorAll(".about-card__wrapper");
    if (!cards.length) return;

    const { author, blogInfo } = this.blogConfig;

    cards.forEach((card) => {
      const authorText = card.querySelector(".about-card__author-text");
      authorText.querySelector("h3").textContent = author.targetAuthor;
      authorText.querySelector("p").textContent = author.introShort;

      card.querySelector(".about-card__desc p").textContent = author.introDetail;

      Object.entries(author.socialMediaPlatform).forEach(([name, { icon, url }]) => {
        card.querySelector(".card__footer").insertAdjacentHTML("afterbegin", `<a href="${url}" class="about-card__social-item" target="_blank">${icon}&nbsp;${name}</a>`);
      });

      card.querySelector(".card__footer").insertAdjacentHTML("beforeend", `<p>写作年限：${blogInfo.yearOfWriting} – ${blogInfo.currentYear}</p>`);
    });
  }

  // ========== 友情链接 ==========
  initFriendLinks() {
    const friendLinksDom = document.querySelector(".friend-links__grid");

    if (!friendLinksDom || !this.blogConfig.friendLinks) return;

    const friendLinksHtml = [];

    this.blogConfig.friendLinks.forEach((link) => {
      friendLinksHtml.push(`
        <div>
          <a href="${link.url}" target="_blank" rel="noopener noreferrer" class="friend-links__card">
            <div class="friend-links__card-icon" aria-hidden="true">
              ${link.icon}
            </div>
            <div class="friend-links__card-info">
              <h3 class="friend-links__card-name">${link.name}</h3>
              <p class="friend-links__card-desc">${link.description}</p>
            </div>
            <span class="sr-only">新窗口打开</span>
          </a>
        </div>
        `);
    });

    friendLinksDom.innerHTML = friendLinksHtml.join('');
  }

  getAbsolutePath(href) {
    const webHost = location.host;
    const repositoryName = this.blogConfig.blogInfo.repositoryName;

    if (!href) throw new Error("未传入参数！");

    if (repositoryName === webHost) {
      return href;
    } else {
      return `${repositoryName}${href}`;
    }
  }

  navigation(href) {
    if (!href) throw new Error("未传入参数，请传入如/pages的参数！");

    const base = this.getAbsolutePath(href);
    // 页面间跳转添加 skipLoading 参数，使目标页跳过加载动画
    location.href = base + (base.includes("?") ? "&" : "?") + "skipLoading=true";
  }

}

// ========== 可复用模态框组件 ==========
class Modal {
  constructor(overlay, panel, { panelShowAnim = "showThemeModalAnimation", panelHideAnim = "hideThemeModalAnimation" } = {}) {
    this.overlay = overlay;
    this.panel = panel;
    this.panelShowAnim = panelShowAnim;
    this.panelHideAnim = panelHideAnim;
    this._isOpen = false;
    this._duration = 400;

    overlay.addEventListener("click", () => this.hide());
    panel.addEventListener("click", (e) => e.stopPropagation());
    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape" && this._isOpen) this.hide();
    });
  }

  show() {
    if (this._isOpen) return;
    this._isOpen = true;

    this.overlay.style.animation = "none";
    this.panel.style.animation = "none";
    void this.overlay.offsetHeight;

    this.overlay.style.display = "block";
    this.panel.style.display = "flex";
    this.overlay.style.animation = `showOverlayAnimation ${this._duration}ms forwards`;
    this.panel.style.animation = `${this.panelShowAnim} ${this._duration}ms cubic-bezier(0.0, 0.0, 0.2, 1) forwards`;
    document.body.style.overflow = "hidden";
  }

  hide() {
    if (!this._isOpen) return;

    this.overlay.style.animation = "none";
    this.panel.style.animation = "none";
    void this.overlay.offsetHeight;
    this.overlay.style.animation = `hideOverlayAnimation ${this._duration}ms forwards`;
    this.panel.style.animation = `${this.panelHideAnim} ${this._duration}ms cubic-bezier(0.4, 0, 0.2, 1) forwards`;
    setTimeout(() => {
      this.overlay.style.display = "none";
      this.panel.style.display = "none";
      document.body.style.overflow = "auto";
      this._isOpen = false;
    }, this._duration);
  }
}

// ========== 初始化实例 ==========
// 挂载到全局供HTML内联事件调用
window.qingBlogInstance = new QingBlog();
// DOM加载完成后初始化
window.addEventListener("DOMContentLoaded", () => window.qingBlogInstance.init());
