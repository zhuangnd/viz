/**
 * D3.js 演示实现
 * 特点展现:
 * 1. 显式控制 SVG 原生图元与数据绑定 (Enter-Update-Exit)
 * 2. 纯数学比例尺 (d3.scaleLinear, d3.scaleSqrt, d3.scaleOrdinal)
 * 3. 缓动入场动画与交互式画刷圈选 (d3.brush)
 * 4. 圈选区域动态统计计算 (数据驱动微交互)
 */
window.initD3Demo = function(containerId) {
  const container = document.getElementById(containerId);
  if (!container) return null;
  container.innerHTML = "";

  const data = window.VIZ_TECH_DATA;
  const colorMap = window.VIZ_SECTOR_COLORS;

  const margin = { top: 40, right: 30, bottom: 65, left: 60 };
  const width = container.clientWidth || 720;
  const height = 480;
  const innerWidth = width - margin.left - margin.right;
  const innerHeight = height - margin.top - margin.bottom;

  // 创建 SVG 画布
  const svg = d3.select(container)
    .append("svg")
    .attr("width", "100%")
    .attr("height", height)
    .attr("viewBox", `0 0 ${width} ${height}`)
    .attr("style", "overflow: visible; font-family: inherit;");

  // 比例尺定义
  const xScale = d3.scaleLinear()
    .domain([0, 80])
    .range([0, innerWidth]);

  const yScale = d3.scaleLinear()
    .domain([-80, 200])
    .range([innerHeight, 0]);

  const rScale = d3.scaleSqrt()
    .domain([0, d3.max(data, d => d.marketCap)])
    .range([5, 32]);

  const g = svg.append("g")
    .attr("transform", `translate(${margin.left},${margin.top})`);

  // 网格线
  g.append("g")
    .attr("class", "grid grid-x")
    .attr("transform", `translate(0,${innerHeight})`)
    .call(d3.axisBottom(xScale).ticks(8).tickSize(-innerHeight).tickFormat(""))
    .selectAll(".tick line")
    .attr("stroke", "#E2E8F0")
    .attr("stroke-dasharray", "3 3");

  g.append("g")
    .attr("class", "grid grid-y")
    .call(d3.axisLeft(yScale).ticks(8).tickSize(-innerWidth).tickFormat(""))
    .selectAll(".tick line")
    .attr("stroke", "#E2E8F0")
    .attr("stroke-dasharray", "3 3");

  // 0刻度基准参考线
  g.append("line")
    .attr("x1", 0)
    .attr("x2", innerWidth)
    .attr("y1", yScale(0))
    .attr("y2", yScale(0))
    .attr("stroke", "#94A3B8")
    .attr("stroke-width", 1.2)
    .attr("stroke-dasharray", "4 4");

  // X 坐标轴
  const xAxisGroup = g.append("g")
    .attr("transform", `translate(0,${innerHeight})`)
    .call(d3.axisBottom(xScale).ticks(8).tickFormat(d => `${d}%`));

  xAxisGroup.select(".domain").attr("stroke", "#CBD5E1");
  xAxisGroup.selectAll("text").attr("fill", "#64748B").attr("font-size", "11px");

  // X 轴标签
  g.append("text")
    .attr("x", innerWidth / 2)
    .attr("y", innerHeight + 42)
    .attr("fill", "#64748B")
    .attr("font-size", "12px")
    .attr("text-anchor", "middle")
    .text("研发投入营收占比 (%)");

  // Y 坐标轴
  const yAxisGroup = g.append("g")
    .call(d3.axisLeft(yScale).ticks(8).tickFormat(d => `${d}%`));

  yAxisGroup.select(".domain").attr("stroke", "#CBD5E1");
  yAxisGroup.selectAll("text").attr("fill", "#64748B").attr("font-size", "11px");

  // Y 轴标签
  g.append("text")
    .attr("transform", "rotate(-90)")
    .attr("x", -innerHeight / 2)
    .attr("y", -42)
    .attr("fill", "#64748B")
    .attr("font-size", "12px")
    .attr("text-anchor", "middle")
    .text("年营收增长率 (%)");

  // Tooltip 浮层容器 (DOM)
  let tooltip = d3.select(container).select(".d3-custom-tooltip");
  if (tooltip.empty()) {
    tooltip = d3.select(container)
      .append("div")
      .attr("class", "d3-custom-tooltip")
      .style("position", "absolute")
      .style("visibility", "hidden")
      .style("background", "rgba(255, 255, 255, 0.96)")
      .style("border", "1px solid #E2E8F0")
      .style("border-radius", "8px")
      .style("padding", "10px 14px")
      .style("box-shadow", "0 10px 25px -5px rgba(0,0,0,0.1)")
      .style("pointer-events", "none")
      .style("font-size", "12px")
      .style("z-index", "10");
  }

  // 绘制数据圆点 (Enter Transition)
  const dotsGroup = g.append("g").attr("class", "dots-group");

  const circles = dotsGroup.selectAll("circle")
    .data(data)
    .enter()
    .append("circle")
    .attr("cx", d => xScale(d.rdRatio))
    .attr("cy", d => yScale(d.growthRate))
    .attr("r", 0) // 从 0 启动缓动
    .attr("fill", d => colorMap[d.sector] || "#3B82F6")
    .attr("fill-opacity", 0.75)
    .attr("stroke", "#FFFFFF")
    .attr("stroke-width", 1.5)
    .style("cursor", "pointer")
    .on("mouseenter", function(event, d) {
      d3.select(this)
        .transition().duration(150)
        .attr("stroke", "#0F172A")
        .attr("stroke-width", 2.5)
        .attr("fill-opacity", 1);

      tooltip.html(`
        <div style="font-weight:700;font-size:14px;color:#0F172A;margin-bottom:4px;">
          ${d.name} <span style="font-size:11px;font-weight:400;color:${colorMap[d.sector]};">[${d.sector}]</span>
        </div>
        <div style="color:#475569;line-height:1.6;">
          <div>研发占比: <b>${d.rdRatio}%</b> | 增速: <b>${d.growthRate}%</b></div>
          <div>市值/估值: <b>$${d.marketCap} 亿</b> | 研发额: <b>$${d.rdSpend} 亿</b></div>
        </div>
      `)
      .style("visibility", "visible");
    })
    .on("mousemove", function(event) {
      const bounds = container.getBoundingClientRect();
      const x = event.clientX - bounds.left + 15;
      const y = event.clientY - bounds.top - 20;
      tooltip.style("left", `${x}px`).style("top", `${y}px`);
    })
    .on("mouseleave", function() {
      d3.select(this)
        .transition().duration(150)
        .attr("stroke", "#FFFFFF")
        .attr("stroke-width", 1.5)
        .attr("fill-opacity", 0.75);
      tooltip.style("visibility", "hidden");
    });

  // 触发 D3 弹性质感入场动画
  circles.transition()
    .duration(850)
    .delay((d, i) => i * 18)
    .ease(d3.easeCubicOut)
    .attr("r", d => rScale(d.marketCap));

  // D3 特色交互：画刷圈选 (Brush) 统计
  const brushGroup = g.append("g").attr("class", "brush");
  const brush = d3.brush()
    .extent([[0, 0], [innerWidth, innerHeight]])
    .on("start brush end", brushed);

  brushGroup.call(brush);

  // 状态统计条 (HUD)
  const hud = d3.select(container).select(".d3-hud");
  function brushed(event) {
    const selection = event.selection;
    if (!selection) {
      circles.attr("fill-opacity", 0.75).attr("stroke", "#FFFFFF");
      if (!hud.empty()) {
        hud.html(`💡 <b>D3 微交互提示：</b>可在图表任意区域拖拽鼠标<b>绘制方框（Brush）</b>进行多点批量圈选与动态聚合分析。`);
      }
      return;
    }

    const [[x0, y0], [x1, y1]] = selection;
    const selected = [];

    circles.each(function(d) {
      const cx = xScale(d.rdRatio);
      const cy = yScale(d.growthRate);
      const isInside = cx >= x0 && cx <= x1 && cy >= y0 && cy <= y1;
      d3.select(this)
        .attr("fill-opacity", isInside ? 1 : 0.12)
        .attr("stroke", isInside ? "#0F172A" : "#FFFFFF")
        .attr("stroke-width", isInside ? 2 : 1);
      if (isInside) selected.push(d);
    });

    if (!hud.empty()) {
      if (selected.length > 0) {
        const avgGrowth = (d3.mean(selected, d => d.growthRate)).toFixed(1);
        const totalCap = (d3.sum(selected, d => d.marketCap)).toFixed(0);
        hud.html(`🎯 <b>圈选成功：</b> 选中 <b>${selected.length}</b> 家企业 | 平均增速: <b style="color:${avgGrowth >= 0 ? '#16A34A' : '#DC2626'}">${avgGrowth}%</b> | 累计总估值: <b>$${totalCap} 亿</b> <a href="javascript:void(0)" id="d3-clear-brush" style="margin-left:10px;color:#2563EB;text-decoration:underline;">清除圈选</a>`);
        const clearBtn = document.getElementById("d3-clear-brush");
        if (clearBtn) {
          clearBtn.onclick = () => brushGroup.call(brush.move, null);
        }
      } else {
        hud.html(`当前选区无数据点，松开鼠标或点击空白处重置。`);
      }
    }
  }

  return {
    resize: () => {
      window.initD3Demo(containerId);
    },
    resetAnimation: () => {
      circles.attr("r", 0)
        .transition()
        .duration(800)
        .delay((d, i) => i * 18)
        .ease(d3.easeCubicOut)
        .attr("r", d => rScale(d.marketCap));
    }
  };
};
