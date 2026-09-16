# 前端可视化技术栈展示与应用范例 (viz_tech)

本项目全面解构并横向评测前端可视化三大主流技术栈：**Apache ECharts**、**D3.js** 与 **Observable Plot**。包含全景对比矩阵、同一份真实数据集的三引擎同构现场渲染演练场（Live Showcase）、源码检视器以及交互式智能选型决策向导。

所有第三方核心库均已下载至本地 `lib/` 目录，完全支持离线打开与本地预览。

---

## 目录结构

```
viz_tech/
├── index.html        # 主页面骨架与结构化语义标记
├── style.css         # 现代美学样式（排版规范、三引擎主题色、响应式网格与代码高亮）
├── app.js            # 页面交互控制器（Tab 切换、D3 微交互控制、Plot 动态分面、选型向导逻辑）
├── lib/              # 本地离线第三方依赖库 (无需外部 CDN)
│   ├── echarts.min.js   # Apache ECharts 5.5.0 生产精简版
│   ├── d3.min.js        # D3.js v7.9.0 生产精简版
│   └── plot.umd.min.js  # Observable Plot 0.6.14 UMD 离线包
├── charts/
│   ├── data.js          # 统一演示数据集（全球科技研发投入、营收增速、市值多维数据）
│   ├── echarts-demo.js  # ECharts 完整初始化（DataZoom, Tooltip, Toolbox, Canvas 渲染）
│   ├── d3-demo.js       # D3.js 完整渲染管线（Scales, Axes, Enter 缓动入场, Brush 框选聚合）
│   └── plot-demo.js     # Observable Plot 声明式图层（Marks, 回归趋势拟合, 分面映射）
└── README.md
```

---

## 快速预览与运行

由于所有 JS 库和样式均为相对路径本地引用，您可以通过以下任意方式预览：

### 方式 1：直接在浏览器中双击打开
直接双击 `viz_tech/index.html`，或在终端中使用浏览器打开：
```bash
open viz_tech/index.html
```

### 方式 2：使用任意本地静态服务器
```bash
# 进入 viz_tech 目录
cd viz_tech

# 使用 Python 内置简易 HTTP 服务器
python3 -m http.server 8080

# 然后在浏览器访问: http://localhost:8080
```

---

## 核心展示模块与技术亮点

1. **三大技术栈全景对比矩阵**：
   - 涵盖抽象层级、核心心智模型、定制上限、大数据量承载、React/Vue 契合度、社区生态等多维度对比。
2. **同构数据三引擎实战演练场 (Live Tri-Engine Arena)**：
   - **并排同屏矩阵 (Side-by-Side)**：使用同一批真实科技行业数据，三张图表同时渲染，直观对比视觉风格与默认交互。
   - **Apache ECharts 单图模式**：体验开箱即用的 DataZoom 滑块区域缩放、右上角 Toolbox 图片导出与图例交互。
   - **D3.js 单图模式**：具备弹性质感的数据入场缓动动画，并支持**鼠标绘制方框（Brush）进行多点批量圈选**，状态栏实时计算圈选企业的平均增速与总市值。
   - **Observable Plot 单图模式**：体验纯粹的声明式图形语法，支持一键切换「线性回归趋势拟合线」与「按区域进行小多组分面 (Faceting)」。
3. **源码对照检视器 (Code Inspector)**：
   - 切换查看三者渲染同款图表的核心代码。
   - 直观量化对比代码行数（LOC，约 68 行 vs 112 行 vs 28 行）、心智模型与架构范式，并支持一键复制代码。
4. **架构深度剖析**：
   - React / Vue 中 DOM 控制权冲突与工业界最佳实践（D3 作为纯数学计算层 + JSX/模板渲染）。
   - Canvas (3k~100k点) vs SVG (<3k点) vs WebGL (100k+点) 性能分水岭。
5. **交互式智能选型决策向导 (Interactive Decision Wizard)**：
   - 提供 5 个典型工程维度的单选评估，实时计算三者匹配百分比，输出综合裁决与落地组合建议。
