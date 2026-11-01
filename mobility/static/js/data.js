/* WAY-BE — helpers pages données : thème Chart.js, compteurs animés, reveal. */
(function () {
  "use strict";

  const COLORS = { voiture: "#ff3ea5", velo: "#39e1ff", pieton: "#ffd23f", lourd: "#b388ff" };
  const nf = new Intl.NumberFormat("fr-BE");
  const reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  function alpha(hex, a) {
    const n = parseInt(hex.slice(1), 16);
    return `rgba(${n >> 16},${(n >> 8) & 255},${n & 255},${a})`;
  }

  function fmt(n, digits) {
    if (n === null || n === undefined || isNaN(n)) return "–";
    return digits ? new Intl.NumberFormat("fr-BE", { maximumFractionDigits: digits, minimumFractionDigits: digits }).format(n)
                  : nf.format(Math.round(n));
  }

  /* Thème global Chart.js, appelé une fois Chart chargé */
  function theme() {
    if (!window.Chart || theme.done) return;
    theme.done = true;
    const css = getComputedStyle(document.documentElement);
    const muted = css.getPropertyValue("--text-muted").trim() || "#b3a3c9";
    const body = css.getPropertyValue("--font-body").trim() || "system-ui";
    Chart.defaults.color = muted;
    Chart.defaults.font.family = body;
    Chart.defaults.font.size = 12;
    Chart.defaults.borderColor = "rgba(255,255,255,.06)";
    Chart.defaults.animation.duration = reduced ? 0 : 900;
    Chart.defaults.animation.easing = "easeOutQuart";
    Chart.defaults.maintainAspectRatio = false;
    Chart.defaults.responsive = true;
    Chart.defaults.interaction = { mode: "index", intersect: false };
    const tt = Chart.defaults.plugins.tooltip;
    tt.backgroundColor = "rgba(19,11,36,.96)";
    tt.borderColor = "rgba(255,140,220,.38)";
    tt.borderWidth = 1;
    tt.padding = 12;
    tt.cornerRadius = 10;
    tt.titleColor = "#f6eefc";
    tt.bodyColor = "#f6eefc";
    tt.titleFont = { family: body, weight: "600" };
    tt.boxPadding = 4;
    tt.usePointStyle = true;
    const lg = Chart.defaults.plugins.legend.labels;
    lg.usePointStyle = true;
    lg.pointStyle = "rectRounded";
    lg.boxWidth = 10;
    lg.boxHeight = 10;
    lg.padding = 16;
  }

  /* Compteurs : <span data-count="1234" data-digits="1"> */
  function countUp(root) {
    (root || document).querySelectorAll("[data-count]").forEach(countEl);
  }

  function countEl(el) {
    {
      const target = parseFloat(el.dataset.count);
      const digits = parseInt(el.dataset.digits || "0", 10);
      if (isNaN(target)) return;
      if (reduced) { el.textContent = fmt(target, digits); return; }
      const t0 = performance.now(), dur = 1400;
      const step = (t) => {
        const p = Math.min(1, (t - t0) / dur);
        const e = 1 - Math.pow(1 - p, 4);
        el.textContent = fmt(target * e, digits);
        if (p < 1) requestAnimationFrame(step);
      };
      requestAnimationFrame(step);
    }
  }

  /* Reveal au scroll + callback (pour lancer un graphique quand il devient visible) */
  function onVisible(el, cb) {
    if (!("IntersectionObserver" in window)) { cb(); return; }
    const io = new IntersectionObserver((entries) => {
      entries.forEach((e) => { if (e.isIntersecting) { io.disconnect(); cb(); } });
    }, { threshold: 0.2 });
    io.observe(el);
  }

  function reveal() {
    document.querySelectorAll(".reveal").forEach((el) => onVisible(el, () => {
      el.classList.add("is-in");
      countUp(el);
    }));
  }

  window.WB = { COLORS, alpha, fmt, theme, countUp, onVisible };

  document.addEventListener("DOMContentLoaded", () => {
    theme();
    reveal();
    document.querySelectorAll("[data-count]").forEach((el) => {
      if (!el.closest(".reveal")) countEl(el);
    });
  });
})();
