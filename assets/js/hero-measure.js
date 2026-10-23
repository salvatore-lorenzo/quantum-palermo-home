// The figure in the home-page hero: a qubit measured while you watch. Loaded only by layouts/index.html.
//
// 512 records of <sigma_z> for a qubit under continuous measurement, each prepared in
// |psi> = sqrt(0.7)|0> + sqrt(0.3)|1>, are simulated in the browser and drawn as they collapse onto the
// |0> and |1> rails, while the tallies count the records on each rail.
//
// Physics: for continuous (QND) measurement of sigma_z the conditional state stays on the z axis,
//   z(t) = tanh(atanh z0 + s*Gamma*t + W(Gamma*t)),
// with the outcome s = +1 / -1 drawn with the Born weights 0.7 / 0.3 and W a Wiener process (the drift of
// the record is the eigenvalue). z is a martingale, so the fraction ending on |0> converges on
// (1 + z0) / 2 = 0.7. Nothing drawn or counted uses s: the tallies count z itself.
//
// Without JavaScript the figure is not shown (see .measure in main.css); with prefers-reduced-motion the
// final state is drawn at once.

(() => {
  const fig = document.querySelector(".measure");
  const box = fig && fig.querySelector(".measure-plot");
  const canvas = box && box.querySelector("canvas");
  if (!canvas || !canvas.getContext) return;
  const ctx = canvas.getContext("2d");
  const $ = (s) => fig.querySelector(s);
  const n0El = $("[data-n0]"), n1El = $("[data-n1]"), liveEl = $("[data-live]"), sayEl = $("[data-announce]"), againBtn = $("[data-again]");
  const reduce = matchMedia("(prefers-reduced-motion: reduce)");
  const SEED = +new URLSearchParams(location.search).get("seed") || 0;   // ?seed=N: a reproducible first run

  const P0 = 0.7, Z0 = 2 * P0 - 1;            // z0 = 0.4
  const N = 512, S = 720;                     // records, time steps
  const LOG = [-3, Math.log10(40)];           // Gamma t from 0.001 to 40, log axis
  const EPS = 0.02;                           // "on a rail": |z| > 0.98
  const PREP = 240, SWEEP = 2250;             // ms
  const INK_K = 0.55;                         // Beer-Lambert constant: brightness of the records
  const AXIS_H = 24;                          // px under the band for the time axis

  const TK = new Float64Array(S + 1);
  for (let k = 0; k <= S; k++) TK[k] = Math.pow(10, LOG[0] + (LOG[1] - LOG[0]) * k / S);

  let Z, c0, c1, last, geom, plot, st, raf = 0, t0 = 0, progress = 0, running = false, shown = -1, inView = true, userRun = false;
  const totals = { runs: 0, n0: 0, n: 0 };

  function mulberry32(a) {
    return () => {
      a |= 0; a = a + 0x6D2B79F5 | 0;
      let t = Math.imul(a ^ a >>> 15, 1 | a);
      t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t;
      return ((t ^ t >>> 14) >>> 0) / 4294967296;
    };
  }

  function simulate(seed) {
    const rnd = mulberry32(seed);
    let spare = null;
    const gauss = () => {   // Box-Muller
      if (spare !== null) { const g = spare; spare = null; return g; }
      let u = 0; while (u === 0) u = rnd();
      const v = rnd(), r = Math.sqrt(-2 * Math.log(u));
      spare = r * Math.sin(2 * Math.PI * v); return r * Math.cos(2 * Math.PI * v);
    };
    const a0 = Math.atanh(Z0);
    Z = new Float32Array(N * (S + 1)); c0 = new Uint16Array(S + 1); c1 = new Uint16Array(S + 1); last = new Uint16Array(N);
    for (let i = 0; i < N; i++) {
      const s = rnd() < P0 ? 1 : -1, o = i * (S + 1);
      let B = Math.sqrt(TK[0]) * gauss();
      Z[o] = Math.tanh(a0 + s * TK[0] + B);
      for (let k = 1; k <= S; k++) { B += Math.sqrt(TK[k] - TK[k - 1]) * gauss(); Z[o + k] = Math.tanh(a0 + s * TK[k] + B); }
      let L = S; while (L > 0 && Math.abs(Z[o + L]) > 0.9995) L--;      // after this, flat on a rail
      last[i] = Math.min(S, L + 1);
    }
    for (let k = 0; k <= S; k++) {
      let a = 0, b = 0;
      for (let i = 0; i < N; i++) { const z = Z[i * (S + 1) + k]; if (z > 1 - EPS) a++; else if (z < -1 + EPS) b++; }
      c0[k] = a; c1[k] = b;
    }
  }

  // Colours and margins come from the custom properties of .measure in main.css
  function readStyle() {
    const cs = getComputedStyle(fig), rem = parseFloat(getComputedStyle(document.documentElement).fontSize) || 16;
    const len = (name, d) => { const v = cs.getPropertyValue(name).trim(), n = parseFloat(v); return isFinite(n) ? (/rem$/.test(v) ? n * rem : n) : d; };
    const color = (name, d) => cs.getPropertyValue(name).trim() || d;
    const ink = color("--measure-ink", "#f4f6ff");
    return {
      ink, inkRGB: (ink.match(/[0-9a-f]{2}/gi) || ["f4", "f6", "ff"]).slice(0, 3).map((h) => parseInt(h, 16)),
      accent: color("--measure-accent", "#ff8a3d"), axis: color("--measure-axis", "#c9d3f0"),
      font: "500 12px " + cs.fontFamily, ml: len("--measure-ml", 44), mr: len("--measure-mr", 104),
    };
  }

  // Geometry (CSS px): the |0> rail on top, the |1> rail below, room outside each rail for its tally
  // wedge, the time axis under the band; time runs from the kets (left) to the tallies (right), and the
  // settled records run on to the right edge.
  function measureGeom() {
    const r = canvas.getBoundingClientRect();
    const dpr = Math.min(window.devicePixelRatio || 1, 2);
    const W = r.width, H = r.height, U = H - AXIS_H, room = Math.round(U * 0.13);
    return { W, H, dpr, U, room, zP: room, zM: U - room, tA: st.ml, tB: Math.max(st.ml + 40, W - st.mr) };
  }
  const T = (k) => geom.tA + (k / S) * (geom.tB - geom.tA);                 // time axis
  const Q = (z) => geom.zM + (1 + z) * 0.5 * (geom.zP - geom.zM);           // z axis

  // Brightness by dwell time, like a scope trace: every record lays down the same ink per unit of the
  // time axis, spread along its path, so brightness is the ensemble density P(z, t). Ink is accumulated
  // in a buffer and developed with Beer-Lambert absorption, 1 - exp(-K rho).
  function renderPlot() {
    const { W, H, dpr, room } = geom;
    const PW = Math.max(1, Math.round(W * dpr)), PH = Math.max(1, Math.round(H * dpr));
    const rho = new Float32Array(PW * PH);
    const splat = (x, y, w) => {
      const gx = x - 0.5, gy = y - 0.5, ix = Math.floor(gx), iy = Math.floor(gy);
      if (ix < 0 || iy < 0 || ix + 1 >= PW || iy + 1 >= PH) return;
      const fx = gx - ix, fy = gy - iy, o = iy * PW + ix;
      rho[o] += w * (1 - fx) * (1 - fy); rho[o + 1] += w * fx * (1 - fy);
      rho[o + PW] += w * (1 - fx) * fy; rho[o + PW + 1] += w * fx * fy;
    };
    const seg = (xa, ya, xb, yb) => {   // device px; weight = progress along the time axis
      const dx = xb - xa, dy = yb - ya, n = Math.max(1, Math.ceil(Math.max(Math.abs(dx), Math.abs(dy))));
      const sx = dx / n, sy = dy / n, w = Math.abs(sx);
      if (w === 0) return;
      for (let j = 0; j < n; j++) splat(xa + (j + 0.5) * sx, ya + (j + 0.5) * sy, w);
    };
    const X = new Float32Array(S + 1);
    for (let k = 0; k <= S; k++) X[k] = T(k) * dpr;
    const zc = (geom.zM + geom.zP) * 0.5 * dpr, zs = (geom.zP - geom.zM) * 0.5 * dpr, END = W * dpr;
    for (let i = 0; i < N; i++) {
      const o = i * (S + 1), L = last[i];
      let xa = X[0], ya = zc + Z0 * zs;
      for (let k = 0; k <= L; k++) { const xb = X[k], yb = zc + Z[o + k] * zs; seg(xa, ya, xb, yb); xa = xb; ya = yb; }
      if (L < S) { const yb = zc + (Z[o + S] > 0 ? 1 : -1) * zs; seg(xa, ya, X[S], yb); xa = X[S]; ya = yb; }
      if (END > xa) seg(xa, ya, END, ya);           // past the axis the settled record runs on
    }
    const span = Math.abs(geom.zP - geom.zM), len = Math.abs(geom.tB - geom.tA);
    const K = INK_K * (span / 390) * Math.sqrt(1270 / Math.max(300, len)) * dpr;
    const img = new ImageData(PW, PH), d = img.data, [r, g, b] = st.inkRGB;
    for (let q = 0, p = 0; q < rho.length; q++, p += 4) {
      const rr = rho[q];
      if (rr <= 0) continue;
      d[p] = r; d[p + 1] = g; d[p + 2] = b; d[p + 3] = 255 * (1 - Math.exp(-K * rr));
    }
    plot = plot || document.createElement("canvas");
    plot.width = PW; plot.height = PH;
    const pc = plot.getContext("2d");
    pc.putImageData(img, 0, 0);
    // tally wedges: thickness outside each rail = records currently within 2% of that rail
    pc.setTransform(dpr, 0, 0, dpr, 0, 0);
    pc.fillStyle = st.accent;
    const h = (room - 3) / (N * 0.74);
    const wedge = (zr, dir, c) => {
      pc.beginPath(); pc.moveTo(T(0), zr);
      for (let k = 0; k <= S; k++) pc.lineTo(T(k), zr + dir * c[k] * h);
      pc.lineTo(W, zr + dir * c[S] * h); pc.lineTo(W, zr); pc.closePath(); pc.fill();
    };
    wedge(geom.zP, -1, c0);
    wedge(geom.zM, 1, c1);
  }

  function drawAxes() {
    const { W, U } = geom;
    ctx.globalAlpha = 1;
    ctx.fillStyle = st.accent;                       // eigenvalue rails, known before any click; they start after the kets
    const r0 = Math.max(0, geom.tA - 8);
    ctx.fillRect(r0, Math.round(geom.zP) - 0.5, W - r0, 1);
    ctx.fillRect(r0, Math.round(geom.zM) - 0.5, W - r0, 1);
    // time axis under the band: decade ticks; a label is skipped where it would touch the previous one
    ctx.fillStyle = st.axis; ctx.font = st.font; ctx.textBaseline = "top"; ctx.textAlign = "left";
    let right = -Infinity;
    for (const [dd, label] of [[-3, "0.001"], [-2, "0.01"], [-1, "0.1"], [0, "1"], [1, "10"]]) {
      const a = geom.tA + (dd - LOG[0]) / (LOG[1] - LOG[0]) * (geom.tB - geom.tA);
      ctx.fillRect(Math.round(a) - 0.5, U + 2, 1, 4);
      const w = ctx.measureText(label).width, x = dd === -3 ? a : a - w / 2;
      if (x < right + 14) continue;
      ctx.fillText(label, x, U + 8);
      right = x + w;
    }
    const full = "Γt, log scale";
    const label = W - ctx.measureText(full).width > right + 12 ? full : W - ctx.measureText("Γt").width > right + 12 ? "Γt" : "";
    ctx.textAlign = "right";
    if (label) ctx.fillText(label, W, U + 8);
  }

  function frame(pr) {
    const { W, H, dpr } = geom;
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.clearRect(0, 0, W, H);
    const k = Math.max(0, Math.min(S, Math.floor(pr * S + 1e-9)));
    const c = pr >= 1 ? W : T(k);
    if (pr > 0) { const cd = Math.ceil(c * dpr); ctx.drawImage(plot, 0, 0, cd, plot.height, 0, 0, cd / dpr, H); }
    drawAxes();
    ctx.fillStyle = st.ink;
    ctx.beginPath(); ctx.arc(T(0), Q(Z0), 4.5, 0, Math.PI * 2); ctx.fill();   // the prepared state
    if (pr > 0 && pr < 1) {                                                    // the sweep and its records
      const lo = Math.min(geom.zP, geom.zM), span = Math.abs(geom.zP - geom.zM);
      ctx.globalAlpha = 0.5; ctx.fillRect(Math.round(c) - 0.5, lo, 1, span);
      ctx.globalAlpha = 0.85;
      for (let i = 0; i < N; i++) ctx.fillRect(c - 1, Q(Z[i * (S + 1) + k]) - 1, 2, 2);
      ctx.globalAlpha = 1;
    }
    if (shown !== k) { shown = k; n0El.textContent = c0[k]; n1El.textContent = c1[k]; }
  }

  function finish() {
    running = false; progress = 1; shown = -1; frame(1);
    const a = c0[S], b = c1[S], u = N - a - b;
    totals.runs++; totals.n0 += a; totals.n += N;
    const pct = (100 * totals.n0 / totals.n).toFixed(1);
    //const sentence = (totals.runs === 1 ? "This visit: " : "Run " + totals.runs + ": ") + a + " in |0⟩, " + b + " in |1⟩" +
    //  (u ? ", " + u + " still undecided" : "") + ". " + (totals.runs === 1 ? "" : "All runs: ") + pct + "% in |0⟩ against the Born weight of 70%.";
    const sentence = `Observed: ${pct}% in |0⟩ · Born prediction: 70%`;
    //const sentence = `Observed: ${pct}% in <span class="ket">|0⟩</span> · Born prediction: 70%`;
    liveEl.innerHTML = sentence.replace(/\|[^|⟩<]*⟩/g, (k) => `<span class="ket">${k}</span>`);   // kets in the ket font
    // announced once, at the end, when the figure is on screen or the visitor asked for the run
    if (sayEl && (inView || userRun)) sayEl.textContent = sentence;
  }

  // time spent per unit of x: brisk along the prepared beam, slow through the split, easing out
  const TW = (() => {
    const n = 400, w = new Float64Array(n + 1);
    for (let i = 0; i <= n; i++) {
      const p = i / n;
      w[i] = 0.55 + 1.5 * Math.exp(-Math.pow((p - 0.74) / 0.16, 2)) + 0.9 * Math.max(0, (p - 0.9) / 0.1) ** 2;
    }
    const cum = new Float64Array(n + 1);
    for (let i = 1; i <= n; i++) cum[i] = cum[i - 1] + (w[i] + w[i - 1]) / 2;
    for (let i = 0; i <= n; i++) cum[i] /= cum[n];
    return { n, cum };
  })();
  function sweepAt(u) {      // invert cumulative time -> x progress
    const { n, cum } = TW;
    let lo = 0, hi = n;
    while (hi - lo > 1) { const m = (lo + hi) >> 1; if (cum[m] < u) lo = m; else hi = m; }
    return (lo + (u - cum[lo]) / Math.max(1e-9, cum[hi] - cum[lo])) / n;
  }

  function tick(now) {
    if (!running) return;
    const t = now - t0 - PREP;
    if (t >= 0) {
      const u = Math.min(1, t / SWEEP);
      progress = u >= 1 ? 1 : sweepAt(u);
      frame(progress);
      if (u >= 1) { finish(); return; }
    }
    raf = requestAnimationFrame(tick);
  }

  function setup() {
    st = readStyle();
    geom = measureGeom();
    canvas.width = Math.round(geom.W * geom.dpr); canvas.height = Math.round(geom.H * geom.dpr);
    box.style.setProperty("--y-0", geom.zP + "px");          // the kets and tallies follow the rails
    box.style.setProperty("--y-psi", Q(Z0) + "px");
    box.style.setProperty("--y-1", geom.zM + "px");
    renderPlot();
  }

  function run(animate) {
    cancelAnimationFrame(raf);
    const seed = SEED && totals.runs === 0 ? SEED : (Math.random() * 4294967296) >>> 0;
    simulate(seed);
    setup();
    if (!animate || reduce.matches || document.hidden || !inView) { finish(); return; }
    liveEl.textContent = "Measuring…";
    running = true; t0 = performance.now(); shown = -1; frame(0);
    raf = requestAnimationFrame(tick);
  }

  // resize (debounced): the same records, redrawn to the new geometry at the current progress
  let lastW = 0, lastH = 0, rt = 0;
  const size = () => { const b = canvas.getBoundingClientRect(); return [Math.round(b.width), Math.round(b.height)]; };
  const ro = new ResizeObserver(() => {
    clearTimeout(rt);
    rt = setTimeout(() => {
      const [W, H] = size();
      if (!Z || (W === lastW && H === lastH)) return;
      lastW = W; lastH = H; setup(); shown = -1; frame(running ? progress : 1);
    }, 150);
  });
  // theme switch (the toggle sets data-theme on <html>; without a choice the system setting applies):
  // re-read the --measure-* colours and redraw the same records at the current progress
  const recolour = () => { if (!Z) return; setup(); shown = -1; frame(running ? progress : 1); };
  new MutationObserver(recolour).observe(document.documentElement, { attributes: true, attributeFilter: ["data-theme"] });
  matchMedia("(prefers-color-scheme: dark)").addEventListener("change", recolour);
  // never animate unseen: a hidden tab or an off-screen hero jumps to the final state
  document.addEventListener("visibilitychange", () => { if (document.hidden && running) { cancelAnimationFrame(raf); finish(); } });
  new IntersectionObserver((es) => {
    inView = es[es.length - 1].isIntersecting;
    if (!inView && running) { cancelAnimationFrame(raf); finish(); }
  }).observe(fig);
  againBtn.addEventListener("click", () => { userRun = true; run(true); });

  const start = () => { [lastW, lastH] = size(); run(true); ro.observe(canvas); };
  (document.fonts && document.fonts.ready ? document.fonts.ready : Promise.resolve()).then(start);
})();
