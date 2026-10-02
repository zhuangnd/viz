/**
 * 《值得专程前往的福建美食之都》核心交互应用逻辑
 */

(function () {
  "use strict";

  // 应用状态管理
  const state = {
    activeChapter: "all",
    activeRegion: "all",
    activeDiningTime: "all",
    searchQuery: "",
    selectedFoodId: null,
    
    // 面线糊实验室状态
    noodleLab: {
      broth: "fish", // 'pork' or 'fish'
      toppings: ["t_curou", "t_dachang", "t_youtiao"]
    },

    // 牛肉三件套实验室状态
    beefTrioActiveIndex: 0,

    // 路线活跃项
    activeRouteId: "route_licheng",

    // 寻味护照 (已收藏美食 ID 列表)
    passport: JSON.parse(localStorage.getItem("quanzhou_food_passport") || '["mianxianhu", "minnan_beef_steak", "zhongji_jiangmuxia"]')
  };

  // DOM 元素缓存
  const el = {
    header: document.getElementById("main-header"),
    foodsContainer: document.getElementById("foods-grid"),
    foodCountLabel: document.getElementById("food-count-label"),
    searchInput: document.getElementById("search-input"),
    regionFilterRow: document.getElementById("region-filter-row"),
    timeFilterRow: document.getElementById("time-filter-row"),
    chapterBar: document.getElementById("chapter-quick-nav"),
    
    // 模态框
    modalBackdrop: document.getElementById("food-modal-backdrop"),
    modalBody: document.getElementById("food-modal-content"),
    modalCloseBtn: document.getElementById("modal-close-btn"),

    // 面线糊实验室 DOM
    noodleBrothBtnPork: document.getElementById("broth-btn-pork"),
    noodleBrothBtnFish: document.getElementById("broth-btn-fish"),
    noodleBowlBroth: document.getElementById("bowl-broth-layer"),
    noodleToppingsPool: document.getElementById("toppings-options-pool"),
    noodleBowlTagsContainer: document.getElementById("bowl-active-tags"),
    noodleTotalPrice: document.getElementById("noodle-total-price"),
    noodleReviewText: document.getElementById("noodle-expert-review"),
    presetLocalBtn: document.getElementById("preset-local-btn"),
    presetDeluxeBtn: document.getElementById("preset-deluxe-btn"),

    // 牛肉三件套 DOM
    beefTrioCardsContainer: document.getElementById("beef-trio-cards"),
    beefTrioDetailBox: document.getElementById("beef-trio-detail-box"),

    // 寻味路线 DOM
    routeTabs: document.getElementById("route-tabs"),
    routeContent: document.getElementById("route-content-container"),

    // 护照抽屉 DOM
    passportBtn: document.getElementById("passport-toggle-btn"),
    passportBadge: document.getElementById("passport-badge-count"),
    passportDrawer: document.getElementById("passport-drawer"),
    passportCloseBtn: document.getElementById("passport-close-btn"),
    passportItemsList: document.getElementById("passport-items-list"),
    passportProgressBar: document.getElementById("passport-progress-fill"),
    passportProgressText: document.getElementById("passport-progress-text"),
    passportPrintBtn: document.getElementById("passport-print-btn"),
    passportClearBtn: document.getElementById("passport-clear-btn")
  };

  /**
   * 初始化应用
   */
  function init() {
    renderChapterNav();
    renderFilterPills();
    renderFoods();
    initNoodleLab();
    initBeefTrioLab();
    initRoutes();
    updatePassportUI();
    bindGlobalEvents();
  }

  /**
   * 绑定全局交互事件
   */
  function bindGlobalEvents() {
    // 滚动吸顶阴影
    window.addEventListener("scroll", () => {
      if (window.scrollY > 40) {
        el.header.classList.add("scrolled");
      } else {
        el.header.classList.remove("scrolled");
      }
    });

    // 搜索监听
    el.searchInput.addEventListener("input", (e) => {
      state.searchQuery = e.target.value.trim().toLowerCase();
      renderFoods();
    });

    // 弹窗关闭
    el.modalCloseBtn.addEventListener("click", closeModal);
    el.modalBackdrop.addEventListener("click", (e) => {
      if (e.target === el.modalBackdrop) closeModal();
    });
    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape") {
        closeModal();
        closePassportDrawer();
      }
    });

    // 护照抽屉开关
    el.passportBtn.addEventListener("click", openPassportDrawer);
    el.passportCloseBtn.addEventListener("click", closePassportDrawer);
    el.passportPrintBtn.addEventListener("click", () => window.print());
    el.passportClearBtn.addEventListener("click", () => {
      if (confirm("确定要清空您的所有寻味打卡收藏吗？")) {
        state.passport = [];
        savePassport();
        updatePassportUI();
        renderFoods(); // 更新卡片上的书签状态
      }
    });
  }

  /**
   * 渲染章节快捷导航
   */
  function renderChapterNav() {
    const chapters = FOOD_CAPITAL_DATA.chapters;
    let html = `
      <button class="chapter-badge-card px-4 py-3 rounded-lg text-left transition flex items-center gap-3 ${state.activeChapter === 'all' ? 'active' : ''}" data-chapter="all">
        <span class="w-8 h-8 rounded-full bg-stone-100 flex items-center justify-center text-stone-700">
          ${getIcon("compass", "w-4 h-4")}
        </span>
        <div>
          <div class="text-xs text-stone-500 font-sans">全览</div>
          <div class="text-sm font-bold font-serif">全域风味总谱</div>
        </div>
      </button>
    `;

    chapters.forEach((chap) => {
      const isActive = state.activeChapter === chap.id;
      html += `
        <button class="chapter-badge-card px-4 py-3 rounded-lg text-left transition flex items-center gap-3 ${isActive ? 'active' : ''}" data-chapter="${chap.id}">
          <span class="w-8 h-8 rounded-full bg-stone-100 flex items-center justify-center text-stone-700">
            ${getIcon(chap.icon, "w-4 h-4")}
          </span>
          <div>
            <div class="text-xs text-stone-500 font-sans">${chap.number} · ${chap.name}</div>
            <div class="text-sm font-bold font-serif text-stone-800">${chap.subname.split("·")[0]}</div>
          </div>
        </button>
      `;
    });

    el.chapterBar.innerHTML = html;

    // 绑定点击
    el.chapterBar.querySelectorAll("button").forEach((btn) => {
      btn.addEventListener("click", () => {
        state.activeChapter = btn.dataset.chapter;
        el.chapterBar.querySelectorAll("button").forEach(b => b.classList.remove("active"));
        btn.classList.add("active");
        renderFoods();
      });
    });
  }

  /**
   * 渲染筛选药丸按钮 (按地区 / 按时段)
   */
  function renderFilterPills() {
    const regions = [
      { id: "all", label: "全部坐标" },
      { id: "鲤城古城", label: "鲤城老街" },
      { id: "晋江", label: "晋江安海" },
      { id: "石狮", label: "石狮老城" },
      { id: "深沪", label: "深沪崇武(滨海)" }
    ];

    let rHtml = "";
    regions.forEach(r => {
      const active = state.activeRegion === r.id ? "active" : "";
      rHtml += `<button class="filter-pill ${active}" data-region="${r.id}">${getIcon("pin", "w-3.5 h-3.5")} ${r.label}</button>`;
    });
    el.regionFilterRow.innerHTML = rHtml;

    el.regionFilterRow.querySelectorAll(".filter-pill").forEach(btn => {
      btn.addEventListener("click", () => {
        state.activeRegion = btn.dataset.region;
        el.regionFilterRow.querySelectorAll(".filter-pill").forEach(b => b.classList.remove("active"));
        btn.classList.add("active");
        renderFoods();
      });
    });

    const times = [
      { id: "all", label: "全部时段" },
      { id: "早市", label: "清晨早点" },
      { id: "正餐", label: "晌午正席" },
      { id: "下午", label: "下午茶配" },
      { id: "宵夜", label: "深夜食堂" }
    ];

    let tHtml = "";
    times.forEach(t => {
      const active = state.activeDiningTime === t.id ? "active" : "";
      tHtml += `<button class="filter-pill ${active}" data-time="${t.id}">${getIcon("clock", "w-3.5 h-3.5")} ${t.label}</button>`;
    });
    el.timeFilterRow.innerHTML = tHtml;

    el.timeFilterRow.querySelectorAll(".filter-pill").forEach(btn => {
      btn.addEventListener("click", () => {
        state.activeDiningTime = btn.dataset.time;
        el.timeFilterRow.querySelectorAll(".filter-pill").forEach(b => b.classList.remove("active"));
        btn.classList.add("active");
        renderFoods();
      });
    });
  }

  /**
   * 核心渲染：美食卡片网格
   */
  function renderFoods() {
    let filtered = FOOD_CAPITAL_DATA.foods.filter(item => {
      // 章节筛选
      if (state.activeChapter !== "all" && item.chapterId !== state.activeChapter) {
        return false;
      }
      // 地区筛选
      if (state.activeRegion !== "all" && !item.region.includes(state.activeRegion)) {
        return false;
      }
      // 时段筛选
      if (state.activeDiningTime !== "all" && !item.diningTime.includes(state.activeDiningTime)) {
        return false;
      }
      // 关键词搜索
      if (state.searchQuery) {
        const fullStr = (item.name + item.pinyin + item.alias + item.summary + item.deepDive + item.articleQuote).toLowerCase();
        if (!fullStr.includes(state.searchQuery)) return false;
      }
      return true;
    });

    el.foodCountLabel.textContent = `共呈现 ${filtered.length} 处刺桐珍味`;

    if (filtered.length === 0) {
      el.foodsContainer.innerHTML = `
        <div class="col-span-full py-16 text-center text-stone-500">
          <div class="w-12 h-12 mx-auto mb-3 text-stone-300">${getIcon("search", "w-12 h-12")}</div>
          <p class="font-serif text-lg text-stone-600">未检索到符合条件的泉州美食</p>
          <p class="text-sm mt-1">建议尝试切换分类标签或缩短搜索关键词</p>
        </div>
      `;
      return;
    }

    let html = "";
    filtered.forEach(item => {
      const isBookmarked = state.passport.includes(item.id);
      const chapterObj = FOOD_CAPITAL_DATA.chapters.find(c => c.id === item.chapterId);
      
      // 生成简易雷达直方条
      const radarKeys = Object.keys(item.radar);
      let radarBarHtml = "";
      radarKeys.slice(0, 3).forEach(k => {
        const val = item.radar[k];
        radarBarHtml += `
          <div class="text-xs flex items-center justify-between text-stone-500 mb-1">
            <span>${k}</span>
            <div class="w-20 bg-stone-100 h-1.5 rounded-full overflow-hidden ml-2">
              <div class="bg-amber-700 h-full rounded-full" style="width: ${val}%"></div>
            </div>
          </div>
        `;
      });

      html += `
        <article class="food-card" data-id="${item.id}">
          <div>
            <!-- 头部元标签 -->
            <div class="flex items-center justify-between gap-2 mb-3">
              <div class="flex items-center gap-2">
                <span class="minnan-seal">${item.badge}</span>
                <span class="text-xs text-stone-500 font-sans">${item.region}</span>
              </div>
              <button class="bookmark-card-btn p-1.5 rounded-full text-stone-400 hover:text-red-700 transition" title="加入寻味护照" data-id="${item.id}">
                ${getIcon(isBookmarked ? "bookmarkFilled" : "bookmark", isBookmarked ? "w-5 h-5 text-red-700" : "w-5 h-5")}
              </button>
            </div>

            <!-- 菜名与别名 -->
            <div class="mb-3">
              <h3 class="text-xl font-bold font-serif text-stone-900 group-hover:text-red-800 transition">
                ${item.name}
              </h3>
              <p class="text-xs text-stone-400 font-sans tracking-wider mt-0.5">${item.pinyin} · ${item.alias}</p>
            </div>

            <!-- 摘要引文 -->
            <p class="text-stone-600 text-sm leading-relaxed mb-4 line-clamp-3">
              ${item.summary}
            </p>

            <!-- 风味标签 -->
            <div class="flex flex-wrap gap-1.5 mb-4">
              ${item.flavorProfile.map(f => `<span class="text-xs px-2 py-0.5 rounded bg-stone-100 text-stone-600">${f}</span>`).join("")}
            </div>
          </div>

          <!-- 卡片底部操作与风味微标 -->
          <div class="pt-4 border-t border-stone-100">
            <div class="mb-3">
              ${radarBarHtml}
            </div>
            
            <div class="flex items-center justify-between">
              <span class="text-xs text-stone-400 flex items-center gap-1 font-sans">
                ${getIcon("clock", "w-3.5 h-3.5")} ${item.diningTime.split("/")[0]}
              </span>
              <button class="open-detail-btn text-xs font-semibold text-red-800 hover:text-red-900 inline-flex items-center gap-1 group" data-id="${item.id}">
                深度品鉴与名店
                <span class="transition transform group-hover:translate-x-0.5">${getIcon("arrowRight", "w-3.5 h-3.5")}</span>
              </button>
            </div>
          </div>
        </article>
      `;
    });

    el.foodsContainer.innerHTML = html;

    // 绑定卡片交互
    el.foodsContainer.querySelectorAll(".open-detail-btn").forEach(btn => {
      btn.addEventListener("click", (e) => {
        e.stopPropagation();
        openModal(btn.dataset.id);
      });
    });

    el.foodsContainer.querySelectorAll(".food-card").forEach(card => {
      card.addEventListener("click", (e) => {
        if (!e.target.closest(".bookmark-card-btn")) {
          openModal(card.dataset.id);
        }
      });
    });

    el.foodsContainer.querySelectorAll(".bookmark-card-btn").forEach(btn => {
      btn.addEventListener("click", (e) => {
        e.stopPropagation();
        togglePassportItem(btn.dataset.id);
      });
    });
  }

  /**
   * 打开深度美食模态弹窗
   */
  function openModal(foodId) {
    const food = FOOD_CAPITAL_DATA.foods.find(f => f.id === foodId);
    if (!food) return;

    state.selectedFoodId = foodId;
    const isBookmarked = state.passport.includes(food.id);
    const chapter = FOOD_CAPITAL_DATA.chapters.find(c => c.id === food.chapterId);

    // 渲染名店列表
    let shopsHtml = "";
    food.recommendedShops.forEach((shop, idx) => {
      shopsHtml += `
        <div class="p-3.5 rounded-lg border border-stone-200 bg-stone-50/70 hover:bg-stone-50 transition">
          <div class="flex items-center justify-between mb-1">
            <span class="font-serif font-bold text-stone-900 flex items-center gap-1.5">
              ${getIcon("pin", "w-4 h-4 text-red-800")} ${shop.name}
            </span>
            <span class="text-xs text-stone-400 font-sans">${shop.location}</span>
          </div>
          <p class="text-xs text-stone-600 font-sans leading-relaxed">${shop.highlight}</p>
        </div>
      `;
    });

    // 渲染风味雷达图数值
    let radarHtml = "";
    Object.entries(food.radar).forEach(([dim, val]) => {
      radarHtml += `
        <div class="bg-stone-50 p-2.5 rounded text-center border border-stone-100">
          <div class="text-xs text-stone-500 mb-1">${dim}</div>
          <div class="font-serif font-bold text-base text-stone-900">${val}</div>
        </div>
      `;
    });

    el.modalBody.innerHTML = `
      <div class="p-6 md:p-8">
        <!-- 头部章节印章与关闭 -->
        <div class="flex items-center justify-between mb-4">
          <div class="flex items-center gap-2">
            <span class="gold-seal">${chapter ? chapter.name : '风味特写'}</span>
            <span class="minnan-seal">${food.badge}</span>
            <span class="text-xs text-stone-500">${food.region}</span>
          </div>
        </div>

        <!-- 标题区 -->
        <div class="mb-6">
          <h2 class="text-2xl md:text-3xl font-serif font-bold text-stone-900 mb-1">
            ${food.name}
          </h2>
          <p class="text-xs md:text-sm text-stone-400 tracking-wider">${food.pinyin} · ${food.alias}</p>
        </div>

        <!-- 经典原著引述 Callout -->
        <div class="p-4 rounded-xl bg-amber-50/60 border border-amber-200/70 text-amber-950 mb-6 font-serif italic text-sm md:text-base leading-relaxed">
          ${food.articleQuote}
        </div>

        <!-- 技艺与风味深度探微 -->
        <div class="mb-6">
          <h4 class="text-sm font-bold font-sans text-stone-900 uppercase tracking-widest mb-2 flex items-center gap-1.5">
            ${getIcon("sparkle", "w-4 h-4 text-amber-600")} 烹调玄机与风味密码
          </h4>
          <div class="text-stone-700 text-sm md:text-base leading-relaxed space-y-2 whitespace-pre-line font-sans">
            ${food.deepDive.trim()}
          </div>
        </div>

        <!-- 老饕吃法与秘辛 -->
        <div class="mb-6 p-4 rounded-lg bg-red-50/50 border border-red-100">
          <h4 class="text-xs font-bold text-red-900 uppercase tracking-wider mb-1 flex items-center gap-1">
            ${getIcon("star", "w-3.5 h-3.5 text-red-700")} 老饕独家赏味建议
          </h4>
          <p class="text-xs md:text-sm text-red-950 leading-relaxed">${food.secretTips}</p>
        </div>

        <!-- 风味矩阵雷达 -->
        <div class="mb-6">
          <h4 class="text-xs font-bold text-stone-500 uppercase tracking-wider mb-2">五维风味指数</h4>
          <div class="grid grid-cols-5 gap-2">
            ${radarHtml}
          </div>
        </div>

        <!-- 推荐老字号 -->
        <div class="mb-6">
          <h4 class="text-sm font-bold font-sans text-stone-900 uppercase tracking-widest mb-3 flex items-center gap-1.5">
            ${getIcon("compass", "w-4 h-4 text-stone-700")} 文章考据老字号地标
          </h4>
          <div class="space-y-2.5">
            ${shopsHtml}
          </div>
        </div>

        <!-- 弹窗底部操作 -->
        <div class="flex items-center justify-between pt-4 border-t border-stone-200">
          <button class="btn-outline-gold text-xs py-2 px-4" id="modal-bookmark-toggle-btn">
            ${getIcon(isBookmarked ? "bookmarkFilled" : "bookmark", isBookmarked ? "w-4 h-4 text-red-700" : "w-4 h-4")}
            <span>${isBookmarked ? '已在寻味清单' : '加入寻味清单'}</span>
          </button>
          <button class="text-xs text-stone-400 hover:text-stone-700 transition" onclick="document.getElementById('modal-close-btn').click()">
            返回风味总谱
          </button>
        </div>
      </div>
    `;

    // 绑定模态框内书签点击
    document.getElementById("modal-bookmark-toggle-btn").addEventListener("click", () => {
      togglePassportItem(food.id);
      openModal(food.id); // 刷新弹窗内按钮状态
    });

    el.modalBackdrop.classList.add("active");
    document.body.style.overflow = "hidden";
  }

  function closeModal() {
    el.modalBackdrop.classList.remove("active");
    document.body.style.overflow = "";
    state.selectedFoodId = null;
  }

  /**
   * 交互实验室 1：面线糊自选调配碗
   */
  function initNoodleLab() {
    const labData = FOOD_CAPITAL_DATA.noodleLab;

    // 渲染料头选择池
    let poolHtml = "";
    labData.toppings.forEach(t => {
      const isSelected = state.noodleLab.toppings.includes(t.id);
      poolHtml += `
        <button class="topping-select-btn p-3 rounded-xl border text-left transition flex items-start gap-3 ${isSelected ? 'border-amber-700 bg-amber-50/60 shadow-sm' : 'border-stone-200 bg-white hover:border-stone-300'}" data-tid="${t.id}">
          <span class="w-8 h-8 rounded-lg flex items-center justify-center shrink-0 ${isSelected ? 'bg-amber-700 text-white' : 'bg-stone-100 text-stone-600'}">
            ${getIcon(t.icon, "w-4 h-4")}
          </span>
          <div class="flex-1 min-w-0">
            <div class="flex items-center justify-between mb-0.5">
              <span class="text-sm font-bold font-serif text-stone-900">${t.name}</span>
              <span class="text-xs font-semibold text-amber-800">¥${t.price}</span>
            </div>
            <p class="text-xs text-stone-500 line-clamp-1">${t.desc}</p>
          </div>
        </button>
      `;
    });
    el.noodleToppingsPool.innerHTML = poolHtml;

    // 绑定料头点击
    el.noodleToppingsPool.querySelectorAll(".topping-select-btn").forEach(btn => {
      btn.addEventListener("click", () => {
        const tid = btn.dataset.tid;
        if (state.noodleLab.toppings.includes(tid)) {
          state.noodleLab.toppings = state.noodleLab.toppings.filter(id => id !== tid);
        } else {
          state.noodleLab.toppings.push(tid);
        }
        updateNoodleBowlVisual();
        initNoodleLab(); // 重新渲染状态样式
      });
    });

    // 绑定汤底切换
    el.noodleBrothBtnPork.addEventListener("click", () => {
      state.noodleLab.broth = "pork";
      el.noodleBrothBtnPork.classList.add("active");
      el.noodleBrothBtnFish.classList.remove("active");
      updateNoodleBowlVisual();
    });

    el.noodleBrothBtnFish.addEventListener("click", () => {
      state.noodleLab.broth = "fish";
      el.noodleBrothBtnFish.classList.add("active");
      el.noodleBrothBtnPork.classList.remove("active");
      updateNoodleBowlVisual();
    });

    // 预设组合一键切换
    el.presetLocalBtn.addEventListener("click", () => {
      state.noodleLab.broth = "fish";
      state.noodleLab.toppings = ["t_curou", "t_dachang", "t_youtiao"];
      el.noodleBrothBtnFish.click();
      initNoodleLab();
      updateNoodleBowlVisual();
    });

    el.presetDeluxeBtn.addEventListener("click", () => {
      state.noodleLab.broth = "pork";
      state.noodleLab.toppings = ["t_curou", "t_dachang", "t_haidai", "t_xia", "t_youtiao", "t_wuxiang"];
      el.noodleBrothBtnPork.click();
      initNoodleLab();
      updateNoodleBowlVisual();
    });

    updateNoodleBowlVisual();
  }

  /**
   * 更新面线糊碗中视觉与老饕点评
   */
  function updateNoodleBowlVisual() {
    const isPork = state.noodleLab.broth === "pork";
    el.noodleBowlBroth.className = `bowl-broth-layer ${isPork ? 'broth-pork' : 'broth-fish'}`;

    // 计算总价
    const labData = FOOD_CAPITAL_DATA.noodleLab;
    let basePrice = isPork ? 6 : 6;
    let total = basePrice;
    let selectedToppingObjs = [];

    state.noodleLab.toppings.forEach(tid => {
      const top = labData.toppings.find(t => t.id === tid);
      if (top) {
        total += top.price;
        selectedToppingObjs.push(top);
      }
    });

    el.noodleTotalPrice.textContent = `¥${total}`;

    // 渲染碗中动态料头微标
    let tagsHtml = "";
    selectedToppingObjs.forEach(top => {
      tagsHtml += `
        <span class="bowl-topping-tag text-xs font-semibold px-2.5 py-1 rounded-full bg-white/95 text-stone-800 shadow-sm border border-stone-200/80 inline-flex items-center gap-1 backdrop-blur-sm m-1">
          ${getIcon(top.icon, "w-3 h-3 text-amber-700")} ${top.name}
        </span>
      `;
    });
    el.noodleBowlTagsContainer.innerHTML = tagsHtml || `<span class="text-xs text-stone-400 italic">尚未勾选料头（请点击右侧配料池）</span>`;

    // 智能老饕点评引擎
    let review = "";
    const hasCurou = state.noodleLab.toppings.includes("t_curou");
    const hasDachang = state.noodleLab.toppings.includes("t_dachang");
    const hasYoutiao = state.noodleLab.toppings.includes("t_youtiao");
    const hasHaidai = state.noodleLab.toppings.includes("t_haidai");

    if (hasCurou && hasDachang && hasYoutiao) {
      review = "【绝代黄金标配】醋肉微酸解腻、大肠弹韧入味、剪段油条吸尽滚烫糊汤。这是全泉州老饕心照不宣的灵魂配置，无可挑剔！";
    } else if (hasHaidai && !isPork) {
      review = "【鱼骨清甜派精粹】鲜活海蛎投进鱼骨虾油熬出的清亮糊汤中，海潮的清甜在舌尖翻卷，极具县后街文啊、罗记风骨！";
    } else if (selectedToppingObjs.length >= 5) {
      review = "【豪奢海陆全席】料头重重叠叠几乎盖过糊汤，大骨浓汤浸润山珍海错，这是犒赏自己的极致市井盛宴！";
    } else if (!hasYoutiao) {
      review = "【老饕轻声提醒】碗里似乎少了一根剪成小段的金黄油条。油条入汤半脆半吸汁，才是面线糊画龙点睛的奥义所在。";
    } else {
      review = `【清润古早品味】选用${isPork ? '大骨高汤' : '鱼骨清汤'}，配料清雅适口，一碗入腹，通体温热舒坦。`;
    }

    el.noodleReviewText.textContent = review;
  }

  /**
   * 交互实验室 2：一人食牛肉三件套解构台
   */
  function initBeefTrioLab() {
    const trioData = FOOD_CAPITAL_DATA.beefTrioLab;
    const comps = trioData.components;

    let cardsHtml = "";
    comps.forEach((comp, idx) => {
      const isSelected = state.beefTrioActiveIndex === idx;
      cardsHtml += `
        <div class="trio-component-card ${isSelected ? 'selected' : ''}" data-idx="${idx}">
          <div class="flex items-center justify-between mb-2">
            <span class="w-8 h-8 rounded-full bg-amber-100/70 text-amber-900 flex items-center justify-center font-bold text-xs">
              0${idx + 1}
            </span>
            <span class="text-xs text-stone-400 font-sans">${comp.role}</span>
          </div>
          <h4 class="text-lg font-serif font-bold text-stone-900 mb-1">${comp.name}</h4>
          <p class="text-xs text-stone-500 font-sans line-clamp-2">${comp.craft}</p>
        </div>
      `;
    });

    el.beefTrioCardsContainer.innerHTML = cardsHtml;

    // 绑定卡片切换
    el.beefTrioCardsContainer.querySelectorAll(".trio-component-card").forEach(card => {
      card.addEventListener("click", () => {
        const idx = parseInt(card.dataset.idx, 10);
        state.beefTrioActiveIndex = idx;
        initBeefTrioLab();
      });
    });

    // 渲染当前组件的深度解构内容
    const current = comps[state.beefTrioActiveIndex];
    el.beefTrioDetailBox.innerHTML = `
      <div class="p-6 md:p-8 bg-stone-50/80 rounded-2xl border border-stone-200">
        <div class="flex items-center gap-2 mb-3">
          <span class="minnan-seal">部件解构 0${state.beefTrioActiveIndex + 1}</span>
          <span class="gold-seal">${current.role}</span>
        </div>
        <h3 class="text-2xl font-serif font-bold text-stone-900 mb-2">${current.name}</h3>
        
        <div class="space-y-4 text-stone-700 text-sm md:text-base font-sans mt-4">
          <div>
            <div class="text-xs font-bold text-stone-400 uppercase tracking-widest mb-1 flex items-center gap-1">
              ${getIcon("fire", "w-3.5 h-3.5 text-red-700")} 制作玄机与手艺
            </div>
            <p class="leading-relaxed">${current.craft}</p>
          </div>
          <div>
            <div class="text-xs font-bold text-stone-400 uppercase tracking-widest mb-1 flex items-center gap-1">
              ${getIcon("sparkle", "w-3.5 h-3.5 text-amber-600")} 老饕品鉴心法
            </div>
            <p class="leading-relaxed text-amber-950 bg-amber-50/60 p-3 rounded-lg border border-amber-100">${current.wisdom}</p>
          </div>
        </div>
      </div>
    `;
  }

  /**
   * 四大深度寻味路线渲染
   */
  function initRoutes() {
    const routes = FOOD_CAPITAL_DATA.routes;

    // 渲染路线选项卡
    let tabsHtml = "";
    routes.forEach(r => {
      const isSelected = state.activeRouteId === r.id;
      tabsHtml += `
        <button class="filter-pill font-serif ${isSelected ? 'active' : ''}" data-rid="${r.id}">
          ${getIcon("compass", "w-3.5 h-3.5")} ${r.name.split("·")[0]}
        </button>
      `;
    });
    el.routeTabs.innerHTML = tabsHtml;

    el.routeTabs.querySelectorAll("button").forEach(btn => {
      btn.addEventListener("click", () => {
        state.activeRouteId = btn.dataset.rid;
        initRoutes();
      });
    });

    // 渲染当前路线详情
    const activeRoute = routes.find(r => r.id === state.activeRouteId) || routes[0];
    let stopsHtml = "";
    activeRoute.stops.forEach((stop, idx) => {
      stopsHtml += `
        <div class="timeline-item pb-6">
          <div class="timeline-dot"></div>
          <div class="flex items-center gap-2 mb-1">
            <span class="text-xs font-mono font-semibold px-2 py-0.5 rounded bg-stone-100 text-stone-700">${stop.time}</span>
            <span class="font-serif font-bold text-stone-900">${stop.name}</span>
          </div>
          <div class="text-sm text-stone-800 font-medium mb-1">${stop.dish}</div>
          <div class="text-xs text-stone-500 font-sans italic flex items-center gap-1">
            ${getIcon("star", "w-3 h-3 text-amber-600")} ${stop.tip}
          </div>
        </div>
      `;
    });

    el.routeContent.innerHTML = `
      <div class="bg-white rounded-2xl p-6 md:p-8 border border-stone-200/90 shadow-sm">
        <div class="flex flex-wrap items-center justify-between gap-3 pb-5 mb-6 border-b border-stone-100">
          <div>
            <span class="minnan-seal mb-1.5">${activeRoute.region}</span>
            <h3 class="text-2xl font-serif font-bold text-stone-900">${activeRoute.name}</h3>
          </div>
          <div class="text-xs font-semibold px-3 py-1.5 rounded-full bg-amber-50 text-amber-900 border border-amber-200">
            ${activeRoute.timeSpan}
          </div>
        </div>
        <p class="text-stone-600 text-sm md:text-base leading-relaxed mb-6 font-sans">
          ${activeRoute.description}
        </p>
        <div class="mt-4">
          ${stopsHtml}
        </div>
      </div>
    `;
  }

  /**
   * 寻味护照 (打卡清单) 系统
   */
  function togglePassportItem(foodId) {
    const idx = state.passport.indexOf(foodId);
    if (idx > -1) {
      state.passport.splice(idx, 1);
    } else {
      state.passport.push(foodId);
    }
    savePassport();
    updatePassportUI();
    renderFoods(); // 刷新卡片书签图标
  }

  function savePassport() {
    localStorage.setItem("quanzhou_food_passport", JSON.stringify(state.passport));
  }

  function updatePassportUI() {
    const totalCount = FOOD_CAPITAL_DATA.foods.length;
    const collectedCount = state.passport.length;
    const pct = Math.round((collectedCount / totalCount) * 100);

    el.passportBadge.textContent = collectedCount;
    el.passportProgressBar.style.width = `${pct}%`;
    el.passportProgressText.textContent = `已解锁 ${collectedCount} / ${totalCount} 处绝味 (${pct}%)`;

    // 渲染护照内抽屉列表
    if (collectedCount === 0) {
      el.passportItemsList.innerHTML = `
        <div class="py-12 text-center text-stone-400">
          <div class="w-10 h-10 mx-auto mb-2 text-stone-300">${getIcon("bookmark", "w-10 h-10")}</div>
          <p class="text-sm font-serif">您的寻味护照尚空</p>
          <p class="text-xs mt-1">浏览美食图谱时，点击书签图标即可收录</p>
        </div>
      `;
      return;
    }

    let itemsHtml = "";
    state.passport.forEach(id => {
      const food = FOOD_CAPITAL_DATA.foods.find(f => f.id === id);
      if (!food) return;

      itemsHtml += `
        <div class="p-3.5 rounded-xl border border-stone-100 bg-stone-50 flex items-center justify-between gap-3 hover:bg-white transition group">
          <div class="min-w-0 flex-1 cursor-pointer" onclick="window.quanzhouApp.openModal('${food.id}')">
            <div class="flex items-center gap-1.5 mb-0.5">
              <span class="text-xs text-red-800 font-semibold font-serif">${food.badge}</span>
              <span class="text-xs text-stone-400 font-sans">${food.region}</span>
            </div>
            <h4 class="text-sm font-bold font-serif text-stone-900 group-hover:text-red-800 transition truncate">${food.name}</h4>
          </div>
          <button class="remove-passport-item-btn p-1.5 text-stone-300 hover:text-red-700 transition" data-id="${food.id}" title="移出清单">
            ${getIcon("close", "w-4 h-4")}
          </button>
        </div>
      `;
    });

    el.passportItemsList.innerHTML = itemsHtml;

    el.passportItemsList.querySelectorAll(".remove-passport-item-btn").forEach(btn => {
      btn.addEventListener("click", () => {
        togglePassportItem(btn.dataset.id);
      });
    });
  }

  function openPassportDrawer() {
    el.passportDrawer.classList.add("open");
  }

  function closePassportDrawer() {
    el.passportDrawer.classList.remove("open");
  }

  // 挂载全局 API 以供行内回调
  window.quanzhouApp = {
    openModal: openModal
  };

  // 页面加载完成后启动
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
