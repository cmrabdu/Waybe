from datetime import datetime
from .db import *
from flask import Flask, render_template, request, jsonify

from . import moon_utils
from flask import redirect, url_for
from . import table as T


date_voulu = None
def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('WAYBE_SECRET_KEY', 'dev'),
        DATABASE=os.environ.get('WAYBE_DB', os.path.join(app.root_path, 'test2.db')),
        MAX_CONTENT_LENGTH=16 * 1024,  # aucun formulaire du site n'envoie plus que quelques octets
    )
    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    # La base n'est (re)construite depuis le CSV que si elle est vide :
    # avant, elle était effacée puis recréée à chaque démarrage et à chaque rechargement du serveur.
    try:
        with app.app_context():
            try:
                deja_remplie = get_db().execute("SELECT 1 FROM ville LIMIT 1").fetchone() is not None
            except Exception:
                deja_remplie = False
            if not deja_remplie:
                init_data()
    except Exception:
        pass

    # Assets statiques : URL versionnée (?v=date de modif) + cache long côté navigateur.
    # Les pages ne re-téléchargent plus CSS/JS/images à chaque navigation, mais toute modif est vue tout de suite.
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 31536000

    @app.url_defaults
    def _static_version(endpoint, values):
        if endpoint == 'static' and values.get('filename') and 'v' not in values:
            try:
                values['v'] = int(os.path.getmtime(os.path.join(app.static_folder, values['filename'])))
            except OSError:
                pass
    # --- Garde-fous production ---------------------------------------------
    # Limite de débit simple par IP (en mémoire, par worker) : 120 pages / minute.
    # Les fichiers statiques ne comptent pas. Suffisant pour une vitrine.
    import time
    from collections import defaultdict, deque
    _hits = defaultdict(deque)
    RATE, WINDOW = int(os.environ.get('WAYBE_RATE_PER_MIN', 120)), 60.0

    @app.before_request
    def _rate_limit():
        if request.path.startswith('/static/') or request.path == '/__livereload' or app.testing:
            return None
        ip = request.headers.get('X-Forwarded-For', request.remote_addr or '').split(',')[0].strip()
        now = time.monotonic()
        q = _hits[ip]
        while q and now - q[0] > WINDOW:
            q.popleft()
        if len(q) >= RATE:
            return ('Trop de requêtes, réessaie dans une minute.', 429, {'Retry-After': '60'})
        q.append(now)
        if len(_hits) > 5000:  # pas de croissance mémoire infinie
            for k in [k for k, v in _hits.items() if not v or now - v[-1] > WINDOW]:
                del _hits[k]
        return None

    @app.after_request
    def _security_headers(resp):
        resp.headers.setdefault('X-Content-Type-Options', 'nosniff')
        resp.headers.setdefault('X-Frame-Options', 'DENY')
        resp.headers.setdefault('Referrer-Policy', 'strict-origin-when-cross-origin')
        resp.headers.setdefault('Permissions-Policy', 'camera=(), microphone=(), geolocation=()')
        # Tout est servi par le site lui-même : aucune ressource externe autorisée.
        resp.headers.setdefault('Content-Security-Policy',
            "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data:; font-src 'self'; media-src 'self'; connect-src 'self'; "
            "frame-ancestors 'none'; base-uri 'self'; form-action 'self'"
            + ("; report-uri /__csp-report" if app.debug else ""))
        return resp

    if app.debug:
        @app.route('/__csp-report', methods=['POST'])
        def __csp_report():
            app.logger.warning('CSP VIOLATION %s', request.get_data(as_text=True)[:400])
            return ('', 204)

    _home_cache = {}

    @app.route('/')
    def home():
        if 'stats' not in _home_cache:
            try:
                db = get_db()
                _home_cache['stats'] = {
                    'villes': db.execute("SELECT COUNT(*) FROM ville").fetchone()[0],
                    'rues': db.execute("SELECT COUNT(*) FROM rue").fetchone()[0],
                    'velos': int(db.execute("SELECT COALESCE(SUM(nb_vehicules), 0) FROM traffic "
                                            "WHERE type_vehicule = 'velo'").fetchone()[0]),
                }
            except Exception:
                _home_cache['stats'] = None
        return render_template('home.html', stats=_home_cache['stats'])
    TEAM = [
        {'id': 'noah', 'nom': 'Noah Moussaoui', 'pseudo': 'Noah'},
        {'id': 'abdu', 'nom': 'Abdullah Camur', 'pseudo': 'Abdu'},
        {'id': 'houari', 'nom': 'Houari Boumeddien Benkechida', 'pseudo': 'Houari'},
        {'id': 'guigui', 'nom': 'Guillaume Sablon', 'pseudo': 'Guigui'},
    ]

    @app.route('/about')
    def about():
        return render_template('about.html', team=TEAM)

    # ----- Jeu (agent B) -----
    @app.route('/chosegame', methods=['GET', 'POST'])
    def chosegame():
        if request.method == 'POST':
            return redirect(url_for('game', ville=request.form.get('ville', '')))
        villes = [dict(v, label=T.display_city(v['nom']),
                       prefix=T.CARD_PREFIX.get(v['nom'].lower()))
                  for v in T.villes()]
        return render_template('chosegame.html', villes=villes,
                               error=request.args.get('error'))

    @app.route('/game')
    def game():
        v = T.ville(request.args.get('ville'))
        prefix = T.CARD_PREFIX.get(v['nom'].lower()) if v else None
        if not prefix:
            return redirect(url_for('chosegame', error='1') if request.args.get('ville')
                            else url_for('chosegame'))
        rep = T.repartition_ville(v['code_postal'])
        return render_template('game.html', ville=v, label=T.display_city(v['nom']),
                               prefix=prefix, pct=rep['pct'], labels=T.LABELS, types=T.TYPES)

    # ----- Données (agent B) -----
    _stats_cache = {}

    @app.route('/stats')
    def stats():
        if 'data' not in _stats_cache:
            _stats_cache['data'] = T.stats_globales()
        return render_template('stats.html', s=_stats_cache['data'], labels=T.LABELS, types=T.TYPES)

    @app.route('/request', methods=['GET', 'POST'])
    def request_handler():
        if request.method == 'POST':  # ancien formulaire -> étape 2
            return redirect(url_for('nextrequest', ville=request.form.get('ville', '')))
        villes = [dict(v, label=T.display_city(v['nom']), rep=T.repartition_ville(v['code_postal']))
                  for v in T.villes()]
        return render_template('request.html', villes=villes, labels=T.LABELS, types=T.TYPES,
                               error=request.args.get('error'))

    def _render_step2(v, error=None, form=None, status=200):
        rues = T.rues(v['code_postal'])
        return render_template('nextrequest.html', ville=v, label=T.display_city(v['nom']),
                               rues=rues, rep=T.repartition_ville(v['code_postal']),
                               labels=T.LABELS, types=T.TYPES, error=error,
                               form=form or {}), status

    @app.route('/nextrequest', methods=['GET', 'POST'])
    def nextrequest():
        if request.method == 'POST':  # ancien formulaire -> résultats
            return redirect(url_for('endrequest', **request.form.to_dict()))
        v = T.ville(request.args.get('ville'))
        if not v:
            return redirect(url_for('request_handler', error='ville') if request.args.get('ville')
                            else url_for('request_handler'))
        return _render_step2(v, form=request.args)

    @app.route('/endrequest')
    def endrequest():
        args = request.args
        r = T.rue(args.get('rue'))
        if not r:
            v = T.ville(args.get('ville'))
            if v:
                return _render_step2(v, error="Choisis une rue dans la liste.", form=args, status=400)
            return redirect(url_for('request_handler'))
        try:
            debut, fin = T.parse_bounds(args.get('start_date') or r['debut'],
                                        args.get('end_date') or r['fin'],
                                        args.get('heure_debut'), args.get('heure_fin'))
        except ValueError as e:
            return _render_step2(T.ville(r['ville']), error=str(e), form=args, status=400)
        data = T.analyse_rue(r['rue_id'], debut, fin)
        return render_template('endrequest.html', rue=r, ville_label=T.display_city(r['ville']),
                               d=data, debut=debut, fin=fin, labels=T.LABELS, types=T.TYPES,
                               args=args)

    # ----- Lune (agent A) -----
    _moon_cache = {}

    def _render_moon(date_str=None, template='moon.html'):
        error = None
        date_voulu = datetime.now()
        if date_str:
            try:
                date_voulu = datetime.strptime(date_str, '%Y-%m-%d').replace(hour=21)
            except ValueError:
                error = "Date invalide : utilise le format AAAA-MM-JJ."
        if 'velos' not in _moon_cache:
            try:
                _moon_cache['velos'] = moon_utils.velos_par_phase()
            except Exception:
                _moon_cache['velos'] = None
        return render_template(template, lune=moon_utils.infos_lune(date_voulu),
                               cycle=moon_utils.cycle_miniatures(), velos=_moon_cache['velos'],
                               date_str=date_voulu.strftime('%Y-%m-%d'), error=error,
                               is_today=not date_str or error is not None), (400 if error else 200)

    @app.route('/chosemoon', methods=['GET', 'POST'])
    def chosemoon():
        if request.method == 'POST':
            return redirect(url_for('moon_phase_view', date=request.form.get('start_date', '')))
        return _render_moon(request.args.get('date'), template='chosemoon.html')

    @app.route('/moon')
    def moon_phase_view():
        return _render_moon(request.args.get('date'))

    @app.route('/base')
    def base():
        return render_template('base.html', noah='hello world')

    # --- Live reload (dev only): le navigateur se recharge dès qu'un fichier change ---
    if app.debug:
        def _latest_mtime():
            latest = 0.0
            for folder in (app.template_folder, app.static_folder):
                root_dir = os.path.join(app.root_path, folder) if not os.path.isabs(folder) else folder
                for dirpath, _, files in os.walk(root_dir):
                    for f in files:
                        if f.endswith(('.html', '.css', '.js', '.svg', '.png', '.jpg', '.webp')):
                            try:
                                latest = max(latest, os.path.getmtime(os.path.join(dirpath, f)))
                            except OSError:
                                pass
            return latest

        @app.route('/__livereload')
        def __livereload():
            return jsonify(v=_latest_mtime())

        _snippet = (b"<script>(()=>{let v=null;setInterval(async()=>{try{const r=await fetch('/__livereload');"
                    b"const j=await r.json();if(v!==null&&j.v!==v)location.reload();v=j.v}catch(e){}},1000)})()</script>")

        @app.after_request
        def __inject_livereload(resp):
            if resp.mimetype == 'text/html' and not resp.direct_passthrough:
                resp.set_data(resp.get_data() + _snippet)
            return resp

    return app