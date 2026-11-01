/* WAY-BE — mini lecteur MP3 Y2K : play/pause, titre défilant, position, piste suivante.
   Les MP3 (70–90 Mo) ne sont chargés qu'au premier play (preload="none"). */
(function () {
  'use strict';
  var root = document.querySelector('[data-player]');
  if (!root) return;
  function q(s) { return root.querySelector(s); }

  var audio = q('audio'), playBtn = q('[data-play]'), seek = q('[data-seek]'), timeEl = q('[data-time]'),
      statusEl = q('[data-status]'), marquee = q('[data-marquee]'), live = q('[data-live]');
  var tracks = [].map.call(root.querySelectorAll('[data-tracks] li'), function (li) {
    return { src: li.dataset.src, title: li.dataset.title, dur: +li.dataset.duration || 0 };
  });
  var cur = 0, loaded = false, dragging = false, pending = 0, skipPause = false, inView = false;
  var LABELS = { stop: 'STOP', load: 'LOAD…', play: 'PLAY', pause: 'PAUSE' };

  function fmt(t) { t = Math.max(0, Math.floor(t || 0)); var s = t % 60; return Math.floor(t / 60) + ':' + (s < 10 ? '0' : '') + s; }
  function dur() { return loaded && isFinite(audio.duration) && audio.duration > 0 ? audio.duration : tracks[cur].dur; }

  function setState(s) {
    root.dataset.state = s;
    statusEl.textContent = LABELS[s];
    playBtn.setAttribute('aria-label', s === 'play' || s === 'load' ? 'Pause' : 'Lecture');
  }
  function render(t) {
    var d = dur(), p = d ? Math.min(1, t / d) : 0;
    timeEl.textContent = fmt(t) + ' / ' + fmt(d);
    seek.value = Math.round(p * 1000);
    seek.style.setProperty('--p', p * 100 + '%');
    seek.setAttribute('aria-valuetext', fmt(t) + ' sur ' + fmt(d));
  }
  function show(announce) {
    var txt = (cur + 1) + '. ' + tracks[cur].title + '  ***  ';
    [].forEach.call(marquee.children, function (s) { s.textContent = txt; });
    if (announce) live.textContent = 'Piste ' + (cur + 1) + ' : ' + tracks[cur].title;
    render(0);
  }

  function play() {
    if (!loaded) { audio.src = tracks[cur].src; loaded = true; }
    if (audio.readyState < 3) setState('load');
    var p = audio.play();
    if (p && p.catch) p.catch(function (e) { if (e.name !== 'AbortError') setState('pause'); });
  }
  function toggle() { if (audio.paused) play(); else audio.pause(); }
  function next(autoplay) {
    var resume = autoplay === true || !audio.paused;
    if (!audio.paused) { skipPause = true; audio.pause(); }
    if (loaded) { audio.removeAttribute('src'); audio.load(); loaded = false; }
    cur = (cur + 1) % tracks.length;
    pending = 0;
    setState('stop');
    show(true);
    if (resume) play();
  }

  playBtn.addEventListener('click', toggle);
  q('[data-next]').addEventListener('click', next);

  audio.addEventListener('playing', function () { setState('play'); });
  audio.addEventListener('waiting', function () { if (!audio.paused) setState('load'); });
  audio.addEventListener('pause', function () { if (skipPause) { skipPause = false; return; } if (!audio.ended) setState('pause'); });
  audio.addEventListener('ended', function () { next(true); });
  audio.addEventListener('timeupdate', function () { if (!dragging) render(audio.currentTime); });
  audio.addEventListener('loadedmetadata', function () {
    if (pending) { audio.currentTime = pending; pending = 0; }
    render(audio.currentTime);
  });

  /* Barre de position : cliquable / déplaçable ; avant chargement, on mémorise la position voulue */
  seek.addEventListener('input', function () { dragging = true; render(seek.value / 1000 * dur()); });
  seek.addEventListener('change', function () {
    var t = seek.value / 1000 * dur();
    dragging = false;
    if (loaded && audio.readyState > 0) audio.currentTime = t; else pending = t;
    render(t);
  });

  /* Espace = lecture/pause dans le lecteur, ou sur la page quand le lecteur est visible (hors champs) */
  if ('IntersectionObserver' in window) {
    new IntersectionObserver(function (en) { inView = en[0].intersectionRatio >= 0.5; }, { threshold: [0, 0.5, 1] }).observe(root);
  }
  document.addEventListener('keydown', function (e) {
    if (e.key !== ' ' || e.repeat || e.ctrlKey || e.metaKey || e.altKey) return;
    var t = e.target;
    if (t.closest && t.closest('button, a, select, textarea, [contenteditable], input:not([type="range"])')) return;
    if (!root.contains(t) && !((t === document.body || t === document.documentElement) && inView)) return;
    e.preventDefault();
    toggle();
  });

  show();
})();
