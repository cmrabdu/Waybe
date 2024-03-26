import os
import sqlite3
from .table import all ,requestsville,requestsrue,selectrequest,selectruerequest
from flask import Flask, render_template
import webbrowser


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


    from . import city
    app.register_blueprint(city.bp)

    app.add_url_rule('/', endpoint='index')

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass


    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

<<<<<<< mobility/__init__.py
# Ensure the instance folder exists
try:
    os.makedirs(app.instance_path)
except OSError:
    pass


=======
    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Exécutez une autre requête pour obtenir les noms de toutes les villes
    db.execute("SELECT nom FROM ville;")
    noms_des_villes = db.fetchall()

    # Fermer la connexion à la base de données
    connexion.close()

    # Retourne les données récupérées
    return nombre_de_villes, noms_des_villes
>>>>>>> mobility/__init__.py


# Routes
@app.route('/')
def home():
    return render_template('home.html')

    @app.route('/')
    def base():
        return render_template('base.html',base='bonjour')

    @app.route('/about')
    def about():
        return render_template('about.html', about='Bonjour tout le monde')

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


@app.route('/endrequest')
def endrequest():
    return render_template('endrequest.html')

ville_info=None
@app.route('/request', methods=['GET', 'POST'])
def request_handler():
    global ville_info
    if request.method == 'POST':
        # Récupérer la valeur sélectionnée dans le sélecteur de ville
        ville_info = request.form['ville']
        #print(request.form['ville'])
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
        #print(rue_info)
        # Faire quelque chose avec la valeur sélectionnée, comme l'afficher
        x = requestsrue(rue_info,ville_info)
        return render_template('endrequest.html',x=x)
    else:
        return render_template('nextrequest.html', rue=rue )


    @app.route('/request')
    def request():
        return render_template('request.html', data='bonjour le monde')


@app.route('/moon')
def moon():
    return render_template('moon.html', noah='hello world')

@app.route('/base')
def base():
    return render_template('base.html.html', noah='hello world')



if __name__ == "__main__":
    app.run(debug=True)
