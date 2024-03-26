from flask import Flask, render_template , request
import os
import sqlite3
from .table  import *
from datetime import datetime
from .moon_utils import age, phase


app = Flask(__name__)
def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    if test_config:
        app.config.from_mapping(test_config)
    else:
        app.config.from_mapping(
            SECRET_KEY='dev',
            DATABASE=os.path.join(app.root_path, 'poudlard.sqlite'),
        )



# Ensure the instance folder exists
try:
    os.makedirs(app.instance_path)
except OSError:
    pass




# Routes
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
    return render_template('stats.html', x=result1
                           , entreVille=result2, entreVitesse=result3, entreV85=result4,
                           entreTraffic=result5, entreRue=result6, qtt_velo=result7)

ville_info=None
@app.route('/endrequest')
def endrequest():
    return render_template('endrequest.html',)


@app.route('/request', methods=['GET', 'POST'])
def request_handler():
    global ville_info
    if request.method == 'POST':
        # Récupérer la valeur sélectionnée dans le sélecteur de ville
        ville_info = request.form['ville']
        # Faire quelque chose avec la valeur sélectionnée, comme l'afficher
        x = requestsville(ville_info)
        rue = selectruerequest(ville_info)
        return render_template('nextrequest.html', ville_request=x,rue=rue)

    else:
        ville = selectrequest()
        return render_template('request.html',ville=ville)




@app.route('/nextrequest', methods=['GET', 'POST'])
def nextrequest():
    rue = selectruerequest(ville_info)
    if request.method == 'POST':
        rue_info = request.form.get('rue')
        # Faire quelque chose avec la valeur sélectionnée, comme l'afficher
        x = requestsrue(rue_info,ville_info)
        return render_template('endrequest.html',x=x)
    else:
        return render_template('nextrequest.html', rue=rue )




@app.route('/moon')
def moon_phase_view():
    date_voulu = datetime(2005, 7, 5) #datetime.now()  #date de aujourd'hui (peux mettre une date fixe aussi)
    date_reference = datetime(2000, 1, 5) #date de pleine lune connue -> bon, pas correcte car erreur dans le code, mais ça marche donc osef (temporairement)

    age_lune = moon_utils.age(date_voulu, date_reference)
    phase_lune = moon_utils.phase(age_lune)

    #pour associer phases to images
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

    return render_template('moon.html', age_lune=age_lune, moon_phase=phase_lune.name, moon_image=moon_image)

@app.route('/base')
def base():
    return render_template('base.html.html', noah='hello world')



if __name__ == "__main__":
    app.run(debug=True)
