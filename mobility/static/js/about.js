/* WAY-BE — cartes équipe : retournement au clic, inclinaison 3D et reflet holo au survol. */
(function () {
  'use strict';

  var cards = Array.prototype.slice.call(document.querySelectorAll('[data-card]'));
  var flipAll = document.querySelector('[data-flip-all]');
  var canHover = window.matchMedia('(hover: hover) and (pointer: fine)').matches;
  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function setFlipped(card, on) {
    card.classList.toggle('is-flipped', on);
    card.setAttribute('aria-pressed', String(on));
  }

  function syncFlipAll() {
    if (!flipAll) return;
    var all = cards.every(function (c) { return c.classList.contains('is-flipped'); });
    flipAll.textContent = all ? 'Tout remettre de dos' : 'Tout retourner';
    flipAll.setAttribute('aria-pressed', String(all));
  }

  cards.forEach(function (card) {
    card.addEventListener('click', function () {
      setFlipped(card, !card.classList.contains('is-flipped'));
      syncFlipAll();
    });

    if (!canHover || reduced) return;

    card.addEventListener('pointermove', function (e) {
      var r = card.getBoundingClientRect();
      var x = (e.clientX - r.left) / r.width, y = (e.clientY - r.top) / r.height;
      card.classList.add('is-tilting');
      card.style.setProperty('--ry', ((x - 0.5) * 18).toFixed(2) + 'deg');
      card.style.setProperty('--rx', ((0.5 - y) * 14).toFixed(2) + 'deg');
      card.style.setProperty('--mx', (x * 100).toFixed(1) + '%');
      card.style.setProperty('--my', (y * 100).toFixed(1) + '%');
    });
    card.addEventListener('pointerleave', function () {
      card.classList.remove('is-tilting');
      card.style.setProperty('--rx', '0deg');
      card.style.setProperty('--ry', '0deg');
    });
  });

  if (flipAll) {
    flipAll.addEventListener('click', function () {
      var target = !cards.every(function (c) { return c.classList.contains('is-flipped'); });
      cards.forEach(function (c, i) {
        setTimeout(function () { setFlipped(c, target); }, reduced ? 0 : i * 90);
      });
      setTimeout(syncFlipAll, reduced ? 0 : cards.length * 90);
    });
  }
})();
