/* WAY-BE Memory : associe chaque véhicule à sa part du trafic dans la ville.
   Config injectée par game.html dans <script id="game-config">. */
(function () {
  "use strict";

  const cfg = JSON.parse(document.getElementById("game-config").textContent);
  const mode = new URLSearchParams(location.search).get("mode") === "expert" ? "expert" : "classic";
  const reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  // type -> nom d'image du véhicule (car.jpg) et de la carte ville (chr_car.jpg)
  const IMG = { voiture: "car", velo: "cycle", pieton: "human", lourd: "truc" };
  const TYPES = Object.keys(IMG);
  const PREVIEW_MS = 3000;
  const FLIP_BACK_MS = 850;

  const $ = (id) => document.getElementById(id);
  const board = $("board"), toast = $("toast");
  const ui = {
    pairs: $("pairs"), moves: $("moves"), errors: $("errors"), time: $("time"),
    best: $("best"), progress: $("progress"),
  };
  const bestKey = `wb-memory-${cfg.prefix}-${mode}`;
  const store = {
    get(k) { try { return JSON.parse(localStorage.getItem(k)); } catch (e) { return null; } },
    set(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) {} },
  };

  let state;

  const src = (name) => `${cfg.static}${name}.webp`;
  const fmtTime = (s) => `${Math.floor(s / 60)}:${String(s % 60).padStart(2, "0")}`;
  const fmtPct = (n) => new Intl.NumberFormat("fr-BE", { maximumFractionDigits: 1 }).format(n);

  function shuffle(a) {
    for (let i = a.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [a[i], a[j]] = [a[j], a[i]];
    }
    return a;
  }

  function preload() {
    const names = ["back", ...TYPES.flatMap((t) => [IMG[t], `${cfg.prefix}_${IMG[t]}`])];
    return Promise.all(names.map((n) => new Promise((res) => {
      const img = new Image(); img.onload = img.onerror = res; img.src = src(n);
    })));
  }

  function showToast(text, ok, ms) {
    toast.textContent = text;
    toast.classList.toggle("toast--ok", !!ok);
    toast.classList.add("is-on");
    clearTimeout(showToast.t);
    if (ms !== 0) showToast.t = setTimeout(() => toast.classList.remove("is-on"), ms || 1100);
  }

  function bump(el, value) {
    el.textContent = value;
    el.parentElement.classList.remove("bump");
    el.classList.remove("bump");
    void el.offsetWidth;
    el.classList.add("bump");
  }

  function renderBest() {
    const b = store.get(bestKey);
    ui.best.textContent = b ? `${b.moves}c` : "–";
    ui.best.title = b ? `${b.stars} étoile(s), ${b.moves} coups, ${fmtTime(b.time)}` : "";
  }

  function makeCard(card, i) {
    const btn = document.createElement("button");
    btn.type = "button";
    btn.className = "card";
    btn.style.setProperty("--i", i);
    btn.dataset.type = card.type;
    btn.setAttribute("aria-label", "Carte cachée");
    btn.innerHTML =
      `<span class="card__shake"><span class="card__inner">` +
      `<span class="card__face card__face--back"><img src="${src("back")}" alt="" draggable="false"></span>` +
      `<span class="card__face card__face--front"><img src="${src(card.img)}" alt="" draggable="false"></span>` +
      `</span></span>`;
    btn.addEventListener("click", () => select(btn, card));
    return btn;
  }

  function setAll(flipped) {
    board.querySelectorAll(".card").forEach((c) => c.classList.toggle("is-flipped", flipped));
  }

  function newGame() {
    clearInterval(state && state.timer);
    clearTimeout(state && state.previewT);
    closeWin();
    state = {
      first: null, lock: true, moves: 0, errors: 0, pairs: 0, combo: 0,
      seconds: 0, timer: null, started: false, done: false,
    };
    ui.pairs.textContent = "0"; ui.moves.textContent = "0"; ui.errors.textContent = "0";
    ui.time.textContent = "0:00"; ui.progress.style.width = "0%";
    renderBest();
    const s = state; // les timers d'une ancienne partie ne touchent pas la nouvelle

    const deck = shuffle(TYPES.flatMap((t) => [
      { type: t, kind: "vehicule", img: IMG[t], label: cfg.labels[t] },
      { type: t, kind: "ville", img: `${cfg.prefix}_${IMG[t]}`, label: `${fmtPct(cfg.pct[t])} %` },
    ]));
    board.classList.remove("is-loading");
    board.innerHTML = "";
    deck.forEach((c, i) => board.appendChild(makeCard(c, i)));

    const dealMs = reduced ? 0 : 300 + deck.length * 30;
    if (mode === "expert") {
      $("mode-label").textContent = "Mode expert : aucun aperçu, à toi de jouer.";
      setTimeout(() => { s.lock = false; }, dealMs);
      return;
    }
    $("mode-label").textContent = "Mémorise les cartes, elles vont se retourner…";
    s.previewT = setTimeout(() => {
      if (s !== state) return;
      setAll(true);
      let left = Math.round(PREVIEW_MS / 1000);
      showToast(`Mémorise… ${left}`, false, 0);
      const cd = setInterval(() => {
        left -= 1;
        if (s !== state) { clearInterval(cd); return; }
        if (left > 0) { showToast(`Mémorise… ${left}`, false, 0); return; }
        clearInterval(cd);
        setAll(false);
        showToast("C'est parti !", true, 900);
        $("mode-label").textContent = "Associe chaque véhicule à sa part du trafic.";
        setTimeout(() => { s.lock = false; }, 600);
      }, 1000);
      s.previewT = cd;
    }, dealMs);
  }

  function startTimer() {
    if (state.started) return;
    state.started = true;
    state.timer = setInterval(() => {
      state.seconds += 1;
      ui.time.textContent = fmtTime(state.seconds);
    }, 1000);
  }

  function select(btn, card) {
    if (state.lock || state.done || btn.classList.contains("is-flipped")) return;
    startTimer();
    btn.classList.add("is-flipped");
    btn.setAttribute("aria-label", card.label);

    if (!state.first) { state.first = { btn, card }; return; }

    const a = state.first, b = { btn, card };
    state.first = null;
    state.moves += 1;
    bump(ui.moves, state.moves);

    if (a.card.type === b.card.type && a.card.kind !== b.card.kind) {
      state.pairs += 1;
      state.combo += 1;
      [a.btn, b.btn].forEach((el) => { el.classList.add("is-matched"); el.disabled = true; });
      bump(ui.pairs, state.pairs);
      ui.progress.style.width = `${(state.pairs / TYPES.length) * 100}%`;
      const combo = state.combo > 1 ? `  ·  combo x${state.combo}` : "";
      showToast(`${cfg.labels[card.type]} : ${fmtPct(cfg.pct[card.type])} %${combo}`, true, 1300);
      if (state.pairs === TYPES.length) finish();
    } else {
      state.lock = true;
      state.errors += 1;
      state.combo = 0;
      bump(ui.errors, state.errors);
      setTimeout(() => [a.btn, b.btn].forEach((el) => el.classList.add("is-wrong")), 350);
      setTimeout(() => {
        [a.btn, b.btn].forEach((el) => {
          el.classList.remove("is-flipped", "is-wrong");
          el.setAttribute("aria-label", "Carte cachée");
        });
        state.lock = false;
      }, FLIP_BACK_MS + 350);
    }
  }

  function starsFor(errors) {
    const limit = mode === "expert" ? [3, 6] : [1, 4];
    return errors <= limit[0] ? 3 : errors <= limit[1] ? 2 : 1;
  }

  function finish() {
    state.done = true;
    clearInterval(state.timer);
    const stars = starsFor(state.errors);
    const prev = store.get(bestKey);
    const better = !prev || state.moves < prev.moves || (state.moves === prev.moves && state.seconds < prev.time);
    if (better) store.set(bestKey, { moves: state.moves, time: state.seconds, stars });
    renderBest();

    $("win-title").textContent = stars === 3 ? "Parfait !" : stars === 2 ? "Bien joué !" : "Toutes trouvées !";
    $("win-moves").textContent = state.moves;
    $("win-errors").textContent = state.errors;
    $("win-time").textContent = fmtTime(state.seconds);
    $("win-record").textContent = better && prev ? "Nouveau record !" : better ? "Premier record enregistré" :
      `Record : ${prev.moves} coups en ${fmtTime(prev.time)}`;
    const starEls = $("stars").querySelectorAll("span");
    starEls.forEach((s, i) => { s.classList.toggle("on", i < stars); s.style.animation = "none"; void s.offsetWidth; s.style.animation = ""; });
    $("stars").setAttribute("aria-label", `${stars} étoile${stars > 1 ? "s" : ""} sur 3`);

    setTimeout(() => { openWin(); if (stars >= 2) confetti(); }, 900);
  }

  function openWin() {
    const w = $("win");
    w.hidden = false;
    requestAnimationFrame(() => requestAnimationFrame(() => w.classList.add("is-open")));
    $("win-again").focus({ preventScroll: true });
  }

  function closeWin() {
    const w = $("win");
    if (w.hidden) return;
    w.classList.remove("is-open");
    setTimeout(() => { w.hidden = true; }, 350);
  }

  function confetti() {
    if (reduced) return;
    const colors = ["#ff3ea5", "#39e1ff", "#ffd23f", "#b388ff", "#5dffb0"];
    const box = document.createElement("div");
    box.className = "confetti";
    for (let i = 0; i < 70; i++) {
      const p = document.createElement("i");
      p.style.left = `${Math.random() * 100}%`;
      p.style.background = colors[i % colors.length];
      p.style.setProperty("--x", `${(Math.random() - 0.5) * 240}px`);
      p.style.setProperty("--r", `${360 + Math.random() * 720}deg`);
      p.style.setProperty("--d", `${1.8 + Math.random() * 1.6}s`);
      p.style.animationDelay = `${Math.random() * 0.4}s`;
      box.appendChild(p);
    }
    document.body.appendChild(box);
    setTimeout(() => box.remove(), 4200);
  }

  $("restart").addEventListener("click", newGame);
  $("win-again").addEventListener("click", newGame);
  $("win").addEventListener("click", (e) => { if (e.target.id === "win") closeWin(); });
  document.addEventListener("keydown", (e) => { if (e.key === "Escape") closeWin(); });

  // Images déjà en cache si on vient de /chosegame (préchargées au survol) ; sinon on n'attend pas plus de 2,5 s
  Promise.race([preload(), new Promise((r) => setTimeout(r, 2500))]).then(newGame);
})();
