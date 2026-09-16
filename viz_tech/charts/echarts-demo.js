/**
 * ECharts 演示实现
 * 特点展现:
 * 1. 开箱即用的企业级商业交互: Tooltip, Legend, DataZoom, Toolbox
 * 2. 气泡多维映射: X轴-研发占营收比, Y轴-年增长率, 气泡大小-企业市值, 颜色-行业分类
 * 3. Canvas 渲染引擎与平滑动画
 */
window.initEChartsDemo = function(containerId) {
  const container = document.getElementById(containerId);
  if (!container) return null;

  // 销毁旧实例防止重复绑定
  const oldInstance = echarts.getInstanceByDom(container);
  if (oldInstance) {
    oldInstance.dispose();
  }

  const chart = echarts.init(container, null, { renderer: 'canvas' });
  const rawData = window.VIZ_TECH_DATA;
  const sectors = window.VIZ_SECTORS;
  const colorMap = window.VIZ_SECTOR_COLORS;

  // 按领域拆分 series 便于原生图例切换与着色
  const series = sectors.map(sector => {
    const sectorData = rawData
      .filter(item => item.sector === sector)
      .map(item => [
        item.rdRatio,      // index 0: X
        item.growthRate,    // index 1: Y
        item.marketCap,     // index 2: 气泡大小
        item.name,          // index 3: 企业名称
        item.rdSpend,       // index 4: 研发金额
        item.employees,     // index 5: 员工
        item.sector         // index 6: 赛道
      ]);

    return {
      name: sector,
      type: 'scatter',
      data: sectorData,
      symbolSize: function(val) {
        // 市值开方映射为视觉半径 (5px ~ 42px)
        return Math.max(8, Math.min(46, Math.sqrt(val[2]) * 0.78));
      },
      itemStyle: {
        color: colorMap[sector],
        opacity: 0.78,
        borderColor: '#ffffff',
        borderWidth: 1.5,
        shadowBlur: 8,
        shadowColor: 'rgba(0,0,0,0.12)'
      },
      emphasis: {
        focus: 'series',
        itemStyle: {
          opacity: 1,
          borderColor: '#0f172a',
          borderWidth: 2,
          shadowBlur: 14,
          shadowColor: 'rgba(0,0,0,0.25)'
        }
      }
    };
  });

  const option = {
    backgroundColor: 'transparent',
    grid: {
      top: 60,
      right: 40,
      bottom: 80,
      left: 60,
      containLabel: true
    },
    tooltip: {
      trigger: 'item',
      backgroundColor: 'rgba(255, 255, 255, 0.96)',
      borderColor: '#E2E8F0',
      borderWidth: 1,
      padding: [10, 14],
      textStyle: { color: '#1E293B', fontSize: 13 },
      extraCssText: 'box-shadow: 0 10px 25px -5px rgba(0,0,0,0.1), 0 8px 10px -6px rgba(0,0,0,0.1); border-radius: 8px;',
      formatter: function(params) {
        const d = params.value;
        const color = colorMap[d[6]] || '#3B82F6';
        return `
          <div style="font-weight: 700; font-size: 15px; margin-bottom: 6px; display:flex; align-items:center; gap:6px;">
            <span style="display:inline-block;width:10px;height:10px;border-radius:50%;background:${color};"></span>
            ${d[3]}
            <span style="font-size:11px;font-weight:normal;color:#64748B;padding:1px 6px;background:#F1F5F9;border-radius:4px;">${d[6]}</span>
          </div>
          <div style="font-size: 12px; color: #475569; line-height: 1.7;">
            <div>研发占营收比: <b style="color:#0F172A;">${d[0]}%</b></div>
            <div>年度营收增速: <b style="color:${d[1] >= 0 ? '#16A34A' : '#DC2626'};">${d[1] > 0 ? '+' : ''}${d[1]}%</b></div>
            <div>企业估值/市值: <b style="color:#0F172A;">$${d[2]} 亿</b></div>
            <div>年度研发支出: <b style="color:#0F172A;">$${d[4]} 亿</b></div>
          </div>
        `;
      }
    },
    toolbox: {
      right: 15,
      top: 10,
      feature: {
        dataZoom: { title: { zoom: '区域缩放', back: '还原缩放' } },
        restore: { title: '复位' },
        saveAsImage: { title: '导出图片', pixelRatio: 2 }
      },
      iconStyle: {
        borderColor: '#64748B'
      }
    },
    legend: {
      top: 12,
      left: 60,
      orient: 'horizontal',
      itemWidth: 12,
      itemHeight: 12,
      icon: 'circle',
      textStyle: { color: '#475569', fontSize: 12 }
    },
    xAxis: {
      type: 'value',
      name: '研发投入营收占比 (%)',
      nameLocation: 'middle',
      nameGap: 32,
      nameTextStyle: { color: '#64748B', fontSize: 12 },
      min: 0,
      max: 80,
      splitLine: { lineStyle: { type: 'dashed', color: '#E2E8F0' } },
      axisLine: { lineStyle: { color: '#CBD5E1' } },
      axisLabel: { color: '#64748B', formatter: '{value}%' }
    },
    yAxis: {
      type: 'value',
      name: '年营收增长率 (%)',
      nameTextStyle: { color: '#64748B', fontSize: 12 },
      min: -80,
      max: 200,
      splitLine: { lineStyle: { type: 'dashed', color: '#E2E8F0' } },
      axisLine: { lineStyle: { color: '#CBD5E1' } },
      axisLabel: { color: '#64748B', formatter: '{value}%' }
    },
    dataZoom: [
      {
        type: 'slider',
        show: true,
        xAxisIndex: [0],
        start: 0,
        end: 100,
        height: 20,
        bottom: 12,
        borderColor: 'transparent',
        fillerColor: 'rgba(59, 130, 246, 0.12)',
        handleStyle: { color: '#3B82F6' },
        textStyle: { color: '#94A3B8', fontSize: 10 }
      },
      {
        type: 'inside',
        xAxisIndex: [0]
      }
    ],
    series: series
  };

  chart.setOption(option);

  // 监听窗口缩放
  window.addEventListener('resize', () => chart.resize());

  return chart;
};
