# -*- coding: utf-8 -*-
"""
Builds japan-travel-guide/v2.html with embedded vector SVG map and full interactive logic.
"""
import json

with open('japan-travel-guide/routes_v2_spec.json', 'r', encoding='utf-8') as f:
    bundle = json.load(f)

polygons_json = json.dumps(bundle['polygons'], ensure_ascii=False)
routes_json = json.dumps(bundle['routes'], ensure_ascii=False)

html_code = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>日本深度自游全景仪 v2 · 官方地理与文化纵深导览</title>
  <meta name="description" content="基于2026最新外务省、JNTO及JR体系构建的15-20日深度旅行系统。空间地理为轴、双模交通（公共交通/合规自驾）动态切换、D3高程剖面、全矢量独立地图引擎（零API依赖）。">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&family=Noto+Serif+SC:wght@500;700;900&family=Noto+Sans+SC:wght@300;400;500;600;700&display=swap" rel="stylesheet">
  
  <style>
    /* ==========================================================================
       设计系统基座 (Swiss-Japanese Grid & Semantic Color Palette)
       基调：和纸暖白 (浅色) / 玄武岩暗色 (暗色)
       路线色：Ai-iro 靛蓝 (#264653) · Shakudo 赤铜 (#BC4749) · Koke-iro 苔绿 (#386641)
       规则：零 Emoji · 纯 SVG 矢量图标 · 零外部地图API依赖
       ========================================================================== */
    :root {{
      --bg-washi: #F8F6F0;
      --bg-surface: #FFFFFF;
      --bg-surface-subtle: #F1EFE8;
      --bg-card: #FFFFFF;
      --text-main: #1D232A;
      --text-muted: #596573;
      --text-faint: #9AA5B1;
      --border-color: rgba(29, 35, 42, 0.12);
      --border-strong: rgba(29, 35, 42, 0.22);
      
      --c-ai: #264653;        /* 路线1: 靛蓝 */
      --c-shakudo: #BC4749;   /* 路线2: 赤铜 */
      --c-koke: #386641;      /* 路线3: 苔绿 */
      --c-gold: #D4A373;      /* 琥珀金 */
      --c-alert: #C92A2A;     /* 警示红 */
      --c-active: var(--c-ai);
      
      --map-sea: #E2ECE9;
      --map-land: #EDE8DC;
      --map-land-stroke: #C9C2B3;
      --map-ridge: rgba(140, 130, 115, 0.25);
      
      --font-serif: "Noto Serif SC", "Source Han Serif SC", STSong, serif;
      --font-mono: "JetBrains Mono", Consolas, monospace;
      --font-sans: "Noto Sans SC", system-ui, -apple-system, sans-serif;
      
      --shadow-sm: 0 1px 3px rgba(0,0,0,0.06);
      --shadow-md: 0 4px 12px rgba(0,0,0,0.08);
      --shadow-lg: 0 12px 28px rgba(0,0,0,0.12);
      --radius-sm: 4px;
      --radius-md: 8px;
      --radius-lg: 14px;
    }}

    body.dark-theme {{
      --bg-washi: #141619;
      --bg-surface: #1C1F24;
      --bg-surface-subtle: #242930;
      --bg-card: #1C1F24;
      --text-main: #ECEFF4;
      --text-muted: #9AA5B1;
      --text-faint: #616E7C;
      --border-color: rgba(255, 255, 255, 0.12);
      --border-strong: rgba(255, 255, 255, 0.22);
      
      --map-sea: #0E1217;
      --map-land: #262B33;
      --map-land-stroke: #3A424E;
      --map-ridge: rgba(255, 255, 255, 0.12);
    }}

    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    html {{ scroll-behavior: smooth; }}
    body {{
      font-family: var(--font-sans);
      background-color: var(--bg-washi);
      color: var(--text-main);
      line-height: 1.65;
      -webkit-font-smoothing: antialiased;
      transition: background-color 0.3s ease, color 0.3s ease;
    }}

    /* SVG Icon System */
    .icon {{
      display: inline-block;
      width: 1.15em;
      height: 1.15em;
      stroke-width: 2;
      stroke: currentColor;
      fill: none;
      stroke-linecap: round;
      stroke-linejoin: round;
      vertical-align: -0.18em;
    }}

    /* Global Header */
    header {{
      background: var(--bg-surface);
      border-bottom: 1px solid var(--border-color);
      position: sticky;
      top: 0;
      z-index: 1000;
      box-shadow: var(--shadow-sm);
    }}
    .header-inner {{
      max-width: 1720px;
      margin: 0 auto;
      padding: 0.65rem 1.25rem;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 1rem;
      flex-wrap: wrap;
    }}
    .brand-box {{
      display: flex;
      align-items: center;
      gap: 0.75rem;
    }}
    .brand-badge {{
      width: 36px;
      height: 36px;
      background: var(--c-active);
      color: #FFFFFF;
      font-family: var(--font-serif);
      font-weight: 900;
      font-size: 1.2rem;
      border-radius: var(--radius-sm);
      display: flex;
      align-items: center;
      justify-content: center;
      transition: background-color 0.3s;
    }}
    .brand-text h1 {{
      font-family: var(--font-serif);
      font-size: 1.1rem;
      font-weight: 700;
      letter-spacing: 0.5px;
    }}
    .brand-text p {{
      font-size: 0.72rem;
      color: var(--text-muted);
      font-family: var(--font-mono);
    }}

    /* Controls Group */
    .header-controls {{
      display: flex;
      align-items: center;
      gap: 0.6rem;
      flex-wrap: wrap;
    }}
    
    .segmented {{
      display: inline-flex;
      background: var(--bg-surface-subtle);
      padding: 3px;
      border-radius: var(--radius-md);
      border: 1px solid var(--border-color);
    }}
    .seg-btn {{
      padding: 0.38rem 0.75rem;
      font-size: 0.8rem;
      font-weight: 500;
      border: none;
      background: transparent;
      color: var(--text-muted);
      border-radius: var(--radius-sm);
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 0.35rem;
      transition: all 0.2s ease;
    }}
    .seg-btn.active {{
      background: var(--bg-surface);
      color: var(--text-main);
      font-weight: 600;
      box-shadow: var(--shadow-sm);
    }}
    .seg-btn[data-route="route-1"].active {{ color: var(--c-ai); }}
    .seg-btn[data-route="route-2"].active {{ color: var(--c-shakudo); }}
    .seg-btn[data-route="route-3"].active {{ color: var(--c-koke); }}

    .mode-toggle {{
      background: var(--bg-surface-subtle);
      border: 1px solid var(--border-color);
      border-radius: var(--radius-md);
      padding: 3px;
      display: inline-flex;
    }}
    .mode-btn {{
      padding: 0.38rem 0.75rem;
      font-size: 0.8rem;
      font-weight: 600;
      border: none;
      background: transparent;
      color: var(--text-muted);
      border-radius: var(--radius-sm);
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 0.35rem;
      transition: all 0.2s;
    }}
    .mode-btn.active {{
      background: var(--c-active);
      color: #FFFFFF;
    }}

    .action-btn {{
      background: var(--bg-surface-subtle);
      border: 1px solid var(--border-color);
      color: var(--text-main);
      padding: 0.42rem 0.8rem;
      border-radius: var(--radius-md);
      font-size: 0.8rem;
      font-weight: 500;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 0.35rem;
      transition: all 0.2s;
    }}
    .action-btn:hover {{
      background: var(--border-color);
    }}
    .action-btn.danger {{
      background: rgba(201, 42, 42, 0.08);
      border-color: rgba(201, 42, 42, 0.3);
      color: var(--c-alert);
      font-weight: 600;
    }}
    .action-btn.danger:hover {{
      background: rgba(201, 42, 42, 0.15);
    }}

    /* Global Alert Notice */
    .banner-alert {{
      background: rgba(201, 42, 42, 0.07);
      border-bottom: 1px solid rgba(201, 42, 42, 0.2);
      padding: 0.5rem 1.25rem;
      font-size: 0.8rem;
      color: var(--c-alert);
      display: flex;
      align-items: center;
      justify-content: space-between;
    }}
    .banner-alert-inner {{
      max-width: 1720px;
      margin: 0 auto;
      width: 100%;
      display: flex;
      align-items: center;
      gap: 0.6rem;
    }}
    .banner-alert a {{
      color: var(--c-alert);
      text-decoration: underline;
      font-weight: 700;
      cursor: pointer;
    }}

    /* App Main Grid: Tri-state Adaptive Shell */
    .app-layout {{
      max-width: 1720px;
      margin: 1.25rem auto;
      padding: 0 1.25rem;
      display: grid;
      grid-template-columns: 44% 56%;
      gap: 1.5rem;
      align-items: start;
    }}

    @media (max-width: 1180px) {{
      .app-layout {{ grid-template-columns: 1fr; }}
      .map-sticky-wrap {{ position: relative !important; top: 0 !important; }}
    }}

    /* Left Column: Narrative Stream */
    .narrative-stream {{
      display: flex;
      flex-direction: column;
      gap: 1.25rem;
    }}

    /* KPI Dashboard Cards */
    .kpi-board {{
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: var(--radius-lg);
      padding: 1.25rem;
      box-shadow: var(--shadow-sm);
      border-top: 4px solid var(--c-active);
      transition: border-color 0.3s ease;
    }}
    .kpi-header {{
      display: flex;
      align-items: flex-start;
      justify-content: space-between;
      margin-bottom: 0.85rem;
      gap: 0.5rem;
    }}
    .kpi-title-area h2 {{
      font-family: var(--font-serif);
      font-size: 1.3rem;
      font-weight: 700;
      line-height: 1.35;
      margin-bottom: 0.35rem;
    }}
    .kpi-title-area p {{
      font-size: 0.84rem;
      color: var(--text-muted);
    }}
    .kpi-badge {{
      font-size: 0.72rem;
      font-family: var(--font-mono);
      font-weight: 600;
      padding: 0.2rem 0.5rem;
      border-radius: var(--radius-sm);
      background: var(--bg-surface-subtle);
      border: 1px solid var(--border-color);
      white-space: nowrap;
    }}
    
    .kpi-grid {{
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 0.75rem;
      padding-top: 0.85rem;
      border-top: 1px dashed var(--border-color);
    }}
    @media (max-width: 600px) {{
      .kpi-grid {{ grid-template-columns: repeat(2, 1fr); }}
    }}
    .kpi-stat-item {{
      display: flex;
      flex-direction: column;
    }}
    .kpi-stat-label {{
      font-size: 0.72rem;
      color: var(--text-faint);
      display: flex;
      align-items: center;
      gap: 0.25rem;
    }}
    .kpi-stat-value {{
      font-family: var(--font-mono);
      font-size: 1.05rem;
      font-weight: 700;
      color: var(--text-main);
      margin-top: 0.15rem;
    }}

    .season-info-box {{
      background: var(--bg-surface-subtle);
      border-radius: var(--radius-md);
      padding: 0.85rem 1rem;
      margin-top: 0.85rem;
      font-size: 0.825rem;
      color: var(--text-muted);
      border-left: 3px solid var(--c-gold);
      display: flex;
      gap: 0.6rem;
      align-items: flex-start;
    }}

    /* Day Card Styles */
    .timeline-container {{
      display: flex;
      flex-direction: column;
      gap: 1rem;
    }}
    .day-card {{
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: var(--radius-md);
      padding: 1.15rem;
      box-shadow: var(--shadow-sm);
      transition: all 0.2s ease;
      cursor: pointer;
      position: relative;
    }}
    .day-card:hover {{
      border-color: var(--border-strong);
      transform: translateY(-1px);
      box-shadow: var(--shadow-md);
    }}
    .day-card.selected {{
      border-color: var(--c-active);
      box-shadow: 0 0 0 2px var(--c-active);
      background: var(--bg-surface);
    }}
    .day-top-row {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 0.45rem;
    }}
    .day-num-badge {{
      font-family: var(--font-mono);
      font-size: 0.75rem;
      font-weight: 700;
      background: var(--bg-surface-subtle);
      color: var(--text-main);
      padding: 0.18rem 0.5rem;
      border-radius: var(--radius-sm);
      letter-spacing: 0.5px;
    }}
    .day-elev-tag {{
      font-family: var(--font-mono);
      font-size: 0.72rem;
      color: var(--c-active);
      background: var(--bg-surface-subtle);
      border: 1px solid var(--border-color);
      padding: 0.15rem 0.45rem;
      border-radius: var(--radius-sm);
      display: inline-flex;
      align-items: center;
      gap: 0.25rem;
    }}
    .day-title {{
      font-family: var(--font-serif);
      font-size: 1.05rem;
      font-weight: 700;
      color: var(--text-main);
      margin-bottom: 0.4rem;
    }}
    .day-story {{
      font-size: 0.84rem;
      color: var(--text-muted);
      line-height: 1.6;
      margin-bottom: 0.75rem;
    }}

    /* Transport Mode Card Details */
    .mode-subcard {{
      background: var(--bg-surface-subtle);
      border-radius: var(--radius-sm);
      padding: 0.75rem;
      margin-bottom: 0.65rem;
      border-left: 3px solid var(--c-active);
      font-size: 0.8rem;
    }}
    .mode-subcard-title {{
      font-weight: 700;
      font-size: 0.825rem;
      display: flex;
      align-items: center;
      gap: 0.35rem;
      margin-bottom: 0.35rem;
    }}
    .mode-grid-specs {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(130px, 1fr));
      gap: 0.4rem;
      margin-top: 0.35rem;
      font-family: var(--font-mono);
      font-size: 0.75rem;
    }}
    .mode-spec-item {{
      color: var(--text-muted);
    }}
    .mode-spec-item strong {{
      color: var(--text-main);
    }}

    .day-foot-meta {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 0.5rem;
      padding-top: 0.65rem;
      border-top: 1px dashed var(--border-color);
      font-size: 0.78rem;
    }}
    .meta-box-title {{
      font-size: 0.72rem;
      color: var(--text-faint);
      display: flex;
      align-items: center;
      gap: 0.25rem;
      margin-bottom: 0.15rem;
    }}
    .tabelog-badge {{
      font-family: var(--font-mono);
      font-weight: 700;
      color: #B45309;
      background: #FEF3C7;
      padding: 0.05rem 0.3rem;
      border-radius: 3px;
      font-size: 0.7rem;
      margin-left: 0.25rem;
    }}

    /* Right Column: Sticky Cartographic Viewport */
    .map-sticky-wrap {{
      position: sticky;
      top: 4.8rem;
      display: flex;
      flex-direction: column;
      gap: 0.75rem;
    }}
    .map-canvas-card {{
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: var(--radius-lg);
      overflow: hidden;
      box-shadow: var(--shadow-md);
      display: flex;
      flex-direction: column;
    }}
    .map-toolbar {{
      padding: 0.75rem 1rem;
      background: var(--bg-surface);
      border-bottom: 1px solid var(--border-color);
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 0.5rem;
    }}
    .map-status-text {{
      font-family: var(--font-serif);
      font-size: 0.95rem;
      font-weight: 700;
      display: flex;
      align-items: center;
      gap: 0.4rem;
    }}
    .map-badge-guarantee {{
      font-family: var(--font-mono);
      font-size: 0.68rem;
      color: #047857;
      background: #D1FAE5;
      padding: 0.2rem 0.45rem;
      border-radius: 4px;
      display: inline-flex;
      align-items: center;
      gap: 0.25rem;
    }}
    
    .map-viewport {{
      width: 100%;
      height: 520px;
      background: var(--map-sea);
      position: relative;
      overflow: hidden;
      cursor: grab;
      user-select: none;
    }}
    .map-viewport:active {{ cursor: grabbing; }}
    
    #japan-svg-map {{
      width: 100%;
      height: 100%;
      display: block;
    }}
    .land-path {{
      fill: var(--map-land);
      stroke: var(--map-land-stroke);
      stroke-width: 0.75;
      transition: fill 0.3s, stroke 0.3s;
    }}
    .route-track-line {{
      fill: none;
      stroke-linecap: round;
      stroke-linejoin: round;
      transition: stroke 0.3s;
    }}
    .route-animated-dash {{
      fill: none;
      stroke: #FFFFFF;
      stroke-width: 2;
      stroke-dasharray: 6 12;
      animation: dashMove 25s linear infinite;
    }}
    @keyframes dashMove {{
      from {{ stroke-dashoffset: 400; }}
      to {{ stroke-dashoffset: 0; }}
    }}

    .map-node {{
      cursor: pointer;
    }}
    .map-node circle {{
      stroke-width: 2;
      stroke: #FFFFFF;
      filter: drop-shadow(0 2px 4px rgba(0,0,0,0.25));
      transition: r 0.18s ease, stroke 0.18s ease, stroke-width 0.18s ease, filter 0.18s ease;
    }}
    .map-node:hover circle {{
      r: 13;
      stroke-width: 3;
      filter: drop-shadow(0 3px 6px rgba(0,0,0,0.45));
    }}
    .map-node.active-node circle {{
      r: 14;
      stroke-width: 3.5;
      stroke: var(--c-gold);
      filter: drop-shadow(0 0 8px rgba(212, 163, 115, 0.75));
    }}
    .map-node-num {{
      font-family: var(--font-mono);
      font-size: 9px;
      font-weight: 700;
      fill: #FFFFFF !important;
      text-anchor: middle;
      dominant-baseline: central;
      pointer-events: none;
      user-select: none;
    }}
    .map-node-label {{
      font-family: var(--font-sans);
      font-size: 11px;
      font-weight: 600;
      fill: var(--text-main);
      paint-order: stroke;
      stroke: var(--bg-surface);
      stroke-width: 1px;
      pointer-events: none;
      user-select: none;
      transition: fill 0.18s ease, font-weight 0.18s ease;
    }}
    .map-node:hover .map-node-label,
    .map-node.active-node .map-node-label {{
      fill: var(--c-active);
      font-weight: 700;
    }}

    /* Map Controls Float */
    .map-controls-float {{
      position: absolute;
      right: 12px;
      bottom: 12px;
      display: flex;
      flex-direction: column;
      gap: 4px;
      z-index: 10;
    }}
    .map-ctrl-btn {{
      width: 32px;
      height: 32px;
      border-radius: var(--radius-sm);
      background: var(--bg-surface);
      border: 1px solid var(--border-color);
      color: var(--text-main);
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      box-shadow: var(--shadow-sm);
    }}
    .map-ctrl-btn:hover {{ background: var(--bg-surface-subtle); }}

    /* Elevation Profile Dock */
    .elevation-dock {{
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: var(--radius-lg);
      padding: 0.85rem 1rem;
      box-shadow: var(--shadow-sm);
    }}
    .elev-header {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 0.4rem;
      font-size: 0.78rem;
    }}
    .elev-header h4 {{
      font-family: var(--font-serif);
      font-size: 0.85rem;
      font-weight: 700;
      display: flex;
      align-items: center;
      gap: 0.35rem;
    }}
    .elev-readout {{
      font-family: var(--font-mono);
      font-size: 0.75rem;
      color: var(--c-active);
      font-weight: 600;
    }}
    #elevation-svg {{
      width: 100%;
      height: 90px;
      display: block;
      overflow: visible;
    }}

    /* Full Width Lower Section: Budget Sandbox & Specs */
    .lower-section {{
      max-width: 1720px;
      margin: 2rem auto;
      padding: 0 1.25rem;
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 1.5rem;
    }}
    @media (max-width: 1024px) {{
      .lower-section {{ grid-template-columns: 1fr; }}
    }}

    .box-card {{
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: var(--radius-lg);
      padding: 1.25rem;
      box-shadow: var(--shadow-sm);
    }}
    .box-card-title {{
      font-family: var(--font-serif);
      font-size: 1.15rem;
      font-weight: 700;
      margin-bottom: 1rem;
      display: flex;
      align-items: center;
      justify-content: space-between;
      border-bottom: 1px solid var(--border-color);
      padding-bottom: 0.65rem;
    }}

    /* Sandbox Sliders */
    .slider-row {{
      display: flex;
      flex-direction: column;
      gap: 0.35rem;
      margin-bottom: 1rem;
    }}
    .slider-label {{
      display: flex;
      justify-content: space-between;
      font-size: 0.82rem;
      font-weight: 600;
    }}
    .slider-label span:last-child {{
      font-family: var(--font-mono);
      color: var(--c-active);
    }}
    .custom-range {{
      width: 100%;
      height: 6px;
      background: var(--bg-surface-subtle);
      border-radius: 3px;
      outline: none;
      -webkit-appearance: none;
    }}
    .custom-range::-webkit-slider-thumb {{
      -webkit-appearance: none;
      width: 18px;
      height: 18px;
      border-radius: 50%;
      background: var(--c-active);
      cursor: pointer;
      box-shadow: var(--shadow-sm);
    }}

    .budget-result-display {{
      background: var(--bg-surface-subtle);
      border-radius: var(--radius-md);
      padding: 1rem;
      border-left: 4px solid var(--c-active);
    }}
    .budget-total-num {{
      font-family: var(--font-mono);
      font-size: 1.7rem;
      font-weight: 700;
      color: var(--c-active);
      display: flex;
      align-items: baseline;
      gap: 0.5rem;
    }}
    .budget-total-num small {{
      font-size: 0.85rem;
      color: var(--text-muted);
    }}

    .stacked-bar {{
      height: 8px;
      border-radius: 4px;
      background: rgba(0,0,0,0.08);
      display: flex;
      overflow: hidden;
      margin: 0.75rem 0;
    }}
    .stacked-seg {{ height: 100%; }}

    .budget-legend-grid {{
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 0.4rem;
      font-size: 0.75rem;
      font-family: var(--font-mono);
    }}

    /* Modals */
    .modal-backdrop {{
      position: fixed;
      inset: 0;
      background: rgba(0,0,0,0.6);
      backdrop-filter: blur(3px);
      z-index: 2000;
      display: none;
      align-items: center;
      justify-content: center;
      padding: 1rem;
    }}
    .modal-backdrop.active {{ display: flex; }}
    .modal-box {{
      background: var(--bg-surface);
      border-radius: var(--radius-lg);
      max-width: 780px;
      width: 100%;
      max-height: 88vh;
      overflow-y: auto;
      box-shadow: var(--shadow-lg);
      border: 1px solid var(--border-color);
      display: flex;
      flex-direction: column;
    }}
    .modal-header {{
      padding: 1rem 1.25rem;
      border-bottom: 1px solid var(--border-color);
      display: flex;
      align-items: center;
      justify-content: space-between;
      position: sticky;
      top: 0;
      background: var(--bg-surface);
      z-index: 2;
    }}
    .modal-header h3 {{
      font-family: var(--font-serif);
      font-size: 1.15rem;
      font-weight: 700;
      display: flex;
      align-items: center;
      gap: 0.4rem;
    }}
    .modal-close-btn {{
      background: none;
      border: none;
      font-size: 1.25rem;
      cursor: pointer;
      color: var(--text-muted);
    }}
    .modal-content {{
      padding: 1.25rem;
      font-size: 0.85rem;
      line-height: 1.65;
    }}

    /* Visa Table Formatter */
    .visa-table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 0.75rem;
      margin-top: 1rem;
    }}
    .visa-table th, .visa-table td {{
      border: 1px solid var(--border-color);
      padding: 0.45rem 0.6rem;
      text-align: left;
    }}
    .visa-table th {{
      background: var(--bg-surface-subtle);
      font-family: var(--font-mono);
      font-weight: 700;
    }}

    /* Tooltip */
    #node-tooltip {{
      position: absolute;
      pointer-events: none;
      background: var(--bg-surface);
      color: var(--text-main);
      padding: 0.4rem 0.65rem;
      border-radius: var(--radius-sm);
      font-size: 0.75rem;
      box-shadow: var(--shadow-md);
      border: 1px solid var(--border-color);
      display: none;
      z-index: 100;
      transform: translate(-50%, -120%);
      white-space: nowrap;
    }}
  </style>
</head>
<body>

  <!-- Sticky Header -->
  <header>
    <div class="header-inner">
      <div class="brand-box">
        <div class="brand-badge" id="brand-badge">日</div>
        <div class="brand-text">
          <h1>日本深度自游全景仪 · v2</h1>
          <p>SPATIAL GIS · DUAL-MODE DYNAMICS · 2026 SPEC</p>
        </div>
      </div>

      <div class="header-controls">
        <!-- Route Segmented Switcher -->
        <div class="segmented" role="tablist">
          <button class="seg-btn active" data-route="route-1">
            <svg class="icon" viewBox="0 0 24 24"><polygon points="3 11 22 2 13 21 11 13 3 11"/></svg>
            路线一：本州脊梁 (18日)
          </button>
          <button class="seg-btn" data-route="route-2">
            <svg class="icon" viewBox="0 0 24 24"><path d="M4 15s1-1 4-1 5 2 8 2 4-1 4-1V3s-1 1-4 1-5-2-8-2-4 1-4 1z"/><line x1="4" y1="22" x2="4" y2="15"/></svg>
            路线二：山阴濑户 (17日)
          </button>
          <button class="seg-btn" data-route="route-3">
            <svg class="icon" viewBox="0 0 24 24"><path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/></svg>
            路线三：奥羽秘汤 (16日)
          </button>
        </div>

        <!-- Dual-Mode Transport Toggle -->
        <div class="mode-toggle">
          <button class="mode-btn active" data-mode="transit" id="btn-mode-transit">
            <svg class="icon" viewBox="0 0 24 24"><rect x="2" y="7" width="20" height="14" rx="2" ry="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/></svg>
            模式 A: 公共交通
          </button>
          <button class="mode-btn" data-mode="drive" id="btn-mode-drive">
            <svg class="icon" viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="3"/><line x1="12" y1="3" x2="12" y2="9"/><line x1="12" y1="15" x2="12" y2="21"/></svg>
            模式 B: 合规自驾
          </button>
        </div>

        <!-- Season Toggle -->
        <div class="segmented">
          <button class="seg-btn active" data-season="winter" id="season-winter">
            <svg class="icon" viewBox="0 0 24 24"><path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>
            1–2月 豪雪秘汤
          </button>
          <button class="seg-btn" data-season="autumn" id="season-autumn">
            <svg class="icon" viewBox="0 0 24 24"><path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 4.18 2 8 0 5.5-4.78 10-10 10Z"/></svg>
            9–10月 早秋自然
          </button>
        </div>

        <!-- Action Modals -->
        <button class="action-btn" id="btn-open-visa-modal">
          <svg class="icon" viewBox="0 0 24 24"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>
          送签行程单
        </button>
        <button class="action-btn danger" id="btn-open-legal-modal">
          <svg class="icon" viewBox="0 0 24 24"><polygon points="7.86 2 16.14 2 22 7.86 22 16.14 16.14 22 7.86 22 2 16.14 2 7.86 7.86 2"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
          自驾合规警示
        </button>
        <button class="action-btn" id="btn-toggle-theme" title="切换暗色/和纸白">
          <svg class="icon" viewBox="0 0 24 24"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/></svg>
        </button>
      </div>
    </div>
  </header>

  <!-- Legal & Visa Warning Ribbon -->
  <div class="banner-alert">
    <div class="banner-alert-inner">
      <svg class="icon" viewBox="0 0 24 24"><polygon points="7.86 2 16.14 2 22 7.86 22 16.14 16.14 22 7.86 22 2 16.14 2 7.86 7.86 2"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
      <div>
        <strong>2026 法律红线勘误：</strong>
        中国大陆驾照在日自驾属于<strong>非法无证驾驶犯罪</strong>（日本仅认可1949日内瓦公约IDP，无资质者租车行一律拒提车）；行程达 15–20 天必须申请 <strong>30 天单次签或多次往返签</strong>，15 天单次签将构成逾期滞留！
        <a id="link-show-legal">查阅日内瓦公约与外务省原文</a>
      </div>
    </div>
  </div>

  <!-- Main View: Left Scrollytelling + Right Sticky Map -->
  <main class="app-layout">
    
    <!-- LEFT COLUMN: Scrollytelling Narrative -->
    <div class="narrative-stream">
      
      <!-- KPI Overview Card -->
      <section class="kpi-board" id="kpi-board">
        <div class="kpi-header">
          <div class="kpi-title-area">
            <h2 id="kpi-route-title">本州脊梁与千年古道：中山道、北陆工艺、纪伊熊野纵贯线</h2>
            <p id="kpi-route-season-tip">最佳适行期：4–6月（新绿雪墙）、10–11月（阶梯红叶）</p>
          </div>
          <div class="kpi-badge" id="kpi-route-badge">ROUTE 01</div>
        </div>

        <div class="kpi-grid">
          <div class="kpi-stat-item">
            <span class="kpi-stat-label">
              <svg class="icon" viewBox="0 0 24 24"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
              建议日程
            </span>
            <span class="kpi-stat-value" id="kpi-days-val">18 天</span>
          </div>
          <div class="kpi-stat-item">
            <span class="kpi-stat-label">
              <svg class="icon" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
              总移动里程
            </span>
            <span class="kpi-stat-value" id="kpi-dist-val">880 km</span>
          </div>
          <div class="kpi-stat-item">
            <span class="kpi-stat-label">
              <svg class="icon" viewBox="0 0 24 24"><path d="M18 8h1a4 4 0 0 1 0 8h-1"/><path d="M2 8h16v9a4 4 0 0 1-4 4H6a4 4 0 0 1-4-4V8z"/></svg>
              古道徒步段
            </span>
            <span class="kpi-stat-value" id="kpi-trail-val">32 km</span>
          </div>
          <div class="kpi-stat-item">
            <span class="kpi-stat-label">
              <svg class="icon" viewBox="0 0 24 24"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
              起讫机场
            </span>
            <span class="kpi-stat-value" id="kpi-air-val" style="font-size: 0.85rem;">NGO ➔ KIX</span>
          </div>
        </div>

        <div class="season-info-box" id="season-info-box">
          <svg class="icon" viewBox="0 0 24 24" style="flex-shrink: 0; color: var(--c-gold);"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>
          <div id="season-info-content">
            <strong>物候适应：</strong>冬季豪雪期，信越与北陆白雪皑皑，五箇山与地狱谷极富诗意；上高地冬季闭山封路，自动换乘为松本城与安昙野冬线。
          </div>
        </div>
      </section>

      <!-- Day by Day Timeline Stream -->
      <section class="timeline-container" id="timeline-container">
        <!-- Rendered dynamically by JS -->
      </section>

    </div>

    <!-- RIGHT COLUMN: Sticky Cartography & Elevation Dock -->
    <div class="map-sticky-wrap">
      
      <!-- Self-Contained SVG Map Card -->
      <div class="map-canvas-card">
        <div class="map-toolbar">
          <div class="map-status-text">
            <svg class="icon" viewBox="0 0 24 24"><polygon points="1 6 1 22 8 18 16 22 23 18 23 2 16 6 8 2 1 6"/><line x1="8" y1="2" x2="8" y2="18"/><line x1="16" y1="6" x2="16" y2="22"/></svg>
            <span id="map-active-route-name">本州脊梁与千年古道 空间拓扑</span>
          </div>
          <div class="map-badge-guarantee">
            <svg class="icon" viewBox="0 0 24 24"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
            100% 独立矢量引擎 · 零API依赖
          </div>
        </div>

        <div class="map-viewport" id="map-viewport">
          <svg id="japan-svg-map" viewBox="0 0 1000 750" preserveAspectRatio="xMidYMid meet">
            <defs>
              <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
                <feGaussianBlur stdDeviation="3" result="blur" />
                <feComposite in="SourceGraphic" in2="blur" operator="over" />
              </filter>
            </defs>
            <g id="map-transform-group">
              <!-- Sea Labels -->
              <text x="320" y="320" fill="var(--border-strong)" font-size="16" font-family="var(--font-serif)" letter-spacing="4" opacity="0.6">日 本 海</text>
              <text x="750" y="580" fill="var(--border-strong)" font-size="16" font-family="var(--font-serif)" letter-spacing="4" opacity="0.6">太 平 洋</text>
              <text x="300" y="590" fill="var(--border-strong)" font-size="11" font-family="var(--font-serif)" opacity="0.5">濑户内海</text>
              
              <!-- Embedded Pre-projected Japan Land Polygons -->
              <g id="land-layer"></g>

              <!-- Active Route Track Polyline -->
              <path id="route-track-bg" class="route-track-line" stroke-width="5" opacity="0.75"></path>
              <path id="route-track-fg" class="route-animated-dash"></path>

              <!-- Route Station Nodes -->
              <g id="nodes-layer"></g>

              <!-- Interactive Elevation Probe Crosshair -->
              <g id="map-probe-group" style="display: none;">
                <circle id="probe-circle" r="8" fill="none" stroke="#FFFFFF" stroke-width="3" filter="url(#glow)"></circle>
                <circle id="probe-dot" r="4" fill="var(--c-gold)"></circle>
              </g>
            </g>
          </svg>

          <!-- Floating Zoom & Reset Controls -->
          <div class="map-controls-float">
            <button class="map-ctrl-btn" id="btn-zoom-in" title="放大">
              <svg class="icon" viewBox="0 0 24 24"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
            </button>
            <button class="map-ctrl-btn" id="btn-zoom-out" title="缩小">
              <svg class="icon" viewBox="0 0 24 24"><line x1="5" y1="12" x2="19" y2="12"/></svg>
            </button>
            <button class="map-ctrl-btn" id="btn-zoom-reset" title="还原全图">
              <svg class="icon" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="3"/></svg>
            </button>
          </div>

          <div id="node-tooltip"></div>
        </div>
      </div>

      <!-- D3 Elevation Profile Dock -->
      <div class="elevation-dock">
        <div class="elev-header">
          <h4>
            <svg class="icon" viewBox="0 0 24 24"><polygon points="3 11 22 2 13 21 11 13 3 11"/></svg>
            D3.js 全程高程与地势剖面图 (Elevation Profile)
          </h4>
          <span class="elev-readout" id="elev-readout">滑动光标实时探查海拔高程</span>
        </div>
        <svg id="elevation-svg" viewBox="0 0 600 90" preserveAspectRatio="none"></svg>
      </div>

    </div>

  </main>

  <!-- Lower Functional Section: Budget Sandbox & Specs -->
  <section class="lower-section">
    
    <!-- Budget Sandbox -->
    <div class="box-card">
      <div class="box-card-title">
        <span>
          <svg class="icon" viewBox="0 0 24 24"><rect x="2" y="4" width="20" height="16" rx="2"/><line x1="2" y1="10" x2="22" y2="10"/></svg>
          双模交通与动态预算精算沙盒
        </span>
        <span style="font-size: 0.75rem; color: var(--text-muted); font-family: var(--font-mono);">100円 ≈ 4.8元基准</span>
      </div>

      <div class="slider-row">
        <div class="slider-label">
          <span>同行人数 (影响人均租车/包车摊算)</span>
          <span id="slider-travelers-val">2 人同行</span>
        </div>
        <input type="range" class="custom-range" id="slider-travelers" min="1" max="4" value="2" step="1">
      </div>

      <div class="slider-row">
        <div class="slider-label">
          <span>旅行计划天数</span>
          <span id="slider-days-val">18 天</span>
        </div>
        <input type="range" class="custom-range" id="slider-days" min="15" max="20" value="18" step="1">
      </div>

      <div class="slider-row">
        <div class="slider-label">
          <span>住宿偏好档次</span>
          <span id="slider-stay-val">经典舒适档 (商务+3晚秘汤)</span>
        </div>
        <div class="segmented" style="width: 100%; display: grid; grid-template-columns: repeat(3, 1fr);">
          <button class="seg-btn" data-stay="economy" id="btn-stay-eco">经济深度档</button>
          <button class="seg-btn active" data-stay="comfort" id="btn-stay-com">经典舒适档</button>
          <button class="seg-btn" data-stay="luxury" id="btn-stay-lux">品质名宿档</button>
        </div>
      </div>

      <div class="budget-result-display">
        <div style="font-size: 0.78rem; color: var(--text-muted); margin-bottom: 0.2rem;">预估单人全部综合成本 (含机票/签证/食宿/交通)</div>
        <div class="budget-total-num" id="calc-total-rmb">
          ¥19,450 <small id="calc-total-jpy">≈ 405,200円</small>
        </div>

        <div class="stacked-bar">
          <div class="stacked-seg" id="seg-flight" style="width: 18%; background: #264653;"></div>
          <div class="stacked-seg" id="seg-transit" style="width: 22%; background: #2A9D8F;"></div>
          <div class="stacked-seg" id="seg-hotel" style="width: 32%; background: #E76F51;"></div>
          <div class="stacked-seg" id="seg-food" style="width: 20%; background: #F4A261;"></div>
          <div class="stacked-seg" id="seg-misc" style="width: 8%; background: #E9C46A;"></div>
        </div>

        <div class="budget-legend-grid">
          <div><span style="color: #264653;">■</span> 往返机票: <strong id="val-flight">¥2,800</strong></div>
          <div><span style="color: #2A9D8F;">■</span> 境内交通: <strong id="val-transit">¥4,080</strong></div>
          <div><span style="color: #E76F51;">■</span> 宿泊费用: <strong id="val-hotel">¥6,200</strong></div>
          <div><span style="color: #F4A261;">■</span> 餐饮风味: <strong id="val-food">¥4,320</strong></div>
        </div>
      </div>
    </div>

    <!-- Practical Matrix Card -->
    <div class="box-card">
      <div class="box-card-title">
        <span>
          <svg class="icon" viewBox="0 0 24 24"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>
          2026 深度自由行在地工具箱
        </span>
        <span style="font-size: 0.75rem; color: var(--text-muted);">一手实战指南</span>
      </div>

      <div style="display: flex; flex-direction: column; gap: 0.75rem; font-size: 0.825rem;">
        <div style="padding: 0.65rem; background: var(--bg-surface-subtle); border-radius: var(--radius-sm); border-left: 3px solid var(--c-active);">
          <strong>Tabelog (食べログ) 评分避坑基准：</strong>
          日本餐饮评分极其严苛。3.30–3.45 分为极优质本地好店；3.50 分以上为全日本前 4% 顶尖名店；3.70 分以上为殿堂百名店。无需迷信国内网红店排队。
        </div>

        <div style="padding: 0.65rem; background: var(--bg-surface-subtle); border-radius: var(--radius-sm); border-left: 3px solid var(--c-gold);">
          <strong>黑猫宅急便 (Yamato Transport) 宿场托运：</strong>
          徒步中山道（马笼至妻笼）当天早上 8:30 前在观光案内所填单，1,000 日元/件直接送抵妻笼宿；跨城大行李箱亦可在酒店前台直寄次日目的地。
        </div>

        <div style="padding: 0.65rem; background: var(--bg-surface-subtle); border-radius: var(--radius-sm); border-left: 3px solid #2A9D8F;">
          <strong>温泉（Onsen）入浴核心礼节：</strong>
          入浴前必须在淋浴位彻底洗净全身；长发盘起，毛巾切勿浸入池水；传统名汤禁止显露纹身（可用防水肤色贴遮盖或预订贷切私汤）。
        </div>

        <div style="padding: 0.65rem; background: var(--bg-surface-subtle); border-radius: var(--radius-sm); border-left: 3px solid var(--c-alert);">
          <strong>熊野古道与白神山地生态防熊：</strong>
          徒步山林参道背包务必佩戴熊铃（Bear Bell），下午 16:00 前结束步道行程返回宿场，垃圾全数随身带出山林。
        </div>
      </div>
    </div>

  </section>

  <!-- Modal: Visa Itinerary Exporter -->
  <div class="modal-backdrop" id="modal-visa">
    <div class="modal-box">
      <div class="modal-header">
        <h3>
          <svg class="icon" viewBox="0 0 24 24"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>
          送签专用标准行程单 (Visa Submission Itinerary)
        </h3>
        <button class="modal-close-btn" data-close="modal-visa">&times;</button>
      </div>
      <div class="modal-content">
        <p style="color: var(--text-muted); margin-bottom: 0.75rem;">
          已根据当前选定的路线及天数自动格式化为日本使领馆标准送签中英文表格。您可直接复制或打印用于递送指定特许旅行社。
        </p>
        <div style="display: flex; gap: 0.5rem; margin-bottom: 0.75rem;">
          <button class="action-btn" id="btn-copy-visa-table">复制表格文本</button>
          <button class="action-btn" onclick="window.print()">打印 / 存为 PDF</button>
        </div>
        <div id="visa-table-wrap"></div>
      </div>
    </div>
  </div>

  <!-- Modal: Geneva 1949 Driver License Compliance -->
  <div class="modal-backdrop" id="modal-legal">
    <div class="modal-box">
      <div class="modal-header">
        <h3 style="color: var(--c-alert);">
          <svg class="icon" viewBox="0 0 24 24"><polygon points="7.86 2 16.14 2 22 7.86 22 16.14 16.14 22 7.86 22 2 16.14 2 7.86 7.86 2"/></svg>
          《1949 日内瓦公约》在日驾驶合规性核验说明
        </h3>
        <button class="modal-close-btn" data-close="modal-legal">&times;</button>
      </div>
      <div class="modal-content">
        <div style="background: rgba(201, 42, 42, 0.08); border: 1px solid rgba(201, 42, 42, 0.25); border-radius: var(--radius-sm); padding: 0.85rem; margin-bottom: 1rem; color: var(--c-alert);">
          <strong>刑事犯罪预警：</strong>
          中国大陆机动车驾驶证在日无法合法租车或驾驶。任何国内电商平台销售的“国际驾照翻译件/KRP”在日均属<strong>非法伪造无证驾驶</strong>，一旦遇交警临检或发生交通事故，直接按日本刑法拘留起诉，并列入永久拒签黑名单！
        </div>

        <h4 style="margin: 0.85rem 0 0.35rem 0; font-family: var(--font-serif);">1. 什么是合法在日自驾资质？</h4>
        <p>日本道路交通法仅承认基于<strong>《1949 年日内瓦道路交通公约（Geneva Convention 1949）》</strong>签发的纸质国际驾驶许可证（IDP）。合规前提为您同时持有：</p>
        <ul style="margin-left: 1.25rem; margin-top: 0.35rem;">
          <li>缔约国/地区（如<strong>中国香港、中国澳门、英国、美国、加拿大、澳大利亚</strong>等）签发的正式驾照；</li>
          <li>由上述缔约国官方运输署/交管部门核发的 <strong>1949 格式纸质 IDP 国际驾驶许可证原件</strong>；</li>
          <li>或持有<strong>中国台湾地区驾照配合 JAF（日本自动车联盟）官方日文翻译本</strong>。</li>
        </ul>

        <h4 style="margin: 0.85rem 0 0.35rem 0; font-family: var(--font-serif);">2. 2025–2026 外免切替政策收紧</h4>
        <p>自 2025 年 10 月 1 日起，日本警察厅正式收紧“外国驾照换领日本驾照（外免切替）”，必须提供长住日本的《住民票》副本，短期旅游签证已完全无法换领日本当地驾照。</p>

        <h4 style="margin: 0.85rem 0 0.35rem 0; font-family: var(--font-serif);">3. 若无合规海外证件怎么办？</h4>
        <p><strong>请放心采用本系统为您量身定制的【模式 A: 公共交通微循环】！</strong>日本拥有世界最准时密集的铁路与观光巴士系统，配合各站前观光案内所的 e-Bike 电助力自行车租赁，完全可以舒适漫游深山古道与海岛。</p>
      </div>
    </div>
  </div>

  <!-- Data Bundle Injection -->
  <script>
    const JAPAN_POLYGONS = {polygons_json};
    const ROUTES_DATA = {routes_json};
  </script>

  <!-- Interactive JavaScript Engine -->
  <script>
    // State Manager
    let currentRouteId = 'route-1';
    let currentMode = 'transit'; // 'transit' | 'drive'
    let currentSeason = 'winter'; // 'winter' | 'autumn'
    let currentStayTier = 'comfort'; // 'economy' | 'comfort' | 'luxury'
    let selectedDayIdx = 0;

    // SVG Map Pan/Zoom State
    let zoomLevel = 1.0;
    let panX = 0;
    let panY = 0;
    let isDragging = false;
    let hasDragged = false;
    let startX = 0;
    let startY = 0;
    let startMouseX = 0;
    let startMouseY = 0;

    // Initialize View
    document.addEventListener('DOMContentLoaded', () => {{
      renderBaseMap();
      renderRoute(currentRouteId);
      updateBudget();
      bindEvents();
    }});

    // ==========================================
    // RENDER SELF-CONTAINED SVG VECTOR MAP
    // ==========================================
    function renderBaseMap() {{
      const landLayer = document.getElementById('land-layer');
      landLayer.innerHTML = '';
      
      // Draw Japan Landmass
      JAPAN_POLYGONS.forEach(pathD => {{
        const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
        path.setAttribute('d', pathD);
        path.setAttribute('class', 'land-path');
        landLayer.appendChild(path);
      }});
    }}

    function renderRoute(routeId) {{
      currentRouteId = routeId;
      selectedDayIdx = 0;
      const route = ROUTES_DATA[routeId];
      if (!route) return;

      // Sync Duration Slider
      const daysSlider = document.getElementById('slider-days');
      if (daysSlider) {{
        daysSlider.value = route.durationDays;
        document.getElementById('slider-days-val').innerText = `${{route.durationDays}} 天`;
      }}

      // Update Root Accent Colors
      document.documentElement.style.setProperty('--c-active', route.themeColor);
      document.getElementById('brand-badge').style.backgroundColor = route.themeColor;
      document.getElementById('kpi-board').style.borderTopColor = route.themeColor;

      // Update KPI Board
      document.getElementById('kpi-route-title').innerText = route.title;
      document.getElementById('kpi-route-season-tip').innerText = `最佳适行期：${{route.bestSeason}}`;
      document.getElementById('kpi-route-badge').innerText = routeId.toUpperCase();
      document.getElementById('kpi-days-val').innerText = `${{route.durationDays}} 天`;
      document.getElementById('kpi-dist-val').innerText = `${{route.totalDistanceKm}} km`;
      document.getElementById('kpi-trail-val').innerText = `${{route.trailWalkingKm}} km`;
      document.getElementById('kpi-air-val').innerText = `${{route.entryAirport}} ➔ ${{route.exitAirport}}`;
      document.getElementById('map-active-route-name').innerText = `${{route.shortTitle}} 空间拓扑`;

      // Update Season Tip
      updateSeasonTip();

      // Project Route Path onto SVG Map
      // Bounds: MIN_LNG = 129.0, MAX_LNG = 143.5, MIN_LAT = 31.0, MAX_LAT = 42.8
      function projectPoint(lng, lat) {{
        const x = (lng - 129.0) / (143.5 - 129.0) * 1000;
        const latRad = lat * Math.PI / 180;
        const mercY = Math.log(Math.tan(Math.PI / 4 + latRad / 2));
        const minMerc = Math.log(Math.tan(Math.PI / 4 + 31.0 * Math.PI / 360));
        const maxMerc = Math.log(Math.tan(Math.PI / 4 + 42.8 * Math.PI / 360));
        const y = (maxMerc - mercY) / (maxMerc - minMerc) * 750;
        return [Math.round(x * 10) / 10, Math.round(y * 10) / 10];
      }}

      const coords = route.stops.map(s => projectPoint(s.lng, s.lat));
      const pathD = 'M ' + coords.map(c => `${{c[0]}},${{c[1]}}`).join(' L ');

      const trackBg = document.getElementById('route-track-bg');
      trackBg.setAttribute('d', pathD);
      trackBg.setAttribute('stroke', route.themeColor);

      const trackFg = document.getElementById('route-track-fg');
      trackFg.setAttribute('d', pathD);

      // Render Nodes Layer
      const nodesLayer = document.getElementById('nodes-layer');
      nodesLayer.innerHTML = '';

      coords.forEach((c, idx) => {{
        const stop = route.stops[idx];
        const g = document.createElementNS('http://www.w3.org/2000/svg', 'g');
        g.setAttribute('class', `map-node ${{idx === selectedDayIdx ? 'active-node' : ''}}`);
        g.setAttribute('data-idx', idx);

        const circle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
        circle.setAttribute('cx', c[0]);
        circle.setAttribute('cy', c[1]);
        circle.setAttribute('r', idx === 0 || idx === coords.length - 1 ? 11 : 9);
        circle.setAttribute('fill', route.themeColor);

        const numText = document.createElementNS('http://www.w3.org/2000/svg', 'text');
        numText.setAttribute('x', c[0]);
        numText.setAttribute('y', c[1]);
        numText.setAttribute('class', 'map-node-num');
        numText.textContent = idx + 1;

        const nameText = document.createElementNS('http://www.w3.org/2000/svg', 'text');
        nameText.setAttribute('x', c[0] + 13);
        nameText.setAttribute('y', c[1] + 4);
        nameText.setAttribute('class', 'map-node-label');
        nameText.textContent = stop.name.split(' ')[0];

        g.appendChild(circle);
        g.appendChild(numText);
        g.appendChild(nameText);

        // Tooltip & Click Focus (with drag check)
        g.addEventListener('mouseenter', (e) => showTooltip(e, stop, idx + 1));
        g.addEventListener('mouseleave', hideTooltip);
        g.addEventListener('click', (e) => {{
          if (hasDragged) return;
          focusDay(idx);
        }});

        nodesLayer.appendChild(g);
      }});

      // Render Day Cards Timeline
      renderTimelineCards(route);

      // Render Elevation Profile
      renderElevationProfile(route);

      // Reset Map Transform to optimal fit
      resetMapTransform();
    }}

    function updateSeasonTip() {{
      const route = ROUTES_DATA[currentRouteId];
      const box = document.getElementById('season-info-content');
      if (currentSeason === 'winter') {{
        box.innerHTML = `<strong>1–2月 豪雪物候：</strong>${{route.winterNote}}`;
      }} else {{
        box.innerHTML = `<strong>9–10月 早秋物候：</strong>${{route.autumnNote}}`;
      }}
    }}

    // ==========================================
    // RENDER TIMELINE NARRATIVE CARDS
    // ==========================================
    function renderTimelineCards(route) {{
      const container = document.getElementById('timeline-container');
      container.innerHTML = '';

      route.daysDetail.forEach((day, idx) => {{
        const card = document.createElement('div');
        card.className = `day-card ${{idx === selectedDayIdx ? 'selected' : ''}}`;
        card.setAttribute('data-idx', idx);

        let modeHtml = '';
        if (currentMode === 'transit') {{
          modeHtml = `
            <div class="mode-subcard">
              <div class="mode-subcard-title" style="color: ${{route.themeColor}};">
                <svg class="icon" viewBox="0 0 24 24"><rect x="2" y="7" width="20" height="14" rx="2" ry="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/></svg>
                模式 A: 公共铁道与接驳
              </div>
              <div style="font-weight: 600;">${{day.modeA.line}}</div>
              <div class="mode-grid-specs">
                <span class="mode-spec-item">通票覆盖: <strong>${{day.modeA.pass}}</strong></span>
                <span class="mode-spec-item">单程基准: <strong>${{day.modeA.cost}}</strong></span>
              </div>
              <div style="color: var(--text-muted); font-size: 0.72rem; margin-top: 0.25rem;">接驳要诀: ${{day.modeA.tip}}</div>
            </div>
          `;
        }} else {{
          modeHtml = `
            <div class="mode-subcard" style="border-left-color: #E76F51;">
              <div class="mode-subcard-title" style="color: #E76F51;">
                <svg class="icon" viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="3"/></svg>
                模式 B: 合规自驾方案
              </div>
              <div style="font-weight: 600;">${{day.modeB.route}}</div>
              <div class="mode-grid-specs">
                <span class="mode-spec-item">移动里程: <strong>${{day.modeB.dist}}</strong></span>
                <span class="mode-spec-item">预估车程: <strong>${{day.modeB.time}}</strong></span>
                <span class="mode-spec-item">ETC高速费: <strong>${{day.modeB.toll}}</strong></span>
                <span class="mode-spec-item">山道难度: <strong>${{day.modeB.difficulty}}</strong></span>
                <span class="mode-spec-item">MapCode: <strong>${{day.modeB.mapCode}}</strong></span>
              </div>
              <div style="color: var(--text-muted); font-size: 0.72rem; margin-top: 0.25rem;">泊车指引: ${{day.modeB.park}}</div>
            </div>
          `;
        }}

        card.innerHTML = `
          <div class="day-top-row">
            <span class="day-num-badge">DAY ${{day.day < 10 ? '0' + day.day : day.day}}</span>
            <span class="day-elev-tag">
              <svg class="icon" viewBox="0 0 24 24"><polygon points="3 11 22 2 13 21 11 13 3 11"/></svg>
              ${{day.elev}}
            </span>
          </div>
          <div class="day-title">${{day.title}}</div>
          <div class="day-story">${{day.story}}</div>
          
          ${{modeHtml}}

          <div class="day-foot-meta">
            <div>
              <div class="meta-box-title">
                <svg class="icon" viewBox="0 0 24 24"><path d="M18 8h1a4 4 0 0 1 0 8h-1"/><path d="M2 8h16v9a4 4 0 0 1-4 4H6a4 4 0 0 1-4-4V8z"/></svg>
                Tabelog 餐饮推荐
              </div>
              <strong>${{day.dining.name}}</strong>
              <span class="tabelog-badge">${{day.dining.score}}</span>
              <div style="color: var(--text-muted); font-size: 0.7rem;">${{day.dining.specialty}} (人均约${{day.dining.cost}})</div>
            </div>
            <div>
              <div class="meta-box-title">
                <svg class="icon" viewBox="0 0 24 24"><path d="M2 4v16M2 8h18a2 2 0 0 1 2 2v10M2 17h20M6 8v9"/></svg>
                宿泊建议 (${{currentStayTier === 'economy' ? '经济档' : '舒适档'}})
              </div>
              <strong>${{currentStayTier === 'economy' ? day.stay.economy : day.stay.comfort}}</strong>
            </div>
          </div>
        `;

        card.addEventListener('click', () => focusDay(idx));
        container.appendChild(card);
      }});
    }}

    // ==========================================
    // RENDER D3-STYLE ELEVATION PROFILE
    // ==========================================
    function renderElevationProfile(route) {{
      const svg = document.getElementById('elevation-svg');
      svg.innerHTML = '';
      const stops = route.stops;
      if (!stops || stops.length === 0) return;

      const maxElev = 1600;
      const width = 600;
      const height = 90;

      const points = stops.map((s, i) => {{
        const x = (i / (stops.length - 1)) * (width - 40) + 20;
        const y = height - 15 - (s.elev / maxElev) * (height - 30);
        return [x, y, s.elev, s.name];
      }});

      // Area Path
      let areaD = `M ${{points[0][0]}},${{height - 15}} L ` + points.map(p => `${{p[0]}},${{p[1]}}`).join(' L ') + ` L ${{points[points.length - 1][0]}},${{height - 15}} Z`;
      
      const area = document.createElementNS('http://www.w3.org/2000/svg', 'path');
      area.setAttribute('d', areaD);
      area.setAttribute('fill', route.themeColor);
      area.setAttribute('opacity', '0.18');
      svg.appendChild(area);

      // Line Path
      let lineD = 'M ' + points.map(p => `${{p[0]}},${{p[1]}}`).join(' L ');
      const line = document.createElementNS('http://www.w3.org/2000/svg', 'path');
      line.setAttribute('d', lineD);
      line.setAttribute('fill', 'none');
      line.setAttribute('stroke', route.themeColor);
      line.setAttribute('stroke-width', '2.5');
      svg.appendChild(line);

      // Probe Line & Circle
      const probeLine = document.createElementNS('http://www.w3.org/2000/svg', 'line');
      probeLine.setAttribute('y1', 5);
      probeLine.setAttribute('y2', height - 15);
      probeLine.setAttribute('stroke', '#E76F51');
      probeLine.setAttribute('stroke-width', '1.5');
      probeLine.setAttribute('stroke-dasharray', '3 3');
      probeLine.style.display = 'none';
      svg.appendChild(probeLine);

      const probeCircle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
      probeCircle.setAttribute('r', '4.5');
      probeCircle.setAttribute('fill', '#E76F51');
      probeCircle.setAttribute('stroke', '#FFFFFF');
      probeCircle.setAttribute('stroke-width', '1.5');
      probeCircle.style.display = 'none';
      svg.appendChild(probeCircle);

      // Interactive Overlay
      svg.addEventListener('mousemove', (e) => {{
        const rect = svg.getBoundingClientRect();
        const mouseX = ((e.clientX - rect.left) / rect.width) * width;
        
        // Find nearest point
        let nearestIdx = 0;
        let minDiff = 9999;
        points.forEach((p, idx) => {{
          const diff = Math.abs(p[0] - mouseX);
          if (diff < minDiff) {{
            minDiff = diff;
            nearestIdx = idx;
          }}
        }});

        const p = points[nearestIdx];
        probeLine.setAttribute('x1', p[0]);
        probeLine.setAttribute('x2', p[0]);
        probeLine.style.display = 'block';

        probeCircle.setAttribute('cx', p[0]);
        probeCircle.setAttribute('cy', p[1]);
        probeCircle.style.display = 'block';

        document.getElementById('elev-readout').innerHTML = `<strong>${{p[3]}}</strong>: 海拔 ${{p[2]}} 米`;

        // Sync Map Probe
        syncMapProbe(nearestIdx);
      }});

      svg.addEventListener('mouseleave', () => {{
        probeLine.style.display = 'none';
        probeCircle.style.display = 'none';
        document.getElementById('map-probe-group').style.display = 'none';
        document.getElementById('elev-readout').innerText = '滑动光标实时探查海拔高程';
      }});
    }}

    function syncMapProbe(idx) {{
      const route = ROUTES_DATA[currentRouteId];
      if (!route || !route.stops[idx]) return;
      
      const s = route.stops[idx];
      const x = (s.lng - 129.0) / (143.5 - 129.0) * 1000;
      const latRad = s.lat * Math.PI / 180;
      const mercY = Math.log(Math.tan(Math.PI / 4 + latRad / 2));
      const minMerc = Math.log(Math.tan(Math.PI / 4 + 31.0 * Math.PI / 360));
      const maxMerc = Math.log(Math.tan(Math.PI / 4 + 42.8 * Math.PI / 360));
      const y = (maxMerc - mercY) / (maxMerc - minMerc) * 750;

      const probeGroup = document.getElementById('map-probe-group');
      const probeCircle = document.getElementById('probe-circle');
      const probeDot = document.getElementById('probe-dot');

      probeCircle.setAttribute('cx', x);
      probeCircle.setAttribute('cy', y);
      probeDot.setAttribute('cx', x);
      probeDot.setAttribute('cy', y);
      probeGroup.style.display = 'block';
    }}

    // Focus on Day
    function focusDay(idx) {{
      selectedDayIdx = idx;
      document.querySelectorAll('.day-card').forEach((c, i) => {{
        c.classList.toggle('selected', i === idx);
        if (i === idx) {{
          c.scrollIntoView({{ behavior: 'smooth', block: 'nearest' }});
        }}
      }});
      // Highlight active node on SVG map
      document.querySelectorAll('.map-node').forEach((n, i) => {{
        n.classList.toggle('active-node', i === idx);
      }});
      syncMapProbe(idx);
    }}

    // ==========================================
    // MAP PAN & ZOOM ENGINE (API-Independent)
    // ==========================================
    const mapViewport = document.getElementById('map-viewport');
    const transformGroup = document.getElementById('map-transform-group');

    function updateMapTransform() {{
      transformGroup.setAttribute('transform', `translate(${{panX}}, ${{panY}}) scale(${{zoomLevel}})`);
    }}

    function resetMapTransform() {{
      zoomLevel = 1.0;
      panX = 0;
      panY = 0;
      updateMapTransform();
    }}

    mapViewport.addEventListener('mousedown', (e) => {{
      isDragging = true;
      hasDragged = false;
      startMouseX = e.clientX;
      startMouseY = e.clientY;
      startX = e.clientX - panX;
      startY = e.clientY - panY;
    }});

    window.addEventListener('mousemove', (e) => {{
      if (!isDragging) return;
      if (Math.abs(e.clientX - startMouseX) > 4 || Math.abs(e.clientY - startMouseY) > 4) {{
        hasDragged = true;
      }}
      panX = e.clientX - startX;
      panY = e.clientY - startY;
      updateMapTransform();
    }});

    window.addEventListener('mouseup', () => {{
      isDragging = false;
    }});

    mapViewport.addEventListener('wheel', (e) => {{
      e.preventDefault();
      const zoomFactor = e.deltaY < 0 ? 1.15 : 0.87;
      zoomLevel = Math.min(Math.max(0.7, zoomLevel * zoomFactor), 4.5);
      updateMapTransform();
    }});

    document.getElementById('btn-zoom-in').addEventListener('click', () => {{
      zoomLevel = Math.min(zoomLevel * 1.25, 4.5);
      updateMapTransform();
    }});
    document.getElementById('btn-zoom-out').addEventListener('click', () => {{
      zoomLevel = Math.max(zoomLevel / 1.25, 0.7);
      updateMapTransform();
    }});
    document.getElementById('btn-zoom-reset').addEventListener('click', resetMapTransform);

    // Tooltip with boundary awareness
    const tooltip = document.getElementById('node-tooltip');
    function showTooltip(e, stop, dayNum) {{
      const rect = mapViewport.getBoundingClientRect();
      let x = e.clientX - rect.left;
      let y = e.clientY - rect.top;

      if (x < 110) x = 110;
      if (x > rect.width - 110) x = rect.width - 110;

      tooltip.style.left = `${{x}}px`;
      if (y < 55) {{
        tooltip.style.top = `${{y + 20}}px`;
        tooltip.style.transform = 'translate(-50%, 0)';
      }} else {{
        tooltip.style.top = `${{y - 12}}px`;
        tooltip.style.transform = 'translate(-50%, -100%)';
      }}
      tooltip.innerHTML = `<strong>Day ${{dayNum}}: ${{stop.name}}</strong><br>海拔: ${{stop.elev}}m · ${{stop.desc}}`;
      tooltip.style.display = 'block';
    }}
    function hideTooltip() {{
      tooltip.style.display = 'none';
    }}

    // ==========================================
    // BUDGET CALCULATOR ENGINE
    // ==========================================
    function updateBudget() {{
      const travelers = parseInt(document.getElementById('slider-travelers').value, 10);
      const days = parseInt(document.getElementById('slider-days').value, 10);
      
      document.getElementById('slider-travelers-val').innerText = `${{travelers}} 人同行`;
      document.getElementById('slider-days-val').innerText = `${{days}} 天`;

      let stayFactor = 6200;
      if (currentStayTier === 'economy') stayFactor = 4200;
      if (currentStayTier === 'luxury') stayFactor = 11500;

      // Base single traveler factors
      const flight = 2800;
      let transit = 4080;
      if (currentMode === 'drive') {{
        // Car rent + ETC split between travelers
        const carRentTotal = days * 7500; // JPY
        const etcTotal = 25000; // JPY
        const driveCostRmbPerPerson = Math.round(((carRentTotal + etcTotal) / travelers) * 0.048);
        transit = driveCostRmbPerPerson;
      }}
      const hotel = Math.round(stayFactor * (days / 18));
      const food = Math.round(240 * days);
      const misc = 1400;

      const totalRmb = flight + transit + hotel + food + misc;
      const totalJpy = Math.round(totalRmb / 0.048);

      document.getElementById('calc-total-rmb').innerHTML = `¥${{totalRmb.toLocaleString()}} <small id="calc-total-jpy">≈ ${{totalJpy.toLocaleString()}}円</small>`;
      document.getElementById('val-flight').innerText = `¥${{flight.toLocaleString()}}`;
      document.getElementById('val-transit').innerText = `¥${{transit.toLocaleString()}}`;
      document.getElementById('val-hotel').innerText = `¥${{hotel.toLocaleString()}}`;
      document.getElementById('val-food').innerText = `¥${{food.toLocaleString()}}`;

      document.getElementById('seg-flight').style.width = `${{Math.round(flight / totalRmb * 100)}}%`;
      document.getElementById('seg-transit').style.width = `${{Math.round(transit / totalRmb * 100)}}%`;
      document.getElementById('seg-hotel').style.width = `${{Math.round(hotel / totalRmb * 100)}}%`;
      document.getElementById('seg-food').style.width = `${{Math.round(food / totalRmb * 100)}}%`;
      document.getElementById('seg-misc').style.width = `${{Math.round(misc / totalRmb * 100)}}%`;
    }}

    // ==========================================
    // VISA TABLE EXPORTER
    // ==========================================
    function renderVisaTable() {{
      const route = ROUTES_DATA[currentRouteId];
      const wrap = document.getElementById('visa-table-wrap');
      
      let rows = route.daysDetail.map((d, i) => `
        <tr>
          <td>Day ${{d.day}}</td>
          <td>${{d.title}}</td>
          <td>${{currentStayTier === 'economy' ? d.stay.economy : d.stay.comfort}}</td>
          <td>${{route.stops[i] ? route.stops[i].name : 'Japan Hotel'}}</td>
          <td>+81-3-0000-0000</td>
        </tr>
      `).join('');

      wrap.innerHTML = `
        <table class="visa-table">
          <thead>
            <tr>
              <th>Date / Day</th>
              <th>Activity & Destination (活动与地点)</th>
              <th>Accommodation Name (住宿设施名称)</th>
              <th>Location (所在地)</th>
              <th>Contact Phone (联系电话)</th>
            </tr>
          </thead>
          <tbody>
            ${{rows}}
          </tbody>
        </table>
      `;
    }}

    // ==========================================
    // EVENT BINDINGS
    // ==========================================
    function bindEvents() {{
      // Route Switcher
      document.querySelectorAll('[data-route]').forEach(btn => {{
        btn.addEventListener('click', () => {{
          document.querySelectorAll('[data-route]').forEach(b => b.classList.remove('active'));
          btn.classList.add('active');
          renderRoute(btn.getAttribute('data-route'));
          updateBudget();
          renderVisaTable();
        }});
      }});

      // Mode Switcher (Transit vs Drive)
      const btnTransit = document.getElementById('btn-mode-transit');
      const btnDrive = document.getElementById('btn-mode-drive');

      btnTransit.addEventListener('click', () => {{
        currentMode = 'transit';
        btnTransit.classList.add('active');
        btnDrive.classList.remove('active');
        renderTimelineCards(ROUTES_DATA[currentRouteId]);
        updateBudget();
      }});

      btnDrive.addEventListener('click', () => {{
        // Trigger Compliance Warning Dialog
        document.getElementById('modal-legal').classList.add('active');
        currentMode = 'drive';
        btnDrive.classList.add('active');
        btnTransit.classList.remove('active');
        renderTimelineCards(ROUTES_DATA[currentRouteId]);
        updateBudget();
      }});

      // Season Switcher
      const seasonWinter = document.getElementById('season-winter');
      const seasonAutumn = document.getElementById('season-autumn');

      seasonWinter.addEventListener('click', () => {{
        currentSeason = 'winter';
        seasonWinter.classList.add('active');
        seasonAutumn.classList.remove('active');
        updateSeasonTip();
      }});

      seasonAutumn.addEventListener('click', () => {{
        currentSeason = 'autumn';
        seasonAutumn.classList.add('active');
        seasonWinter.classList.remove('active');
        updateSeasonTip();
      }});

      // Stay Tier Switcher
      document.querySelectorAll('[data-stay]').forEach(btn => {{
        btn.addEventListener('click', () => {{
          document.querySelectorAll('[data-stay]').forEach(b => b.classList.remove('active'));
          btn.classList.add('active');
          currentStayTier = btn.getAttribute('data-stay');
          renderTimelineCards(ROUTES_DATA[currentRouteId]);
          updateBudget();
          renderVisaTable();
        }});
      }});

      // Budget Sliders
      document.getElementById('slider-travelers').addEventListener('input', updateBudget);
      document.getElementById('slider-days').addEventListener('input', updateBudget);

      // Dark / Light Theme
      document.getElementById('btn-toggle-theme').addEventListener('click', () => {{
        document.body.classList.toggle('dark-theme');
      }});

      // Modals
      const modalVisa = document.getElementById('modal-visa');
      const modalLegal = document.getElementById('modal-legal');

      document.getElementById('btn-open-visa-modal').addEventListener('click', () => {{
        renderVisaTable();
        modalVisa.classList.add('active');
      }});
      document.getElementById('btn-open-legal-modal').addEventListener('click', () => modalLegal.classList.add('active'));
      document.getElementById('link-show-legal').addEventListener('click', () => modalLegal.classList.add('active'));

      document.querySelectorAll('.modal-close-btn').forEach(btn => {{
        btn.addEventListener('click', () => {{
          modalVisa.classList.remove('active');
          modalLegal.classList.remove('active');
        }});
      }});

      document.querySelectorAll('.modal-backdrop').forEach(b => {{
        b.addEventListener('click', (e) => {{
          if (e.target === b) {{
            b.classList.remove('active');
          }}
        }});
      }});

      // Copy Visa Table
      document.getElementById('btn-copy-visa-table').addEventListener('click', () => {{
        const tableText = document.getElementById('visa-table-wrap').innerText;
        navigator.clipboard.writeText(tableText).then(() => {{
          alert('送签表格文本已复制至剪贴板！');
        }});
      }});
    }}
  </script>
</body>
</html>
"""

with open('japan-travel-guide/v2.html', 'w', encoding='utf-8') as f:
    f.write(html_code)

print("japan-travel-guide/v2.html successfully generated!")
