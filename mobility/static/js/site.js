/* WAY-BE — comportements communs : menu mobile, nav au scroll, apparitions. */
(function () {
  'use strict';

  var nav = document.querySelector('[data-nav]');
  var toggle = document.querySelector('[data-nav-toggle]');

  if (nav && toggle) {
    toggle.addEventListener('click', function () {
      var open = nav.classList.toggle('is-open');
      toggle.setAttribute('aria-expanded', String(open));
      toggle.setAttribute('aria-label', open ? 'Fermer le menu' : 'Ouvrir le menu');
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && nav.classList.contains('is-open')) {
        nav.classList.remove('is-open');
        toggle.setAttribute('aria-expanded', 'false');
        toggle.focus();
      }
    });
  }

  if (nav) {
    var onScroll = function () { nav.classList.toggle('is-scrolled', window.scrollY > 8); };
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
  }

  /* ---------- Transitions entre pages ---------- */
  var root = document.documentElement;
  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function internalLink(a, e) {
    if (!a || e.defaultPrevented || e.button !== 0) return false;
    if (e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return false;
    if (a.target && a.target !== '_self') return false;
    if (a.hasAttribute('download') || a.origin !== location.origin) return false;
    if (a.pathname === location.pathname && a.search === location.search && a.hash) return false; // ancre locale
    if (a.pathname.indexOf('/static/') === 0) return false;
    return true;
  }

  /* Préchargement au survol : la page suivante arrive quasi instantanément */
  var prefetched = {};
  function prefetch(a) {
    if (!a || a.origin !== location.origin || prefetched[a.href] || a.pathname.indexOf('/static/') === 0) return;
    prefetched[a.href] = true;
    var l = document.createElement('link');
    l.rel = 'prefetch'; l.href = a.href;
    document.head.appendChild(l);
  }
  document.addEventListener('pointerover', function (e) { prefetch(e.target.closest && e.target.closest('a[href]')); }, { passive: true });
  document.addEventListener('focusin', function (e) { prefetch(e.target.closest && e.target.closest('a[href]')); });
  document.addEventListener('touchstart', function (e) { warm(e.target.closest && e.target.closest('a[href]')); }, { passive: true });

  /* iPhone : Safari ignore <link rel=prefetch>. On met les pages en cache HTTP avec fetch,
     au repos, pour que la navigation soit immédiate. Rien si l'économie de données est active. */
  function warm(a) {
    if (!a || a.origin !== location.origin || prefetched['f' + a.href] || a.pathname.indexOf('/static/') === 0) return;
    prefetched['f' + a.href] = true;
    try { fetch(a.href, { credentials: 'same-origin' }).catch(function () {}); } catch (err) {}
  }
  var conn = navigator.connection;
  if (!(conn && conn.saveData)) {
    var idle = window.requestIdleCallback || function (f) { return setTimeout(f, 800); };
    window.addEventListener('load', function () {
      idle(function () { document.querySelectorAll('.site-nav a[href]').forEach(warm); });
    });
  }

  /* Repli JS pour les navigateurs sans View Transitions entre documents */
  if (root.classList.contains('no-vt') && !reduceMotion) {
    document.addEventListener('click', function (e) {
      var a = e.target.closest && e.target.closest('a[href]');
      if (!internalLink(a, e)) return;
      e.preventDefault();
      root.classList.add('is-leaving');
      setTimeout(function () { location.href = a.href; }, 70);
    });
    document.addEventListener('submit', function (e) {
      if (!e.defaultPrevented) root.classList.add('is-leaving');
    });
    /* Retour arrière (bfcache) : ne pas réafficher une page restée effacée */
    window.addEventListener('pageshow', function () { root.classList.remove('is-leaving'); });
  }

  /* Apparition douce des éléments [data-reveal] */
  var items = document.querySelectorAll('[data-reveal]');
  if ('IntersectionObserver' in window && items.length) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          io.unobserve(entry.target);
        }
      });
    }, { rootMargin: '0px 0px 15% 0px', threshold: 0 });
    items.forEach(function (el) { io.observe(el); });
  } else {
    items.forEach(function (el) { el.classList.add('is-visible'); });
  }
})();
