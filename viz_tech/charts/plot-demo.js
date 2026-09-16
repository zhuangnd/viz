/**
 * Observable Plot 演示实现
 * 特点展现:
 * 1. 纯正的图形语法 (Grammar of Graphics): 极度简洁的 Mark 图层堆叠
 * 2. 声明式通道映射 (x, y, r, fill, stroke) 与内置统计变换 (linearRegressionY)
 * 3. 纯函数式设计: 输入配置对象，直接返回标准 SVG DOM 元素挂载
 * 4. 内置小多组分面 (Faceting) 与原生色彩图例 (Color Legend)
 */
window.initPlotDemo = function(containerId, options = {}) {
  const container = document.getElementById(containerId);
  if (!container) return null;
  container.innerHTML = "";

  const data = window.VIZ_TECH_DATA;
  const sectors = window.VIZ_SECTORS;
  const colorMap = window.VIZ_SECTOR_COLORS;
  const colorRange = sectors.map(s => colorMap[s]);

  const showRegression = options.showRegression !== false;
  const facetMode = options.facetMode || 'none'; // 'none' | 'region'

  const width = container.clientWidth || 720;
  const height = facetMode === 'region' ? 520 : 440;

  // 基础 Marks 图层
  const marks = [
    Plot.gridX({ stroke: "#E2E8F0", strokeDasharray: "3 3" }),
    Plot.gridY({ stroke: "#E2E8F0", strokeDasharray: "3 3" }),
    Plot.ruleY([0], { stroke: "#94A3B8", strokeWidth: 1.2, strokeDasharray: "4 4" }),
  ];

  // 线性回归拟合趋势线 (Plot 内置高阶统计变换)
  if (showRegression) {
    marks.push(
      Plot.linearRegressionY(data, {
        x: "rdRatio",
        y: "growthRate",
        stroke: "#64748B",
        strokeWidth: 2,
        strokeDasharray: "5 5",
        title: "全行业线性回归趋势线"
      })
    );
  }

  // 散点图元 (Dot Mark)
  const dotConfig = {
    x: "rdRatio",
    y: "growthRate",
    r: d => Math.sqrt(d.marketCap) * 0.75,
    fill: "sector",
    stroke: "#FFFFFF",
    strokeWidth: 1.5,
    fillOpacity: 0.78,
    tip: true, // Plot 原生智能 Tooltip
    title: d => `${d.name} (${d.sector})\n研发营收比: ${d.rdRatio}%\n年增速: ${d.growthRate}%\n估值: $${d.marketCap} 亿\n区域: ${d.region}`
  };

  if (facetMode === 'region') {
    dotConfig.fx = "region"; // 分面横轴映射
  }

  marks.push(Plot.dot(data, dotConfig));

  // 标注特定代表性企业标签 (Text Mark)
  marks.push(
    Plot.text(
      data.filter(d => d.marketCap > 1000 || d.growthRate > 150 || d.rdRatio > 70),
      {
        x: "rdRatio",
        y: "growthRate",
        text: "name",
        dy: -10,
        fontSize: 10,
        fill: "#1E293B",
        fontWeight: 600
      }
    )
  );

  // 组装声明式 Plot Spec
  const plotSpec = {
    width: width,
    height: height,
    inset: 12,
    style: {
      background: "transparent",
      fontFamily: "inherit",
      fontSize: "12px",
      overflow: "visible"
    },
    x: {
      label: "研发投入营收占比 (%) →",
      domain: [0, 80],
      ticks: 8,
      tickFormat: d => `${d}%`
    },
    y: {
      label: "↑ 年营收增长率 (%)",
      domain: [-80, 200],
      ticks: 8,
      tickFormat: d => `${d}%`
    },
    color: {
      domain: sectors,
      range: colorRange,
      legend: true
    },
    marks: marks
  };

  // 生成纯净 SVG 节点并挂载
  const chartNode = Plot.plot(plotSpec);
  container.appendChild(chartNode);

  return {
    node: chartNode,
    spec: plotSpec
  };
};
