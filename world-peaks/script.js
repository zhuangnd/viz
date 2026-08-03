document.addEventListener('DOMContentLoaded', () => {
  const canvas = document.getElementById('mountainsCanvas');
  const filterBtns = document.querySelectorAll('.filter-btn');
  
  // Detail panel elements
  const detailOverlay = document.getElementById('detailOverlay');
  const detailPanel = document.getElementById('detailPanel');
  const closeBtn = document.getElementById('closeBtn');
  
  const peakNameZh = document.getElementById('peakNameZh');
  const peakNameEn = document.getElementById('peakNameEn');
  const peakElevation = document.getElementById('peakElevation');
  const peakCountry = document.getElementById('peakCountry');
  const peakPhoto = document.getElementById('peakPhoto');
  const firstAscentTime = document.getElementById('firstAscentTime');
  const firstAscenders = document.getElementById('firstAscenders');

  const MAX_ELEVATION = 9000;

  // Render mountains
  function renderMountains(filter = 'all') {
    canvas.innerHTML = ''; // Clear current

    // Filter and sort by elevation (descending visually looks nice, or preserve array order)
    let displayData = window.peaksData;
    if (filter !== 'all') {
      displayData = window.peaksData.filter(peak => peak.categories.includes(filter));
    }
    
    // Sort descending by elevation
    displayData.sort((a, b) => b.elevation - a.elevation);

    displayData.forEach((peak, index) => {
      // Calculate height percentage (min 10% to ensure visibility)
      const heightPercent = Math.max((peak.elevation / MAX_ELEVATION) * 100, 10);
      
      const wrapper = document.createElement('div');
      wrapper.className = 'mountain-wrapper';
      wrapper.style.setProperty('--mountain-height', `${heightPercent}%`);
      
      // Delay animation for a staggered entrance
      wrapper.style.animationDelay = `${index * 0.05}s`;

      const mountain = document.createElement('div');
      mountain.className = 'mountain';
      mountain.style.height = `${heightPercent}%`;

      const label = document.createElement('div');
      label.className = 'mountain-label';
      label.innerHTML = `
        <div class="label-zh">${peak.nameZh}</div>
        <div class="label-elevation">${peak.elevation}m</div>
      `;

      wrapper.appendChild(mountain);
      wrapper.appendChild(label);

      // Click event for detail panel
      wrapper.addEventListener('click', () => openDetailPanel(peak));

      canvas.appendChild(wrapper);
      
      // Trigger reflow to restart transition if needed, though they start from 0 height mostly
      setTimeout(() => {
        mountain.style.height = `${heightPercent}%`;
      }, 50);
    });
  }

  // Handle Filtering
  filterBtns.forEach(btn => {
    btn.addEventListener('click', (e) => {
      filterBtns.forEach(b => b.classList.remove('active'));
      e.target.classList.add('active');
      renderMountains(e.target.dataset.filter);
    });
  });

  // Handle Panel Open/Close
  function openDetailPanel(peak) {
    peakNameZh.textContent = peak.nameZh;
    peakNameEn.textContent = peak.nameEn;
    peakElevation.textContent = `${peak.elevation} m`;
    peakCountry.textContent = peak.country;
    peakPhoto.src = peak.photoUrl;
    peakPhoto.alt = peak.nameZh;
    firstAscentTime.textContent = peak.firstAscentTime;
    firstAscenders.textContent = peak.firstAscenders;

    detailOverlay.classList.add('active');
    detailPanel.classList.add('active');
  }

  function closePanel() {
    detailOverlay.classList.remove('active');
    detailPanel.classList.remove('active');
  }

  closeBtn.addEventListener('click', closePanel);
  detailOverlay.addEventListener('click', closePanel);

  // Initialize
  renderMountains('all');
});
