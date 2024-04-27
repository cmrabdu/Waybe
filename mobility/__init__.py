from datetime import datetime
from .db import *
from flask import Flask, render_template, request

from .moon_utils import age, phase, calcul_moonpahse
from .table import all, requestsville, requestsrue, selectrequest, selectruerequest


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.root_path, 'test2.db'),
    )
    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    try:
        with app.app_context():
            init_data()
    except:
        pass
    @app.route('/')
    def home():
        return render_template('home.html')
    @app.route('/about')
    def about():
        return render_template('about.html', HelloWorld='Hello World')
    @app.route('/stats')
    def stats():
        result1 = all("nb_rues_par_ville")
        result2 = all("nbr_entreVille")
        result3 = all("nbr_entreVitesse")
        result4 = all("nbr_entreV85")
        result5 = all("nbr_entreTraffic")
        result6 = all("nbr_entreRue")
        result7 = all("cyclable")
        return render_template('stats.html', x=result1, entreVille=result2, entreVitesse=result3, entreV85=result4,
                               entreTraffic=result5, entreRue=result6, qtt_velo=result7)


    ville_info = None


    @app.route('/endrequest')
    def endrequest():
        return render_template('endrequest.html', )


    @app.route('/request', methods=['GET', 'POST'])
    def request_handler():
        global ville_info
        if request.method == 'POST':
            # Récupérer la valeur sélectionnée dans le sélecteur de ville
            ville_info = request.form['ville']
            # Faire quelque chose avec la valeur sélectionnée, comme l'afficher
            x = requestsville(ville_info)
            rue = selectruerequest(ville_info)
            return render_template('nextrequest.html', ville_request=x, rue=rue)

        else:
            ville = selectrequest()
            return render_template('request.html', ville=ville)

    @app.route('/nextrequest', methods=['GET', 'POST'])
    def nextrequest():
        rue = selectruerequest(ville_info)
        if request.method == 'POST':
            rue_info = request.form.get('rue')
            # Faire quelque chose avec la valeur sélectionnée, comme l'afficher
            x = requestsrue(rue_info, ville_info)
            return render_template('endrequest.html', x=x)
        else:
            return render_template('nextrequest.html', rue=rue)


    @app.route('/moon')
    def moon_phase_view():
        date_voulu = datetime(2004, 4, 23)  # datetime.now()  #date de aujourd'hui (peux mettre une date fixe aussi)
        date_reference = datetime(2000, 1, 5)

        age_lune = moon_utils.age(date_voulu, date_reference)
        phase_lune = moon_utils.phase(age_lune)

        # pour associer phases to images
        images = {
            'NEW_MOON': 'NEW_MOON.png',
            'WAXING_CRESCENT': 'WAXING_CRESCENT.png',
            'FIRST_QUARTER': 'FIRST_QUARTER.png',
            'WAXING_GIBBOUS': 'WAXING_GIBBOUS.png',
            'FULL_MOON': 'FULL_MOON.png',
            'WANING_GIBBOUS': 'WANING_GIBBOUS.png',
            'LAST_QUARTER': 'LAST_QUARTER.png',
            'WANING_CRESCENT': 'WANING_CRESCENT.png',
        }

        moon_image = images[phase_lune.name]

        return render_template('moon.html', age_lune=age_lune, moon_phase=phase_lune.name, moon_image=moon_image, smur=int(calcul_moonpahse()[1]),
                               sump=int(calcul_moonpahse()[0]))


    @app.route('/base')
    def base():
        return render_template('base.html', noah='hello world')

    @app.route('/game')
    def game():
        return render_template('game.html', noah='hello world')


    return app