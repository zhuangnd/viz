# Alec Soth 空间摄影地图导览系统（Spatial Atlas）设计方案

## 一、 项目定位与核心目标

本项目在 `viz/alec_soth/` 目录下构建全新的**空间地理与时间叙事摄影导览页面（`atlas.html`）**，与原有的作品集画廊页（`index.html`）共同组成「**画册专题精读 + 空间公路巡礼**」双模式数字文献系统。

### 核心目标
1. **全量收录 11 部作品集**：完整纳入 `https://alecsoth.com/photography/projects/` 全部 **11 个官方专题**（《Looking for Love》《Sleeping by the Mississippi》《Dog Days Bogotá》《Niagara》《Paris / Minnesota》《The Last Days of W.》《Broken Manual》《Songbook》《I Know How Furiously Your Heart Is Beating》《A Pound of Pictures》《Advice for Young Artists》）。
2. **实体画册完整图版补全**：针对代表作 **《Sleeping by the Mississippi》**（Steidl 2004 初版 46 幅图版 + MACK 2017 增订版 2 幅，共 48 幅）与 **《Niagara》**（Steidl 2006 画册核心图版），在官网展示图源基础上，结合沃克艺术中心（Walker Art Center）、芝加哥艺术博物馆（Art Institute of Chicago）、旧金山现代艺术博物馆（SFMOMA）、玛格南图片社（Magnum Photos）等馆藏目录补全实体书全部图版信息、精确拍摄地标与馆藏图源。
3. **3:7 屏幕比例双栏空间交互**：参考 `viz/japan-travel-guide/index.html` 的工程架构，采用左侧 **30% 多维检索与叙事面板** + 右侧 **70% 交互式地图画布**，实现圆点标记、公路/河道行旅路线（Polylines）、悬停缩略图预览、点击联动详情与全屏滚轮缩放灯箱（`0.5x–4.5x`）。
4. **多维度时空探索**：支持按 **时间（1995–2024 年份/月份）**、**作品集（11 部系列）**、**地点（国家 / 州 State / 县 County / 城市与地标）** 及 **文献来源（官网高清 / 实体书补全图版）** 进行组合过滤与地图自动飞跃对焦。

---

## 二、 数据层架构与地理编码规范（`atlas-data.json`）

### 1. 字段结构定义
每条作品记录（Photo Node）遵循统一 JSON Schema：

```json
{
  "id": "sbtm-01",
  "projectSlug": "sleeping-by-the-mississippi",
  "projectTitle": "Sleeping by the Mississippi",
  "projectTitleZh": "密西西比河畔的沉睡",
  "plateNumber": 1,
  "title": "Peter's Houseboat, Winona, MN, 2002",
  "subject": "Peter's Houseboat",
  "year": 2002,
  "month": 3,
  "dateCode": "2002-03",
  "country": "United States",
  "state": "Minnesota",
  "stateCode": "MN",
  "county": "Winona County",
  "city": "Winona",
  "landmark": "Latsch Island Boathouse Community, Mississippi River Pool 5A",
  "lat": 44.0588,
  "lng": -91.6322,
  "precision": "landmark",
  "precisionLabel": "精确地标",
  "sourceType": "official_web",
  "src": "https://alecsoth.com/photography/media/pages/projects/sleeping-by-the-mississippi/...",
  "routeOrder": 6,
  "notes": "摄于明尼苏达州威诺纳拉奇岛（Latsch Island）百年水上船屋社区。"
}
```

### 2. 三级地理定位精度体系（Precision Tiers）
- **`landmark`（精确地标级）**：标题或馆藏文献包含明确建筑、道路、墓园、教堂、监狱或汽车旅馆名称。
  - *示例 1*：`Peter's Houseboat, Winona, MN` → 威诺纳 Latsch Island 水上船屋区（`44.0588, -91.6322`）。
  - *示例 2*：`Charles Lindbergh's Boyhood Home, Little Falls, MN` → 林德伯格州立公园故居（`45.9575, -94.3881`）。
  - *示例 3*：`Fort Jefferson Memorial Cross, Wickliffe, KY` → 肯塔基州威克利夫密西西比河与俄亥俄河交汇处巨型十字架（`36.9589, -89.0928`）。
  - *示例 4*：`Johnny Cash's Boyhood Home, Dyess, AR` → 阿肯色州戴스殖民地卡什童年故居（`35.5901, -90.2134`）。
  - *示例 5*：`A-1 Motel` / `Cadillac Motel` / `The Voyageur`（《Niagara》）→ 加拿大安大略省尼亚加拉瀑布城 **Lundy's Lane** 历史汽车旅馆走廊真实门牌坐标。
- **`city`（城镇/街区级）**：标题包含明确城市、乡镇或社区名称（如 `Vasa, MN`、`luxora, AR`、`New Madrid, MO`），定位至该城镇滨河或核心历史街区，并对同城多张作品施加黄金角微距偏移（`0.002°–0.006°`）以防止图标完全叠合。
- **`series_locus`（作品集核心区兜底级）**：无具体地点标注的室内肖像或静物（如《Niagara》部分匿名情书/室内肖像、《Broken Manual》隐士木屋、《Dog Days Bogotá》波哥大街景、《Advice for Young Artists》艺术学院课堂），归入所属作品集的核心地理发生地并按环状聚类微偏移分布。

### 3. 底片归档文件名时间解码（Archival Filename Decoding）
通过正则解析 `alecsoth.com` 原始文件名（如 `2002_03zl0046_f.jpg`、`19-2012_05md1001_0242.jpg`、`1995_06wm0002-012-f.jpg`），提取前缀 `YYYY_MM`，为原本仅标年份或未标年份的作品还原精确到**拍摄年份与月份**的时空序列。

---

## 三、 界面布局与视觉交互规范（3:7 屏幕比例）

### 1. 整体框架（`100vw × 100vh` 全屏应用）
- **顶部固定导航栏（`height: 50px`）**：
  - 左侧：品牌印记 + 页面模式切换胶囊（「画册专题导览 `index.html`」↔「空间地图导览 `atlas.html`」）。
  - 中部：核心公路路线快速切换器（全部作品总览 / 密西西比河顺流南下全线 / 尼亚加拉边境双城记 / Songbook 社群纪行 / Last Days of W. 等）。
  - 右侧：地图底图切换下拉框（Carto Voyager / Carto Positron / Dark Matter / OSM / Esri 地形图）、路线轨迹线开关、日/夜主题切换。
- **主工作区（`height: calc(100vh - 50px)`，`grid-template-columns: 30% 70%`）**：
  - **左栏（30% 宽度，独立滚动）**：
    1. **多维探索控制台**：
       - **作品集筛选（11 个专题色标胶囊）**：支持单选聚焦与全集总览。
       - **时间轴直方图与区间滑块（1995–2024）**：D3.js 渲染年度作品数量分布柱状图，点击或拖拽年份快速过滤。
       - **地理行政级联与搜索框**：按「国家 → 州/省 (State) → 县/城市 (County/City)」筛选，支持精度等级与图源类型过滤。
    2. **当前视图统计摘要栏**：实时展示当前筛选下的「作品总数 / 涵盖州县 / 时间跨度 / 路线里程」。
    3. **作品卡片流列表（Photo Cards）**：展示缩略图、图版号（如 `Plate #06`）、作品名称、拍摄年月、州/县/地标名称及精度徽章。悬停卡片时高亮地图对应圆点，点击卡片时地图平滑飞跃至该点位。
  - **右栏（70% 宽度，交互式地图画布）**：
    1. **多色彩分层圆点标记（SVG DivIcon Markers）**：按作品集赋予专属古典色谱；精确地标点位带内环靶心；实体画册补全图版带专属角标。
    2. **行旅拍摄路线（Sequential Route Polylines）**：
       - 选中特定作品集（尤其是《Sleeping by the Mississippi》自北向南沿河 2,300 英里路线）时，自动绘制带流向感的公路/河道折线，并在圆点显示路线序号。
    3. **鼠标悬停（Hover）缩略图浮层**：悬停任意地图圆点，即刻弹出无延迟浮动预览卡（高清缩略图 + 标题 + 年月 + 州县地标 + 拍摄背景简注）。
    4. **鼠标点击（Click）联动与可缩放灯箱**：点击圆点同步激活左侧卡片详情，并支持一键打开**全屏高清缩放灯箱**（支持 `0.5x–4.5x` 滚轮缩放、鼠标拖拽平移、`1:1` 像素检视、全屏切换与键盘方向键巡航）。
    5. **地图底部可折叠纵向剖面/纬度时间轴底座（Latitude / Timeline Dock）**：参考 `japan-travel-guide` 底部剖面图设计，展示「北纬 47°（明尼苏达源头）→ 北纬 29°（路易斯安那入海口）」的纬度演进或时间演进曲线，实现图表与地图双向探针联动。

---

## 四、 执行步骤清单

1. **抓取补齐官网全部 11 个作品集**：将 `looking-for-love`、`dog-days-bogota`、`paris-minnesota` 合并入 `photos.json`。
2. **考据补全实体画册图版**：整理《Sleeping by the Mississippi》全部 48 幅图版（46 初版 + 2 增订版）及《Niagara》实体书完整图版清单，匹配馆藏公开图源与精确地理坐标。
3. **生成 `atlas-data.json`**：编写 Python 地理编码与元数据构建脚本，生成包含全量照片（约 330+ 条记录）的精确经纬度、州/县/市层级、拍摄年月与路线序列数据。
4. **开发 `viz/alec_soth/atlas.html`**：实现 3:7 分屏布局、Leaflet 多源地图、D3 时间/纬度剖面图、多维筛选器、悬停缩略图浮层与全屏可缩放灯箱。
5. **更新入口导航与文档**：在 `viz/alec_soth/index.html`、`viz/index.html` 与 `viz/alec_soth/README.md` 中添加 `atlas.html` 入口链接并验证所有交互。
