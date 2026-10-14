# 日本深度自助旅行交互式导览平台 — 网页版架构与设计规范（Web Spec & Design Document）

> **设计定位**：超越传统静态图文游记，构建一个以**空间地理（GIS）为轴、时间日程与预算模型联动、支持双模交通动态切换**的现代数据可视化旅行规划系统。  
> **技术栈基准**：Node.js v22 + Observable Framework / Vite + MapLibre GL JS (Vector Tiles) + D3.js v7 + CSS Grid/Container Queries 响应式布局。

---

## 一、 视觉语言与设计哲学（Design Philosophy）

1. **编辑级信息叙事（Editorial Cartography）**：
   * 摒弃杂乱的弹窗广告与小红书式九宫格拼图，采用日本现代平面设计（Swiss-Japanese Grid）的克制美学——高对比度衬线标题（Noto Serif SC / Shippori Mincho）、等宽数据字体（JetBrains Mono 用于海拔、里程、日元预算与列车时刻）与大面积留白（Ma，间）。
2. **色彩语义系统（Semantic Color Palette）**：
   * **背景基调**：和纸暖白（`#F8F6F0` 浅色模式）与玄武岩深灰（`#141619` 暗色山岳模式）。
   * **路线主题色**：
     * 路线一（本州脊梁·古道山岳）：**靛蓝（Ai-iro, `#264653`）**
     * 路线二（山阴海岸·濑户内海）：**赤铜（Shakudo, `#BC4749`）**
     * 路线三（奥羽秘汤·绳文森林）：**苔绿（Koke-iro, `#386641`）**
   * **交通模式编码**：轨道交通采用实线双轨纹理，自驾公路采用平滑渐变色带，徒步古道与骑行段采用高对比虚线（Dash-array）。

---

## 二、 响应式自适应布局架构（Responsive Layout & Viewport Adaptation）

系统采用 **“三态自适应容器架构（Tri-State Adaptive Shell）”**，根据视口宽度与交互手势平滑流转：

```
+-----------------------------------------------------------------------------------+
| 顶部全局控制栏 (Header Bar): 路线切换 [路线1 | 路线2 | 路线3] | 交通模式 [公共交通 ⇄ 自驾] | 预算基准 |
+-----------------------------------+-----------------------------------------------+
|                                   |                                               |
|   左侧：叙事与日程流 (42% 宽度)     |          右侧：全屏粘性画布 (58% 宽度)          |
|   [Scrollytelling Narrative]      |          [Sticky Interactive Viewport]        |
|                                   |                                               |
|   +---------------------------+   |   +---------------------------------------+   |
|   | 行程概览仪表盘 (KPI Cards)  |   |   |                                       |   |
|   | 总里程 | 徒步段 | 预估总费 |   |   |      MapLibre GL 3D 地形与轨迹图层     |   |
|   +---------------------------+   |   |      (支持倾斜角 Pitch 45° 观察山脉)    |   |
|                                   |   |                                       |   |
|   +---------------------------+   |   +---------------------------------------+   |
|   | Day 03: 木曾路·马笼至妻笼  | ====> | 联动高亮: 马笼宿 -> 妻笼宿 8km 徒步轨迹 |   |
|   | - 地理锚点与文化背景       |   |   +---------------------------------------+   |
|   | - [模式A/B] 交通接驳微卡片 |   |   |  底部停靠: D3.js 海拔高程与坡度剖面图   |   |
|   | - 食宿推荐与当日预算拆解   |   |   |  [马笼 600m] ---\___/--- [妻笼 420m]  |   |
|   +---------------------------+   |   +---------------------------------------+   |
|                                   |                                               |
+-----------------------------------+-----------------------------------------------+
```

### 多端断点策略（Breakpoints）
* **Desktop Wide (`≥ 1280px`)**：双栏分屏（Left Scrollytelling 42% + Right Sticky Map & Elevation 58%），底部常驻预算累加器。
* **Tablet / Laptop (`768px – 1279px`)**：50% / 50% 分栏，高程剖面图可折叠为浮动抽屉（Collapsible Drawer）。
* **Mobile (`< 768px`)**：采用 **“底层全屏地图 + 顶部日程胶囊滑块 + 底部三段式可拖拽抽屉（Bottom Sheet: Peek 25% / Half 55% / Full 90%）”**，完美适配单手大拇指在旅途现场检索车站、MapCode 与 Tabelog 链接。

---

## 三、 核心可视化与交互模块设计（Core Interactive Modules）

### 模块 1：3D 地形感知地图导览（MapLibre GL + DEM 地形高程）
* **底图与高程源**：加载日本国土地理院（GSI Japan）开源矢量切片与 DEM 高程纹理，开启三维地形夸张系数（`exaggeration: 1.3`），直观呈现中央阿尔卑斯、纪伊山地、四国喀斯特与奥羽山脉的险峻地势，解释为何某路段“必须换乘登山巴士或绕行海岸”。
* **图层分级渲染（Zoom-Level Semantic Layering）**：
  * `Zoom 5–7`（宏观路线层）：展示三条 15–20 日大环线的空间拓扑、进出港机场与核心宿场节点。
  * `Zoom 8–11`（日程区间层）：展示当日城际移动轨迹（JR 特急/新干线 vs 高速公路）、沿途“道の駅”与秘汤位置，动态流动粒子（Animated Dash）指示行进方向。
  * `Zoom 12–16`（微观步导层）：精准渲染古道徒步路径（如中山道石板路、熊野古道发心门段、奥入濑溪流步道）、行李托运点、观光案内所 e-Bike 租赁点与 Tabelog 餐饮锚点。

### 模块 2：D3.js 行程高程剖面与时间轴矩阵（Elevation & Timeline Brush）
* **交互双向绑定（Bidirectional Brushing）**：
  * 画布底部配置由 `d3.area` 与 `d3.brushX` 驱动的**海拔高程—里程剖面图（Elevation Profile）**。
  * 当鼠标在剖面图上滑动时，地图上同步移动一个实时高程探针（显示当前位置海拔、坡度百分比及与下一宿场的距离）；反之，滚动左侧日程卡片时，剖面图平滑缩放（Zoom-to-Segment）至当日行程区间。
* **日程甘特与季节物候热力条（Phenology Heatmap）**：
  * 提供 1–12 月份气候与物候滑动条（新绿、紫阳花、花火、红叶前线、豪雪秘汤），切换月份时自动高亮当前月份最契合的路线与海拔带（例如 10 月中旬自动高亮八甲田山与上高地红叶带，11 月中旬高亮熊野与濑户内海）。

### 模块 3：双模交通与动态预算沙盒（Transport & Budget Reactive Sandbox）
* **全局模式一键切换（Mode A `公共交通` ⇄ Mode B `合规自驾`）**：
  * 切换至 **公共交通模式** 时：日程卡片自动渲染 JR 换乘番线、区域周游券覆盖标识、巴士时刻表预警（如“五箇山末班车 16:45”）及行李托运建议；注意栏自动隐藏自驾参数。
  * 切换至 **合规自驾模式** 时：触发醒目的**《1949 日内瓦公约驾照合规性校验弹窗》**，确认持有合规证件后，日程卡片自动切换为每日驾驶里程（km）、预估驾驶时长、高速过路费（ETC 折后价）、终点停车场 MapCode 及山道驾驶难度评级（1–5 星）。
* **实时预算精算器（Reactive Budget Calculator）**：
  * 支持用户调节四个核心滑块：`同行人数 (1–4人)`、`出行天数 (15–20天)`、`住宿档次 (青旅古民家 / 温泉商务 / 秘汤旅馆)`、`实时汇率基准`。
  * 利用 D3 堆叠条形图（Stacked Bar Chart）实时重算并对比各项支出（签证机票、城际交通、住宿、餐饮、门票杂项），直观展示“2 人拼车自驾 vs 2 人购买 JR 周游券”的成本临界点。

---

## 四、 核心数据结构规范（GeoJSON + Itinerary Schema）

前端数据层采用强类型 JSON/GeoJSON 驱动，便于扩展与离线缓存（PWA 支持山间无信号区查阅）：

```json
{
  "routeId": "route-01-nakasendo-kumano",
  "title": "本州脊梁与千年古道：中山道、北陆与熊野纵贯线",
  "durationDays": 18,
  "entryAirport": "NGO",
  "exitAirport": "KIX",
  "themeColor": "#264653",
  "days": [
    {
      "day": 3,
      "dateOffset": 2,
      "segmentTitle": "木曾路古道徒步：马笼宿 → 妻笼宿 → 奈良井宿",
      "overnightNode": {
        "name": "奈良井宿 (Narai-juku)",
        "prefecture": "长野县",
        "coordinates": [137.8124, 35.9669],
        "elevationMeters": 940
      },
      "highlights": [
        {
          "name": "马笼—妻笼中山道石板路 (8.0km)",
          "category": "historic_trail",
          "coordinates": [137.5661, 35.5262],
          "difficulty": "Easy-Moderate",
          "durationHours": 2.5,
          "notes": "8:30前在马笼观光案内所办理行李托运（1,000日元/件），轻装翻越马笼峠。"
        }
      ],
      "transportModes": {
        "publicTransit": {
          "summary": "JR中央本线（中津川 → 南木曾 → 奈良井）",
          "passCoverage": "不适用全国Pass，建议直接刷Suica或买分段乘车券",
          "costJPY": 2840,
          "durationMinutes": 95,
          "criticalAlert": "南木曾前往奈良井的普通列车每1-2小时一班，务必衔接15:18或16:35班次。"
        },
        "selfDrive": {
          "summary": "国道19号（木曾高速街道）北上",
          "distanceKm": 62,
          "driveMinutes": 80,
          "tollJPY": 0,
          "mapCode": "398 524 112*44",
          "parkingInfo": "奈良井宿权现桥免费公营停车场（步行至老街2分钟）",
          "NoteForWalk": "自驾者可将车停在妻笼宿停车场，乘早班接驳巴士至马笼宿，徒步走回妻笼取车。"
        }
      },
      "dining": [
        {
          "name": "越后屋 (Echigoya) 手打荞麦面",
          "specialty": "木曾路投汁荞麦面 (Toji Soba) & 五平饼",
          "budgetJPY": 1600,
          "tabelogScore": 3.54
        }
      ],
      "accommodation": {
        "economy": { "name": "奈良井宿 民芸旅館 深山", "type": "Hatago", "pricePerPersonJPY": 9500 },
        "comfort": { "name": "BYAKU Narai (百岁酒藏古民家改建)", "type": "Heritage Boutique", "pricePerPersonJPY": 28000 }
      }
    }
  ]
}
```

---

## 五、 工程落地与离线可用性设计（Implementation & PWA Readiness）

1. **静态预构建与边缘加速**：基于 Observable Framework 或 Vite 构建纯静态资产包（SSG），将三条路线的 GeoJSON 轨迹、高程数组与食宿数据编译为压缩率极高的 `.parquet` 或 `.json` 数据块，首屏加载时间 `< 1.2s`。
2. **旅途现场离线模式（Service Worker + IndexedDB）**：由于熊野古道、白神山地与奥入濑溪流部分区间移动网络信号较弱，系统通过 Service Worker 预缓存当前选定路线的矢量地图切片、时刻表预警与预订单摘要，支持离线查看当日海拔探针与列车衔接时刻。
3. **一键导出（Export Actions）**：支持将用户定制后的 15–20 日方案一键导出为：
   * **送签专用标准行程单（Visa Submission Itinerary PDF）**：自动格式化为日本驻华领馆标准英文/日文/中文三语表格（含每日日期、起止点、住宿名称、地址与电话），直接用于签证申请。
   * **Google Maps / MapCode 书签包（KML / CSV）**：一键导入手机地图或租车导航。
