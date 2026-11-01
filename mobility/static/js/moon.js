/* WAY-BE · Lune : changer de date sans recharger la page.
   La lune « tourne » à travers ses phases jusqu'à la date choisie, puis les infos se mettent à jour. */
(function () {
  'use strict';

  var LUNAISON = 29.530588853;
  var root = document.querySelector('[data-moon]');
  var form = document.querySelector('[data-moon-form]');
  if (!root || !form || !window.fetch || !window.DOMParser) return;

  var lit = root.querySelector('[data-moon-lit]');
  var clip = root.querySelector('[data-moon-clip]');
  var svg = root.querySelector('svg');
  var halo = root.querySelector('.moon-visual__halo');
  var input = form.querySelector('input[type="date"]');
  var today = document.querySelector('[data-moon-today]');
  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  var age = parseFloat(root.dataset.age) || 0;
  var currentDate = input.value;
  var raf = null, busy = 0;

  /* Même géométrie que moon_utils.moon_svg_path (Python) */
  function illumination(a) { return (1 - Math.cos(2 * Math.PI * a / LUNAISON)) / 2; }
  function path(a) {
    a = ((a % LUNAISON) + LUNAISON) % LUNAISON;
    if (illumination(a) < 0.005) return '';
    var r = 90, frac = a / LUNAISON;
    var rx = Math.abs(Math.cos(2 * Math.PI * frac)) * r;
    var waxing = frac < 0.5, gibbous = frac > 0.25 && frac < 0.75;
    var outer = waxing ? 1 : 0;
    var term = waxing ? (gibbous ? 1 : 0) : (gibbous ? 0 : 1);
    return 'M 100 10 A 90 90 0 0 ' + outer + ' 100 190 A ' + rx.toFixed(2) + ' 90 0 0 ' + term + ' 100 10 Z';
  }
  function draw(a) {
    var d = path(a);
    lit.setAttribute('d', d);
    clip.setAttribute('d', d);
    if (halo) halo.style.setProperty('--lit', illumination(a).toFixed(2));
  }

  function daysBetween(a, b) {
    return (Date.parse(b + 'T12:00:00Z') - Date.parse(a + 'T12:00:00Z')) / 86400000;
  }
  var ease = function (t) { return t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2; };

  /* Anime l'âge de la lune de `from` vers `to`, dans le sens du temps */
  function spin(to, days) {
    cancelAnimationFrame(raf);
    var from = age;
    var delta = ((to - from) % LUNAISON + LUNAISON) % LUNAISON;    // vers l'avant
    if (days < 0) delta -= LUNAISON;                                 // vers l'arrière
    if (Math.abs(days) >= LUNAISON) delta += days > 0 ? LUNAISON : -LUNAISON; // grand saut : un tour complet en plus
    if (reduced || Math.abs(delta) < 0.01) { age = to; draw(age); return Promise.resolve(); }
    var dur = Math.min(1800, 500 + Math.abs(delta) * 35);
    var t0 = performance.now();
    root.classList.add('is-spinning');
    return new Promise(function (done) {
      (function frame(now) {
        var t = Math.min(1, (now - t0) / dur);
        age = from + delta * ease(t);
        draw(age);
        if (t < 1) raf = requestAnimationFrame(frame);
        else { age = ((to % LUNAISON) + LUNAISON) % LUNAISON; root.classList.remove('is-spinning'); done(); }
      })(t0);
    });
  }

  function swap(doc) {
    document.querySelectorAll('[data-swap]').forEach(function (el) {
      var next = doc.querySelector('[data-swap="' + el.dataset.swap + '"]');
      if (!next) return;
      if (el.innerHTML !== next.innerHTML) {
        el.innerHTML = next.innerHTML;
        el.classList.remove('rise', 'is-swapped');
        void el.offsetWidth;
        el.classList.add('is-swapped');
      }
      el.hidden = next.hidden;
    });
    var nextSvg = doc.querySelector('[data-moon] svg');
    if (nextSvg) svg.setAttribute('aria-label', nextSvg.getAttribute('aria-label'));
    var nextToday = doc.querySelector('[data-moon-today]');
    if (today && nextToday) today.hidden = nextToday.hidden;
    document.title = doc.title;
  }

  function go(date, push) {
    var url = date ? form.action + '?date=' + encodeURIComponent(date) : form.action;
    var token = ++busy;
    root.classList.add('is-loading');
    return fetch(url, { headers: { 'X-Requested-With': 'fetch' } })
      .then(function (r) { if (!r.ok && r.status !== 400) throw new Error(r.status); return r.text(); })
      .then(function (html) {
        if (token !== busy) return;
        var doc = new DOMParser().parseFromString(html, 'text/html');
        var next = doc.querySelector('[data-moon]');
        var nextInput = doc.querySelector('[data-moon-form] input[type="date"]');
        root.classList.remove('is-loading');
        if (!next) { location.href = url; return; }
        var target = parseFloat(next.dataset.age) || 0;
        var newDate = nextInput ? nextInput.value : date;
        var days = currentDate && newDate ? daysBetween(currentDate, newDate) : 0;
        currentDate = newDate;
        if (input.value !== newDate && document.activeElement !== input) input.value = newDate;
        if (push) history.pushState({ date: newDate }, '', url);
        swap(doc);                     // le texte change pendant que la lune tourne
        return spin(target, days);
      })
      .catch(function () { location.href = url; });
  }

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    if (input.value) go(input.value, true);
  });
  input.addEventListener('change', function () {
    if (/^\d{4}-\d{2}-\d{2}$/.test(input.value) && input.value !== currentDate) go(input.value, true);
  });
  if (today) today.addEventListener('click', function (e) {
    e.preventDefault();
    e.stopPropagation();
    go('', true).then(function () { input.value = currentDate; });
  });
  window.addEventListener('popstate', function () {
    go(new URLSearchParams(location.search).get('date') || '', false);
  });

  /* Raccourcis : ← / → changent de jour, Maj+← / Maj+→ de semaine */
  document.addEventListener('keydown', function (e) {
    if (e.target.matches('input, textarea, select') || e.metaKey || e.ctrlKey || e.altKey) return;
    if (e.key !== 'ArrowLeft' && e.key !== 'ArrowRight') return;
    var step = (e.key === 'ArrowRight' ? 1 : -1) * (e.shiftKey ? 7 : 1);
    var d = new Date(Date.parse((currentDate || new Date().toISOString().slice(0, 10)) + 'T12:00:00Z') + step * 86400000);
    e.preventDefault();
    go(d.toISOString().slice(0, 10), true);
  });
})();
