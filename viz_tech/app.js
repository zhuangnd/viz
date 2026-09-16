/**
 * viz_tech 页面主交互控制器
 */

document.addEventListener('DOMContentLoaded', () => {
  // 状态与实例持久化
  const state = {
    activeEngine: 'all', // 'all' | 'echarts' | 'd3' | 'plot'
    activeCodeTab: 'echarts',
    plotOptions: {
      showRegression: true,
      facetMode: 'none'
    },
    wizardAnswers: {
      q1: 'a',
      q2: 'a',
      q3: 'a',
      q4: 'a',
      q5: 'a'
    }
  };

  let chartInstances = {
    echartsSingle: null,
    echartsGrid: null,
    d3Single: null,
    d3Grid: null,
    plotSingle: null,
    plotGrid: null
  };

  // 1. 初始化图表展示
  function renderActiveEngineView() {
    const singleContainer = document.getElementById('single-chart-view');
    const multiGrid = document.getElementById('multi-engine-grid');
    const hud = document.getElementById('interactive-hud');
    const plotControls = document.getElementById('plot-extra-controls');
    const d3Controls = document.getElementById('d3-extra-controls');

    if (state.activeEngine === 'all') {
      singleContainer.style.display = 'none';
      multiGrid.style.display = 'grid';
      hud.innerHTML = '✨ <b>同构多引擎矩阵：</b>当前并排展示由同一份数据实时驱动的 ECharts、D3.js 与 Observable Plot 实例。';
      plotControls.style.display = 'none';
      d3Controls.style.display = 'none';

      // 延迟确保容器宽高可用
      setTimeout(() => {
        chartInstances.echartsGrid = window.initEChartsDemo('chart-grid-echarts');
        chartInstances.d3Grid = window.initD3Demo('chart-grid-d3');
        chartInstances.plotGrid = window.initPlotDemo('chart-grid-plot', { showRegression: false });
      }, 50);

    } else {
      multiGrid.style.display = 'none';
      singleContainer.style.display = 'block';
      singleContainer.innerHTML = '';

      if (state.activeEngine === 'echarts') {
        plotControls.style.display = 'none';
        d3Controls.style.display = 'none';
        hud.innerHTML = '📊 <b>ECharts 模式：</b>支持右上角工具箱导出/复位，底部滑块或滚轮缩放，点击图例可隐藏或过滤行业。';
        setTimeout(() => {
          chartInstances.echartsSingle = window.initEChartsDemo('single-chart-view');
        }, 50);

      } else if (state.activeEngine === 'd3') {
        plotControls.style.display = 'none';
        d3Controls.style.display = 'inline-flex';
        hud.innerHTML = '💡 <b>D3.js 模式：</b>可在图表任意区域拖拽鼠标<b>绘制方框（Brush）</b>进行多点批量圈选与动态聚合分析。';
        setTimeout(() => {
          chartInstances.d3Single = window.initD3Demo('single-chart-view');
        }, 50);

      } else if (state.activeEngine === 'plot') {
        plotControls.style.display = 'inline-flex';
        d3Controls.style.display = 'none';
        hud.innerHTML = '📐 <b>Observable Plot 模式：</b>纯正图形语法渲染，包含原生线性拟合与分面能力，返回原生 SVG 节点。';
        setTimeout(() => {
          chartInstances.plotSingle = window.initPlotDemo('single-chart-view', state.plotOptions);
        }, 50);
      }
    }
  }

  // 引擎标签切换事件
  document.querySelectorAll('.engine-tab-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
      document.querySelectorAll('.engine-tab-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      state.activeEngine = btn.dataset.engine;
      renderActiveEngineView();
    });
  });

  // D3 专用控制按钮
  const d3ReplayBtn = document.getElementById('btn-d3-replay');
  if (d3ReplayBtn) {
    d3ReplayBtn.addEventListener('click', () => {
      if (chartInstances.d3Single && chartInstances.d3Single.resetAnimation) {
        chartInstances.d3Single.resetAnimation();
      } else {
        renderActiveEngineView();
      }
    });
  }

  // Plot 专用控制按钮
  const btnToggleRegression = document.getElementById('btn-toggle-regression');
  if (btnToggleRegression) {
    btnToggleRegression.addEventListener('click', () => {
      state.plotOptions.showRegression = !state.plotOptions.showRegression;
      btnToggleRegression.classList.toggle('active', state.plotOptions.showRegression);
      btnToggleRegression.textContent = state.plotOptions.showRegression ? '趋势拟合: 开' : '趋势拟合: 关';
      if (state.activeEngine === 'plot') {
        window.initPlotDemo('single-chart-view', state.plotOptions);
      }
    });
  }

  const btnToggleFacet = document.getElementById('btn-toggle-facet');
  if (btnToggleFacet) {
    btnToggleFacet.addEventListener('click', () => {
      state.plotOptions.facetMode = state.plotOptions.facetMode === 'none' ? 'region' : 'none';
      btnToggleFacet.classList.toggle('active', state.plotOptions.facetMode === 'region');
      btnToggleFacet.textContent = state.plotOptions.facetMode === 'region' ? '区域分面: 开启' : '区域分面: 关闭';
      if (state.activeEngine === 'plot') {
        window.initPlotDemo('single-chart-view', state.plotOptions);
      }
    });
  }

  // 2. 源码检查器 (Code Inspector)
  const CODE_SNIPPETS = {
    echarts: {
      metrics: { loc: '约 68 行', mentalModel: '配置项树 (Option Object)', paradigm: '高阶图表配置 / Canvas' },
      code: `// Apache ECharts 实现核心片段 (配置驱动)
const chart = echarts.init(container, null, { renderer: 'canvas' });

const option = {
  tooltip: {
    trigger: 'item',
    formatter: (params) => \`\${params.value[3]}: 研发占比 \${params.value[0]}%, 增速 \${params.value[1]}%\`
  },
  toolbox: { feature: { dataZoom: {}, restore: {}, saveAsImage: {} } },
  legend: { data: window.VIZ_SECTORS },
  xAxis: { type: 'value', name: '研发营收比 (%)' },
  yAxis: { type: 'value', name: '年增长率 (%)' },
  dataZoom: [{ type: 'slider', height: 20 }, { type: 'inside' }],
  series: window.VIZ_SECTORS.map(sector => ({
    name: sector,
    type: 'scatter',
    data: getSectorData(sector),
    symbolSize: val => Math.max(8, Math.sqrt(val[2]) * 0.78),
    itemStyle: { color: colorMap[sector], opacity: 0.8 }
  }))
};

chart.setOption(option);
window.addEventListener('resize', () => chart.resize());`
    },

    d3: {
      metrics: { loc: '约 112 行', mentalModel: '数据驱动 DOM 管道 (Data Binding)', paradigm: '图形基元与数学比例尺 / 原生 SVG' },
      code: `// D3.js 实现核心片段 (底层图元管道与交互)
const svg = d3.select(container).append("svg").attr("viewBox", \`0 0 \${width} \${height}\`);

// 1. 数学比例尺计算
const xScale = d3.scaleLinear().domain([0, 80]).range([0, innerWidth]);
const yScale = d3.scaleLinear().domain([-80, 200]).range([innerHeight, 0]);
const rScale = d3.scaleSqrt().domain([0, maxCap]).range([5, 32]);

// 2. 绘制坐标轴与网格
g.append("g").call(d3.axisBottom(xScale).ticks(8));
g.append("g").call(d3.axisLeft(yScale).ticks(8));

// 3. 数据绑定与入场缓动动画 (Enter Selection)
const circles = g.selectAll("circle")
  .data(data)
  .enter().append("circle")
  .attr("cx", d => xScale(d.rdRatio))
  .attr("cy", d => yScale(d.growthRate))
  .attr("r", 0)
  .attr("fill", d => colorMap[d.sector])
  .transition().duration(850).ease(d3.easeCubicOut)
  .attr("r", d => rScale(d.marketCap));

// 4. 原生画刷框选交互 (Brush)
const brush = d3.brush().on("brush end", (event) => {
  const sel = event.selection;
  circles.attr("fill-opacity", d => isInside(sel, d) ? 1 : 0.15);
});
g.append("g").call(brush);`
    },

    plot: {
      metrics: { loc: '约 28 行', mentalModel: '图形语法 (Grammar of Graphics Marks)', paradigm: '现代声明式 / 纯函数返回 DOM' },
      code: `// Observable Plot 实现核心片段 (声明式图层正交组合)
const chart = Plot.plot({
  width, height: 440,
  x: { label: "研发营收比 (%) →", domain: [0, 80] },
  y: { label: "↑ 年增长率 (%)", domain: [-80, 200] },
  color: { domain: sectors, range: colorRange, legend: true },
  marks: [
    Plot.gridX(),
    Plot.gridY(),
    Plot.ruleY([0], { stroke: "#94a3b8", strokeDasharray: "4 4" }),
    // 高阶统计变换：线性回归线
    Plot.linearRegressionY(data, { x: "rdRatio", y: "growthRate", strokeDasharray: "4 4" }),
    // 散点图元与通道映射
    Plot.dot(data, {
      x: "rdRatio",
      y: "growthRate",
      r: d => Math.sqrt(d.marketCap) * 0.75,
      fill: "sector",
      tip: true // 原生 Tooltip
    }),
    // 头部重点企业标注
    Plot.text(topData, { x: "rdRatio", y: "growthRate", text: "name", dy: -10 })
  ]
});

container.appendChild(chart);`
    }
  };

  function updateCodeInspector() {
    const item = CODE_SNIPPETS[state.activeCodeTab];
    if (!item) return;

    document.getElementById('metric-loc').textContent = item.metrics.loc;
    document.getElementById('metric-mental').textContent = item.metrics.mentalModel;
    document.getElementById('metric-paradigm').textContent = item.metrics.paradigm;
    document.getElementById('code-pre').textContent = item.code;
  }

  document.querySelectorAll('.code-tab-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.code-tab-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      state.activeCodeTab = btn.dataset.tab;
      updateCodeInspector();
    });
  });

  const copyCodeBtn = document.getElementById('btn-copy-code');
  if (copyCodeBtn) {
    copyCodeBtn.addEventListener('click', () => {
      const codeText = document.getElementById('code-pre').textContent;
      navigator.clipboard.writeText(codeText).then(() => {
        const originalText = copyCodeBtn.textContent;
        copyCodeBtn.textContent = '✓ 已复制到剪贴板';
        setTimeout(() => {
          copyCodeBtn.textContent = originalText;
        }, 1800);
      });
    });
  }

  // 3. 智能选型向导 (Decision Wizard) 计算引擎
  const WIZARD_RULES = {
    q1: { // 图表标准度
      a: { echarts: 35, d3: 10, plot: 25 },
      b: { echarts: 5, d3: 40, plot: 15 },
      c: { echarts: 15, d3: 15, plot: 40 }
    },
    q2: { // 研发周期
      a: { echarts: 30, d3: 5, plot: 25 },
      b: { echarts: 10, d3: 35, plot: 15 },
      c: { echarts: 20, d3: 15, plot: 35 }
    },
    q3: { // 宿主框架与架构
      a: { echarts: 30, d3: 15, plot: 25 },
      b: { echarts: 15, d3: 35, plot: 20 },
      c: { echarts: 10, d3: 15, plot: 40 }
    },
    q4: { // 交互特性
      a: { echarts: 35, d3: 10, plot: 10 },
      b: { echarts: 10, d3: 40, plot: 10 },
      c: { echarts: 15, d3: 15, plot: 35 }
    },
    q5: { // 数据量与性能
      a: { echarts: 40, d3: 10, plot: 10 },
      b: { echarts: 15, d3: 35, plot: 15 },
      c: { echarts: 20, d3: 20, plot: 35 }
    }
  };

  function calculateRecommendation() {
    let scoreE = 0, scoreD = 0, scoreP = 0;

    for (const [qid, answer] of Object.entries(state.wizardAnswers)) {
      const delta = WIZARD_RULES[qid][answer];
      if (delta) {
        scoreE += delta.echarts;
        scoreD += delta.d3;
        scoreP += delta.plot;
      }
    }

    const total = scoreE + scoreD + scoreP;
    const pctE = Math.round((scoreE / total) * 100);
    const pctD = Math.round((scoreD / total) * 100);
    const pctP = Math.round((scoreP / total) * 100);

    // 更新柱状条
    document.getElementById('bar-echarts').style.width = `${pctE}%`;
    document.getElementById('val-echarts').textContent = `${pctE}%`;
    document.getElementById('bar-d3').style.width = `${pctD}%`;
    document.getElementById('val-d3').textContent = `${pctD}%`;
    document.getElementById('bar-plot').style.width = `${pctP}%`;
    document.getElementById('val-plot').textContent = `${pctP}%`;

    // 生成结论
    const titleEl = document.getElementById('verdict-title');
    const textEl = document.getElementById('verdict-text');

    if (scoreE >= scoreD && scoreE >= scoreP) {
      titleEl.innerHTML = '🏆 首选推荐：<span style="color:var(--c-echarts);">Apache ECharts</span>';
      textEl.innerHTML = '您的业务场景高度偏向标准报表或商业仪表盘，注重研发交付效率与开箱即用的交互体验。ECharts 的全套图例、缩放条、中国地图支持以及针对大数据的 Canvas 优化是最佳适配方案。对于极个别特殊定制图形，可借助 ECharts 的 <code>custom series</code> 辅助实现。';
    } else if (scoreD >= scoreE && scoreD >= scoreP) {
      titleEl.innerHTML = '🏆 首选推荐：<span style="color:var(--c-d3);">D3.js (或 D3 + 现代框架混合)</span>';
      textEl.innerHTML = '您的项目具有极高的定制自由度要求，涵盖复杂的物理动画、非标拓扑图谱或细腻的微交互。D3 提供了底层 SVG / DOM 的完全掌控力。<b>工程建议：</b>在 React/Vue 项目中，建议将 D3 作为纯计算层（使用 <code>d3-scale</code>, <code>d3-shape</code>），由框架自身的 JSX/模板接管 DOM 渲染，以兼顾性能与响应式设计。';
    } else {
      titleEl.innerHTML = '🏆 首选推荐：<span style="color:var(--c-plot);">Observable Plot</span>';
      textEl.innerHTML = '您的诉求更侧重于现代探索性数据分析（EDA）与统计图表展示，追求优雅精炼的代码与声明式图层组合。Observable Plot 能够以极少代码实现分面（Faceting）和统计变换，生成的标准 SVG 节点能无缝嵌入任意现代前端框架组件树。';
    }
  }

  // 绑定 Wizard 单选按钮事件
  document.querySelectorAll('.wizard-step').forEach(step => {
    const qid = step.dataset.question;
    step.querySelectorAll('.option-btn').forEach(opt => {
      opt.addEventListener('click', () => {
        step.querySelectorAll('.option-btn').forEach(o => o.classList.remove('selected'));
        opt.classList.add('selected');
        state.wizardAnswers[qid] = opt.dataset.val;
        calculateRecommendation();
      });
    });
  });

  // 窗口重绘自适应
  window.addEventListener('resize', () => {
    if (chartInstances.echartsSingle) chartInstances.echartsSingle.resize();
    if (chartInstances.echartsGrid) chartInstances.echartsGrid.resize();
  });

  // 启动初次渲染
  renderActiveEngineView();
  updateCodeInspector();
  calculateRecommendation();
});
