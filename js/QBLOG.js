// 网页标题切换功能
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

// 导航栏相关功能
function initNavbar() {
  const nav = document.getElementById('navbar');
  if (!nav) return;

  const logo = nav.querySelector('.logo');
  const divider = nav.querySelector('.divider');

  if (!logo || !divider) return;

  logo.style.display = "none";

  const firstLiHeight = nav.querySelector('ul li')?.offsetHeight;
  if (firstLiHeight) {
    logo.style.height = firstLiHeight + "px";
    divider.style.height = (firstLiHeight - 10) + "px";
  }

  logo.style.display = "block";
}

// -------------------------------------------------------------

// 搜索功能
function find(q) {
  if (!q) {
    showAlert("red", "<i class=\"fa fa-exclamation-triangle\"></i>&nbsp;不能搜索空值");
    return false;
  }

  // 清除之前的搜索结果
  document.querySelectorAll('mark.h').forEach(m => m.replaceWith(m.textContent));
  document.body.normalize();

  // 创建正则表达式
  const r = new RegExp(`(${q.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')})`, 'gi');

  // 收集所有文本节点
  const textNodes = [];
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, null);
  while (walker.nextNode()) {
    if (walker.currentNode.parentElement?.closest('mark.h,script,style,noscript,textarea')) continue;
    textNodes.push(walker.currentNode);
  }

  let foundCount = 0;

  // 遍历文本节点进行搜索
  for (let i = textNodes.length - 1; i >= 0; i--) {
    const node = textNodes[i];
    if (!r.test(node.textContent)) continue;
    r.lastIndex = 0;

    const fragment = document.createDocumentFragment();
    let lastIndex = 0;
    node.textContent.replace(r, (match, p, offset) => {
      fragment.append(node.textContent.slice(lastIndex, offset), document.createElement('mark'));
      fragment.lastChild.className = 'h';
      fragment.lastChild.textContent = match;
      lastIndex = offset + match.length;
      foundCount++;
      return match;
    });

    if (lastIndex < node.textContent.length) fragment.append(node.textContent.slice(lastIndex));
    node.parentNode.replaceChild(fragment, node);
  }

  if (foundCount > 0) {
    showAlert("green", `<i class=\"fa fa-check-circle\"></i>&nbsp;找到 ${foundCount} 处匹配`);
    return true;
  } else {
    showAlert("orange", "<i class=\"fa fa-info-circle\"></i>&nbsp;未找到匹配内容");
    return false;
  }
}

// -------------------------------------------------------------

// 初始化搜索功能
function initSearch() {
  const searchInput = document.getElementById("search");
  if (searchInput) {
    searchInput.addEventListener("keydown", function (e) {
      if (e.key === "Enter") {
        find(this.value);
      }
    });
  }

  // 初始化搜索容器样式
  const searchDiv = document.getElementById("search-container");
  if (searchDiv) {
    const searchHeight = searchDiv.querySelector("input")?.offsetHeight;
    const searchBtn = searchDiv.querySelector("button");
    const headerNavHeight = document.getElementById("navbar")?.offsetHeight;
    const barsBtn = document.getElementById("sidebar-toggle");
    const exitBarsBtn = document.getElementById("sidebar-close");

    if (searchHeight && searchBtn) {
      searchBtn.style.height = searchHeight + "px";
      searchBtn.style.width = searchHeight + "px";
    }

    if (headerNavHeight && barsBtn) {
      barsBtn.style.height = headerNavHeight + "px";
      barsBtn.style.width = headerNavHeight + "px";
    }

    if (searchHeight && exitBarsBtn) {
      exitBarsBtn.style.height = searchHeight + "px";
      exitBarsBtn.style.width = searchHeight + "px";
    }
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

    if (body) {
      body.style.overflow = "hidden";
    }
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
      if (body) {
        body.style.overflow = "auto";
      }
    }, 500);
  }
}

// -------------------------------------------------------------

// 设置导航栏高度变量
function setNavHeightVar() {
  const nav = document.getElementById('navbar');
  if (nav) {
    const height = nav.offsetHeight;
    document.documentElement.style.setProperty('--nav-height', `${height}px`);
  }
}

// -------------------------------------------------------------

function loading() {
  const body = document.body;
  const qingBlogIcon = document.querySelector('.loading-icon');
  const loading = document.querySelector('.loading');
  const loadingDivs = document.querySelectorAll('.loading-div');

  body.style.overflow = "hidden";

  setTimeout(function () {
    loadingDivs.forEach(function (div, index) {
      index = ++index;

      if (index % 2 === 0) {
        div.style.animation = "loadingUpAnimation 1.5s forwards";
      } else {
        div.style.animation = "loadingDownAnimation 1.5s forwards";
      }
    });

    qingBlogIcon.style.animation = "hideOverlayAnimation 1.5s forwards";
  }, 1500);

  setTimeout(function () {
    loading.style.display = "none";
    body.style.overflow = "auto";
  }, 3000);
}

// -------------------------------------------------------------

// 页面加载完成后初始化所有功能
window.addEventListener('DOMContentLoaded', function () {
  initNavbar();
  initSearch();
  initBackToTop();
  initSidebar();
  initWebTitle();
  setNavHeightVar();
  loading();
});

// 监听窗口大小变化
window.addEventListener('resize', setNavHeightVar);

// -------------------------------------------------------------