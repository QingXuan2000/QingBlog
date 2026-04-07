// 主题设置
const themes = {
  dark: {
    '--primary-color': '#d9d9deb8',
    '--text-color': 'rgba(197, 197, 197, 1)',
    '--text-shadow-color': 'rgba(32, 67, 80, 1)',
    '--text-secondary-color': 'rgba(161, 161, 161, 1)',
    '--bg-color': 'linear-gradient(180deg, rgba(10, 18, 28, 1), rgba(11, 21, 26, 1), rgba(8, 16, 24, 1), rgba(4, 7, 12, 1))',
    '--hero-bg-color': 'rgba(8, 16, 24, 1)',
    '--surface-color': 'linear-gradient(rgba(25, 45, 55, 0.4), transparent)',
    '--surface-border-color': 'rgba(245, 245, 245, 0.1)',
    '--border-color': 'rgba(245, 245, 245, 0.1)',
    '--box-shadow-color': 'rgba(0, 0, 0, 0.4)',
    '--divider-color': 'rgba(255, 255, 255, 0.3)',
    '--backdrop-blur': 'blur(0.6em)',
  },
  light: {
    '--primary-color': '#2c2c2db8',
    '--text-color': 'rgba(44, 44, 44, 1)',
    '--text-shadow-color': 'rgba(144, 144, 144, 1)',
    '--text-secondary-color': 'rgba(85, 85, 85, 1)',
    '--bg-color': 'linear-gradient(180deg, rgba(233, 233, 237, 1), rgba(224, 225, 228, 1), rgba(220, 220, 220, 1), rgba(215, 213, 213, 1))',
    '--hero-bg-color': 'rgba(217, 218, 220, 1)',
    '--surface-color': 'linear-gradient(rgba(240, 240, 240, 0.4), transparent)',
    '--surface-border-color': 'rgba(255, 255, 255, 0.1)',
    '--border-color': 'rgba(255, 255, 255, 0.1)',
    '--box-shadow-color': 'rgba(0, 0, 0, 0.2)',
    '--divider-color': 'rgba(0, 0, 0, 0.3)',
    '--backdrop-blur': 'blur(0.6em)',
  },
}

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
            <li onclick="contextMenu('copy')">
                <i class="fa fa-copy"></i> 复制
            </li>
            <li class="divider"></li>
            <li onclick="contextMenu('refresh')">
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
                    <a href="../index.html"><i class="fa fa-home" aria-hidden="true"></i>&nbsp;首页</a>
                </li>

                <li>
                    <a href="../pages/"><i class="fa fa-book" aria-hidden="true"></i>&nbsp;文章</a>
                </li>

                <li>
                    <a href="../tags/"><i class="fa fa-tags" aria-hidden="true"></i>&nbsp;标签</a>
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
            <img src="../img/Avatar.png" alt="Avatar" />
            <h1>QingXuanJun</h1>
        </div>

        <nav>
            <ul class="glass">
                <li>
                    <a href="../index.html"><i class="fa fa-home" aria-hidden="true"></i>&nbsp;首页</a>
                </li>

                <div class="divider" style="width: 100%; height: 1px;"></div>

                <li>
                    <a href="../pages/"><i class="fa fa-book" aria-hidden="true"></i>&nbsp;文章</a>
                </li>

                <div class="divider" style="width: 100%; height: 1px;"></div>

                <li>
                    <a href="../tags/"><i class="fa fa-tags" aria-hidden="true"></i>&nbsp;标签</a>
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

document.querySelector('body').insertAdjacentHTML('afterbegin', componentBox);

// 标题切换
function initWebTitle() {
  const webTitleTextList = [
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

  const webTitleLeaveList = [
    "QingBlog - (｡•́︿•̀｡) 你怎么走掉了啦~",
    "QingBlog - 哼！再不回来看我就不理你了！💢",
    "QingBlog - 快回来嘛，我一个人好无聊QAQ 🥺",
    "QingBlog - 去忙吧，记得回来看看我哦 👋💕",
    "QingBlog - while(true) { await you.comeBack(); } ⏳",
    "QingBlog - console.log('用户离开了，悲伤.jpg') 😭",
    "QingBlog - 404 Not Found: 用户已离线 🔌",
    "QingBlog - // TODO: 用户快回来继续逛博客 📝",
    "QingBlog - 无论你走多远，这里永远亮着灯 💡🏠",
    "QingBlog - 累了就回来歇歇脚吧~ ☕🛋️"
  ];

  const webTitleWelcomeBackList = [
    "QingBlog - 你终于回来啦！✨",
    "QingBlog - 欢迎回来！等你好久了~ 🎉",
    "QingBlog - 呀！你回来啦！(◕‿◕)♡",
    "QingBlog - 好久不见，甚是想念！💕",
    "QingBlog - 哼，还知道回来呀~ 😤",
    "QingBlog - 你去哪儿玩了，不带我！🥺",
    "QingBlog - 欢迎回家！我乖不乖~ 🐱",
    "QingBlog - 你不在的时候我有好好看家哦！⭐",
    "QingBlog - 200 OK: 用户已回归 🟢",
    "QingBlog - console.log('用户回来了，开心！')",
    "QingBlog - await user.comeBack() // resolved ✓",
    "QingBlog - git pull origin user-back 🎊",
    "QingBlog - 回来就好，休息一下吧~ ☕",
    "QingBlog - 这里永远为你亮着灯 💡",
    "QingBlog - 欢迎回来，继续我们的故事 📖",
    "QingBlog - 累了就歇会儿，我陪你 🛋️"
  ];

  const webTitleSwitchIntervalSec = 5000;

  document.title = webTitleTextList[0];

  let webTitleSwitchIntervalId;
  function webTitleSwitch(list) {
    clearInterval(webTitleSwitchIntervalId);

    const listLength = list.length;
    document.title = list[Math.floor(Math.random() * listLength)];

    webTitleSwitchIntervalId = setInterval(function () {
      const random = Math.floor(Math.random() * listLength);
      document.title = list[random];
    }, webTitleSwitchIntervalSec);
  }

  // 监听页面可见性变化
  document.addEventListener("visibilitychange", function () {
    if (document.hidden) {
      webTitleSwitch(webTitleLeaveList);
    } else {
      webTitleSwitch(webTitleWelcomeBackList);
      setTimeout(function () {
        webTitleSwitch(webTitleTextList);
      }, webTitleSwitchIntervalSec);
    }
  });

  webTitleSwitch(webTitleTextList);
}

// -------------------------------------------------------------

// 弹窗相关功能
function alertAnimation() {
  const alertMessage = document.getElementById("alert-message");

  if (!alertMessage) return;

  alertMessage.style.animation = "none";
  alertMessage.offsetHeight;
  alertMessage.style.animation = "alertAnimation 2.2s normal forwards";
}

function showAlert(color, message) {
  const alertMessage = document.getElementById("alert-message");

  if (!alertMessage) return;

  alertMessage.querySelector("span").innerHTML = message;

  if (color === "green") {
    alertMessage.style.background = "rgba(34, 197, 94, 0.3)";
    alertMessage.style.border = "1px solid rgba(34, 197, 94, 0.4)";
    alertMessage.style.boxShadow = "0 0 20px rgba(34, 197, 94, 0.2), inset 0 0 10px rgba(34, 197, 94, 0.05)";
    alertAnimation();
  } else if (color === "red") {
    alertMessage.style.background = "rgba(239, 68, 68, 0.3)";
    alertMessage.style.border = "1px solid rgba(239, 68, 68, 0.4)";
    alertMessage.style.boxShadow = "0 0 20px rgba(239, 68, 68, 0.2), inset 0 0 10px rgba(239, 68, 68, 0.05)";
    alertAnimation();
  } else if (color === "orange") {
    alertMessage.style.background = "rgba(249, 115, 22, 0.3)";
    alertMessage.style.border = "1px solid rgba(249, 115, 22, 0.4)";
    alertMessage.style.boxShadow = "0 0 20px rgba(249, 115, 22, 0.2), inset 0 0 10px rgba(249, 115, 22, 0.05)";
    alertAnimation();
  } else if (color === "yellow") {
    alertMessage.style.background = "rgba(234, 179, 8, 0.3)";
    alertMessage.style.border = "1px solid rgba(234, 179, 8, 0.4)";
    alertMessage.style.boxShadow = "0 0 20px rgba(234, 179, 8, 0.2), inset 0 0 10px rgba(234, 179, 8, 0.05)";
    alertAnimation();
  }
}

// -------------------------------------------------------------

// 初始化返回顶部按钮
function initBackToTop() {
  const backToTopBtn = document.getElementById("back-to-top");
  if (!backToTopBtn) return;

  backToTopBtn.addEventListener('click', function () {
    showAlert("green", "<i class=\"fa fa-hand-pointer-o\" aria-hidden=\"true\"></i>&nbsp;Go! Go! Go! 正在返回顶部！");
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });

  // 监听滚动事件
  window.addEventListener("scroll", function () {
    const scrollTop = window.scrollY;
    if (scrollTop > 0) {
      backToTopBtn.style.visibility = "visible";
    } else {
      backToTopBtn.style.visibility = "hidden";
    }
  });
}

// -------------------------------------------------------------

// 侧边栏相关功能
function initSidebar() {
  const body = document.querySelector("body");
  const overlay = document.querySelector(".overlay");
  const sidebar = document.getElementById("sidebar");
  const sidebarToggle = document.getElementById("sidebar-toggle");
  const sidebarClose = document.getElementById("sidebar-close");

  if (!overlay || !sidebar || !sidebarToggle || !sidebarClose) return;

  // 点击遮罩关闭侧边栏
  overlay.addEventListener("click", hideSidebar);

  // 阻止侧边栏点击事件冒泡
  sidebar.addEventListener("click", function (e) {
    e.stopPropagation();
  });

  // 点击按钮显示侧边栏
  sidebarToggle.addEventListener("click", showSidebar);

  // 点击按钮关闭侧边栏
  sidebarClose.addEventListener("click", hideSidebar);

  // 显示侧边栏
  function showSidebar() {
    sidebar.style.animation = "none";
    overlay.style.animation = "none";

    overlay.offsetHeight;

    sidebar.style.animation = "showSidebarAnimation 0.5s forwards";
    overlay.style.animation = "showOverlayAnimation 0.5s forwards";

    overlay.style.display = "block";
    sidebar.style.display = "flex";

    body.style.overflow = "hidden";
  }

  // 隐藏侧边栏
  function hideSidebar() {
    sidebar.style.animation = "none";
    overlay.style.animation = "none";

    overlay.offsetHeight;

    sidebar.style.animation = "hideSidebarAnimation 0.5s forwards";
    overlay.style.animation = "hideOverlayAnimation 0.5s forwards";

    setTimeout(function () {
      overlay.style.display = "none";
      body.style.overflow = "auto";
    }, 500);
  }
}

// -------------------------------------------------------------

// 设置高度变量
function setNavHeightVar() {
  const nav = document.getElementById('navbar');
  if (nav) {
    const height = nav.offsetHeight;
    document.documentElement.style.setProperty('--nav-height', `${height}px`);
    return height;
  }
}

// -------------------------------------------------------------

function loading() {
  const firstLoading = localStorage.getItem('firstLoading') || "true";

  if (firstLoading !== "false") {
    const body = document.body;
    const qingBlogIcon = document.querySelector('.loading-icon');
    const loading = document.querySelector('.loading');
    const loadingDivs = document.querySelectorAll('.loading-div');

    if (loading) {
      body.style.overflow = "hidden";

      setTimeout(function () {
        loadingDivs.forEach(function (div, index) {
          index += 1;

          if (index % 2 === 0) {
            div.style.animation = "loadingRightAnimation 1.5s ease-out forwards";
          } else {
            div.style.animation = "loadingLeftAnimation 1.5s ease-out forwards";
          };
        });

        qingBlogIcon.style.animation = "hideOverlayAnimation 0.5s ease-in-out forwards";
      }, 1600);

      setTimeout(function () {
        loading.style.display = "none";
        body.style.overflow = "auto";

        localStorage.setItem('firstLoading', 'false');
      }, 3000);
    }
  } else {
    const loading = document.querySelector('.loading');
    if (loading) loading.style.display = "none";
  }
}

// -------------------------------------------------------------

// 主题切换
function themesToggle() {
  const body = document.querySelector('body');
  const toggle = document.getElementById('theme-toggle');
  const prefersColorScheme = matchMedia('(prefers-color-scheme: dark)').matches

  const root = document.documentElement;

  function applyTheme(theme) {
    const themeConfig = themes[theme];

    Object.entries(themeConfig).forEach(function ([key, value]) {
      root.style.setProperty(key, value);
    });
  }

  if (!localStorage.getItem('theme')) {
    applyTheme(prefersColorScheme === true ? 'dark' : 'light');
    toggle.innerHTML = `<i class="fa fa-${prefersColorScheme === true ? 'moon' : 'sun'}-o"></i>`
  } else {
    applyTheme(localStorage.getItem('theme'));
    toggle.innerHTML = `<i class="fa fa-${localStorage.getItem('theme') === 'dark' ? 'moon' : 'sun'}-o"></i>`
  };

  toggle.addEventListener('click', () => {
    const newTheme = (localStorage.getItem('theme')) === 'dark' ? 'light' : 'dark';
    applyTheme(newTheme);
    localStorage.setItem('theme', newTheme);

    toggle.innerHTML = `<i class="fa fa-${newTheme === 'light' ? 'sun' : 'moon'}-o"></i>`
    showAlert('green', `<i class="fa fa-${newTheme === 'light' ? 'sun' : 'moon'}-o"></i>&nbsp;已切换到${newTheme === 'light' ? '浅色' : '深色'}主题！`);
  });
}

// -------------------------------------------------------------

function preCopy() {
  document.querySelectorAll('.copy-btn').forEach(function (copyBtn) {
    copyBtn.addEventListener('click', function () {
      const parents = this.parentElement;

      const code = parents.querySelector('code').textContent;

      navigator.clipboard.writeText(code);

      showAlert('green', '<i class="fa fa-check-square-o" aria-hidden="true"></i>&nbsp;复制成功！');
    })
  })
}

// -------------------------------------------------------------

function removeHeaderBackground() {
  const heroDiv = document.getElementById('hero-div');

  if (!heroDiv) return

  const header = document.querySelector('header');

  // 监听滚动事件
  window.addEventListener("scroll", function () {
    const scrollTop = window.scrollY;
    if (scrollTop > (setNavHeightVar() + setNavHeightVar())) {
      header.style.background = "none";
    } else {
      header.style.background = "var(--hero-bg-color)";
    }
  });
}

// -------------------------------------------------------------

function contextMenu(option) {
  function showContextMenu() {
    menu.style.display = "block";
    menu.classList.add('show');
  }

  function hideContextMenu() {
    menu.classList.remove('show');
    setTimeout(function () {
      menu.style.display = "none";
    }, 200)
  }

  const menu = document.getElementById('context-menu');

  // 监听右键
  document.addEventListener('contextmenu', function (e) {
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

    menu.style.left = x + 'px';
    menu.style.top = y + 'px';
    menu.style.visibility = 'visible';
  });

  menu.addEventListener('click', function (e) {
    e.stopPropagation();
  })

  document.addEventListener('click', function () {
    hideContextMenu();
  })

  if (option === "copy") {
    const userSelectText = window.getSelection().toString();
    navigator.clipboard.writeText(userSelectText);
    hideContextMenu();
    showAlert('green', '<i class="fa fa-check-square-o" aria-hidden="true"></i>&nbsp;复制成功！');
  } else if (option === "refresh") {
    location.reload(true);
  }
}

// -------------------------------------------------------------

function clickTagToTagPage() {
  document.querySelectorAll('.tag').forEach(function (tag) {
    tag.addEventListener('click', function (clickTag) {
      clickTag.preventDefault();

      const clickTagText = tag.querySelector('span').textContent;

      location.href = `../tags/${clickTagText}.html`
    })
  })
}

// -------------------------------------------------------------

// DOM加载完成后初始化所有功能
window.addEventListener('DOMContentLoaded', function () {
  initBackToTop();
  initSidebar();
  initWebTitle();
  setNavHeightVar();
  themesToggle();
  loading();
  preCopy();
  removeHeaderBackground();
  contextMenu();
  clickTagToTagPage();
});

// 监听窗口大小变化
window.addEventListener('resize', setNavHeightVar);

// -------------------------------------------------------------
