/* WAY-BE — habillage « web 2000 » : compteur de visites, livre d'or,
   barre d'état façon IE, traînée d'étincelles. Purement décoratif :
   le site fonctionne à l'identique sans ce fichier. */
(function () {
  'use strict';

  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var finePointer = window.matchMedia('(pointer: fine)').matches;

  function store(key, fallback) {
    try { var v = localStorage.getItem(key); return v === null ? fallback : v; } catch (e) { return fallback; }
  }
  function save(key, val) { try { localStorage.setItem(key, val); } catch (e) {} }

  /* ---------- Compteur de visites LCD ---------- */
  var counter = document.querySelector('[data-counter]');
  if (counter) {
    var visits = parseInt(store('wb-visits', '0'), 10) || 0;
    var counted = true;
    try { counted = !!sessionStorage.getItem('wb-counted'); sessionStorage.setItem('wb-counted', '1'); } catch (e) {}
    if (!counted) { visits += 1; save('wb-visits', String(visits)); }
    /* base « historique » qui grimpe doucement avec les jours depuis la mise en ligne */
    var days = Math.max(0, Math.floor((Date.now() - Date.UTC(2024, 4, 1)) / 864e5));
    var n = String(13370 + days * 7 + visits).padStart(7, '0').slice(-7);
    counter.setAttribute('aria-label', String(Number(n)));
    counter.innerHTML = n.split('').map(function (c) { return '<span>' + c + '</span>'; }).join('');
  }

  /* ---------- Livre d'or (clin d'œil) ---------- */
  var book = document.getElementById('guestbook');
  var openBtn = document.querySelector('[data-guestbook-open]');
  if (book && openBtn && typeof book.showModal === 'function') {
    openBtn.hidden = false;
    openBtn.addEventListener('click', function () { book.showModal(); });
    book.querySelectorAll('[data-guestbook-close]').forEach(function (b) {
      b.addEventListener('click', function () { book.close(); });
    });
    book.addEventListener('click', function (e) { if (e.target === book) book.close(); });
  }

  /* ---------- Barre d'état : « Ouverture de la page… » + progression XP ---------- */
  var statusText = document.querySelector('[data-status-text]');
  var statusBar = document.querySelector('[data-status-bar]');
  var timer = null;

  function progress(label, done) {
    if (!statusText || !statusBar) return;
    clearInterval(timer);
    statusText.textContent = label;
    if (reduce) { statusBar.style.setProperty('--p', done ? '0%' : '60%'); if (done) statusText.textContent = 'Terminé'; return; }
    var p = 0;
    timer = setInterval(function () {
      p = Math.min(100, p + (done ? 18 : 9) * Math.random() + 4);
      statusBar.style.setProperty('--p', p + '%');
      if (p >= 100 && done) {
        clearInterval(timer);
        statusText.textContent = 'Terminé';
        setTimeout(function () { statusBar.style.setProperty('--p', '0%'); }, 400);
      }
      if (!done && p >= 92) clearInterval(timer);
    }, 70);
  }

  progress('Chargement de la page ' + location.pathname + '…', true);

  document.addEventListener('pointerover', function (e) {
    var a = e.target.closest && e.target.closest('a[href]');
    if (statusText && a && !timer) statusText.textContent = a.href;
  }, { passive: true });
  document.addEventListener('pointerout', function (e) {
    var a = e.target.closest && e.target.closest('a[href]');
    if (statusText && a && !timer) statusText.textContent = 'Terminé';
  }, { passive: true });
  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('a[href]');
    if (!a || a.target === '_blank' || a.origin !== location.origin || e.metaKey || e.ctrlKey) return;
    if (a.pathname === location.pathname && a.hash) return;
    progress('Ouverture de la page ' + a.href + '…', false);
  });
  document.addEventListener('submit', function () { progress('Envoi de la requête…', false); });
  window.addEventListener('pageshow', function (e) { if (e.persisted) progress('Terminé', true); });
  /* une fois chargé, le timer redevient null pour réactiver l'aperçu des liens */
  setTimeout(function () { clearInterval(timer); timer = null; }, 1600);

  /* ---------- Traînée d'étincelles (souris uniquement, mouvement autorisé) ---------- */
  if (!reduce && finePointer) {
    var colors = ['#ff3ea5', '#39e1ff', '#b388ff', '#ffc61a'];
    var last = 0, live = 0, i = 0;
    document.addEventListener('pointermove', function (e) {
      if (e.pointerType !== 'mouse') return;
      var now = performance.now();
      if (now - last < 45 || live > 14) return;
      last = now; live++; i++;
      var s = document.createElement('span');
      s.className = 'spark';
      s.style.left = e.clientX + 'px';
      s.style.top = e.clientY + 'px';
      s.style.setProperty('--c', colors[i % colors.length]);
      s.style.setProperty('--dx', (Math.random() * 16 - 8).toFixed(1) + 'px');
      if (i % 3 === 0) { s.style.width = s.style.height = '8px'; }
      s.addEventListener('animationend', function () { s.remove(); live--; });
      document.body.appendChild(s);
    }, { passive: true });
  }
})();
