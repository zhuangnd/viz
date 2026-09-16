# 前端可视化技术栈展示与应用范例 (viz_tech) 落地汇报

已在 `viz_tech/` 目录下完成前端三大主流可视化技术栈（**Apache ECharts**、**D3.js** 与 **Observable Plot**）的展示与交互应用范例页面。项目全部依赖均采用本地离线库，无需依赖任何外网 CDN，开箱即用。

---

## 交付文件清单

```
viz_tech/
├── index.html        # 主页面骨架（语义化结构、粘性导航、矩阵卡片）
├── style.css         # 现代美学样式（深浅色反差、三引擎品牌色、代码块高亮、响应式网格）
├── app.js            # 核心控制器（多视图切换、代码检视器、D3与Plot控制交互、选型向导计算）
├── lib/              # 本地离线生产精简版依赖库
│   ├── echarts.min.js   # Apache ECharts 5.5.0 (1.0MB)
│   ├── d3.min.js        # D3.js v7.9.0 (273KB)
│   └── plot.umd.min.js  # Observable Plot 0.6.14 (195KB)
├── charts/
│   ├── data.js          # 统一演示数据集（40+ 真实科技企业研发、营收增速、市值多维指标）
│   ├── echarts-demo.js  # ECharts 初始化（Canvas 渲染、DataZoom 区域缩放、Toolbox 工具箱）
│   ├── d3-demo.js       # D3.js 完整渲染管线（Scales, Axes, 缓动入场动画, Brush 矩形画刷圈选聚合）
│   └── plot-demo.js     # Observable Plot 声明式图层（Marks 组合、线性回归拟合、区域分面）
└── README.md         # 详细使用指南与架构说明
```

---

## 页面核心功能与交互亮点

### 1. 三大技术栈全景对比矩阵
- 深度对比三者的**抽象层级**（图表级 vs 图元算法级 vs 图形语法级）、**核心心智模型**、**典型代码量**、**定制天花板**、**大数据性能瓶颈**与 **React/Vue 契合度**。

### 2. 同源数据现场实战演练场 (Live Tri-Engine Arena)
- **同构三屏矩阵 (Side-by-Side)**：基于统一的科技企业研发数据集，同一时间并排渲染三类图表。
- **Apache ECharts 模式**：体验原生的商业报表交互（双向 DataZoom 缩放条、右上角图片导出/数据视图、图例一键过滤赛道、富文本 Tooltip）。
- **D3.js 模式**：展示原生 SVG 图元控制力，支持**鼠标画刷圈选（Brush）**。拖拽选框即可实时圈选多维数据点，并在状态栏动态计算所选企业的平均增速与累计估值。
- **Observable Plot 模式**：展示纯正的图形语法，支持一键切换「线性回归趋势拟合线」与「按区域进行小多组分面 (Faceting)」。

### 3. 源码对照检视器 (Code Inspector)
- 支持一键切换查看实现该图表的三种核心代码：
  - **ECharts (约 68 行)**：JSON 选项树装配
  - **D3.js (约 112 行)**：比例尺计算 + 数据管道 + DOM 生命周期管理
  - **Observable Plot (约 28 行)**：纯正声明式 Mark 正交组合
- 提供一键复制代码功能与架构心智标签。

### 4. 架构深剖：框架集成与渲染性能
- 剖析 D3 与 React/Vue 虚拟 DOM 的冲突根源，给出成熟解法（**D3 作为纯数学与比例尺计算层 + 框架 JSX 原生渲染**）。
- 梳理 Canvas（3k~10万点）、SVG（<3k点）与 WebGL（10万+点）的选型分水岭。

### 5. 交互式智能选型决策向导 (Interactive Decision Wizard)
- 提供 5 个典型工程维度的单选题（视觉形态、交付周期、框架集成、商业套件诉求、数据体量）。
- 实时计算三大技术栈的匹配百分比，并输出量身定制的技术选型建议与混合落地架构。

---

## 验证情况

1. **依赖文件完整性验证**：
   - 验证 `viz_tech/lib/` 下所有文件大小正常，通过 Node.js VM 模拟环境加载 `window.echarts`、`window.d3` 与 `window.Plot` 全部初始化成功。
2. **代码语法校验**：
   - 使用 `node -c` 对 `data.js`、`echarts-demo.js`、`d3-demo.js`、`plot-demo.js` 与 `app.js` 完成语法检查，零报错。
3. **离线可用性**：
   - 页面内部所有脚本与样式表均采用相对路径，完全支持离线本地加载。

---

## 快速预览指引

直接在本地浏览器中打开：
```bash
open viz_tech/index.html
```
或者通过本地简易 HTTP 服务器预览：
```bash
cd viz_tech && npx serve . # 或 python3 -m http.server 8080
```
