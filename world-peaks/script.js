const MAX_ALT = 9000;              // 统一海拔标尺上限
const SNOWLINE = 30;               // 线稿/插画中的雪线（归一化坐标）

/* ==================== 工具 ==================== */
const $ = s => document.querySelector(s);
const fmt = a => a >= 8000 ? a.toLocaleString('en-US',{minimumFractionDigits:0,maximumFractionDigits:2}) : a.toLocaleString('en-US');
let current = 'ten';
let animId = null;

/* 海拔 -> 天空顶部颜色（越高越深邃，模拟"死亡地带"的深色天空） */
function skyTop(alt){
  const t = Math.min(1, Math.max(0, (alt-4800)/(8849-4800)));
  const lerp=(a,b)=>Math.round(a+(b-a)*t);
  return `rgb(${lerp(168,22)},${lerp(208,37)},${lerp(240,63)})`;
}
/* 海拔 -> 山体基色（越高越冷峻深蓝，越低越温润浅蓝） */
function rockColor(alt){
  const t = Math.min(1, Math.max(0, (alt-4800)/(8849-4800)));
  const lerp=(a,b)=>Math.round(a+(b-a)*t);
  return `rgb(${lerp(127,63)},${lerp(176,111)},${lerp(214,163)})`;
}
/* 归一化山形 -> 绝对路径 */
function shapePath(shape, x0, baseY, w, h, prog=1){
  return shape.map((p,i)=>{
    const x = x0 + p[0]/100*w;
    const y = baseY - (100-p[1])/100*h*prog;
    return (i===0?'M':'L')+x.toFixed(1)+','+y.toFixed(1);
  }).join(' ')+` L${(x0+w).toFixed(1)},${baseY} L${x0.toFixed(1)},${baseY} Z`;
}
/* 归一化山形 -> 雪顶多边形（截取 y <= snow 的顶部区域） */
function snowPath(shape, x0, baseY, w, h, snow=SNOWLINE, prog=1){
  const P = shape.map(p=>({x:x0+p[0]/100*w, y:baseY-(100-p[1])/100*h*prog, v:p[1]}));
  const snowY = baseY-(100-snow)/100*h*prog;
  const pts=[];
  for(let i=0;i<P.length-1;i++){
    const a=P[i], b=P[i+1];
    if(a.v<=snow) pts.push([a.x,a.y]);
    if((a.v-snow)*(b.v-snow)<0){
      const t=(snow-a.v)/(b.v-a.v);
      pts.push([a.x+(b.x-a.x)*t, snowY]);
    }
  }
  if(pts.length<3) return '';
  return 'M'+pts.map(p=>p[0].toFixed(1)+','+p[1].toFixed(1)).join(' L')+' Z';
}
const easeOut = t => 1-Math.pow(1-t,3);

/* ==================== 天际线 ==================== */
function renderSkyline(){
  const data = window.PEAKS[current];
  const svg = $('#skyline');
  const W=1500, H=560, padL=64, padR=26, baseY=500, topY=44;
  const plotW = W-padL-padR;
  const scale = (baseY-topY)/MAX_ALT;
  const slot = plotW/data.length;
  svg.innerHTML='';

  /* 网格线与海拔刻度 */
  let g='';
  for(let a=0;a<=MAX_ALT;a+=1000){
    const y = baseY-a*scale;
    g+=`<line x1="${padL}" y1="${y}" x2="${W-padR}" y2="${y}" stroke="${a===0?'#b9cfe0':'#e3eef6'}" stroke-width="${a===0?1.5:1}"/>`;
    g+=`<text class="grid-label" x="${padL-10}" y="${y+3.5}">${a===0?'0':(a/1000)+'k'}</text>`;
  }
  g+=`<text class="grid-label" x="${padL-10}" y="${topY-14}" style="font-size:11px">海拔/米</text>`;

  /* 山体分组 */
  const groups = data.map((pk,i)=>{
    const h = pk.alt*scale;
    const w = slot*0.82;
    const x0 = padL + slot*i + (slot-w)/2;
    return {pk, x0, w, h, cx:padL+slot*i+slot/2};
  });

  const defs = ['<defs>'];
  const paths = [];
  groups.forEach((gr,i)=>{
    const col = rockColor(gr.pk.alt);
    defs.push(`<linearGradient id="mg-${gr.pk.id}-${i}" gradientUnits="userSpaceOnUse" x1="0" y1="${baseY-gr.h}" x2="0" y2="${baseY}">
      <stop offset="0" stop-color="#f4fafe"/><stop offset=".28" stop-color="#dbeaf7"/>
      <stop offset=".55" stop-color="${col}"/><stop offset="1" stop-color="#33587f"/></linearGradient>`);
    paths.push(`<g class="peak-hit" data-i="${i}">
      <path class="peak-body" d="" fill="url(#mg-${gr.pk.id}-${i})" stroke="#2c557f" stroke-opacity=".35" stroke-width="1.2"/>
      <text class="peak-label" x="${gr.cx}" y="${baseY+24}">${gr.pk.cn}</text>
      <text class="peak-alt" x="${gr.cx}" y="${baseY+42}">${fmt(gr.pk.alt)} m</text>
    </g>`);
  });
  svg.innerHTML = defs.join('')+ '</defs>' + g + paths.join('');

  /* 生长动画（交错延迟） */
  const bodies = svg.querySelectorAll('.peak-body');
  const start = performance.now();
  if(animId) cancelAnimationFrame(animId);
  function frame(now){
    const el = now-start;
    let done = true;
    groups.forEach((gr,i)=>{
      const t = Math.min(1, Math.max(0,(el - i*90)/700));
      if(t<1) done=false;
      const prog = easeOut(t);
      bodies[i].setAttribute('d', shapePath(gr.pk.shape, gr.x0, baseY, gr.w, gr.h, Math.max(prog,0.001)));
    });
    if(!done) animId=requestAnimationFrame(frame);
  }
  animId=requestAnimationFrame(frame);

  /* 交互 */
  const tip = $('#tooltip');
  svg.querySelectorAll('.peak-hit').forEach(el=>{
    const pk = data[+el.dataset.i];
    el.addEventListener('mousemove', e=>{
      tip.innerHTML = `<b>${pk.cn}</b> ${pk.en}<br>海拔 ${fmt(pk.alt)} 米 · ${pk.country}<br><span style="opacity:.75">点击查看详情</span>`;
      tip.style.left = e.clientX+'px'; tip.style.top = e.clientY+'px'; tip.style.opacity=1;
    });
    el.addEventListener('mouseleave', ()=> tip.style.opacity=0);
    el.addEventListener('click', ()=> openDetail(pk));
  });

  $('#skyline-note').textContent = current==='ten'
    ? '全球海拔前十的山峰全部位于亚洲的喜马拉雅与喀喇昆仑山脉，且高度均超过 8,000 米。山体按真实海拔等比绘制，悬停查看概要、点击查看详情。'
    : '七大洲最高峰（Seven Summits 主流版本），与十大高峰共用同一海拔标尺——可以直观看到洲际之巅与世界之巅的差距。悬停查看概要、点击查看详情。';
}

/* ==================== 柱状图 ==================== */
function renderBars(){
  const data = [...window.PEAKS[current]].sort((a,b)=>b.alt-a.alt);
  const box = $('#bars');
  box.innerHTML = data.map(pk=>`
    <div class="bar-row" data-id="${pk.id}">
      <div class="bar-name">${pk.cn}<span>${pk.en}</span></div>
      <div class="bar-track"><div class="bar-fill" data-w="${(pk.alt/MAX_ALT*100).toFixed(1)}"
        style="background:linear-gradient(90deg,${rockColor(pk.alt)},#33587f)"></div></div>
      <div class="bar-val">${fmt(pk.alt)} m</div>
    </div>`).join('');
  requestAnimationFrame(()=>requestAnimationFrame(()=>{
    box.querySelectorAll('.bar-fill').forEach(f=> f.style.width=f.dataset.w+'%');
  }));
  box.querySelectorAll('.bar-row').forEach(r=>{
    r.addEventListener('click', ()=>{
      const pk = window.PEAKS[current].find(p=>p.id===r.dataset.id);
      if(pk) openDetail(pk);
    });
  });
}

/* ==================== 时间轴 ==================== */
function renderTimeline(){
  const data = [...window.PEAKS[current]].sort((a,b)=>a.year-b.year);
  const svg = $('#timeline');
  const W=1400, H=300, padL=70, padR=50, axisY=160;
  const minY = Math.min(...data.map(p=>p.year))-6, maxY = Math.max(...data.map(p=>p.year))+6;
  const X = y => padL + (y-minY)/(maxY-minY)*(W-padL-padR);
  let s = `<line x1="${padL-20}" y1="${axisY}" x2="${W-padR+16}" y2="${axisY}" stroke="#b9cfe0" stroke-width="1.5"/>
           <path d="M${W-padR+16},${axisY} l-9,-4 v8 Z" fill="#b9cfe0"/>`;
  data.forEach((pk,i)=>{
    const x = X(pk.year), up = i%2===0;
    const ly = up ? axisY-64 : axisY+58;
    const ty = up ? axisY-78 : axisY+86;
    s += `<line x1="${x}" y1="${axisY}" x2="${x}" y2="${ly}" stroke="#cfe4f2" stroke-width="1.2"/>
      <circle cx="${x}" cy="${axisY}" r="6" fill="${rockColor(pk.alt)}" stroke="#fff" stroke-width="2.5"/>
      <text x="${x}" y="${ty}" text-anchor="middle" style="font-size:13px;font-weight:700;fill:#22374e">${pk.year}</text>
      <text x="${x}" y="${ty+17}" text-anchor="middle" style="font-size:11.5px;fill:#5a7186">${pk.cn}</text>
      <text x="${x}" y="${ty+32}" text-anchor="middle" style="font-size:10.5px;fill:#8fa5b8">${pk.who[0][0]}（${pk.who[0][1]}）</text>`;
  });
  svg.innerHTML = s;
}

/* ==================== 详情面板 ==================== */
function openDetail(pk){
  const body = $('#cardBody');
  const sceneW=420, sceneH=300, baseY=252, mh=195, mw=340, mx0=(sceneW-mw)/2;
  const sky = skyTop(pk.alt);
  const col = rockColor(pk.alt);
  const stars = pk.alt>=8000
    ? Array.from({length:14},()=>`<circle cx="${(Math.random()*sceneW).toFixed(0)}" cy="${(Math.random()*110).toFixed(0)}" r="${(Math.random()*1.1+0.5).toFixed(1)}" fill="#fff" opacity="${(Math.random()*.5+.4).toFixed(2)}"/>`).join('')
    : '';
  const sunY = pk.alt>=8000 ? 200 : 74;
  const sunFill = pk.alt>=8000 ? '#dfe9f5' : '#fff7e0';

  const scene = `
  <svg viewBox="0 0 ${sceneW} ${sceneH}">
    <defs>
      <linearGradient id="dsky" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0" stop-color="${sky}"/><stop offset="1" stop-color="#dceef9"/>
      </linearGradient>
      <linearGradient id="drock" x1="0" y1="${baseY-mh}" x2="0" y2="${baseY}" gradientUnits="userSpaceOnUse">
        <stop offset="0" stop-color="#f2f9ff"/><stop offset=".3" stop-color="#d3e6f5"/>
        <stop offset=".6" stop-color="${col}"/><stop offset="1" stop-color="#2c557f"/>
      </linearGradient>
    </defs>
    <rect width="${sceneW}" height="${sceneH}" fill="url(#dsky)"/>
    ${stars}
    <circle cx="330" cy="${sunY}" r="26" fill="${sunFill}" opacity=".95"/>
    <circle cx="330" cy="${sunY}" r="38" fill="${sunFill}" opacity=".25"/>
    <path d="${shapePath(pk.shape, mx0, baseY, mw, mh)}" fill="url(#drock)" stroke="#2c557f" stroke-opacity=".4" stroke-width="1.4"/>
    <path d="${snowPath(pk.shape, mx0, baseY, mw, mh)}" fill="#fbfdff" opacity=".96"/>
    <rect x="0" y="${baseY}" width="${sceneW}" height="${sceneH-baseY}" fill="#eaf3fa"/>
    <line x1="0" y1="${baseY}" x2="${sceneW}" y2="${baseY}" stroke="#c4d8e8" stroke-width="1.2"/>
    <text x="${sceneW/2}" y="${sceneH-12}" text-anchor="middle" style="font-size:11px;letter-spacing:3px;fill:#7d96ac">海拔 ${fmt(pk.alt)} 米</text>
  </svg>`;

  /* 线稿（描摹动画）：轮廓 + 两条山脊线 */
  const skW=420, skH=190, skBase=160, skHgt=130, skMw=300, skMx=(skW-skMw)/2;
  const outline = shapePath(pk.shape, skMx, skBase, skMw, skHgt);
  const minY = Math.min(...pk.shape.map(p=>p[1]));
  const apexPts = pk.shape.filter(p=>p[1]===minY);
  const apexNorm = apexPts.reduce((s,p)=>s+p[0],0)/apexPts.length;
  const apexX = skMx + apexNorm/100*skMw;
  const ridge1 = `M${apexX},${skBase-skHgt} L${skMx+skMw*0.3},${skBase-skHgt*0.45}`;
  const ridge2 = `M${apexX},${skBase-skHgt} L${skMx+skMw*0.68},${skBase-skHgt*0.5}`;
  const sketch = `
  <svg viewBox="0 0 ${skW} ${skH}">
    <path id="sk-outline" d="${outline}" fill="none" stroke="#22374e" stroke-width="1.8" stroke-linejoin="round"/>
    <path id="sk-r1" d="${ridge1}" fill="none" stroke="#5b8fc0" stroke-width="1.1" stroke-dasharray="3 3"/>
    <path id="sk-r2" d="${ridge2}" fill="none" stroke="#5b8fc0" stroke-width="1.1" stroke-dasharray="3 3"/>
    <line x1="${skMx-16}" y1="${skBase}" x2="${skMx+skMw+16}" y2="${skBase}" stroke="#b9cfe0" stroke-width="1.2"/>
  </svg>`;

  const whoRows = pk.who.map(w=>`<div>${w[0]}<span style="color:var(--ice-600)">（${w[1]}）</span></div>`).join('');

  body.innerHTML = `
    <div class="card-title">
      <h3>${pk.cn}</h3>
      <div class="en">${pk.en}</div>
    </div>
    <div class="card-grid">
      <div>
        <div class="scene-box">${scene}</div>
        <div class="sketch-box">${sketch}<div class="sketch-cap">山 形 线 稿 · 示 意 描 摹</div></div>
      </div>
      <div>
        <div class="alt-big">${fmt(pk.alt)}<small>米</small></div>
        <dl class="info-list">
          <div class="info-row"><dt>所在国家</dt><dd>${pk.country}</dd></div>
          <div class="info-row"><dt>所属山脉</dt><dd>${pk.range}</dd></div>
          ${pk.continent?`<div class="info-row"><dt>所在大洲</dt><dd>${pk.continent}最高峰</dd></div>`:''}
          <div class="info-row"><dt>首次登顶</dt><dd>${pk.date}（${pk.year} 年）</dd></div>
          <div class="info-row"><dt>登顶者</dt><dd>${whoRows}</dd></div>
        </dl>
        <span class="note-tag">${pk.note}</span>
      </div>
    </div>`;

  $('#overlay').classList.add('open');
  document.body.style.overflow='hidden';

  /* 描摹动画 */
  requestAnimationFrame(()=>{
    ['sk-outline','sk-r1','sk-r2'].forEach((id,idx)=>{
      const p = document.getElementById(id);
      if(!p) return;
      const len = p.getTotalLength();
      const savedDash = p.getAttribute('stroke-dasharray');
      p.style.strokeDasharray = len;
      p.style.strokeDashoffset = len;
      p.style.transition = `stroke-dashoffset ${idx===0?1.4:0.7}s ease ${idx*0.5}s`;
      requestAnimationFrame(()=> p.style.strokeDashoffset = 0);
      setTimeout(()=>{ p.style.transition='none'; p.style.strokeDasharray = savedDash || 'none'; }, 1600+idx*500);
    });
  });
}

function closeDetail(){
  $('#overlay').classList.remove('open');
  document.body.style.overflow='';
}

$('#cardClose').addEventListener('click', closeDetail);
$('#overlay').addEventListener('click', e=>{ if(e.target.id==='overlay') closeDetail(); });
document.addEventListener('keydown', e=>{ if(e.key==='Escape') closeDetail(); });

/* ==================== Tab 切换 ==================== */
document.querySelectorAll('.tab-btn').forEach(btn=>{
  btn.addEventListener('click', ()=>{
    if(btn.dataset.set===current) return;
    document.querySelectorAll('.tab-btn').forEach(b=>b.classList.toggle('active', b===btn));
    current = btn.dataset.set;
    renderAll();
  });
});

/* ==================== Hero 视差 ==================== */
window.addEventListener('scroll', ()=>{
  const y = window.scrollY;
  if(y>400) return;
  const plxBack = $('#plx-back');
  const plxMid = $('#plx-mid');
  const plxFront = $('#plx-front');
  
  if (plxBack) plxBack.style.transform  = `translateY(${y*0.12}px)`;
  if (plxMid) plxMid.style.transform   = `translateY(${y*0.24}px)`;
  if (plxFront) plxFront.style.transform = `translateY(${y*0.38}px)`;
},{passive:true});

/* ==================== 初始化 ==================== */
function renderAll(){ 
  renderSkyline(); 
  renderBars(); 
  renderTimeline(); 
}

// 确保 DOM 已经加载
document.addEventListener('DOMContentLoaded', renderAll);
