(function () {
  'use strict';

  function normalizePath(pathname) {
    if (!pathname) return '/';
    var path = pathname.replace(/\/index\.html$/i, '/').replace(/\.html$/i, '');
    if (path.length > 1 && path.endsWith('/')) path = path.slice(0, -1);
    return path || '/';
  }

  function setActiveLinks() {
    var current = normalizePath(window.location.pathname);
    document.querySelectorAll('.wb-nav__links a[href]').forEach(function (link) {
      link.classList.remove('is-active');
      link.removeAttribute('aria-current');
      var href = link.getAttribute('href');
      if (!href || href.startsWith('http') || href.startsWith('#')) return;
      try {
        var url = new URL(href, window.location.href);
        var linkPath = normalizePath(url.pathname);
        if (linkPath === current || (current !== '/' && current.endsWith(linkPath))) {
          link.classList.add('is-active');
          link.setAttribute('aria-current', 'page');
        }
      } catch (e) { /* ignore */ }
    });
  }

  function initMenu() {
    var toggle = document.querySelector('.wb-nav__toggle');
    var links = document.querySelector('.wb-nav__links');
    if (!toggle || !links) return;

    function close() {
      links.classList.remove('is-open');
      toggle.setAttribute('aria-expanded', 'false');
    }

    toggle.addEventListener('click', function (e) {
      e.stopPropagation();
      var open = links.classList.toggle('is-open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });

    links.querySelectorAll('a').forEach(function (a) {
      a.addEventListener('click', close);
    });

    document.addEventListener('click', function (e) {
      if (!links.classList.contains('is-open')) return;
      if (links.contains(e.target) || toggle.contains(e.target)) return;
      close();
    });

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') close();
    });

    window.addEventListener('resize', function () {
      if (window.matchMedia('(min-width: 769px)').matches) close();
    });
  }

  function init() {
    setActiveLinks();
    initMenu();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
