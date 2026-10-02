# -*- coding: utf-8 -*-
import json

with open("fujian-food-capital-v2/data_bundle.json", "r", encoding="utf-8") as f:
    bundle = json.load(f)

chapters_json = json.dumps(bundle["chapters"], ensure_ascii=False)
foods_json = json.dumps(bundle["foods"], ensure_ascii=False)
shops_json = json.dumps(bundle["shops"], ensure_ascii=False)
routes_json = json.dumps(bundle["routes"], ensure_ascii=False)
origins_json = json.dumps(bundle["origins"], ensure_ascii=False)

html_template = """<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>刺桐食肆全景仪 · 泉州美食图鉴 v2</title>
<meta name="description" content="联合国教科文组织世界美食之都 · 泉州全景美食交互图鉴。从零设计：空间拓扑沙盘、人间十二时辰、八重风味长卷、神凡山海星谱与老饕漫游动线。">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@500;700&family=Noto+Serif+SC:wght@400;600;700;900&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
/* ==========================================================================
   刺桐食肆全景仪 (v2) · 顶级东方美学与交互设计系统
   基调：胭脂砖红 · 蚝壳暖白 · 燕尾脊深黛 · 金葱海丝古金
   准则：零 Emoji · 纯正 SVG 矢量图标 · 原生极速响应 · 五重视域穿梭
   ========================================================================== */

:root {
  --c-brick: #9E3524;
  --c-brick-dark: #782215;
  --c-brick-light: #C44C38;
  --c-brick-soft: rgba(158, 53, 36, 0.08);

  --c-shell: #F7F4EC;
  --c-shell-card: #FFFFFF;
  --c-paper: #FAF8F3;
  --c-paper-dark: #ECE5D8;
  --c-border: rgba(45, 38, 32, 0.11);

  --c-dark: #121A1E;
  --c-dark-surface: #182228;
  --c-dark-border: rgba(255, 255, 255, 0.12);

  --c-gold: #C59341;
  --c-gold-light: #E0B25E;
  --c-gold-soft: rgba(197, 147, 65, 0.14);

  --c-sea: #366B73;
  --c-sea-dark: #1E464D;
  --c-sea-soft: rgba(54, 107, 115, 0.1);

  --c-ink: #1F1B18;
  --c-ink-light: #4A423B;
  --c-ink-muted: #7E756B;
  --c-ink-faint: #AAA095;

  --font-serif: "Noto Serif SC", "Songti SC", "Source Han Serif SC", STSong, serif;
  --font-sans: "Plus Jakarta Sans", -apple-system, BlinkMacSystemFont, "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
  --font-cinzel: "Cinzel", serif;

  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-lg: 16px;
  --radius-xl: 24px;
  --radius-full: 9999px;

  --shadow-sm: 0 2px 10px rgba(35, 30, 25, 0.04);
  --shadow-md: 0 10px 30px rgba(35, 30, 25, 0.08);
  --shadow-lg: 0 20px 50px rgba(35, 30, 25, 0.13);
  --shadow-brick: 0 12px 30px rgba(158, 53, 36, 0.22);
}

* { box-sizing: border-box; margin: 0; padding: 0; }
html { scroll-behavior: smooth; font-size: 15px; }
body {
  font-family: var(--font-sans);
  background-color: var(--c-paper);
  color: var(--c-ink);
  line-height: 1.8;
  -webkit-font-smoothing: antialiased;
  overflow-x: hidden;
  position: relative;
  transition: background-color 0.5s ease, color 0.5s ease;
}

/* 纸实质感微粒噪点底纹 */
body::before {
  content: "";
  position: fixed;
  inset: 0;
  pointer-events: none;
  z-index: 9999;
  opacity: 0.035;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)'/%3E%3C/svg%3E");
}

h1, h2, h3, h4, .font-serif {
  font-family: var(--font-serif);
  letter-spacing: -0.01em;
}

button {
  font-family: inherit;
  color: inherit;
  background: none;
  border: none;
  cursor: pointer;
  outline: none;
}

::selection {
  background: var(--c-brick);
  color: #FFFFFF;
}

/* 容器定义 */
.container {
  width: 100%;
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 24px;
}

/* ==========================================================================
   全景顶栏与视域切换控制器 (Perspective Switcher)
   ========================================================================== */
#astrolabe-bar {
  position: sticky;
  top: 0;
  z-index: 1000;
  background: rgba(250, 248, 243, 0.88);
  backdrop-filter: blur(18px);
  -webkit-backdrop-filter: blur(18px);
  border-bottom: 1px solid var(--c-border);
  transition: all 0.3s ease;
}

#astrolabe-bar.night-mode {
  background: rgba(18, 26, 30, 0.92);
  border-bottom-color: var(--c-dark-border);
  color: #FFFFFF;
}

.nav-wrapper {
  height: 68px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
}

.brand-badge {
  display: flex;
  align-items: center;
  gap: 10px;
  text-decoration: none;
  color: inherit;
  flex-shrink: 0;
}

.brand-seal {
  width: 38px;
  height: 38px;
  background: var(--c-brick);
  color: #FFF;
  border-radius: var(--radius-sm);
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: var(--font-serif);
  font-weight: 700;
  font-size: 15px;
  box-shadow: var(--shadow-sm);
  letter-spacing: 0.05em;
  transition: transform 0.3s ease;
}

.brand-seal:hover {
  transform: rotate(6deg) scale(1.05);
}

.brand-titles {
  display: flex;
  flex-direction: column;
}

.brand-name {
  font-family: var(--font-serif);
  font-weight: 700;
  font-size: 16px;
  letter-spacing: 0.05em;
}

.brand-sub {
  font-size: 10px;
  color: var(--c-ink-muted);
  letter-spacing: 0.12em;
  font-family: var(--font-cinzel);
  text-transform: uppercase;
}

/* 视域控制器 Tabs */
.view-tabs-group {
  display: flex;
  align-items: center;
  gap: 4px;
  background: rgba(45, 38, 32, 0.05);
  padding: 4px;
  border-radius: var(--radius-full);
  border: 1px solid var(--c-border);
}

#astrolabe-bar.night-mode .view-tabs-group {
  background: rgba(255, 255, 255, 0.08);
  border-color: rgba(255, 255, 255, 0.12);
}

.view-tab-btn {
  padding: 6px 14px;
  border-radius: var(--radius-full);
  font-size: 13px;
  font-weight: 600;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  color: var(--c-ink-light);
  transition: all 0.25s ease;
  white-space: nowrap;
}

#astrolabe-bar.night-mode .view-tab-btn {
  color: #CBD5E1;
}

.view-tab-btn:hover {
  color: var(--c-brick);
}

#astrolabe-bar.night-mode .view-tab-btn:hover {
  color: var(--c-gold-light);
}

.view-tab-btn.active {
  background: var(--c-brick);
  color: #FFFFFF;
  box-shadow: 0 4px 14px rgba(158, 53, 36, 0.3);
}

#astrolabe-bar.night-mode .view-tab-btn.active {
  background: var(--c-gold);
  color: #121A1E;
}

.nav-actions {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-shrink: 0;
}

.action-icon-btn {
  width: 36px;
  height: 36px;
  border-radius: var(--radius-full);
  border: 1px solid var(--c-border);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--c-ink-light);
  transition: all 0.2s ease;
  position: relative;
}

.action-icon-btn:hover {
  border-color: var(--c-brick);
  color: var(--c-brick);
  background: var(--c-brick-soft);
}

#astrolabe-bar.night-mode .action-icon-btn {
  border-color: rgba(255, 255, 255, 0.15);
  color: #E2E8F0;
}

#astrolabe-bar.night-mode .action-icon-btn:hover {
  border-color: var(--c-gold);
  color: var(--c-gold);
  background: rgba(197, 147, 65, 0.15);
}

.action-badge {
  position: absolute;
  top: -2px;
  right: -2px;
  width: 16px;
  height: 16px;
  background: var(--c-brick);
  color: #FFF;
  border-radius: 50%;
  font-size: 9px;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* ==========================================================================
   页面顶部宣言与海丝母题 (Prologue Bar)
   ========================================================================== */
.prologue-banner {
  padding: 24px 0 16px;
  border-bottom: 1px solid var(--c-border);
  background: linear-gradient(180deg, rgba(250, 248, 243, 0.6) 0%, rgba(242, 235, 221, 0.4) 100%);
  transition: all 0.4s ease;
}

body.night-active .prologue-banner {
  background: #0E161A;
  border-bottom-color: var(--c-dark-border);
  color: #E2E8F0;
}

.prologue-flex {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
}

.prologue-motto {
  display: flex;
  align-items: center;
  gap: 12px;
}

.motto-seal {
  border: 1px solid var(--c-brick);
  color: var(--c-brick);
  padding: 3px 8px;
  border-radius: var(--radius-sm);
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.1em;
  background: var(--c-brick-soft);
}

body.night-active .motto-seal {
  border-color: var(--c-gold);
  color: var(--c-gold);
  background: var(--c-gold-soft);
}

.motto-text {
  font-family: var(--font-serif);
  font-size: 15px;
  font-weight: 600;
  color: var(--c-ink-light);
}

body.night-active .motto-text {
  color: #CBD5E1;
}

.stats-capsule {
  display: flex;
  align-items: center;
  gap: 16px;
  font-size: 12px;
  color: var(--c-ink-muted);
}

.stat-item b {
  font-family: var(--font-serif);
  font-size: 16px;
  color: var(--c-brick);
  margin-right: 2px;
}

body.night-active .stat-item b {
  color: var(--c-gold);
}

/* ==========================================================================
   视角视域容器 (Viewport Panes)
   ========================================================================== */
.view-stage {
  position: relative;
  min-height: calc(100vh - 140px);
}

.view-pane {
  display: none;
  opacity: 0;
  transform: translateY(12px);
  transition: opacity 0.4s cubic-bezier(0.16, 1, 0.3, 1), transform 0.4s cubic-bezier(0.16, 1, 0.3, 1);
  padding: 32px 0 64px;
}

.view-pane.active {
  display: block;
  opacity: 1;
  transform: translateY(0);
}

/* ==========================================================================
   视域 Ⅰ：刺桐山海图 · 空间拓扑沙盘 (The Spatial Cartogram Canvas)
   ========================================================================== */
.cartogram-shell {
  background: var(--c-shell-card);
  border: 1px solid var(--c-border);
  border-radius: var(--radius-xl);
  overflow: hidden;
  box-shadow: var(--shadow-md);
  position: relative;
}

body.night-active .cartogram-shell {
  background: #111A1F;
  border-color: var(--c-dark-border);
}

.cartogram-toolbar {
  padding: 16px 24px;
  border-bottom: 1px solid var(--c-border);
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  background: rgba(250, 248, 243, 0.5);
}

body.night-active .cartogram-toolbar {
  background: rgba(18, 26, 30, 0.8);
  border-bottom-color: var(--c-dark-border);
}

.district-filter-group, .attitude-filter-group {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 6px;
}

.geo-btn {
  padding: 5px 12px;
  border-radius: var(--radius-full);
  font-size: 12px;
  border: 1px solid var(--c-border);
  background: #FFF;
  color: var(--c-ink-light);
  transition: all 0.2s ease;
}

body.night-active .geo-btn {
  background: #1A242B;
  border-color: rgba(255, 255, 255, 0.12);
  color: #CBD5E1;
}

.geo-btn:hover {
  border-color: var(--c-brick);
  color: var(--c-brick);
}

.geo-btn.active {
  background: var(--c-brick);
  color: #FFF;
  border-color: var(--c-brick);
}

body.night-active .geo-btn.active {
  background: var(--c-gold);
  color: #121A1E;
  border-color: var(--c-gold);
}

.night-mode-toggle-btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 14px;
  border-radius: var(--radius-full);
  font-size: 12px;
  font-weight: 600;
  border: 1px solid var(--c-gold);
  color: var(--c-gold);
  background: var(--c-gold-soft);
  transition: all 0.25s ease;
}

.night-mode-toggle-btn.on {
  background: var(--c-gold);
  color: #121A1E;
}

/* 拓扑地图交互画布 */
.cartogram-canvas-box {
  position: relative;
  width: 100%;
  height: 680px;
  background: #FAF8F2;
  overflow: hidden;
  user-select: none;
}

body.night-active .cartogram-canvas-box {
  background: #0D1418;
}

.cartogram-svg {
  width: 100%;
  height: 100%;
  display: block;
}

/* 地图标注动效 */
.shop-pin {
  cursor: pointer;
  transition: transform 0.25s cubic-bezier(0.34, 1.56, 0.64, 1), opacity 0.25s ease;
}

.shop-pin:hover {
  transform: scale(1.35);
}

.shop-pin.highlighted circle {
  stroke-width: 3px;
  stroke: #FFF;
  animation: pulsePin 1.5s infinite;
}

@keyframes pulsePin {
  0% { r: 7; opacity: 1; }
  50% { r: 11; opacity: 0.6; }
  100% { r: 7; opacity: 1; }
}

/* 拓扑地图侧滑牌匾详情抽屉 */
.shop-ledger-drawer {
  position: absolute;
  top: 0;
  right: 0;
  bottom: 0;
  width: 380px;
  max-width: 90%;
  background: var(--c-shell-card);
  border-left: 1px solid var(--c-border);
  box-shadow: -8px 0 30px rgba(0, 0, 0, 0.1);
  padding: 24px;
  transform: translateX(105%);
  transition: transform 0.35s cubic-bezier(0.16, 1, 0.3, 1);
  z-index: 50;
  display: flex;
  flex-direction: column;
}

body.night-active .shop-ledger-drawer {
  background: #141E24;
  border-left-color: var(--c-dark-border);
  color: #E2E8F0;
}

.shop-ledger-drawer.open {
  transform: translateX(0);
}

/* ==========================================================================
   视域 Ⅱ：人间十二时辰 · 市井时序光轨 (The 24-Hour Chrono-Dial)
   ========================================================================== */
.chrono-controller {
  background: var(--c-shell-card);
  border: 1px solid var(--c-border);
  border-radius: var(--radius-xl);
  padding: 28px;
  margin-bottom: 32px;
  box-shadow: var(--shadow-sm);
  transition: background-color 0.4s ease;
}

body.night-active .chrono-controller {
  background: #131E24;
  border-color: var(--c-dark-border);
}

.dial-phase-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  margin-bottom: 24px;
  overflow-x: auto;
  padding-bottom: 4px;
}

.dial-phase-btn {
  flex: 1;
  padding: 12px 10px;
  border-radius: var(--radius-lg);
  border: 1px solid var(--c-border);
  text-align: center;
  background: #FFF;
  transition: all 0.25s ease;
  min-width: 140px;
}

body.night-active .dial-phase-btn {
  background: #1A262E;
  border-color: rgba(255, 255, 255, 0.1);
  color: #CBD5E1;
}

.dial-phase-btn:hover {
  border-color: var(--c-brick);
}

.dial-phase-btn.active {
  border-color: var(--c-brick);
  background: var(--c-brick-soft);
  box-shadow: 0 4px 16px rgba(158, 53, 36, 0.12);
}

body.night-active .dial-phase-btn.active {
  border-color: var(--c-gold);
  background: rgba(197, 147, 65, 0.15);
}

.dial-phase-btn .hour-tag {
  font-size: 11px;
  font-family: var(--font-cinzel);
  color: var(--c-ink-muted);
}

.dial-phase-btn .phase-title {
  font-family: var(--font-serif);
  font-weight: 700;
  font-size: 15px;
  margin: 2px 0;
}

.dial-phase-btn .phase-mood {
  font-size: 11px;
  color: var(--c-ink-faint);
}

/* 时间滑块控件 */
.slider-container {
  display: flex;
  align-items: center;
  gap: 20px;
}

.time-range-slider {
  flex: 1;
  -webkit-appearance: none;
  height: 8px;
  border-radius: 4px;
  background: linear-gradient(90deg, #F8E2B2 0%, #EAA86C 25%, #E66C52 50%, #526B88 75%, #1B2936 100%);
  outline: none;
}

.time-range-slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  width: 26px;
  height: 26px;
  border-radius: 50%;
  background: var(--c-brick);
  border: 3px solid #FFF;
  box-shadow: 0 2px 10px rgba(0,0,0,0.3);
  cursor: pointer;
  transition: transform 0.15s ease;
}

.time-range-slider::-webkit-slider-thumb:hover {
  transform: scale(1.2);
}

.time-display-bubble {
  font-family: var(--font-cinzel);
  font-size: 24px;
  font-weight: 700;
  color: var(--c-brick);
  min-width: 90px;
  text-align: right;
}

body.night-active .time-display-bubble {
  color: var(--c-gold);
}

/* 时序卡片流 */
.chrono-foods-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 20px;
}

/* ==========================================================================
   视域 Ⅲ：八重风味长卷 · 电影画幅解构剧场 (8 Chapters Deconstruction)
   ========================================================================== */
.chapters-nav-rail {
  display: flex;
  gap: 8px;
  overflow-x: auto;
  padding-bottom: 12px;
  margin-bottom: 24px;
  scrollbar-width: thin;
}

.chapter-nav-card {
  flex: none;
  width: 170px;
  padding: 14px;
  background: var(--c-shell-card);
  border: 1px solid var(--c-border);
  border-radius: var(--radius-lg);
  cursor: pointer;
  transition: all 0.25s ease;
  position: relative;
}

body.night-active .chapter-nav-card {
  background: #141F26;
  border-color: var(--c-dark-border);
  color: #E2E8F0;
}

.chapter-nav-card:hover {
  transform: translateY(-3px);
  border-color: var(--c-brick);
}

.chapter-nav-card.active {
  border-color: var(--c-brick);
  background: #FFF9F7;
  box-shadow: 0 6px 20px rgba(158, 53, 36, 0.15);
}

body.night-active .chapter-nav-card.active {
  border-color: var(--c-gold);
  background: #1C2B34;
}

.chapter-nav-num {
  font-family: var(--font-cinzel);
  font-size: 11px;
  color: var(--c-ink-muted);
}

.chapter-nav-title {
  font-family: var(--font-serif);
  font-size: 15px;
  font-weight: 700;
  margin: 3px 0;
  color: var(--c-ink);
}

body.night-active .chapter-nav-title {
  color: #FFF;
}

.chapter-nav-count {
  font-size: 11px;
  color: var(--c-brick);
}

/* 章节巨幕展台 */
.chapter-theater-stage {
  background: var(--c-shell-card);
  border: 1px solid var(--c-border);
  border-radius: var(--radius-xl);
  padding: 36px;
  box-shadow: var(--shadow-sm);
  margin-bottom: 32px;
  position: relative;
  overflow: hidden;
}

body.night-active .chapter-theater-stage {
  background: #131E24;
  border-color: var(--c-dark-border);
  color: #E2E8F0;
}

.theater-header {
  max-width: 800px;
  margin-bottom: 28px;
}

.theater-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 12px;
}

.theater-title {
  font-size: 32px;
  font-weight: 800;
  color: var(--c-ink);
  margin-bottom: 10px;
  line-height: 1.2;
}

body.night-active .theater-title {
  color: #FFF;
}

.theater-quote {
  font-family: var(--font-serif);
  font-style: italic;
  font-size: 16px;
  color: var(--c-ink-light);
  line-height: 1.7;
  padding-left: 16px;
  border-left: 3px solid var(--c-brick);
}

body.night-active .theater-quote {
  color: #CBD5E1;
  border-left-color: var(--c-gold);
}

/* 食材工艺交互解构展示台 (Exploded Diagram Card) */
.dissection-box {
  background: var(--c-paper);
  border: 1px dashed var(--c-border);
  border-radius: var(--radius-lg);
  padding: 24px;
  margin-top: 24px;
}

body.night-active .dissection-box {
  background: #192730;
  border-color: rgba(255,255,255,0.15);
}

/* ==========================================================================
   视域 Ⅳ：神凡山海谱 · 风味多极引力星盘 (Cosmic Gravity Constellation)
   ========================================================================== */
.constellation-shell {
  background: #0E161B;
  color: #FFF;
  border-radius: var(--radius-xl);
  overflow: hidden;
  box-shadow: var(--shadow-lg);
  border: 1px solid rgba(255, 255, 255, 0.1);
  padding: 28px;
  position: relative;
}

.constellation-toolbar {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  margin-bottom: 20px;
}

.star-dna-filters {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.dna-btn {
  padding: 5px 14px;
  border-radius: var(--radius-full);
  font-size: 12px;
  background: rgba(255, 255, 255, 0.08);
  color: #CBD5E1;
  border: 1px solid rgba(255, 255, 255, 0.15);
  transition: all 0.2s ease;
}

.dna-btn:hover {
  border-color: var(--c-gold);
  color: var(--c-gold);
}

.dna-btn.active {
  background: var(--c-gold);
  color: #0E161B;
  border-color: var(--c-gold);
  font-weight: 700;
}

.constellation-canvas-box {
  width: 100%;
  height: 600px;
  position: relative;
  background: radial-gradient(circle at 50% 50%, #15222A 0%, #0A1014 100%);
  border-radius: var(--radius-lg);
  border: 1px solid rgba(255, 255, 255, 0.06);
}

#star-canvas {
  width: 100%;
  height: 100%;
  display: block;
}

/* ==========================================================================
   视域 Ⅴ：老饕风味动线 · 策展漫游 (Cinematic Walkthrough)
   ========================================================================== */
.routes-selector-bar {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 28px;
}

.route-select-card {
  flex: 1;
  min-width: 240px;
  padding: 18px 20px;
  background: var(--c-shell-card);
  border: 1px solid var(--c-border);
  border-radius: var(--radius-lg);
  cursor: pointer;
  transition: all 0.25s ease;
}

body.night-active .route-select-card {
  background: #141F26;
  border-color: var(--c-dark-border);
  color: #E2E8F0;
}

.route-select-card:hover {
  border-color: var(--c-brick);
}

.route-select-card.active {
  border-color: var(--c-brick);
  background: #FFF9F7;
  box-shadow: 0 4px 18px rgba(158, 53, 36, 0.12);
}

body.night-active .route-select-card.active {
  border-color: var(--c-gold);
  background: #1B2932;
}

.cruise-walkthrough-panel {
  background: var(--c-shell-card);
  border: 1px solid var(--c-border);
  border-radius: var(--radius-xl);
  padding: 32px;
  box-shadow: var(--shadow-sm);
  position: relative;
}

body.night-active .cruise-walkthrough-panel {
  background: #131E24;
  border-color: var(--c-dark-border);
  color: #E2E8F0;
}

.cruise-action-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  padding-bottom: 20px;
  margin-bottom: 28px;
  border-bottom: 1px solid var(--c-border);
}

.cruise-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: var(--c-brick);
  color: #FFF;
  padding: 8px 20px;
  border-radius: var(--radius-full);
  font-size: 13px;
  font-weight: 600;
  transition: all 0.2s ease;
}

.cruise-btn:hover {
  background: var(--c-brick-dark);
  box-shadow: var(--shadow-brick);
}

.station-timeline {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 18px;
}

.station-card {
  border: 1px solid var(--c-border);
  border-radius: var(--radius-lg);
  padding: 18px;
  background: var(--c-paper);
  position: relative;
  transition: all 0.3s ease;
}

body.night-active .station-card {
  background: #192730;
  border-color: rgba(255,255,255,0.1);
}

.station-card.active-step {
  border-color: var(--c-brick);
  background: #FFFDFB;
  box-shadow: 0 8px 24px rgba(158, 53, 36, 0.15);
  transform: translateY(-4px);
}

body.night-active .station-card.active-step {
  border-color: var(--c-gold);
  background: #20333E;
}

/* ==========================================================================
   通用卡片与微交互
   ========================================================================== */
.food-card-v2 {
  background: var(--c-shell-card);
  border: 1px solid var(--c-border);
  border-radius: var(--radius-lg);
  padding: 20px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
  box-shadow: var(--shadow-sm);
  cursor: pointer;
}

body.night-active .food-card-v2 {
  background: #141F26;
  border-color: var(--c-dark-border);
  color: #E2E8F0;
}

.food-card-v2:hover {
  transform: translateY(-5px);
  border-color: var(--c-gold);
  box-shadow: var(--shadow-md);
}

.food-card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 8px;
}

.food-num-tag {
  font-family: var(--font-cinzel);
  font-size: 11px;
  color: var(--c-ink-faint);
  font-weight: 700;
}

.food-name {
  font-family: var(--font-serif);
  font-size: 18px;
  font-weight: 700;
  margin-bottom: 4px;
}

.food-sub {
  font-size: 12px;
  color: var(--c-ink-muted);
  margin-bottom: 10px;
}

body.night-active .food-sub {
  color: #94A3B8;
}

.food-quote-snippet {
  font-size: 13px;
  color: var(--c-ink-light);
  line-height: 1.6;
  margin-bottom: 14px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

body.night-active .food-quote-snippet {
  color: #CBD5E1;
}

.food-card-footer {
  padding-top: 12px;
  border-top: 1px solid var(--c-border);
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 11px;
  color: var(--c-ink-muted);
}

body.night-active .food-card-footer {
  border-top-color: rgba(255, 255, 255, 0.08);
}

/* ==========================================================================
   全局搜索模态框、详情模态框、寻味印章册抽屉
   ========================================================================== */
.modal-layer {
  position: fixed;
  inset: 0;
  background: rgba(14, 20, 24, 0.7);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  z-index: 2000;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.3s ease;
}

.modal-layer.active {
  opacity: 1;
  pointer-events: auto;
}

.modal-window {
  background: var(--c-shell-card);
  border: 1px solid var(--c-border);
  border-radius: var(--radius-xl);
  width: 100%;
  max-width: 820px;
  max-height: 88vh;
  overflow-y: auto;
  padding: 36px;
  position: relative;
  box-shadow: 0 24px 60px rgba(0,0,0,0.3);
  transform: scale(0.96) translateY(20px);
  transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}

.modal-layer.active .modal-window {
  transform: scale(1) translateY(0);
}

.modal-close-btn {
  position: absolute;
  top: 20px;
  right: 20px;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--c-ink-muted);
  transition: all 0.2s ease;
}

.modal-close-btn:hover {
  background: rgba(0, 0, 0, 0.06);
  color: var(--c-ink);
}

/* 寻味印章册侧边抽屉 */
.passport-drawer {
  position: fixed;
  top: 0;
  right: 0;
  bottom: 0;
  width: 420px;
  max-width: 88vw;
  background: var(--c-shell-card);
  border-left: 1px solid var(--c-border);
  box-shadow: -10px 0 40px rgba(0,0,0,0.15);
  z-index: 2100;
  transform: translateX(105%);
  transition: transform 0.35s cubic-bezier(0.16, 1, 0.3, 1);
  display: flex;
  flex-direction: column;
}

.passport-drawer.open {
  transform: translateX(0);
}

/* 打印样式适配 */
@media print {
  #astrolabe-bar, .prologue-banner, .cartogram-toolbar, .dial-phase-bar, .chapters-nav-rail, .constellation-toolbar, .routes-selector-bar, .modal-layer {
    display: none !important;
  }
  .passport-drawer {
    position: static !important;
    transform: none !important;
    width: 100% !important;
    max-width: 100% !important;
    border: none !important;
  }
}
</style>
</head>
<body>

  <!-- 刺桐食肆全景仪 · 顶栏交互罗盘 -->
  <header id="astrolabe-bar">
    <div class="container nav-wrapper">
      <a href="#" class="brand-badge" title="回到顶部">
        <div class="brand-seal">刺桐</div>
        <div class="brand-titles">
          <span class="brand-name">刺桐食肆全景仪</span>
          <span class="brand-sub">Quanzhou Gastronomy Atlas · v2</span>
        </div>
      </a>

      <!-- 五重视角切换罗盘 -->
      <nav class="view-tabs-group" id="view-tabs-nav">
        <button class="view-tab-btn active" data-view="cartogram">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polygon points="16.24 7.76 14.12 14.12 7.76 16.24 9.88 9.88 16.24 7.76"/></svg>
          <span>Ⅰ·山海沙盘</span>
        </button>
        <button class="view-tab-btn" data-view="chrono">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
          <span>Ⅱ·十二时辰</span>
        </button>
        <button class="view-tab-btn" data-view="chapters">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="2"/><line x1="9" y1="3" x2="9" y2="21"/></svg>
          <span>Ⅲ·八章长卷</span>
        </button>
        <button class="view-tab-btn" data-view="constellation">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>
          <span>Ⅳ·神凡星盘</span>
        </button>
        <button class="view-tab-btn" data-view="routes">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="4" y1="9" x2="20" y2="9"/><line x1="4" y1="15" x2="20" y2="15"/><line x1="10" y1="3" x2="8" y2="21"/><line x1="16" y1="3" x2="14" y2="21"/></svg>
          <span>Ⅴ·策展动线</span>
        </button>
      </nav>

      <!-- 右侧快捷交互动作 -->
      <div class="nav-actions">
        <button class="action-icon-btn" id="open-search-btn" title="全局搜索 (快捷键 Ctrl+K)">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
        </button>
        <button class="action-icon-btn" id="open-passport-btn" title="我的寻味印章册">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"/></svg>
          <span class="action-badge" id="passport-count-badge">0</span>
        </button>
      </div>
    </div>
  </header>

  <!-- 页面顶部宣言横幅 -->
  <section class="prologue-banner">
    <div class="container prologue-flex">
      <div class="prologue-motto">
        <span class="motto-seal">世界美食之都</span>
        <span class="motto-text">“半城烟火半城仙 —— 供桌上的糕粿与油锅边的炸物同源，神明与夜宵共用一张餐桌。”</span>
      </div>
      <div class="stats-capsule">
        <span class="stat-item"><b>8</b>大原版章节</span>
        <span class="stat-item"><b>52</b>处世遗珍味</span>
        <span class="stat-item"><b>50</b>家真实食肆</span>
        <span class="stat-item"><b>6</b>大地理板块</span>
      </div>
    </div>
  </section>

  <!-- 主体视域展示舞台 -->
  <main class="view-stage">

    <!-- ==========================================================================
         视域 Ⅰ · 刺桐山海图 (Topographic Cartogram & Landscape Map)
         ========================================================================== -->
    <section class="view-pane active" id="pane-cartogram">
      <div class="container">
        <div class="cartogram-shell">
          <!-- 工具栏 -->
          <div class="cartogram-toolbar">
            <div class="district-filter-group" id="carto-district-filters">
              <button class="geo-btn active" data-geo="all">全域俯瞰 (50店)</button>
              <button class="geo-btn" data-geo="鲤城古城">鲤城古城 (27)</button>
              <button class="geo-btn" data-geo="石狮">石狮老街 (13)</button>
              <button class="geo-btn" data-geo="晋江·安海">晋江·安海 (4)</button>
              <button class="geo-btn" data-geo="晋江·深沪">晋江·深沪 (2)</button>
              <button class="geo-btn" data-geo="晋江·张林">晋江·张林 (3)</button>
              <button class="geo-btn" data-geo="丰泽">丰泽·蟳埔 (1)</button>
            </div>
            
            <div class="attitude-filter-group">
              <button class="night-mode-toggle-btn" id="night-lantern-btn">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2a5 5 0 0 1 5 5v3a5 5 0 0 1-10 0V7a5 5 0 0 1 5-5z"/><line x1="12" y1="15" x2="12" y2="22"/></svg>
                <span>点亮夜市灯火</span>
              </button>
            </div>
          </div>

          <!-- SVG 拓扑沙盘画布 -->
          <div class="cartogram-canvas-box" id="carto-box">
            <svg class="cartogram-svg" viewBox="0 0 1000 700" id="carto-svg">
              <defs>
                <!-- 山水纹理滤镜 -->
                <linearGradient id="riverGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                  <stop offset="0%" stop-color="#4F7E84" stop-opacity="0.35"/>
                  <stop offset="100%" stop-color="#2D5C63" stop-opacity="0.6"/>
                </linearGradient>
                <radialGradient id="cityGlow" cx="50%" cy="50%" r="50%">
                  <stop offset="0%" stop-color="#A8352A" stop-opacity="0.08"/>
                  <stop offset="100%" stop-color="#A8352A" stop-opacity="0"/>
                </radialGradient>
              </defs>

              <!-- 戴云山脉西北山形背景 -->
              <path d="M 50,180 Q 150,80 280,120 T 450,90 Q 520,60 620,110 T 780,70 L 850,150 L 50,220 Z" fill="#EAE3D2" opacity="0.45"/>
              <text x="80" y="110" font-family="Noto Serif SC" font-size="13" fill="#8C8073" opacity="0.7">戴云山脉余脉 · 崇山沃野</text>

              <!-- 晋江与入海口水系 -->
              <path d="M 220,110 Q 320,180 390,240 T 480,380 Q 520,440 600,480 T 750,560 Q 820,600 950,650" fill="none" stroke="url(#riverGrad)" stroke-width="48" stroke-linecap="round"/>
              <path d="M 220,110 Q 320,180 390,240 T 480,380 Q 520,440 600,480 T 750,560 Q 820,600 950,650" fill="none" stroke="#2F6E7A" stroke-width="4" stroke-dasharray="6,8" opacity="0.6"/>
              <text x="540" y="445" font-family="Noto Serif SC" font-size="12" fill="#3D6A70" opacity="0.8" transform="rotate(35, 540, 445)">晋江入海流向 · 刺桐港古航道</text>

              <!-- 台湾海峡与海岸波浪 -->
              <path d="M 720,220 C 780,320 850,420 980,520 L 1000,700 L 600,700 Z" fill="#DCE7E5" opacity="0.3"/>
              <text x="840" y="670" font-family="Noto Serif SC" font-size="14" fill="#4B6F73" opacity="0.6">台湾海峡 · 向海讨鲜</text>

              <!-- 六大地理板块轮廓区 -->
              <!-- 1. 鲤城古城 (核心十字轴) -->
              <g id="zone-gucheng">
                <rect x="360" y="210" width="190" height="225" rx="16" fill="url(#cityGlow)" stroke="#A8352A" stroke-width="1.5" stroke-dasharray="4,4" opacity="0.65"/>
                <text x="375" y="235" font-family="Noto Serif SC" font-weight="700" font-size="13" fill="#A8352A">鲤城古城核心 (27家)</text>
                <text x="375" y="250" font-size="10" fill="#782215" opacity="0.8">西街 · 中山路 · 涂门街 · 县后街</text>
              </g>

              <!-- 2. 石狮老街与商市 -->
              <g id="zone-shishi">
                <rect x="630" y="470" width="160" height="160" rx="14" fill="#FAF0E6" stroke="#C59341" stroke-width="1.5" stroke-dasharray="4,4" opacity="0.65"/>
                <text x="645" y="495" font-family="Noto Serif SC" font-weight="700" font-size="13" fill="#C59341">石狮老街与夜市 (13家)</text>
                <text x="645" y="510" font-size="10" fill="#8C6320" opacity="0.8">城隍老街 · 旧菜市 · 新华路</text>
              </g>

              <!-- 3. 晋江·安海 (五里桥头) -->
              <g id="zone-anhai">
                <rect x="210" y="460" width="125" height="115" rx="12" fill="#E6EEF0" stroke="#366B73" stroke-width="1.5" stroke-dasharray="4,4" opacity="0.6"/>
                <text x="220" y="480" font-family="Noto Serif SC" font-weight="700" font-size="12" fill="#366B73">晋江 · 安海 (4家)</text>
                <text x="220" y="495" font-size="10" fill="#204A50" opacity="0.8">五里桥 · 土笋冻故乡</text>
              </g>

              <!-- 4. 晋江·张林 (姜母鸭一条街) -->
              <g id="zone-zhanglin">
                <rect x="250" y="350" width="100" height="85" rx="10" fill="#F4EFE6" stroke="#9E4A28" stroke-width="1.5" stroke-dasharray="4,4" opacity="0.6"/>
                <text x="260" y="370" font-family="Noto Serif SC" font-weight="700" font-size="11" fill="#9E4A28">晋江 · 张林 (3家)</text>
                <text x="260" y="385" font-size="9" fill="#7A3215">磁灶吃鸭金字招牌</text>
              </g>

              <!-- 5. 晋江·深沪 (渔港小镇) -->
              <g id="zone-shenhu">
                <rect x="520" y="595" width="115" height="80" rx="10" fill="#E0EBEB" stroke="#2F6E7A" stroke-width="1.5" stroke-dasharray="4,4" opacity="0.6"/>
                <text x="530" y="615" font-family="Noto Serif SC" font-weight="700" font-size="11" fill="#2F6E7A">晋江 · 深沪 (2家)</text>
                <text x="530" y="630" font-size="9" fill="#1C454D">宝泉庵 · 壶仔饭水丸</text>
              </g>

              <!-- 6. 丰泽·蟳埔 -->
              <g id="zone-fengze">
                <rect x="645" y="235" width="110" height="75" rx="10" fill="#F0EDE4" stroke="#8C7A68" stroke-width="1.5" stroke-dasharray="4,4" opacity="0.6"/>
                <text x="655" y="255" font-family="Noto Serif SC" font-weight="700" font-size="11" fill="#5F544A">丰泽 · 蟳埔之侧 (1家)</text>
                <text x="655" y="270" font-size="9" fill="#5F544A">渔港小馆 · 炣鲳鱼</text>
              </g>

              <!-- 50 店动态渲染层 (由 JS 注入) -->
              <g id="carto-shops-layer"></g>
            </svg>

            <!-- 店铺侧滑牌匾抽屉 (Shop Ledger Drawer) -->
            <div class="shop-ledger-drawer" id="shop-drawer">
              <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:16px;">
                <div>
                  <span id="drawer-attitude" class="motto-seal">本地力荐</span>
                  <h3 id="drawer-name" style="font-family:var(--font-serif); font-size:22px; font-weight:700; margin-top:6px;">店铺名</h3>
                  <p id="drawer-district" style="font-size:12px; color:var(--c-ink-muted); margin-top:2px;">街区 · 地址</p>
                </div>
                <button id="close-drawer-btn" style="padding:6px; color:var(--c-ink-faint);">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
                </button>
              </div>

              <div style="flex:1; overflow-y:auto; padding-right:4px;">
                <div style="margin-bottom:20px;">
                  <h5 style="font-size:11px; text-transform:uppercase; letter-spacing:0.1em; color:var(--c-ink-muted); margin-bottom:6px;">老饕探店指南</h5>
                  <p id="drawer-desc" style="font-size:14px; line-height:1.7; color:var(--c-ink-light);">探店实录</p>
                </div>

                <div style="margin-bottom:20px;">
                  <h5 style="font-size:11px; text-transform:uppercase; letter-spacing:0.1em; color:var(--c-ink-muted); margin-bottom:8px;">招牌对应名点</h5>
                  <div id="drawer-dishes" style="display:flex; flex-wrap:wrap; gap:6px;"></div>
                </div>
              </div>

              <div style="padding-top:16px; border-top:1px solid var(--c-border);">
                <button id="drawer-bookmark-btn" style="width:100%; padding:10px; border-radius:var(--radius-md); background:var(--c-brick); color:#FFF; font-weight:600; font-size:13px; display:flex; align-items:center; justify-content:center; gap:8px;">
                  <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"/></svg>
                  <span>收藏至寻味印章册</span>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ==========================================================================
         视域 Ⅱ · 人间十二时辰 (24-Hour Chrono-Dial)
         ========================================================================== -->
    <section class="view-pane" id="pane-chrono">
      <div class="container">
        <!-- 环形/横轴时辰控制器 -->
        <div class="chrono-controller">
          <div class="dial-phase-bar">
            <button class="dial-phase-btn active" data-hour="7">
              <div class="hour-tag">06:00 - 09:00</div>
              <div class="phase-title">寅卯 · 破晓晨炊</div>
              <div class="phase-mood">面线糊鱼骨派 · 蛋花花生汤</div>
            </button>
            <button class="dial-phase-btn" data-hour="12">
              <div class="hour-tag">11:00 - 13:30</div>
              <div class="phase-title">巳午 · 晌午正席</div>
              <div class="phase-mood">牛肉三件套 · 72变卤面</div>
            </button>
            <button class="dial-phase-btn" data-hour="15">
              <div class="hour-tag">14:30 - 17:30</div>
              <div class="phase-title">未申 · 闽南茶配</div>
              <div class="phase-mood">安海土笋冻 · 天后宫石花膏</div>
            </button>
            <button class="dial-phase-btn" data-hour="19">
              <div class="hour-tag">18:00 - 20:30</div>
              <div class="phase-title">酉戌 · 暮色大席</div>
              <div class="phase-mood">炭火盐烧姜母鸭 · 居酒屋烧酒配</div>
            </button>
            <button class="dial-phase-btn" data-hour="23">
              <div class="hour-tag">21:00 - 02:00</div>
              <div class="phase-title">亥子 · 暗夜排档</div>
              <div class="phase-mood">花生酱炒钉螺 · 大蒜面线糊</div>
            </button>
          </div>

          <div class="slider-container">
            <span style="font-size:12px; color:var(--c-ink-muted);">时辰推移</span>
            <input type="range" min="6" max="24" step="1" value="7" class="time-range-slider" id="hour-slider">
            <div class="time-display-bubble" id="current-hour-label">07:00</div>
          </div>
        </div>

        <!-- 当前时段美食流 -->
        <div class="chrono-foods-grid" id="chrono-foods-list"></div>
      </div>
    </section>

    <!-- ==========================================================================
         视域 Ⅲ · 八重风味长卷 (8 Chapters Cinematic Deconstruction Theater)
         ========================================================================== -->
    <section class="view-pane" id="pane-chapters">
      <div class="container">
        <!-- 章节选择横轨 -->
        <div class="chapters-nav-rail" id="chapters-rail"></div>

        <!-- 当前章节巨幕展台 -->
        <div class="chapter-theater-stage" id="chapter-stage">
          <div class="theater-header">
            <div class="theater-badge">
              <span class="motto-seal" id="theater-num-tag">第 01 章</span>
              <span style="font-size:12px; color:var(--c-ink-muted);" id="theater-page-tag">PDF 第 2 页</span>
            </div>
            <h2 class="theater-title" id="theater-title">主食配菜二合一</h2>
            <div class="theater-quote" id="theater-desc">
              一碗解决一顿。泉州人把主食与配菜烩进同一只碗、卷进同一张饼皮、包进同一片粽叶——面线糊是这套逻辑的扛把子，咸饭、烧肉粽、润饼菜各擅其场。
            </div>
          </div>

          <!-- 食材工艺交互解构展示台 (Exploded Diagram / Lab) -->
          <div class="dissection-box" id="chapter-dissection-area"></div>
        </div>

        <!-- 属于本章的美食卡片 -->
        <h4 style="font-family:var(--font-serif); font-size:18px; margin-bottom:16px;">本章收录珍味名录</h4>
        <div class="chrono-foods-grid" id="chapter-foods-grid"></div>
      </div>
    </section>

    <!-- ==========================================================================
         视域 Ⅳ · 神凡山海谱 (Cosmic Gravity Constellation)
         ========================================================================== -->
    <section class="view-pane" id="pane-constellation">
      <div class="container">
        <div class="constellation-shell">
          <div class="constellation-toolbar">
            <div>
              <h3 style="font-family:var(--font-serif); font-size:22px; font-weight:700;">神凡山海谱 · 风味多极引力星图</h3>
              <p style="font-size:12px; color:#94A3B8; margin-top:2px;">以「山 ↔ 海」为横轴，「咸 ↔ 甜」为纵轴，探索 52 味美食与神仙、凡俗、海丝的共生网络</p>
            </div>
            <div class="star-dna-filters" id="dna-filters">
              <button class="dna-btn active" data-dna="all">全部星宿 (52)</button>
              <button class="dna-btn" data-dna="海丝印记">海丝香料 (8)</button>
              <button class="dna-btn" data-dna="神明供桌">神明供桌 (11)</button>
              <button class="dna-btn" data-dna="半甜咸魔性">迷之半甜咸 (6)</button>
              <button class="dna-btn" data-dna="大味至简">大味至简 (10)</button>
              <button class="dna-btn" data-dna="一人食神装">一人食神装 (8)</button>
            </div>
          </div>

          <div class="constellation-canvas-box">
            <canvas id="star-canvas"></canvas>
            <!-- 象限极轴标签 -->
            <div style="position:absolute; left:20px; top:50%; transform:translateY(-50%); font-size:12px; color:rgba(255,255,255,0.4); font-family:var(--font-serif); pointer-events:none;">◀ 山珍沃土 (老姜/番薯/黄牛)</div>
            <div style="position:absolute; right:20px; top:50%; transform:translateY(-50%); font-size:12px; color:rgba(255,255,255,0.4); font-family:var(--font-serif); pointer-events:none;">海错狂澜 (星虫/海蛎/马鲛) ▶</div>
            <div style="position:absolute; top:20px; left:50%; transform:translateX(-50%); font-size:12px; color:rgba(255,255,255,0.4); font-family:var(--font-serif); pointer-events:none;">▲ 纯正甘甜 (百花蜜水/花生汤)</div>
            <div style="position:absolute; bottom:20px; left:50%; transform:translateX(-50%); font-size:12px; color:rgba(255,255,255,0.4); font-family:var(--font-serif); pointer-events:none;">▼ 咸鲜大味 (骨汤卤味/酱油水)</div>
          </div>
        </div>
      </div>
    </section>

    <!-- ==========================================================================
         视域 Ⅴ · 老饕风味动线 (Cinematic Walkthrough)
         ========================================================================== -->
    <section class="view-pane" id="pane-routes">
      <div class="container">
        <!-- 路线选择器 -->
        <div class="routes-selector-bar" id="routes-selector-bar"></div>

        <!-- 漫游展示卡 -->
        <div class="cruise-walkthrough-panel">
          <div class="cruise-action-row">
            <div>
              <span class="motto-seal" id="route-badge">古城步行圈</span>
              <h3 id="route-title" style="font-family:var(--font-serif); font-size:24px; font-weight:700; margin-top:6px;">路线标题</h3>
              <p id="route-desc" style="font-size:14px; color:var(--c-ink-light); margin-top:4px;">路线概述说明</p>
            </div>
            <div>
              <button class="cruise-btn" id="start-cruise-btn">
                <svg width="15" height="15" viewBox="0 0 24 24" fill="currentColor"><polygon points="5 3 19 12 5 21 5 3"/></svg>
                <span id="cruise-btn-label">开启自动漫游</span>
              </button>
            </div>
          </div>

          <!-- 站点时间线 -->
          <div class="station-timeline" id="route-stations-timeline"></div>
        </div>
      </div>
    </section>
  </main>

  <!-- 全局搜索弹窗 (Ctrl + K) -->
  <div class="modal-layer" id="search-modal">
    <div class="modal-window" style="max-width:680px; padding:28px;">
      <button class="modal-close-btn" id="close-search-btn">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
      </button>
      <div style="margin-bottom:20px;">
        <h3 style="font-family:var(--font-serif); font-size:20px; font-weight:700;">搜索 52 味珍味与 50 家老字号</h3>
        <p style="font-size:12px; color:var(--c-ink-muted); margin-top:2px;">支持输入菜名、料头、街区、风味特征或店铺招牌</p>
      </div>
      <input type="text" id="global-search-input" placeholder="输入关键词 (如：面线糊、醋肉、安海、姜母鸭、花生酱...)" style="width:100%; padding:14px 18px; border-radius:var(--radius-md); border:1px solid var(--c-border); font-size:15px; outline:none; background:var(--c-paper);">
      <div id="search-results-list" style="margin-top:20px; max-height:420px; overflow-y:auto; display:flex; flex-direction:column; gap:10px;"></div>
    </div>
  </div>

  <!-- 美食深度品鉴模态框 -->
  <div class="modal-layer" id="food-modal">
    <div class="modal-window">
      <button class="modal-close-btn" id="close-food-modal-btn">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
      </button>
      <div id="food-modal-body"></div>
    </div>
  </div>

  <!-- 寻味印章册侧边抽屉 -->
  <aside class="passport-drawer" id="passport-drawer">
    <div style="padding:24px; border-bottom:1px solid var(--c-border); display:flex; justify-content:space-between; align-items:center;">
      <div>
        <h3 style="font-family:var(--font-serif); font-size:18px; font-weight:700;">我的泉州寻味印章册</h3>
        <p style="font-size:12px; color:var(--c-ink-muted);">已收藏美食与老字号打卡清单</p>
      </div>
      <button id="close-passport-drawer-btn" style="padding:6px; color:var(--c-ink-faint);">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
      </button>
    </div>
    <div style="padding:16px 24px; background:var(--c-paper); border-bottom:1px solid var(--c-border); display:flex; justify-content:space-between; align-items:center; font-size:12px;">
      <span>打卡解锁进度</span>
      <b style="color:var(--c-brick); font-family:var(--font-serif);" id="passport-progress-pct">0 / 52 味</b>
    </div>
    <div style="flex:1; overflow-y:auto; padding:20px; display:flex; flex-direction:column; gap:10px;" id="passport-list-box"></div>
    <div style="padding:20px; border-top:1px solid var(--c-border); background:var(--c-paper); display:flex; flex-direction:column; gap:8px;">
      <button onclick="window.print()" style="padding:11px; border-radius:var(--radius-md); background:var(--c-brick); color:#FFF; font-weight:600; font-size:13px; display:flex; align-items:center; justify-content:center; gap:8px;">
        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 6 2 18 2 18 9"/><path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"/><rect x="6" y="14" width="12" height="8"/></svg>
        <span>打印 / 导出我的寻味手账</span>
      </button>
      <button id="clear-passport-btn" style="font-size:12px; color:var(--c-ink-faint); text-align:center; padding:4px;">清空我的印章册</button>
    </div>
  </aside>

  <!-- 嵌入完整核心数据集与交互逻辑 -->
  <script>
    const CHAPTERS = """ + chapters_json + """;
    const FOODS = """ + foods_json + """;
    const SHOPS = """ + shops_json + """;
    const ROUTES = """ + routes_json + """;
    const ORIGINS = """ + origins_json + """;

    // 交互状态
    const STATE = {
      currentView: 'cartogram',
      activeGeo: 'all',
      nightMode: false,
      selectedShop: null,
      currentHour: 7,
      activeChapterId: 1,
      activeDna: 'all',
      activeRouteId: 'route-a',
      cruiseInterval: null,
      cruiseStep: 0,
      passport: JSON.parse(localStorage.getItem('qz_food_passport_v2') || '[1, 16, 21, 37, 44]')
    };

    // 态度配色映射
    const ATTITUDE_COLORS = {
      '本地力荐': '#A8352A',
      '老字号': '#B98A2F',
      '隐世小店': '#2F6E7A',
      '夜宵摊': '#D97724',
      '标杆名店': '#8A2E4B',
      '游客巨头': '#7D7973'
    };

    // 初始化
    document.addEventListener('DOMContentLoaded', () => {
      initNavigation();
      initCartogram();
      initChronoDial();
      initChaptersTheater();
      initConstellation();
      initRoutes();
      initPassport();
      initSearch();
    });

    /* ==========================================================================
       1. 导航与视域切换控制器
       ========================================================================== */
    function initNavigation() {
      const tabs = document.querySelectorAll('#view-tabs-nav .view-tab-btn');
      tabs.forEach(btn => {
        btn.addEventListener('click', () => {
          const view = btn.dataset.view;
          switchView(view);
        });
      });

      // 夜市灯火模式全局联动
      const nightBtn = document.getElementById('night-lantern-btn');
      nightBtn.addEventListener('click', () => {
        STATE.nightMode = !STATE.nightMode;
        document.body.classList.toggle('night-active', STATE.nightMode);
        document.getElementById('astrolabe-bar').classList.toggle('night-mode', STATE.nightMode);
        nightBtn.classList.toggle('on', STATE.nightMode);
        renderCartogramShops();
      });
    }

    function switchView(viewName) {
      STATE.currentView = viewName;
      document.querySelectorAll('#view-tabs-nav .view-tab-btn').forEach(b => {
        b.classList.toggle('active', b.dataset.view === viewName);
      });
      document.querySelectorAll('.view-pane').forEach(p => {
        p.classList.remove('active');
      });
      const targetPane = document.getElementById('pane-' + viewName);
      if (targetPane) {
        targetPane.classList.add('active');
        if (viewName === 'constellation') {
          setTimeout(renderConstellationCanvas, 50);
        }
      }
    }

    /* ==========================================================================
       2. 视域 Ⅰ · 刺桐山海图 (Topographic Cartogram & Landscape Map)
       ========================================================================== */
    function initCartogram() {
      // 地区筛选按钮
      document.querySelectorAll('#carto-district-filters .geo-btn').forEach(btn => {
        btn.addEventListener('click', () => {
          document.querySelectorAll('#carto-district-filters .geo-btn').forEach(b => b.classList.remove('active'));
          btn.classList.add('active');
          STATE.activeGeo = btn.dataset.geo;
          renderCartogramShops();
        });
      });

      // 关闭店铺抽屉
      document.getElementById('close-drawer-btn').addEventListener('click', () => {
        document.getElementById('shop-drawer').classList.remove('open');
      });

      // 抽屉收藏按钮
      document.getElementById('drawer-bookmark-btn').addEventListener('click', () => {
        if (!STATE.selectedShop) return;
        const matchedFood = FOODS.find(f => f.shops.includes(STATE.selectedShop.name));
        if (matchedFood) {
          togglePassport(matchedFood.id);
        }
      });

      renderCartogramShops();
    }

    function renderCartogramShops() {
      const layer = document.getElementById('carto-shops-layer');
      layer.innerHTML = '';

      SHOPS.forEach(shop => {
        // 区域筛选
        if (STATE.activeGeo !== 'all' && shop.district !== STATE.activeGeo) {
          return;
        }

        const isNightShop = shop.attitude === '夜宵摊' || shop.desc.includes('夜市') || shop.desc.includes('夜宵');
        const color = ATTITUDE_COLORS[shop.attitude] || '#A8352A';

        // 夜灯模式下强化夜宵摊
        let opacity = 1;
        let r = 8;
        if (STATE.nightMode) {
          if (isNightShop) {
            r = 13;
          } else {
            opacity = 0.25;
          }
        }

        const g = document.createElementNS('http://www.w3.org/2000/svg', 'g');
        g.setAttribute('class', 'shop-pin' + (isNightShop && STATE.nightMode ? ' highlighted' : ''));
        g.setAttribute('transform', `translate(${shop.x}, ${shop.y})`);

        // 发光外圈
        if (isNightShop && STATE.nightMode) {
          const glow = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
          glow.setAttribute('r', '18');
          glow.setAttribute('fill', '#E07A2B');
          glow.setAttribute('opacity', '0.4');
          g.appendChild(glow);
        }

        const circle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
        circle.setAttribute('r', r);
        circle.setAttribute('fill', color);
        circle.setAttribute('stroke', '#FFFFFF');
        circle.setAttribute('stroke-width', '2');
        circle.setAttribute('opacity', opacity);
        g.appendChild(circle);

        // 文字标注
        const text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
        text.setAttribute('x', '12');
        text.setAttribute('y', '4');
        text.setAttribute('font-family', 'Noto Serif SC');
        text.setAttribute('font-size', '11');
        text.setAttribute('font-weight', '600');
        text.setAttribute('fill', STATE.nightMode ? (isNightShop ? '#FFD494' : '#64748B') : '#2D2620');
        text.setAttribute('opacity', opacity);
        text.textContent = shop.name;
        g.appendChild(text);

        g.addEventListener('click', () => {
          openShopDrawer(shop);
        });

        layer.appendChild(g);
      });
    }

    function openShopDrawer(shop) {
      STATE.selectedShop = shop;
      const drawer = document.getElementById('shop-drawer');
      document.getElementById('drawer-name').textContent = shop.name;
      document.getElementById('drawer-attitude').textContent = shop.attitude;
      document.getElementById('drawer-attitude').style.borderColor = ATTITUDE_COLORS[shop.attitude] || '#A8352A';
      document.getElementById('drawer-attitude').style.color = ATTITUDE_COLORS[shop.attitude] || '#A8352A';
      document.getElementById('drawer-district').textContent = shop.district + ' · ' + shop.street;
      document.getElementById('drawer-desc').textContent = shop.desc;

      // 关联名点
      const dishesBox = document.getElementById('drawer-dishes');
      dishesBox.innerHTML = '';
      const matchedFoods = FOODS.filter(f => f.shops.includes(shop.name));
      if (matchedFoods.length === 0) {
        dishesBox.innerHTML = '<span style="font-size:12px; color:var(--c-ink-faint);">文章综合探店地标</span>';
      } else {
        matchedFoods.forEach(f => {
          const btn = document.createElement('button');
          btn.className = 'geo-btn';
          btn.style.fontSize = '11px';
          btn.style.padding = '3px 8px';
          btn.textContent = f.name;
          btn.addEventListener('click', () => {
            openFoodModal(f.id);
          });
          dishesBox.appendChild(btn);
        });
      }

      drawer.classList.add('open');
    }

    /* ==========================================================================
       3. 视域 Ⅱ · 人间十二时辰 (24-Hour Chrono-Dial)
       ========================================================================== */
    function initChronoDial() {
      const slider = document.getElementById('hour-slider');
      const label = document.getElementById('current-hour-label');
      const phaseBtns = document.querySelectorAll('.dial-phase-btn');

      slider.addEventListener('input', (e) => {
        const h = parseInt(e.target.value, 10);
        STATE.currentHour = h;
        label.textContent = (h < 10 ? '0' + h : h) + ':00';
        updateChronoPhaseBtns(h);
        renderChronoFoods(h);
      });

      phaseBtns.forEach(btn => {
        btn.addEventListener('click', () => {
          const h = parseInt(btn.dataset.hour, 10);
          slider.value = h;
          STATE.currentHour = h;
          label.textContent = (h < 10 ? '0' + h : h) + ':00';
          updateChronoPhaseBtns(h);
          renderChronoFoods(h);
        });
      });

      renderChronoFoods(7);
    }

    function updateChronoPhaseBtns(h) {
      document.querySelectorAll('.dial-phase-btn').forEach(b => {
        const ph = parseInt(b.dataset.hour, 10);
        let active = false;
        if (h <= 9 && ph === 7) active = true;
        else if (h > 9 && h <= 14 && ph === 12) active = true;
        else if (h > 14 && h <= 17 && ph === 15) active = true;
        else if (h > 17 && h <= 20 && ph === 19) active = true;
        else if (h > 20 && ph === 23) active = true;
        b.classList.toggle('active', active);
      });
    }

    function renderChronoFoods(h) {
      const container = document.getElementById('chrono-foods-list');
      container.innerHTML = '';

      let filterKey = '';
      if (h <= 9) filterKey = '早市';
      else if (h <= 14) filterKey = '午市';
      else if (h <= 17) filterKey = '下午茶';
      else if (h <= 20) filterKey = '晚市';
      else filterKey = '夜宵';

      const matched = FOODS.filter(f => f.time.includes(filterKey) || f.time.includes('全天'));

      matched.forEach(food => {
        const card = document.createElement('div');
        card.className = 'food-card-v2';
        card.innerHTML = `
          <div>
            <div class="food-card-header">
              <span class="motto-seal">${food.category}</span>
              <span class="food-num-tag">NO.${food.id < 10 ? '0'+food.id : food.id} · ${food.time}</span>
            </div>
            <h4 class="food-name">${food.name}</h4>
            <div class="food-sub">${food.sub} · ${food.district}</div>
            <p class="food-quote-snippet">“${food.quote}”</p>
          </div>
          <div class="food-card-footer">
            <span>味型：${food.flavor}</span>
            <span style="color:var(--c-brick); font-weight:600;">深度解构 ➔</span>
          </div>
        `;
        card.addEventListener('click', () => openFoodModal(food.id));
        container.appendChild(card);
      });
    }

    /* ==========================================================================
       4. 视域 Ⅲ · 八重风味长卷 (8 Chapters Deconstruction Theater)
       ========================================================================== */
    function initChaptersTheater() {
      const rail = document.getElementById('chapters-rail');
      rail.innerHTML = '';

      CHAPTERS.forEach(chap => {
        const card = document.createElement('div');
        card.className = 'chapter-nav-card' + (chap.id === STATE.activeChapterId ? ' active' : '');
        card.innerHTML = `
          <div class="chapter-nav-num">第 ${chap.num} 章</div>
          <div class="chapter-nav-title">${chap.title}</div>
          <div class="chapter-nav-count">${chap.foodCount} 味名馔</div>
        `;
        card.addEventListener('click', () => {
          STATE.activeChapterId = chap.id;
          document.querySelectorAll('.chapter-nav-card').forEach(c => c.classList.remove('active'));
          card.classList.add('active');
          renderChapterContent(chap.id);
        });
        rail.appendChild(card);
      });

      renderChapterContent(1);
    }

    function renderChapterContent(chapId) {
      const chap = CHAPTERS.find(c => c.id === chapId);
      if (!chap) return;

      document.getElementById('theater-num-tag').textContent = `第 ${chap.num} 章 · PDF 第 ${chap.page} 页原版标题`;
      document.getElementById('theater-page-tag').textContent = chap.proposition;
      document.getElementById('theater-title').textContent = chap.title;
      document.getElementById('theater-desc').textContent = chap.desc;

      // 食材工艺交互解构展示台 (Exploded Diagram Interactive Lab)
      const dissection = document.getElementById('chapter-dissection-area');
      dissection.innerHTML = getChapterDissectionHTML(chapId);

      // 本章食物
      const grid = document.getElementById('chapter-foods-grid');
      grid.innerHTML = '';
      const chapFoods = FOODS.filter(f => f.chapterId === chapId);
      chapFoods.forEach(food => {
        const card = document.createElement('div');
        card.className = 'food-card-v2';
        card.innerHTML = `
          <div>
            <div class="food-card-header">
              <span class="motto-seal">${food.category}</span>
              <span class="food-num-tag">${food.district}</span>
            </div>
            <h4 class="food-name">${food.name}</h4>
            <div class="food-sub">${food.sub}</div>
            <p class="food-quote-snippet">“${food.quote}”</p>
          </div>
          <div class="food-card-footer">
            <span>推荐：${food.shops.split('；')[0]}</span>
            <span style="color:var(--c-brick); font-weight:600;">探微 ➔</span>
          </div>
        `;
        card.addEventListener('click', () => openFoodModal(food.id));
        grid.appendChild(card);
      });
    }

    function getChapterDissectionHTML(chapId) {
      if (chapId === 1) {
        return `
          <div style="display:flex; flex-wrap:wrap; justify-content:space-between; align-items:center; gap:16px;">
            <div>
              <span style="font-size:11px; text-transform:uppercase; letter-spacing:0.1em; color:var(--c-brick); font-weight:700;">解构透视 · 面线糊进食拓扑</span>
              <h4 style="font-family:var(--font-serif); font-size:18px; margin-top:4px;">双派汤底与三十样料头的自选矩阵</h4>
              <p style="font-size:13px; color:var(--c-ink-light); margin-top:4px;">「水门国仔」大骨浓汤派梭子蟹吊鲜 vs 「文啊/罗记」鱼骨派清甜鲜美。地瓜粉浆微沸勾芡成糊而不烂之骨架，蘸剪段油条一润入魂。</p>
            </div>
            <div style="display:flex; gap:8px;">
              <span class="geo-btn" style="background:#FFF;">骨汤梭子蟹派</span>
              <span class="geo-btn" style="background:#FFF;">县后街鱼骨派</span>
              <span class="geo-btn" style="background:#FFF;">当归药酒点睛</span>
            </div>
          </div>
        `;
      } else if (chapId === 2) {
        return `
          <div>
            <span style="font-size:11px; text-transform:uppercase; letter-spacing:0.1em; color:var(--c-brick); font-weight:700;">解构透视 · 救命粮的报恩谱系</span>
            <h4 style="font-family:var(--font-serif); font-size:18px; margin-top:4px;">从明代陈振龙吕宋引种，到泉州小吃的隐形骨架</h4>
            <p style="font-size:13px; color:var(--c-ink-light); margin-top:4px;">地瓜不仅熬成晨光第一碗甘润地瓜粥，更通过纯地瓜粉成为勾芡（面线糊）、裹浆（炸醋肉）、捏团（地瓜粉团、拳头母）的核心。连芋头也一并入伙，成就泉州人迷之爱好的「半甜咸」。</p>
          </div>
        `;
      } else if (chapId === 3) {
        return `
          <div>
            <span style="font-size:11px; text-transform:uppercase; letter-spacing:0.1em; color:var(--c-brick); font-weight:700;">解构透视 · 刺桐港牛肉原动力</span>
            <h4 style="font-family:var(--font-serif); font-size:18px; margin-top:4px;">宋元阿拉伯遗风 × 下南洋番客咖喱</h4>
            <p style="font-size:13px; color:var(--c-ink-light); margin-top:4px;">牛肉之于泉州人好比汽油之于汽车。一人食标配三件套：一碗葱头油炒香芥菜咸饭 + 一支南洋咖喱草果大料焖炖脱骨牛排 + 一份地瓜粉水衣滑爽的牛肉羹。</p>
          </div>
        `;
      } else if (chapId === 4) {
        return `
          <div>
            <span style="font-size:11px; text-transform:uppercase; letter-spacing:0.1em; color:var(--c-brick); font-weight:700;">解构透视 · 向海讨生活的大味至简</span>
            <h4 style="font-family:var(--font-serif); font-size:18px; margin-top:4px;">「炣」无技巧烹饪 · 安海天然星虫果冻 · 白灼小章鱼手磨二十分钟</h4>
            <p style="font-size:13px; color:var(--c-ink-light); margin-top:4px;">「炣」即酱油兑水烹煮，把胜负交给选料的原点；春虹小馆白灼短蛸加入茶油油粕手磨 20 分钟提香增脆；长火土笋冻纯借星虫自身胶原蛋白融水凝冻。</p>
          </div>
        `;
      } else {
        return `
          <div>
            <span style="font-size:11px; text-transform:uppercase; letter-spacing:0.1em; color:var(--c-brick); font-weight:700;">解构透视 · 闽南市井风味流变</span>
            <h4 style="font-family:var(--font-serif); font-size:18px; margin-top:4px;">神明供奉入茶盘，夜市镬气慰凡尘</h4>
            <p style="font-size:13px; color:var(--c-ink-light); margin-top:4px;">泉州饮食贯通了祭祀供桌与街市排档，无论是网油鸡卷还是中空炸枣，抑或石狮旧菜市一壶烧酒配生猛海鲜，食物承载着生生不息的古城生命力。</p>
          </div>
        `;
      }
    }

    /* ==========================================================================
       5. 视域 Ⅳ · 神凡山海谱 (Cosmic Gravity Constellation)
       ========================================================================== */
    function initConstellation() {
      // 过滤器绑定
      document.querySelectorAll('#dna-filters .dna-btn').forEach(btn => {
        btn.addEventListener('click', () => {
          document.querySelectorAll('#dna-filters .dna-btn').forEach(b => b.classList.remove('active'));
          btn.classList.add('active');
          STATE.activeDna = btn.dataset.dna;
          renderConstellationCanvas();
        });
      });

      const canvas = document.getElementById('star-canvas');
      canvas.addEventListener('mousemove', handleCanvasHover);
      canvas.addEventListener('click', handleCanvasClick);
      window.addEventListener('resize', renderConstellationCanvas);
    }

    let starNodes = [];
    let hoveredStar = null;

    function renderConstellationCanvas() {
      const canvas = document.getElementById('star-canvas');
      if (!canvas) return;
      const rect = canvas.getBoundingClientRect();
      canvas.width = rect.width * window.devicePixelRatio;
      canvas.height = rect.height * window.devicePixelRatio;

      const ctx = canvas.getContext('2d');
      ctx.scale(window.devicePixelRatio, window.devicePixelRatio);
      const w = rect.width;
      const h = rect.height;

      ctx.clearRect(0, 0, w, h);

      // 绘制象限坐标十字细线
      ctx.strokeStyle = 'rgba(255, 255, 255, 0.08)';
      ctx.lineWidth = 1;
      ctx.setLineDash([4, 6]);
      ctx.beginPath();
      ctx.moveTo(w / 2, 40); ctx.lineTo(w / 2, h - 40);
      ctx.moveTo(40, h / 2); ctx.lineTo(w - 40, h / 2);
      ctx.stroke();
      ctx.setLineDash([]);

      // 计算节点
      starNodes = [];
      FOODS.forEach(food => {
        const isMatchDna = STATE.activeDna === 'all' || food.tags.includes(STATE.activeDna);
        const padding = 60;
        // x: 0(mountain) -> 100(sea)
        const cx = padding + (food.x / 100) * (w - padding * 2);
        // y: 0(savory) -> 100(sweet), note in canvas top is sweet, bottom is savory
        const cy = (h - padding) - (food.y / 100) * (h - padding * 2);

        starNodes.push({
          id: food.id,
          name: food.name,
          chapterId: food.chapterId,
          x: cx,
          y: cy,
          tags: food.tags,
          active: isMatchDna,
          r: 5
        });
      });

      // 绘制星系引力连线
      ctx.strokeStyle = 'rgba(197, 147, 65, 0.15)';
      ctx.lineWidth = 0.8;
      for (let i = 0; i < starNodes.length; i++) {
        for (let j = i + 1; j < starNodes.length; j++) {
          const a = starNodes[i];
          const b = starNodes[j];
          if (a.active && b.active && a.chapterId === b.chapterId) {
            const dist = Math.hypot(a.x - b.x, a.y - b.y);
            if (dist < 140) {
              ctx.beginPath();
              ctx.moveTo(a.x, a.y);
              ctx.lineTo(b.x, b.y);
              ctx.stroke();
            }
          }
        }
      }

      // 如果有悬浮高亮节点，画金色连接索
      if (hoveredStar && hoveredStar.active) {
        ctx.strokeStyle = 'rgba(224, 178, 94, 0.6)';
        ctx.lineWidth = 1.5;
        starNodes.forEach(other => {
          if (other.id !== hoveredStar.id && other.chapterId === hoveredStar.chapterId) {
            ctx.beginPath();
            ctx.moveTo(hoveredStar.x, hoveredStar.y);
            ctx.lineTo(other.x, other.y);
            ctx.stroke();
          }
        });
      }

      // 绘制星体节点
      starNodes.forEach(node => {
        if (!node.active) {
          ctx.fillStyle = 'rgba(255, 255, 255, 0.1)';
          ctx.beginPath();
          ctx.arc(node.x, node.y, 3, 0, Math.PI * 2);
          ctx.fill();
          return;
        }

        const isHovered = hoveredStar && hoveredStar.id === node.id;
        const chap = CHAPTERS.find(c => c.id === node.chapterId);
        const color = chap ? chap.color : '#C59341';

        // 光晕
        ctx.fillStyle = color;
        ctx.globalAlpha = isHovered ? 0.8 : 0.3;
        ctx.beginPath();
        ctx.arc(node.x, node.y, isHovered ? 12 : 8, 0, Math.PI * 2);
        ctx.fill();

        // 实体核心
        ctx.globalAlpha = 1;
        ctx.fillStyle = isHovered ? '#FFFFFF' : color;
        ctx.beginPath();
        ctx.arc(node.x, node.y, isHovered ? 5 : 4, 0, Math.PI * 2);
        ctx.fill();

        // 标签文字
        ctx.font = `${isHovered ? 'bold 12px' : '10px'} "Noto Serif SC", serif`;
        ctx.fillStyle = isHovered ? '#FFD494' : 'rgba(255, 255, 255, 0.75)';
        ctx.fillText(node.name, node.x + 8, node.y + 3);
      });
    }

    function handleCanvasHover(e) {
      const canvas = document.getElementById('star-canvas');
      const rect = canvas.getBoundingClientRect();
      const mx = e.clientX - rect.left;
      const my = e.clientY - rect.top;

      let found = null;
      for (const node of starNodes) {
        if (Math.hypot(node.x - mx, node.y - my) < 14) {
          found = node;
          break;
        }
      }

      if (found !== hoveredStar) {
        hoveredStar = found;
        renderConstellationCanvas();
      }
    }

    function handleCanvasClick(e) {
      if (hoveredStar) {
        openFoodModal(hoveredStar.id);
      }
    }

    /* ==========================================================================
       6. 视域 Ⅴ · 老饕风味动线 (Cinematic Walkthrough)
       ========================================================================== */
    function initRoutes() {
      const bar = document.getElementById('routes-selector-bar');
      bar.innerHTML = '';

      ROUTES.forEach(r => {
        const card = document.createElement('div');
        card.className = 'route-select-card' + (r.id === STATE.activeRouteId ? ' active' : '');
        card.innerHTML = `
          <span class="motto-seal" style="font-size:10px;">${r.badge}</span>
          <h4 style="font-family:var(--font-serif); font-size:16px; font-weight:700; margin-top:4px;">${r.name.split('·')[0]}</h4>
          <p style="font-size:12px; color:var(--c-ink-muted); margin-top:2px;">${r.stops.length} 个寻味打卡站</p>
        `;
        card.addEventListener('click', () => {
          stopCruise();
          STATE.activeRouteId = r.id;
          document.querySelectorAll('.route-select-card').forEach(c => c.classList.remove('active'));
          card.classList.add('active');
          renderRouteDetail(r.id);
        });
        bar.appendChild(card);
      });

      // 自动漫游按钮
      const cruiseBtn = document.getElementById('start-cruise-btn');
      cruiseBtn.addEventListener('click', () => {
        if (STATE.cruiseInterval) {
          stopCruise();
        } else {
          startCruise();
        }
      });

      renderRouteDetail('route-a');
    }

    function renderRouteDetail(routeId) {
      const r = ROUTES.find(x => x.id === routeId);
      if (!r) return;

      document.getElementById('route-badge').textContent = r.badge;
      document.getElementById('route-title').textContent = r.name;
      document.getElementById('route-desc').textContent = r.desc;

      const timeline = document.getElementById('route-stations-timeline');
      timeline.innerHTML = '';

      r.stops.forEach((stop, idx) => {
        const card = document.createElement('div');
        card.className = 'station-card' + (idx === STATE.cruiseStep ? ' active-step' : '');
        card.id = `stop-card-${idx}`;
        card.innerHTML = `
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
            <span class="motto-seal" style="font-size:10px;">第 0${idx+1} 站 · ${stop.time}</span>
            <span style="font-size:11px; color:var(--c-brick); font-weight:700;">${stop.shop}</span>
          </div>
          <h4 style="font-family:var(--font-serif); font-size:16px; font-weight:700; margin-bottom:6px;">${stop.dish}</h4>
          <p style="font-size:12px; color:var(--c-ink-light); line-height:1.6;">“${stop.tip}”</p>
        `;
        timeline.appendChild(card);
      });
    }

    function startCruise() {
      const r = ROUTES.find(x => x.id === STATE.activeRouteId);
      if (!r) return;
      STATE.cruiseStep = 0;
      document.getElementById('cruise-btn-label').textContent = '暂停漫游';

      highlightCruiseStep(0);
      STATE.cruiseInterval = setInterval(() => {
        STATE.cruiseStep++;
        if (STATE.cruiseStep >= r.stops.length) {
          STATE.cruiseStep = 0;
        }
        highlightCruiseStep(STATE.cruiseStep);
      }, 2600);
    }

    function stopCruise() {
      if (STATE.cruiseInterval) {
        clearInterval(STATE.cruiseInterval);
        STATE.cruiseInterval = null;
      }
      document.getElementById('cruise-btn-label').textContent = '开启自动漫游';
    }

    function highlightCruiseStep(step) {
      document.querySelectorAll('.station-card').forEach((c, idx) => {
        c.classList.toggle('active-step', idx === step);
      });
      const activeCard = document.getElementById(`stop-card-${step}`);
      if (activeCard) {
        activeCard.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
      }
    }

    /* ==========================================================================
       7. 模态框与寻味印章册
       ========================================================================== */
    function openFoodModal(foodId) {
      const food = FOODS.find(f => f.id === foodId);
      if (!food) return;

      const chap = CHAPTERS.find(c => c.id === food.chapterId);
      const isBookmarked = STATE.passport.includes(food.id);

      const body = document.getElementById('food-modal-body');
      body.innerHTML = `
        <div style="display:flex; align-items:center; gap:8px; margin-bottom:12px;">
          <span class="motto-seal">${chap ? chap.title : '世遗风味'}</span>
          <span class="motto-seal" style="background:#FAF8F3; border-color:var(--c-border); color:var(--c-ink);">${food.category}</span>
          <span style="font-size:12px; color:var(--c-ink-muted);">${food.district} · ${food.time}</span>
        </div>
        <h2 style="font-family:var(--font-serif); font-size:28px; font-weight:800; margin-bottom:4px;">${food.name}</h2>
        <div style="font-size:13px; color:var(--c-ink-muted); margin-bottom:18px;">${food.sub} · 味型【${food.flavor}】</div>

        <div style="padding:16px; border-left:3px solid var(--c-brick); background:rgba(158,53,36,0.04); font-family:var(--font-serif); font-size:15px; line-height:1.7; margin-bottom:20px;">
          “${food.quote}”
        </div>

        <div style="margin-bottom:24px;">
          <h4 style="font-size:12px; text-transform:uppercase; letter-spacing:0.1em; color:var(--c-ink-muted); margin-bottom:6px;">寻味详情与掌故</h4>
          <p style="font-size:14px; line-height:1.8; color:var(--c-ink-light);">${food.detail}</p>
        </div>

        <div style="margin-bottom:28px;">
          <h4 style="font-size:12px; text-transform:uppercase; letter-spacing:0.1em; color:var(--c-ink-muted); margin-bottom:8px;">原著考据去哪吃</h4>
          <div style="font-size:13px; line-height:1.7; padding:12px; border-radius:var(--radius-md); background:var(--c-paper); border:1px solid var(--c-border);">
            ${food.shops}
          </div>
        </div>

        <div style="display:flex; justify-content:space-between; align-items:center; padding-top:16px; border-top:1px solid var(--c-border);">
          <button id="modal-bookmark-btn" style="padding:8px 16px; border-radius:var(--radius-full); border:1px solid var(--c-brick); color:var(--c-brick); font-size:13px; font-weight:600; display:flex; align-items:center; gap:6px;">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="${isBookmarked ? 'currentColor' : 'none'}" stroke="currentColor" stroke-width="2"><path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"/></svg>
            <span>${isBookmarked ? '已收录入印章册' : '收录入寻味印章册'}</span>
          </button>
          <span style="font-size:11px; color:var(--c-ink-faint);">《值得专程前往的福建美食之都！》原著考据</span>
        </div>
      `;

      document.getElementById('modal-bookmark-btn').addEventListener('click', () => {
        togglePassport(food.id);
        openFoodModal(food.id);
      });

      document.getElementById('food-modal').classList.add('active');
    }

    document.getElementById('close-food-modal-btn').addEventListener('click', () => {
      document.getElementById('food-modal').classList.remove('active');
    });

    // 寻味印章册
    function initPassport() {
      document.getElementById('open-passport-btn').addEventListener('click', () => {
        document.getElementById('passport-drawer').classList.add('open');
        renderPassportList();
      });
      document.getElementById('close-passport-drawer-btn').addEventListener('click', () => {
        document.getElementById('passport-drawer').classList.remove('open');
      });
      document.getElementById('clear-passport-btn').addEventListener('click', () => {
        if (confirm('确定要清空您的所有寻味印章吗？')) {
          STATE.passport = [];
          savePassport();
          renderPassportList();
        }
      });
      updatePassportBadge();
    }

    function togglePassport(foodId) {
      const idx = STATE.passport.indexOf(foodId);
      if (idx > -1) {
        STATE.passport.splice(idx, 1);
      } else {
        STATE.passport.push(foodId);
      }
      savePassport();
      updatePassportBadge();
      renderPassportList();
    }

    function savePassport() {
      localStorage.setItem('qz_food_passport_v2', JSON.stringify(STATE.passport));
    }

    function updatePassportBadge() {
      document.getElementById('passport-count-badge').textContent = STATE.passport.length;
      document.getElementById('passport-progress-pct').textContent = `${STATE.passport.length} / ${FOODS.length} 味`;
    }

    function renderPassportList() {
      updatePassportBadge();
      const list = document.getElementById('passport-list-box');
      list.innerHTML = '';

      if (STATE.passport.length === 0) {
        list.innerHTML = '<div style="text-align:center; padding:40px 0; color:var(--c-ink-faint); font-size:13px;">暂无收藏，点击美食卡片收录印章</div>';
        return;
      }

      STATE.passport.forEach(fid => {
        const food = FOODS.find(f => f.id === fid);
        if (!food) return;
        const item = document.createElement('div');
        item.style.padding = '12px 14px';
        item.style.borderRadius = 'var(--radius-md)';
        item.style.border = '1px solid var(--c-border)';
        item.style.background = '#FFF';
        item.style.display = 'flex';
        item.style.justifyContent = 'space-between';
        item.style.alignItems = 'center';
        item.innerHTML = `
          <div>
            <div style="font-family:var(--font-serif); font-weight:700; font-size:15px; cursor:pointer;" onclick="openFoodModal(${food.id})">${food.name}</div>
            <div style="font-size:11px; color:var(--c-ink-muted); margin-top:2px;">${food.sub} · ${food.district}</div>
          </div>
          <button style="color:var(--c-ink-faint); padding:4px;" onclick="togglePassport(${food.id})">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
          </button>
        `;
        list.appendChild(item);
      });
    }

    // 全局搜索
    function initSearch() {
      const modal = document.getElementById('search-modal');
      const input = document.getElementById('global-search-input');
      const openBtn = document.getElementById('open-search-btn');
      const closeBtn = document.getElementById('close-search-btn');

      openBtn.addEventListener('click', () => {
        modal.classList.add('active');
        input.focus();
      });
      closeBtn.addEventListener('click', () => {
        modal.classList.remove('active');
      });

      document.addEventListener('keydown', (e) => {
        if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') {
          e.preventDefault();
          modal.classList.add('active');
          input.focus();
        }
        if (e.key === 'Escape') {
          modal.classList.remove('active');
          document.getElementById('food-modal').classList.remove('active');
          document.getElementById('passport-drawer').classList.remove('open');
          document.getElementById('shop-drawer').classList.remove('open');
        }
      });

      input.addEventListener('input', (e) => {
        const q = e.target.value.trim().toLowerCase();
        renderSearchResults(q);
      });
    }

    function renderSearchResults(q) {
      const box = document.getElementById('search-results-list');
      box.innerHTML = '';
      if (!q) return;

      const matchedFoods = FOODS.filter(f => (f.name + f.sub + f.district + f.flavor + f.quote + f.detail + f.shops).toLowerCase().includes(q));
      const matchedShops = SHOPS.filter(s => (s.name + s.district + s.street + s.desc).toLowerCase().includes(q));

      if (matchedFoods.length === 0 && matchedShops.length === 0) {
        box.innerHTML = '<div style="font-size:13px; color:var(--c-ink-faint); padding:20px 0; text-align:center;">未检索到相关风味或食肆</div>';
        return;
      }

      matchedFoods.forEach(food => {
        const item = document.createElement('div');
        item.style.padding = '10px 14px';
        item.style.borderRadius = 'var(--radius-md)';
        item.style.background = '#FFF';
        item.style.border = '1px solid var(--c-border)';
        item.style.cursor = 'pointer';
        item.innerHTML = `
          <div style="display:flex; justify-content:space-between; align-items:center;">
            <b style="font-family:var(--font-serif); color:var(--c-brick); font-size:14px;">${food.name}</b>
            <span style="font-size:11px; color:var(--c-ink-faint);">${food.district} · ${food.category}</span>
          </div>
          <div style="font-size:12px; color:var(--c-ink-light); margin-top:2px;">“${food.quote}”</div>
        `;
        item.addEventListener('click', () => {
          document.getElementById('search-modal').classList.remove('active');
          openFoodModal(food.id);
        });
        box.appendChild(item);
      });

      matchedShops.forEach(shop => {
        const item = document.createElement('div');
        item.style.padding = '10px 14px';
        item.style.borderRadius = 'var(--radius-md)';
        item.style.background = '#FFF';
        item.style.border = '1px solid var(--c-border)';
        item.style.cursor = 'pointer';
        item.innerHTML = `
          <div style="display:flex; justify-content:space-between; align-items:center;">
            <b style="font-family:var(--font-serif); color:var(--c-gold); font-size:14px;">${shop.name}</b>
            <span class="motto-seal" style="font-size:10px;">${shop.attitude}</span>
          </div>
          <div style="font-size:12px; color:var(--c-ink-light); margin-top:2px;">${shop.district} · ${shop.street}：${shop.desc}</div>
        `;
        item.addEventListener('click', () => {
          document.getElementById('search-modal').classList.remove('active');
          switchView('cartogram');
          openShopDrawer(shop);
        });
        box.appendChild(item);
      });
    }
  </script>
</body>
</html>
"""

with open("fujian-food-capital-v2/index.html", "w", encoding="utf-8") as f:
    f.write(html_template)

print("Generated fujian-food-capital-v2/index.html successfully.")
