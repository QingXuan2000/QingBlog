// 变量设置

const blogConfig = {
  maxPageNum: {
    maxArticlePageNum: 1,
    maxTagPageNums: {

    }
  }
};

// 主题设置
const themes = {
  dark: {
    "--primary-color": "#d9d9deb8",
    "--text-color": "rgba(200, 200, 200, 1)",
    "--text-shadow-color": "rgba(0, 0, 0, 0.5)",
    "--text-secondary-color": "rgba(160, 160, 160, 1)",
    "--bg-color": "linear-gradient(180deg, rgba(20, 20, 20, 1), rgba(15, 15, 15, 1), rgba(10, 10, 10, 1), rgba(5, 5, 5, 1))",
    "--hero-bg-color": "rgba(10, 10, 10, 1)",
    "--surface-color": "linear-gradient(rgba(40, 40, 40, 0.6), transparent)",
    "--surface-border-color": "rgba(255, 255, 255, 0.1)",
    "--border-color": "rgba(255, 255, 255, 0.1)",
    "--box-shadow-color": "rgba(0, 0, 0, 0.5)",
    "--divider-color": "rgba(255, 255, 255, 0.15)",
    "--backdrop-blur": "blur(0.6em)",
  },
  light: {
    "--primary-color": "#2c2c2db8",
    "--text-color": "rgba(44, 44, 44, 1)",
    "--text-shadow-color": "rgba(144, 144, 144, 1)",
    "--text-secondary-color": "rgba(85, 85, 85, 1)",
    "--bg-color": "linear-gradient(180deg, rgba(233, 233, 237, 1), rgba(224, 225, 228, 1), rgba(220, 220, 220, 1), rgba(215, 213, 213, 1))",
    "--hero-bg-color": "rgba(217, 218, 220, 1)",
    "--surface-color": "linear-gradient(rgba(240, 240, 240, 0.4), transparent)",
    "--surface-border-color": "rgba(255, 255, 255, 0.1)",
    "--border-color": "rgba(255, 255, 255, 0.1)",
    "--box-shadow-color": "rgba(0, 0, 0, 0.2)",
    "--divider-color": "rgba(0, 0, 0, 0.3)",
    "--backdrop-blur": "blur(0.6em)",
  },
};

// 组件库
const componentBox = `
    <!-- -------------------- 加载动画 -------------------- -->

    <div class="loading">
        <div class="loading-icon">
            <svg class="loading-logo" width="620" height="620" viewBox="0 0 620 620" fill="none"
                xmlns="http://www.w3.org/2000/svg">
                <circle class="qingblog-loading-icon-circle" cx="310" cy="310" r="250" />
                <circle class="qingblog-loading-icon-circle" cx="310" cy="310" r="300" />
                <path class="qingblog-loading-icon" d="M315 70L315 550" />
                <line class="qingblog-loading-icon" x1="124" y1="213" x2="264" y2="213" />
                <line class="qingblog-loading-icon" x1="104" y1="310" x2="284" y2="310" />
                <line class="qingblog-loading-icon" x1="124" y1="407" x2="264" y2="407" />
                <line class="qingblog-loading-icon" x1="365" y1="115" x2="365" y2="245" />
                <line class="qingblog-loading-icon" x1="365" y1="286" x2="365" y2="386" />
                <line class="qingblog-loading-icon" x1="365" y1="427" x2="365" y2="507" />
                <line class="qingblog-loading-icon" x1="423" y1="490" x2="423" y2="380" />
                <line class="qingblog-loading-icon" x1="474" y1="440" x2="474" y2="330" />
                <line class="qingblog-loading-icon" x1="423" y1="345" x2="423" y2="255" />
                <line class="qingblog-loading-icon" x1="423" y1="220" x2="423" y2="140" />
                <line class="qingblog-loading-icon" x1="474" y1="285" x2="474" y2="205" />
            </svg>
        </div>

        <div class="loading-div"></div>
        <div class="loading-div"></div>
    </div>

    <!-- -------------------- 弹窗 -------------------- -->

    <div id="alert">
        <div id="alert-message">
            <span></span>
        </div>
    </div>

    <!-- -------------------- 遮罩层 -------------------- -->

    <div class="overlay"></div>

    <!-- -------------------- 右键菜单 -------------------- -->

    <div id="context-menu" class="context-menu">
        <ul>
            <li onclick="initContextMenu('copy')">
                <i class="fa fa-copy"></i> 复制
            </li>
            <li class="divider"></li>
            <li onclick="initContextMenu('refresh')">
                <i class="fa fa-refresh"></i>&nbsp;<span>刷新</span>
            </li>
        </ul>
    </div>

    <!-- -------------------- 返回顶部 -------------------- -->

    <div id="back-to-top" class="glass btn-active">
        <i class="fa fa-chevron-up"></i>
    </div>

    <!-- -------------------- 头部导航栏 -------------------- -->

    <header>
        <nav id="navbar" class="glass">
            <svg class="loading-logo" width="35" height="35" viewBox="0 0 620 620" fill="none"
                xmlns="http://www.w3.org/2000/svg">
                <circle class="qingblog-loading-icon-circle" cx="310" cy="310" r="250" />
                <circle class="qingblog-loading-icon-circle" cx="310" cy="310" r="300" />
                <path class="qingblog-loading-icon" d="M315 70L315 550" />
                <line class="qingblog-loading-icon" x1="124" y1="213" x2="264" y2="213" />
                <line class="qingblog-loading-icon" x1="104" y1="310" x2="284" y2="310" />
                <line class="qingblog-loading-icon" x1="124" y1="407" x2="264" y2="407" />
                <line class="qingblog-loading-icon" x1="365" y1="115" x2="365" y2="245" />
                <line class="qingblog-loading-icon" x1="365" y1="286" x2="365" y2="386" />
                <line class="qingblog-loading-icon" x1="365" y1="427" x2="365" y2="507" />
                <line class="qingblog-loading-icon" x1="423" y1="490" x2="423" y2="380" />
                <line class="qingblog-loading-icon" x1="474" y1="440" x2="474" y2="330" />
                <line class="qingblog-loading-icon" x1="423" y1="345" x2="423" y2="255" />
                <line class="qingblog-loading-icon" x1="423" y1="220" x2="423" y2="140" />
                <line class="qingblog-loading-icon" x1="474" y1="285" x2="474" y2="205" />
            </svg>
            <h1>QingBlog</h1>

            <div class="divider" style="width: 2px; margin: 0 0.5rem 0 1rem; border-radius: 100em;"></div>

            <ul>
                <li>
                    <a href="/"><i class="fa fa-home" aria-hidden="true"></i>&nbsp;首页</a>
                </li>

                <li>
                    <a href="/article/"><i class="fa fa-book" aria-hidden="true"></i>&nbsp;文章</a>
                </li>

                <li>
                    <a href="/tags/"><i class="fa fa-tags" aria-hidden="true"></i>&nbsp;标签</a>
                </li>

                <li>
                    <a target="_blank" href="https://github.com/QingXuan2000"><i class="fa fa-github-square"
                            aria-hidden="true"></i>&nbsp;GitHub</a>
                </li>
            </ul>
        </nav>

        <div id="theme-toggle" class="nav-button btn-active">
            <i class="fa fa-sun-o"></i>
        </div>

        <div id="sidebar-toggle" class="nav-button btn-active">
            <i class="fa fa-bars" aria-hidden="true"></i>
        </div>
    </header>

    <!-- -------------------- 侧边栏 -------------------- -->

    <div id="sidebar">
        <div id="sidebar-close" class="nav-button btn-active">
            <i class="fa fa-remove" aria-hidden="true"></i>
        </div>

        <div class="user-info">
            <img src="/img/Avatar.png" alt="Avatar" />
            <h1>QingXuanJun</h1>
        </div>

        <nav>
            <ul class="glass">
                <li>
                    <a href="/"><i class="fa fa-home" aria-hidden="true"></i>&nbsp;首页</a>
                </li>

                <div class="divider" style="width: 100%; height: 1px;"></div>

                <li>
                    <a href="/article/"><i class="fa fa-book" aria-hidden="true"></i>&nbsp;文章</a>
                </li>

                <div class="divider" style="width: 100%; height: 1px;"></div>

                <li>
                    <a href="/tags/"><i class="fa fa-tags" aria-hidden="true"></i>&nbsp;标签</a>
                </li>

                <div class="divider" style="width: 100%; height: 1px;"></div>

                <li>
                    <a target="_blank" href="https://github.com/QingXuan2000"><i class="fa fa-github-square"
                            aria-hidden="true"></i>&nbsp;GitHub</a>
                </li>
            </ul>
        </nav>
    </div>
`;

document.querySelector("body").insertAdjacentHTML("afterbegin", componentBox);

// 标题切换
function initWebTitle() {
  const webTitleNormalList = [
    "QingBlog - QingXuanJun的个人博客 💻",
    "QingBlog - 欢迎来到QingXuanJun的个人博客哦~ 🎉",
    "QingBlog - 欢迎来到一位技术宅的Blog 🤓",
    "QingBlog - 这里是QingXuanJun独一无二的小站哦！⭐",
    "QingBlog - 代码、生活与碎碎念 ✨📝",
    "QingBlog - 一个喜欢折腾的极客空间 🛠️⚡",
    "QingBlog - 记录成长，分享热爱 📖❤️",
    "QingBlog - 在0和1的世界里寻找浪漫 💾🌹",
    "QingBlog - 今日份灵感已加载完毕 🚀💡",
    "QingBlog - 探索技术，也探索生活 🔍🌿"
  ];

  const webTitleAwayList = [
    "QingBlog - (｡•́︿•̀｡) 你怎么走掉了啦~",
    "QingBlog - 哼！再不回来看我就不理你了！💢",
    "QingBlog - 快回来嘛，我一个人好无聊QAQ 🥺",
    "QingBlog - 去忙吧，记得回来看看我哦 👋💕",
    "QingBlog - while(true) { await you.comeBack(); } ⏳",
    "QingBlog - console.log(\"用户离开了，悲伤.jpg\") 😭",
    "QingBlog - 404 Not Found: 用户已离线 🔌",
    "QingBlog - // TODO: 用户快回来继续逛博客 📝",
    "QingBlog - 无论你走多远，这里永远亮着灯 💡🏠",
    "QingBlog - 累了就回来歇歇脚吧~ ☕🛋️"
  ];

  const webTitleWelcomeList = [
    "QingBlog - 你终于回来啦！✨",
    "QingBlog - 欢迎回来！等你好久了~ 🎉",
    "QingBlog - 呀！你回来啦！(◕‿◕)♡",
    "QingBlog - 好久不见，甚是想念！💕",
    "QingBlog - 哼，还知道回来呀~ 😤",
    "QingBlog - 你去哪儿玩了，不带我！🥺",
    "QingBlog - 欢迎回家！我乖不乖~ 🐱",
    "QingBlog - 你不在的时候我有好好看家哦！⭐",
    "QingBlog - 200 OK: 用户已回归 🟢",
    "QingBlog - console.log(\"用户回来了，开心！\")",
    "QingBlog - await user.comeBack() // resolved ✓",
    "QingBlog - git pull origin user-back 🎊",
    "QingBlog - 回来就好，休息一下吧~ ☕",
    "QingBlog - 这里永远为你亮着灯 💡",
    "QingBlog - 欢迎回来，继续我们的故事 📖",
    "QingBlog - 累了就歇会儿，我陪你 🛋️"
  ];

  const webTitleSwitchInterval = 5000;
  let webTitleIntervalId;

  const getRandomTitle = (list) => list[Math.floor(Math.random() * list.length)];

  const switchWebTitle = (list) => {
    clearInterval(webTitleIntervalId);
    document.title = getRandomTitle(list);
    webTitleIntervalId = setInterval(() => {
      document.title = getRandomTitle(list);
    }, webTitleSwitchInterval);
  };

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

// 弹窗相关功能
function playAlertAnimation() {
  const alertMessage = document.getElementById("alert-message");
  if (!alertMessage) return;

  alertMessage.style.animation = "none";
  alertMessage.offsetHeight;
  alertMessage.style.animation = "alertAnimation 2.2s normal forwards";
}

const alertColors = {
  green: {
    bg: "rgba(34, 197, 94, 0.3)",
    border: "1px solid rgba(34, 197, 94, 0.4)",
    shadow: "0 0 20px rgba(34, 197, 94, 0.2), inset 0 0 10px rgba(34, 197, 94, 0.05)"
  },
  red: {
    bg: "rgba(239, 68, 68, 0.3)",
    border: "1px solid rgba(239, 68, 68, 0.4)",
    shadow: "0 0 20px rgba(239, 68, 68, 0.2), inset 0 0 10px rgba(239, 68, 68, 0.05)"
  },
  orange: {
    bg: "rgba(249, 115, 22, 0.3)",
    border: "1px solid rgba(249, 115, 22, 0.4)",
    shadow: "0 0 20px rgba(249, 115, 22, 0.2), inset 0 0 10px rgba(249, 115, 22, 0.05)"
  },
  yellow: {
    bg: "rgba(234, 179, 8, 0.3)",
    border: "1px solid rgba(234, 179, 8, 0.4)",
    shadow: "0 0 20px rgba(234, 179, 8, 0.2), inset 0 0 10px rgba(234, 179, 8, 0.05)"
  }
};

function showAlert(color, message) {
  const alertMessage = document.getElementById("alert-message");
  if (!alertMessage) return;

  alertMessage.querySelector("span").innerHTML = message;
  const style = alertColors[color];
  if (style) {
    alertMessage.style.background = style.bg;
    alertMessage.style.border = style.border;
    alertMessage.style.boxShadow = style.shadow;
    playAlertAnimation();
  }
}

// 初始化返回顶部按钮
function initBackToTop() {
  const backToTopBtn = document.getElementById("back-to-top");
  if (!backToTopBtn) return;

  backToTopBtn.addEventListener("click", () => {
    showAlert("green", "<i class=\"fa fa-hand-pointer-o\" aria-hidden=\"true\"></i>&nbsp;Go! Go! Go! 正在返回顶部！");
    window.scrollTo({ top: 0, behavior: "smooth" });
  });

  window.addEventListener("scroll", () => {
    backToTopBtn.style.visibility = window.scrollY > 0 ? "visible" : "hidden";
  });
}

// 侧边栏相关功能
function initSidebar() {
  const body = document.querySelector("body");
  const overlay = document.querySelector(".overlay");
  const sidebar = document.getElementById("sidebar");
  const sidebarToggle = document.getElementById("sidebar-toggle");
  const sidebarClose = document.getElementById("sidebar-close");

  if (!overlay || !sidebar || !sidebarToggle || !sidebarClose) return;

  const showSidebar = () => {
    sidebar.style.animation = "none";
    overlay.style.animation = "none";
    overlay.offsetHeight;
    sidebar.style.animation = "showSidebarAnimation 0.5s forwards";
    overlay.style.animation = "showOverlayAnimation 0.5s forwards";
    overlay.style.display = "block";
    sidebar.style.display = "flex";
    body.style.overflow = "hidden";
  };

  const hideSidebar = () => {
    sidebar.style.animation = "none";
    overlay.style.animation = "none";
    overlay.offsetHeight;
    sidebar.style.animation = "hideSidebarAnimation 0.5s forwards";
    overlay.style.animation = "hideOverlayAnimation 0.5s forwards";
    setTimeout(() => {
      overlay.style.display = "none";
      body.style.overflow = "auto";
    }, 500);
  };

  overlay.addEventListener("click", hideSidebar);
  sidebar.addEventListener("click", (e) => e.stopPropagation());
  sidebarToggle.addEventListener("click", showSidebar);
  sidebarClose.addEventListener("click", hideSidebar);
}

// 设置高度变量
function setNavHeightVariable() {
  const nav = document.getElementById("navbar");
  if (nav) {
    const height = nav.offsetHeight;
    document.documentElement.style.setProperty("--nav-height", `${height}px`);
    return height;
  }
}

// 初始化加载动画
function initLoadingAnimation() {
  const firstLoading = localStorage.getItem("firstLoading") || "true";
  const loadingContainer = document.querySelector(".loading");

  if (!loadingContainer) return;

  if (firstLoading !== "false") {
    const body = document.body;
    const qingBlogIcon = document.querySelector(".loading-icon");
    const loadingDivs = document.querySelectorAll(".loading-div");

    body.style.overflow = "hidden";

    setTimeout(() => {
      loadingDivs.forEach((div, index) => {
        div.style.animation = (index + 1) % 2 === 0
          ? "loadingRightAnimation 1.5s ease-out forwards"
          : "loadingLeftAnimation 1.5s ease-out forwards";
      });
      qingBlogIcon.style.animation = "hideOverlayAnimation 0.5s ease-in-out forwards";
    }, 1600);

    setTimeout(() => {
      loadingContainer.style.display = "none";
      body.style.overflow = "auto";
      localStorage.setItem("firstLoading", "false");
    }, 3000);
  } else {
    loadingContainer.style.display = "none";
  }
}

// 主题切换
function toggleTheme() {
  const toggleBtn = document.getElementById("theme-toggle");
  const prefersColorScheme = matchMedia("(prefers-color-scheme: dark)").matches;
  const root = document.documentElement;

  const applyTheme = (theme) => {
    const themeConfig = themes[theme];
    Object.entries(themeConfig).forEach(([key, value]) => {
      root.style.setProperty(key, value);
    });
  };

  const getThemeIcon = (theme) => theme === "dark" ? "moon" : "sun";

  const setTheme = (theme) => {
    applyTheme(theme);
    localStorage.setItem("theme", theme);
    toggleBtn.innerHTML = `<i class="fa fa-${getThemeIcon(theme)}-o"></i>`;
  };

  const initTheme = () => {
    const savedTheme = localStorage.getItem("theme");
    if (!savedTheme) {
      const defaultTheme = prefersColorScheme ? "dark" : "light";
      applyTheme(defaultTheme);
      toggleBtn.innerHTML = `<i class="fa fa-${getThemeIcon(defaultTheme)}-o"></i>`;
    } else {
      applyTheme(savedTheme);
      toggleBtn.innerHTML = `<i class="fa fa-${getThemeIcon(savedTheme)}-o"></i>`;
    }
  };

  initTheme();

  toggleBtn.addEventListener("click", () => {
    const currentTheme = localStorage.getItem("theme") || (prefersColorScheme ? "dark" : "light");
    const newTheme = currentTheme === "dark" ? "light" : "dark";
    setTheme(newTheme);
    showAlert("green", `<i class="fa fa-${getThemeIcon(newTheme)}-o"></i>&nbsp;已切换到${newTheme === "light" ? "浅色" : "深色"}主题！`);
  });
}

// 初始化复制按钮
function initCopyButtons() {
  document.querySelectorAll(".copy-btn").forEach((copyBtn) => {
    copyBtn.addEventListener("click", async () => {
      const parentElement = copyBtn.parentElement;
      const code = parentElement.querySelector("code").textContent;
      await navigator.clipboard.writeText(code);
      showAlert("green", "<i class=\"fa fa-check-square-o\" aria-hidden=\"true\"></i>&nbsp;复制成功！");
    });
  });
}

// 初始化头部背景
function initHeaderBackground() {
  const heroDiv = document.getElementById("hero-div");
  if (!heroDiv) return;

  const header = document.querySelector("header");
  window.addEventListener("scroll", () => {
    const navHeight = setNavHeightVariable();
    header.style.background = window.scrollY > (navHeight + navHeight) ? "none" : "var(--hero-bg-color)";
  });
}

// 右键菜单
function initContextMenu(option) {
  const menu = document.getElementById("context-menu");

  const showContextMenu = () => {
    menu.style.display = "block";
    menu.classList.add("show");
  };

  const hideContextMenu = () => {
    menu.classList.remove("show");
    setTimeout(() => {
      menu.style.display = "none";
    }, 200);
  };

  document.addEventListener("contextmenu", (e) => {
    e.preventDefault();
    showContextMenu();

    const menuWidth = menu.offsetWidth;
    const menuHeight = menu.offsetHeight;
    const viewportWidth = window.innerWidth;
    const viewportHeight = window.innerHeight;

    let x = e.clientX;
    let y = e.clientY;

    if (x + menuWidth > viewportWidth) {
      x = viewportWidth - menuWidth - 10;
    }

    if (y + menuHeight > viewportHeight) {
      y = viewportHeight - menuHeight - 10;
    }

    menu.style.left = x + "px";
    menu.style.top = y + "px";
    menu.style.visibility = "visible";
  });

  menu.addEventListener("click", (e) => e.stopPropagation());
  document.addEventListener("click", hideContextMenu);

  if (option === "copy") {
    const userSelectedText = window.getSelection().toString();
    navigator.clipboard.writeText(userSelectedText);
    hideContextMenu();
    showAlert("green", "<i class=\"fa fa-check-square-o\" aria-hidden=\"true\"></i>&nbsp;复制成功！");
  } else if (option === "refresh") {
    location.reload(true);
  }
}

// 标签处理模块
const TagManager = {
  init() {
    this.setupTagClickHandler();
  },

  setupTagClickHandler() {
    document.addEventListener("click", (e) => {
      const tagElement = e.target.closest(".tag");
      if (tagElement) {
        e.preventDefault();
        const tagText = tagElement.querySelector("span").textContent;
        TagManager.navigateToTagPage(tagText);
      }
    });
  },

  navigateToTagPage(tagText) {
    location.href = `/tags/${tagText}/`;
  },

  getAllTags() {
    const tags = new Set();
    document.querySelectorAll(".tag span").forEach((tag) => {
      tags.add(tag.textContent);
    });
    return Array.from(tags);
  }
};

function initTagNavigation() {
  TagManager.init();
}

// 分页
function initPagination() {
  const prevTrigger = document.getElementById("prev-trigger");
  const nextTrigger = document.getElementById("next-trigger");
  const goToPageBtn = document.getElementById("go-to-page-btn");
  const pageNum = document.getElementById("page-num");
  const inputPageNum = document.getElementById("input-page-num");

  if (!prevTrigger || !nextTrigger || !pageNum) return;

  const path = window.location.pathname;
  const isTagPage = path.startsWith("/tags/");
  let current = 1;
  let maxPageNum = blogConfig.maxPageNum.maxArticlePageNum;
  let tagName = '';

  if (isTagPage) {
    const pathParts = path.split("/");
    if (pathParts.length > 2) {
      tagName = decodeURIComponent(pathParts[2]);
      
      if (pathParts.length > 3) {
        const pagePart = pathParts[3].replace(".html", "");
        if (pagePart && !isNaN(pagePart)) {
          current = parseInt(pagePart);
        }
      }
      
      maxPageNum = blogConfig.maxPageNum.maxTagPageNums[tagName] || 1;
    }
  } else {
    if (path.includes("/pages/")) {
      const parts = path.split("/pages/");
      if (parts.length > 1) {
        const pagePart = parts[1].replace(".html", "");
        if (pagePart && !isNaN(pagePart)) {
          current = parseInt(pagePart);
        }
      }
    }
  }

  const goToPage = (page) => {
    window.location.href = isTagPage
      ? (page === 1 ? `/tags/${tagName}/` : `/tags/${tagName}/${page}.html`)
      : (page === 1 ? "/" : `/pages/${page}.html`);
  };

  const updatePageDisplay = () => {
    pageNum.textContent = `${current} / ${maxPageNum}`;
  };

  updatePageDisplay();

  prevTrigger.addEventListener("click", () => {
    if (current <= 1) {
      return showAlert("red", "<i class=\"fa fa-warning\" aria-hidden=\"true\"></i>&nbsp;已经到第一页了！");
    }
    goToPage(current - 1);
  });

  nextTrigger.addEventListener("click", () => {
    if (current >= maxPageNum) {
      return showAlert("red", "<i class=\"fa fa-warning\" aria-hidden=\"true\"></i>&nbsp;已经到最后一页了！");
    }
    goToPage(current + 1);
  });

  goToPageBtn?.addEventListener("click", () => {
    if (!inputPageNum) return;
    const target = parseInt(inputPageNum.value.trim());

    if (isNaN(target)) {
      return showAlert("red", "<i class=\"fa fa-warning\" aria-hidden=\"true\"></i>&nbsp;请输入有效的页码！");
    }
    if (target < 1 || target > maxPageNum) {
      return showAlert("red", "<i class=\"fa fa-warning\" aria-hidden=\"true\"></i>&nbsp;页码超出范围！");
    }
    goToPage(target);
  });

  inputPageNum?.addEventListener("keypress", (e) => {
    if (e.key === "Enter") {
      goToPageBtn?.click();
    }
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

// DOM加载完成后初始化所有功能
window.addEventListener("DOMContentLoaded", () => {
  initBackToTop();
  initSidebar();
  initWebTitle();
  setNavHeightVariable();
  toggleTheme();
  initLoadingAnimation();
  initCopyButtons();
  initHeaderBackground();
  initContextMenu();
  initTagNavigation();
  initPagination();
});

// 监听窗口大小变化
window.addEventListener("resize", setNavHeightVariable);
