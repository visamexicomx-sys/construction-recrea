/* ============================================================
   Recrea Construction — main.js
   Adapted from MexVisa Pro golden-ratio UI engine
   WhatsApp: 529844525333
   ============================================================ */

document.addEventListener('DOMContentLoaded', () => {

  /* ── Navbar height CSS variable ── */
  const navbar = document.querySelector('.navbar-custom');
  if (navbar) {
    document.documentElement.style.setProperty('--navbar-h', navbar.offsetHeight + 'px');
    window.addEventListener('resize', () => {
      document.documentElement.style.setProperty('--navbar-h', navbar.offsetHeight + 'px');
    });
  }

  /* ── Scroll: navbar shrink, progress bar, back-to-top ── */
  const progressBar = document.querySelector('.scroll-progress');
  const backToTop = document.querySelector('.back-to-top');

  window.addEventListener('scroll', () => {
    const isScrolled = window.scrollY > 50;
    if (navbar) {
      navbar.classList.toggle('scrolled', isScrolled);
      navbar.classList.toggle('navbar-shrink', isScrolled);
    }

    if (progressBar) {
      const scrolled = (window.scrollY / (document.body.scrollHeight - window.innerHeight)) * 100;
      progressBar.style.width = scrolled + '%';
    }

    if (backToTop) {
      backToTop.classList.toggle('visible', window.scrollY > 500);
    }
  });

  /* ── Smooth scroll for anchor links ── */
  document.querySelectorAll('a[href^="#"]').forEach(a => {
    a.addEventListener('click', e => {
      e.preventDefault();
      const target = document.querySelector(a.getAttribute('href'));
      if (target) {
        target.scrollIntoView({ behavior: 'smooth' });
        const collapse = document.querySelector('.navbar-collapse');
        if (collapse && collapse.classList.contains('show')) {
          new bootstrap.Collapse(collapse).hide();
        }
      }
    });
  });

  /* ── Init all modules ── */
  initScrollReveal();
  initCounterAnimation();
  initActiveNav();
  initWhatsAppWidget();
  initTestimonialCarousel();
  initGoldenCanvas();
  initVanillaTilt();
  initMagneticButtons();
  initSpotlightGlow();
  initMouseParallax();
  initRippleEffect();
  initTextScramble();

  /* ── Preloader dismiss ── */
  const preloader = document.getElementById('preloader');
  if (preloader) {
    preloader.classList.add('loaded');
  }
});


/* ============================================================
   initScrollReveal
   IntersectionObserver for .reveal, .reveal-left,
   .reveal-right, .reveal-scale
   ============================================================ */
function initScrollReveal() {
  const reveals = document.querySelectorAll('.reveal, .reveal-left, .reveal-right, .reveal-scale');
  if (!reveals.length) return;

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('revealed');
      }
    });
  }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });

  reveals.forEach(el => observer.observe(el));
}


/* ============================================================
   initCounterAnimation + animateCounter
   Animates [data-count] elements with eased counting
   ============================================================ */
function initCounterAnimation() {
  const counters = document.querySelectorAll('[data-count]');
  if (!counters.length) return;

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting && !entry.target.dataset.counted) {
        entry.target.dataset.counted = 'true';
        animateCounter(entry.target);
      }
    });
  }, { threshold: 0.5 });

  counters.forEach(el => observer.observe(el));
}

function animateCounter(el) {
  const target = parseInt(el.dataset.count);
  const suffix = el.dataset.suffix || '';
  const prefix = el.dataset.prefix || '';
  const duration = 1618;
  const start = performance.now();

  function update(now) {
    const elapsed = now - start;
    const progress = Math.min(elapsed / duration, 1);
    const eased = 1 - Math.pow(1 - progress, 3);
    const current = Math.floor(eased * target);

    el.textContent = prefix + current.toLocaleString() + suffix;

    if (progress < 1) requestAnimationFrame(update);
  }

  requestAnimationFrame(update);
}


/* ============================================================
   initWhatsAppWidget
   Toggle / close WhatsApp chat popup
   #waToggle, #waChatBox, #waClose, #waIcon
   WhatsApp number: 529844525333
   ============================================================ */
function initWhatsAppWidget() {
  const toggle = document.getElementById('waToggle');
  const chatBox = document.getElementById('waChatBox');
  const closeBtn = document.getElementById('waClose');
  const icon = document.getElementById('waIcon');
  if (!toggle || !chatBox) return;

  let isOpen = false;

  toggle.addEventListener('click', (e) => {
    e.preventDefault();
    isOpen = !isOpen;
    chatBox.classList.toggle('open', isOpen);
    if (icon) icon.className = isOpen ? 'bi bi-x-lg' : 'bi bi-whatsapp';
  });

  if (closeBtn) {
    closeBtn.addEventListener('click', () => {
      isOpen = false;
      chatBox.classList.remove('open');
      if (icon) icon.className = 'bi bi-whatsapp';
    });
  }

  document.addEventListener('click', (e) => {
    if (isOpen && !e.target.closest('.wa-widget')) {
      isOpen = false;
      chatBox.classList.remove('open');
      if (icon) icon.className = 'bi bi-whatsapp';
    }
  });

  /* Wire up any quick-action buttons to the correct WhatsApp number */
  document.querySelectorAll('[data-wa-msg]').forEach(el => {
    const msg = el.getAttribute('data-wa-msg');
    if (msg) {
      el.href = 'https://wa.me/529844525333?text=' + encodeURIComponent(msg);
    }
  });
}


/* ============================================================
   initActiveNav
   Scroll spy — highlight active nav link
   ============================================================ */
function initActiveNav() {
  const sections = document.querySelectorAll('section[id]');
  const navLinks = document.querySelectorAll('.navbar-nav .nav-link');

  window.addEventListener('scroll', () => {
    let current = '';
    sections.forEach(section => {
      const top = section.offsetTop - 120;
      if (window.scrollY >= top) current = section.getAttribute('id');
    });

    navLinks.forEach(link => {
      link.classList.remove('active');
      if (link.getAttribute('href') === '#' + current) {
        link.classList.add('active');
      }
    });
  });
}


/* ============================================================
   initGoldenCanvas
   Full golden-ratio canvas animation system
   Sub-functions: drawGoldenRectangles, drawGeometricRings,
   drawPhyllotaxis, drawPentagonLayers, drawGoldenSpiral,
   drawExponentialCurves, drawRatioSegments
   Plus section-level layer helpers
   ============================================================ */
function initGoldenCanvas() {
  const PHI = (1 + Math.sqrt(5)) / 2;
  const TAU = Math.PI * 2;
  const GOLDEN_ANGLE = TAU / (PHI * PHI);

  function createGolden(canvasId, centerX) {
    const canvas = document.getElementById(canvasId);
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    let w, h, cx, cy, t = 0;
    let maxR;

    function resize() {
      const rect = canvas.parentElement.getBoundingClientRect();
      w = canvas.width = rect.width;
      h = canvas.height = rect.height;
      cx = w * centerX;
      cy = h * 0.5;
      maxR = Math.min(w, h) * 0.42;
    }

    function drawGoldenRectangles() {
      ctx.save();
      ctx.rotate(t * 0.15);
      let rw = maxR * 0.85;
      let rh = rw / PHI;
      let ox = 0, oy = 0;
      const depth = 10;

      for (let i = 0; i < depth; i++) {
        const alpha = 0.18 - i * 0.014;
        if (alpha <= 0) break;

        ctx.save();
        ctx.translate(ox, oy);

        ctx.strokeStyle = 'rgba(240,165,0,' + alpha + ')';
        ctx.lineWidth = 1.2 - i * 0.08;
        ctx.strokeRect(-rw / 2, -rh / 2, rw, rh);

        const squareSide = Math.min(rw, rh);
        const arcR = squareSide;
        let arcX, arcY, startAngle;

        switch (i % 4) {
          case 0:
            arcX = -rw / 2 + squareSide;
            arcY = -rh / 2 + squareSide;
            startAngle = Math.PI;
            ctx.strokeStyle = 'rgba(0,200,83,' + (alpha * 0.8) + ')';
            break;
          case 1:
            arcX = rw / 2 - squareSide;
            arcY = -rh / 2;
            startAngle = Math.PI * 0.5;
            ctx.strokeStyle = 'rgba(13,110,253,' + (alpha * 0.8) + ')';
            break;
          case 2:
            arcX = rw / 2 - squareSide;
            arcY = rh / 2 - squareSide;
            startAngle = 0;
            ctx.strokeStyle = 'rgba(240,165,0,' + (alpha * 0.8) + ')';
            break;
          case 3:
            arcX = -rw / 2;
            arcY = rh / 2;
            startAngle = -Math.PI * 0.5;
            ctx.strokeStyle = 'rgba(0,200,83,' + (alpha * 0.6) + ')';
            break;
        }

        ctx.beginPath();
        ctx.arc(arcX, arcY, arcR, startAngle, startAngle + Math.PI * 0.5);
        ctx.lineWidth = 1.5 - i * 0.1;
        ctx.stroke();

        ctx.restore();

        const newW = rw - squareSide;
        const newH = squareSide;

        switch (i % 4) {
          case 0: ox += (squareSide - rw / 2 + newW / 2); break;
          case 1: oy += (-rh / 2 + newH / 2); break;
          case 2: ox -= (squareSide - rw / 2 + newW / 2); break;
          case 3: oy -= (-rh / 2 + newH / 2); break;
        }

        if (rw > rh) { rw = rw - rh; }
        else { const tmp = rh - rw; rh = rw; rw = tmp; }
        if (rw < 2 || rh < 2) break;
      }
      ctx.restore();
    }

    function drawGeometricRings() {
      let r = maxR * 0.06;
      const rings = [];
      while (r < maxR) {
        rings.push(r);
        r *= PHI;
      }

      rings.forEach((radius, i) => {
        const alpha = 0.06 + 0.03 * Math.sin(t * 1.5 + i);
        ctx.beginPath();
        ctx.arc(0, 0, radius, 0, TAU);
        ctx.strokeStyle = 'rgba(240,165,0,' + alpha + ')';
        ctx.lineWidth = 0.8;
        ctx.setLineDash([radius * 0.02, radius * 0.04]);
        ctx.stroke();
        ctx.setLineDash([]);

        const dotAngle = t * (0.3 + i * 0.1);
        const dx = Math.cos(dotAngle) * radius;
        const dy = Math.sin(dotAngle) * radius;
        const dotR = 2 + i * 0.5;
        ctx.beginPath();
        ctx.arc(dx, dy, dotR, 0, TAU);
        ctx.fillStyle = 'rgba(240,165,0,' + (0.3 + 0.2 * Math.sin(t * 2 + i)) + ')';
        ctx.fill();

        if (i > 0) {
          const prevR = rings[i - 1];
          const pdx = Math.cos(t * (0.3 + (i - 1) * 0.1)) * prevR;
          const pdy = Math.sin(t * (0.3 + (i - 1) * 0.1)) * prevR;
          ctx.beginPath();
          ctx.moveTo(pdx, pdy);
          ctx.lineTo(dx, dy);
          ctx.strokeStyle = 'rgba(240,165,0,0.06)';
          ctx.lineWidth = 0.5;
          ctx.stroke();
        }
      });
    }

    function drawPhyllotaxis() {
      const numSeeds = 200;
      const spacing = maxR * 0.028;

      for (let n = 0; n < numSeeds; n++) {
        const angle = n * GOLDEN_ANGLE + t * 0.4;
        const r = spacing * Math.sqrt(n);
        if (r > maxR * 0.95) continue;

        const x = Math.cos(angle) * r;
        const y = Math.sin(angle) * r;
        const distRatio = r / maxR;
        const pulse = 1 + 0.4 * Math.sin(t * 2 + n * 0.1);
        const size = (1.2 + distRatio * 1.5) * pulse;
        const alpha = 0.08 + 0.12 * (1 - distRatio);

        ctx.beginPath();
        ctx.arc(x, y, size, 0, TAU);

        if (n % 3 === 0) ctx.fillStyle = 'rgba(240,165,0,' + alpha + ')';
        else if (n % 3 === 1) ctx.fillStyle = 'rgba(13,110,253,' + (alpha * 0.7) + ')';
        else ctx.fillStyle = 'rgba(0,200,83,' + (alpha * 0.6) + ')';
        ctx.fill();
      }
    }

    function drawPentagonLayers() {
      for (let layer = 0; layer < 3; layer++) {
        const r = maxR * (0.25 * Math.pow(PHI, layer) / Math.pow(PHI, 2));
        const rotSpeed = (layer % 2 === 0 ? 1 : -1) * (0.2 + layer * 0.1);

        ctx.save();
        ctx.rotate(t * rotSpeed);

        const pts = [];
        for (let i = 0; i < 5; i++) {
          const a = (i * TAU / 5) - Math.PI / 2;
          pts.push({ x: Math.cos(a) * r, y: Math.sin(a) * r });
        }

        ctx.beginPath();
        pts.forEach((p, i) => {
          if (i === 0) ctx.moveTo(p.x, p.y);
          else ctx.lineTo(p.x, p.y);
        });
        ctx.closePath();
        ctx.strokeStyle = 'rgba(240,165,0,' + (0.15 - layer * 0.04) + ')';
        ctx.lineWidth = 1;
        ctx.stroke();

        for (let i = 0; i < 5; i++) {
          const j = (i + 2) % 5;
          ctx.beginPath();
          ctx.moveTo(pts[i].x, pts[i].y);
          ctx.lineTo(pts[j].x, pts[j].y);
          ctx.strokeStyle = 'rgba(240,165,0,' + (0.06 - layer * 0.015) + ')';
          ctx.stroke();
        }

        pts.forEach(p => {
          const glow = 2 + Math.sin(t * 3 + layer) * 1;
          ctx.beginPath();
          ctx.arc(p.x, p.y, glow, 0, TAU);
          ctx.fillStyle = 'rgba(240,165,0,' + (0.35 - layer * 0.08) + ')';
          ctx.fill();
        });

        ctx.restore();
      }
    }

    function drawGoldenSpiral() {
      ctx.save();
      ctx.rotate(t * 0.2);

      ctx.beginPath();
      for (let i = 0; i < 500; i++) {
        const theta = i * 0.04;
        const r = 2.5 * Math.pow(PHI, theta / (Math.PI / 2));
        if (r > maxR) break;
        const x = Math.cos(theta) * r;
        const y = Math.sin(theta) * r;
        if (i === 0) ctx.moveTo(x, y);
        else ctx.lineTo(x, y);
      }
      ctx.strokeStyle = 'rgba(240,165,0,0.2)';
      ctx.lineWidth = 1.8;
      ctx.stroke();

      ctx.beginPath();
      for (let i = 0; i < 500; i++) {
        const theta = i * 0.04;
        const r = 2.5 * Math.pow(PHI, theta / (Math.PI / 2));
        if (r > maxR) break;
        const x = Math.cos(theta + Math.PI) * r;
        const y = Math.sin(theta + Math.PI) * r;
        if (i === 0) ctx.moveTo(x, y);
        else ctx.lineTo(x, y);
      }
      ctx.strokeStyle = 'rgba(13,110,253,0.1)';
      ctx.lineWidth = 1;
      ctx.stroke();

      ctx.restore();
    }

    function drawExponentialCurves() {
      ctx.save();
      var curves = [
        { base: Math.E, color: '240,165,0', width: 2, label: 'e' },
        { base: PHI, color: '13,110,253', width: 1.5, label: 'φ' },
        { base: 2, color: '0,200,83', width: 1, label: '2' }
      ];
      var scale = maxR * 0.8;
      var xRange = 4;

      for (var c = 0; c < curves.length; c++) {
        var curve = curves[c];
        var phase = t * (0.3 + c * 0.1);

        ctx.beginPath();
        for (var i = 0; i <= 200; i++) {
          var frac = i / 200;
          var xVal = -xRange + frac * xRange * 2;
          var yVal = Math.pow(curve.base, xVal + Math.sin(phase) * 0.5);
          var px = (frac - 0.5) * scale * 2;
          var py = -yVal / Math.pow(curve.base, xRange) * scale * 0.6;
          if (py < -scale) continue;
          if (i === 0 || py < -scale + 1) ctx.moveTo(px, py);
          else ctx.lineTo(px, py);
        }
        var alpha = 0.15 + Math.sin(phase * 0.7) * 0.05;
        ctx.strokeStyle = 'rgba(' + curve.color + ',' + alpha + ')';
        ctx.lineWidth = curve.width;
        ctx.stroke();

        var labelX = scale * 0.85;
        var labelYVal = Math.pow(curve.base, xRange * 0.85 + Math.sin(phase) * 0.5);
        var labelY = -labelYVal / Math.pow(curve.base, xRange) * scale * 0.6;
        if (labelY > -scale) {
          ctx.font = '600 11px Inter, sans-serif';
          ctx.fillStyle = 'rgba(' + curve.color + ',' + (alpha + 0.1) + ')';
          ctx.fillText(curve.label + '^x', labelX + 4, labelY);
        }
      }

      ctx.beginPath();
      ctx.moveTo(-scale, 0);
      ctx.lineTo(scale, 0);
      ctx.strokeStyle = 'rgba(255,255,255,0.03)';
      ctx.lineWidth = 0.5;
      ctx.stroke();
      ctx.beginPath();
      ctx.moveTo(0, -scale);
      ctx.lineTo(0, scale * 0.1);
      ctx.stroke();

      var numDots = 8;
      for (var d = 0; d < numDots; d++) {
        var dotPhase = t * 0.5 + d * PHI;
        var dotX = ((dotPhase % (xRange * 2)) - xRange);
        var dotY = Math.pow(Math.E, dotX);
        var dpx = (dotX / xRange) * scale;
        var dpy = -dotY / Math.pow(Math.E, xRange) * scale * 0.6;
        if (dpy < -scale || dpy > scale) continue;
        var dotAlpha = 0.3 + Math.sin(dotPhase * 2) * 0.15;
        var dotR = 2 + Math.sin(dotPhase * 3) * 1;
        ctx.beginPath();
        ctx.arc(dpx, dpy, dotR, 0, TAU);
        ctx.fillStyle = 'rgba(240,165,0,' + dotAlpha + ')';
        ctx.fill();
        ctx.beginPath();
        ctx.arc(dpx, dpy, dotR + 3, 0, TAU);
        ctx.fillStyle = 'rgba(240,165,0,' + (dotAlpha * 0.2) + ')';
        ctx.fill();
      }

      ctx.restore();
    }

    function drawRatioSegments() {
      const numLines = 12;
      for (let i = 0; i < numLines; i++) {
        const angle = (i * TAU / numLines) + t * 0.15;
        const len = maxR * 0.9;

        ctx.beginPath();
        ctx.moveTo(0, 0);
        const x2 = Math.cos(angle) * len;
        const y2 = Math.sin(angle) * len;
        ctx.lineTo(x2, y2);
        ctx.strokeStyle = 'rgba(255,255,255,0.02)';
        ctx.lineWidth = 0.5;
        ctx.stroke();

        let seg = len;
        for (let k = 0; k < 5; k++) {
          seg /= PHI;
          const px = Math.cos(angle) * seg;
          const py = Math.sin(angle) * seg;
          const dotPulse = 1.5 + Math.sin(t * 2.5 + k + i * 0.5);
          ctx.beginPath();
          ctx.arc(px, py, dotPulse, 0, TAU);
          ctx.fillStyle = 'rgba(240,165,0,' + (0.25 - k * 0.04) + ')';
          ctx.fill();
        }
      }
    }

    function draw() {
      t += 0.00382;
      ctx.clearRect(0, 0, w, h);
      ctx.save();
      ctx.translate(cx, cy);

      drawGoldenRectangles();
      drawGeometricRings();
      drawPhyllotaxis();
      drawPentagonLayers();
      drawGoldenSpiral();
      drawExponentialCurves();
      drawRatioSegments();

      ctx.restore();
    }

    resize();
    window.addEventListener('resize', resize);

    var rafId = null;
    var visible = false;
    function tick() {
      draw();
      rafId = requestAnimationFrame(tick);
    }
    var obs = new IntersectionObserver(function(entries) {
      entries.forEach(function(e) {
        if (e.isIntersecting && !visible) {
          visible = true;
          rafId = requestAnimationFrame(tick);
        } else if (!e.isIntersecting && visible) {
          visible = false;
          if (rafId) { cancelAnimationFrame(rafId); rafId = null; }
        }
      });
    }, { threshold: 0 });
    obs.observe(canvas);
  }

  /* ── Section-level canvas layer helpers ── */

  function createSection(canvasId, cxRatio, layers) {
    const canvas = document.getElementById(canvasId);
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    let w, h, cx2, cy2, ts = 0;
    let maxRS;

    function resizeS() {
      const rect = canvas.parentElement.getBoundingClientRect();
      w = canvas.width = rect.width;
      h = canvas.height = rect.height;
      cx2 = w * cxRatio;
      cy2 = h * 0.5;
      maxRS = Math.min(w, h) * 0.42;
    }

    function drawS() {
      ts += 0.00236;
      ctx.clearRect(0, 0, w, h);
      ctx.save();
      ctx.translate(cx2, cy2);

      const env = { ctx, maxR: maxRS, t: ts, PHI, TAU, GOLDEN_ANGLE };
      layers.forEach(fn => fn(env));

      ctx.restore();
    }

    resizeS();
    window.addEventListener('resize', resizeS);

    var rafId = null;
    var visible = false;
    function tick() {
      drawS();
      rafId = requestAnimationFrame(tick);
    }
    var obs = new IntersectionObserver(function(entries) {
      entries.forEach(function(e) {
        if (e.isIntersecting && !visible) {
          visible = true;
          rafId = requestAnimationFrame(tick);
        } else if (!e.isIntersecting && visible) {
          visible = false;
          if (rafId) { cancelAnimationFrame(rafId); rafId = null; }
        }
      });
    }, { threshold: 0 });
    obs.observe(canvas);
  }

  function layerSpiral(e) {
    e.ctx.save();
    e.ctx.rotate(e.t * 0.2);
    e.ctx.beginPath();
    for (let i = 0; i < 500; i++) {
      const theta = i * 0.04;
      const r = 2.5 * Math.pow(e.PHI, theta / (Math.PI / 2));
      if (r > e.maxR) break;
      const x = Math.cos(theta) * r;
      const y = Math.sin(theta) * r;
      if (i === 0) e.ctx.moveTo(x, y);
      else e.ctx.lineTo(x, y);
    }
    e.ctx.strokeStyle = 'rgba(240,165,0,0.18)';
    e.ctx.lineWidth = 1.2;
    e.ctx.stroke();
    e.ctx.restore();
  }

  function layerRings(e) {
    let r = e.maxR * 0.06;
    let idx = 0;
    while (r < e.maxR) {
      const alpha = 0.05 + 0.02 * Math.sin(e.t * 1.5 + idx);
      e.ctx.beginPath();
      e.ctx.arc(0, 0, r, 0, e.TAU);
      e.ctx.strokeStyle = 'rgba(240,165,0,' + alpha + ')';
      e.ctx.lineWidth = 0.6;
      e.ctx.setLineDash([r * 0.02, r * 0.05]);
      e.ctx.stroke();
      e.ctx.setLineDash([]);

      const da = e.t * (0.2 + idx * 0.08);
      e.ctx.beginPath();
      e.ctx.arc(Math.cos(da) * r, Math.sin(da) * r, 1.5 + idx * 0.3, 0, e.TAU);
      e.ctx.fillStyle = 'rgba(240,165,0,' + (0.25 + 0.15 * Math.sin(e.t * 2 + idx)) + ')';
      e.ctx.fill();

      r *= e.PHI;
      idx++;
    }
  }

  function layerPhyllotaxis(e) {
    const sp = e.maxR * 0.028;
    for (let n = 0; n < 180; n++) {
      const angle = n * e.GOLDEN_ANGLE + e.t * 0.35;
      const r = sp * Math.sqrt(n);
      if (r > e.maxR * 0.9) continue;
      const x = Math.cos(angle) * r;
      const y = Math.sin(angle) * r;
      const dr = r / e.maxR;
      const pulse = 1 + 0.3 * Math.sin(e.t * 2 + n * 0.08);
      const sz = (1 + dr * 1.2) * pulse;
      e.ctx.beginPath();
      e.ctx.arc(x, y, sz, 0, e.TAU);
      e.ctx.fillStyle = n % 3 === 0 ? 'rgba(240,165,0,' + (0.07 + 0.08 * (1 - dr)) + ')'
        : n % 3 === 1 ? 'rgba(13,110,253,' + (0.05 + 0.06 * (1 - dr)) + ')'
        : 'rgba(0,200,83,' + (0.04 + 0.05 * (1 - dr)) + ')';
      e.ctx.fill();
    }
  }

  function layerPentagons(e) {
    for (let l = 0; l < 2; l++) {
      const r = e.maxR * (0.25 * Math.pow(e.PHI, l) / (e.PHI * e.PHI));
      e.ctx.save();
      e.ctx.rotate(e.t * (l % 2 === 0 ? 0.3 : -0.2));
      const pts = [];
      for (let i = 0; i < 5; i++) {
        const a = (i * e.TAU / 5) - Math.PI / 2;
        pts.push({ x: Math.cos(a) * r, y: Math.sin(a) * r });
      }
      e.ctx.beginPath();
      pts.forEach((p, i) => { if (i === 0) e.ctx.moveTo(p.x, p.y); else e.ctx.lineTo(p.x, p.y); });
      e.ctx.closePath();
      e.ctx.strokeStyle = 'rgba(240,165,0,' + (0.12 - l * 0.04) + ')';
      e.ctx.lineWidth = 0.8;
      e.ctx.stroke();
      pts.forEach(p => {
        e.ctx.beginPath();
        e.ctx.arc(p.x, p.y, 2, 0, e.TAU);
        e.ctx.fillStyle = 'rgba(240,165,0,0.3)';
        e.ctx.fill();
      });
      e.ctx.restore();
    }
  }

  function layerSegments(e) {
    for (let i = 0; i < 8; i++) {
      const angle = (i * e.TAU / 8) + e.t * 0.12;
      const len = e.maxR * 0.8;
      e.ctx.beginPath();
      e.ctx.moveTo(0, 0);
      e.ctx.lineTo(Math.cos(angle) * len, Math.sin(angle) * len);
      e.ctx.strokeStyle = 'rgba(255,255,255,0.015)';
      e.ctx.lineWidth = 0.5;
      e.ctx.stroke();

      let seg = len;
      for (let k = 0; k < 4; k++) {
        seg /= e.PHI;
        const dp = 1.2 + Math.sin(e.t * 2 + k + i * 0.4);
        e.ctx.beginPath();
        e.ctx.arc(Math.cos(angle) * seg, Math.sin(angle) * seg, dp, 0, e.TAU);
        e.ctx.fillStyle = 'rgba(240,165,0,' + (0.2 - k * 0.04) + ')';
        e.ctx.fill();
      }
    }
  }

  function layerRects(e) {
    e.ctx.save();
    e.ctx.rotate(e.t * 0.1);
    let rw = e.maxR * 0.7;
    let rh = rw / e.PHI;
    for (let i = 0; i < 8; i++) {
      const alpha = 0.12 - i * 0.013;
      if (alpha <= 0) break;
      e.ctx.strokeStyle = 'rgba(240,165,0,' + alpha + ')';
      e.ctx.lineWidth = 1 - i * 0.08;
      e.ctx.strokeRect(-rw / 2, -rh / 2, rw, rh);

      const sq = Math.min(rw, rh);
      const arcR = sq;
      let ax, ay, sa;
      switch (i % 4) {
        case 0: ax = -rw / 2 + sq; ay = -rh / 2 + sq; sa = Math.PI; e.ctx.strokeStyle = 'rgba(0,200,83,' + (alpha * 0.6) + ')'; break;
        case 1: ax = rw / 2 - sq; ay = -rh / 2; sa = Math.PI * 0.5; e.ctx.strokeStyle = 'rgba(13,110,253,' + (alpha * 0.6) + ')'; break;
        case 2: ax = rw / 2 - sq; ay = rh / 2 - sq; sa = 0; e.ctx.strokeStyle = 'rgba(240,165,0,' + (alpha * 0.6) + ')'; break;
        case 3: ax = -rw / 2; ay = rh / 2; sa = -Math.PI * 0.5; e.ctx.strokeStyle = 'rgba(0,200,83,' + (alpha * 0.4) + ')'; break;
      }
      e.ctx.beginPath();
      e.ctx.arc(ax, ay, arcR, sa, sa + Math.PI * 0.5);
      e.ctx.lineWidth = 1.2 - i * 0.1;
      e.ctx.stroke();

      if (rw > rh) rw = rw - rh;
      else { const tmp = rh - rw; rh = rw; rw = tmp; }
      if (rw < 2 || rh < 2) break;
    }
    e.ctx.restore();
  }

  /* ── Instantiate canvases ── */
  createGolden('goldenCanvas', 0.618);
  createGolden('goldenCanvasCta', 0.5);

  if (window.innerWidth > 768) {
    createSection('gcServices', 0.5, [layerSpiral, layerRings]);
    createSection('gcProjects', 0.618, [layerRects, layerPhyllotaxis]);
    createSection('gcProcess', 0.618, [layerRects, layerPentagons]);
    createSection('gcFaq', 0.382, [layerRings, layerSpiral]);
    createSection('gcFooter', 0.618, [layerPhyllotaxis, layerPentagons]);
    createSection('gcVisas', 0.618, [layerPhyllotaxis, layerRings]);
    createSection('gcHistory', 0.382, [layerSpiral, layerSegments]);
  }
}


/* ============================================================
   initTestimonialCarousel
   Mobile testimonial carousel with auto-advance
   ============================================================ */
function initTestimonialCarousel() {
  const track = document.getElementById('testimonialTrack');
  const dots = document.querySelectorAll('.carousel-dot');
  if (!track || !dots.length) return;

  let current = 0;
  const total = dots.length;

  function goTo(idx) {
    current = idx;
    track.style.transform = 'translateX(-' + (idx * 100) + '%)';
    dots.forEach((d, i) => d.classList.toggle('active', i === idx));
  }

  dots.forEach(d => {
    d.addEventListener('click', () => goTo(parseInt(d.dataset.slide)));
  });

  setInterval(() => {
    goTo((current + 1) % total);
  }, 4236);
}


/* ============================================================
   initVanillaTilt
   3D tilt effect on hover for cards
   ============================================================ */
function initVanillaTilt() {
  if (window.matchMedia('(hover: none)').matches) return;
  const cards = document.querySelectorAll('.service-card, .visa-card, .testimonial-card, .blog-card, .timeline-card, .hero-card, .step-card, .accordion-item, .project-card, .team-card');
  cards.forEach(card => {
    card.addEventListener('mousemove', e => {
      const rect = card.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;
      const cx = rect.width / 2;
      const cy = rect.height / 2;
      const rotateX = ((y - cy) / cy) * -4.236;
      const rotateY = ((x - cx) / cx) * 4.236;
      card.style.transform = 'perspective(800px) rotateX(' + rotateX + 'deg) rotateY(' + rotateY + 'deg) scale(1.0236)';
    });
    card.addEventListener('mouseleave', () => {
      card.style.transform = '';
      card.style.transition = 'transform .618s cubic-bezier(.22,1,.36,1)';
      setTimeout(() => { card.style.transition = ''; }, 618);
    });
  });
}


/* ============================================================
   initMagneticButtons
   Magnetic pull effect on hover for buttons
   ============================================================ */
function initMagneticButtons() {
  if (window.matchMedia('(hover: none)').matches) return;
  const btns = document.querySelectorAll('.btn-gold, .btn-outline-light-custom, .whatsapp-float, .back-to-top');
  btns.forEach(btn => {
    btn.addEventListener('mousemove', e => {
      const rect = btn.getBoundingClientRect();
      const x = e.clientX - rect.left - rect.width / 2;
      const y = e.clientY - rect.top - rect.height / 2;
      btn.style.transform = 'translate(' + (x * 0.236) + 'px,' + (y * 0.236) + 'px)';
    });
    btn.addEventListener('mouseleave', () => {
      btn.style.transform = '';
      btn.style.transition = 'transform .618s cubic-bezier(.22,1,.36,1)';
      setTimeout(() => { btn.style.transition = ''; }, 618);
    });
  });
}


/* ============================================================
   initSpotlightGlow
   Radial glow follows cursor over dark sections
   ============================================================ */
function initSpotlightGlow() {
  if (window.matchMedia('(hover: none)').matches) return;
  const sections = document.querySelectorAll('.section-dark, .section-dark2, .cta-section, .footer');
  sections.forEach(sec => {
    const glow = document.createElement('div');
    glow.className = 'spotlight-glow';
    sec.style.position = 'relative';
    sec.appendChild(glow);

    sec.addEventListener('mousemove', e => {
      const rect = sec.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;
      glow.style.background = 'radial-gradient(423.6px circle at ' + x + 'px ' + y + 'px, rgba(240,165,0,0.06), transparent 61.8%)';
      glow.style.opacity = '1';
    });
    sec.addEventListener('mouseleave', () => {
      glow.style.opacity = '0';
    });
  });
}


/* ============================================================
   initMouseParallax
   Subtle parallax on hero section layers
   ============================================================ */
function initMouseParallax() {
  if (window.matchMedia('(hover: none)').matches) return;
  const hero = document.querySelector('.hero');
  const layers = hero ? hero.querySelectorAll('.hero-content, .hero-visual, .hero-float-badge') : [];
  if (!layers.length) return;

  hero.addEventListener('mousemove', e => {
    const rect = hero.getBoundingClientRect();
    const x = (e.clientX - rect.left - rect.width / 2) / rect.width;
    const y = (e.clientY - rect.top - rect.height / 2) / rect.height;

    layers.forEach((layer, i) => {
      const depth = (i + 1) * 6.18;
      const moveX = x * depth;
      const moveY = y * depth;
      layer.style.transform = 'translate(' + moveX + 'px, ' + moveY + 'px)';
    });
  });

  hero.addEventListener('mouseleave', () => {
    layers.forEach(layer => {
      layer.style.transition = 'transform .618s cubic-bezier(.22,1,.36,1)';
      layer.style.transform = 'translate(0,0)';
      setTimeout(() => { layer.style.transition = ''; }, 618);
    });
  });
}


/* ============================================================
   initRippleEffect
   Material-style click ripple on buttons
   ============================================================ */
function initRippleEffect() {
  document.querySelectorAll('.btn-gold, .btn-outline-light-custom, .wa-quick-btn, .gov-link-item, .blog-link').forEach(btn => {
    btn.style.position = 'relative';
    btn.style.overflow = 'hidden';
    btn.addEventListener('click', function(e) {
      const ripple = document.createElement('span');
      ripple.className = 'ripple-effect';
      const rect = this.getBoundingClientRect();
      const size = Math.max(rect.width, rect.height) * 2;
      ripple.style.width = ripple.style.height = size + 'px';
      ripple.style.left = (e.clientX - rect.left - size / 2) + 'px';
      ripple.style.top = (e.clientY - rect.top - size / 2) + 'px';
      this.appendChild(ripple);
      setTimeout(() => ripple.remove(), 618);
    });
  });
}


/* ============================================================
   initTextScramble
   Scramble-in reveal for section titles
   ============================================================ */
function initTextScramble() {
  const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
  const titles = document.querySelectorAll('.section-title');

  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting && !entry.target.dataset.scrambled) {
        entry.target.dataset.scrambled = 'true';
        scramble(entry.target);
      }
    });
  }, { threshold: 0.5 });

  titles.forEach(t => observer.observe(t));

  function scramble(el) {
    const original = el.textContent;
    const len = original.length;
    let iteration = 0;

    const interval = setInterval(() => {
      el.textContent = original.split('').map((ch, i) => {
        if (ch === ' ') return ' ';
        if (i < iteration) return original[i];
        return chars[Math.floor(Math.random() * chars.length)];
      }).join('');

      iteration += 1 / 2;
      if (iteration >= len) {
        el.textContent = original;
        clearInterval(interval);
      }
    }, 23.6);
  }
}

/* ── Portfolio Filter ── */
function initPortfolioFilter() {
  const filters = document.querySelectorAll('.portfolio-filter');
  const items = document.querySelectorAll('.portfolio-item');
  if (!filters.length || !items.length) return;

  filters.forEach(btn => {
    btn.addEventListener('click', () => {
      filters.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      const cat = btn.dataset.filter;
      items.forEach(item => {
        if (cat === 'all' || item.dataset.category === cat) {
          item.classList.remove('hidden');
          item.style.position = '';
        } else {
          item.classList.add('hidden');
        }
      });
    });
  });
}

document.addEventListener('DOMContentLoaded', initPortfolioFilter);
