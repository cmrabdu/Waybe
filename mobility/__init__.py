from flask import Flask, render_template , request
import os
import sqlite3
from .table import all ,requestsville


app = Flask(__name__)



# Ensure the instance folder exists
try:
    os.makedirs(app.instance_path)
except OSError:
    pass


def obtenir_stats_villes():
    # Connexion à la base de données SQLite
    connexion = sqlite3.connect('test2.db')
    db = connexion.cursor()

    # Exécutez une requête pour sélectionner toutes les villes
    db.execute("SELECT COUNT(*) FROM ville;")
    nombre_de_villes = db.fetchone()[0]

    # Exécutez une autre requête pour obtenir les noms de toutes les villes
    db.execute("SELECT nom FROM ville;")
    noms_des_villes = db.fetchall()

    # Fermer la connexion à la base de données
    connexion.close()

    # Retourne les données récupérées
    return nombre_de_villes, noms_des_villes


# Routes
@app.route('/')
def home ():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html', HelloWorld='Hello World')


@app.route('/stats')
def stats():
    print("cc")
    result1  = all("nb_rues_par_ville")
    result2 = all("nbr_entreVille")
    result3 = all("nbr_entreVitesse")
    result4 = all("nbr_entreV85")
    result5 = all("nbr_entreTraffic")
    result6 = all("nbr_entreRue")
    result7 = all("cyclable")
    return render_template('stats.html', x=result1
                           , entreVille=result2, entreVitesse=result3, entreV85=result4,
                           entreTraffic=result5, entreRue=result6, qtt_velo=result7)

@app.route('/nextrequest')
def nextrequest():
   return  render_template ('nextrequest.html')
@app.route('/request', methods=['GET', 'POST'])
def request_handler():
    if request.method == 'POST':
        # Récupérer la valeur sélectionnée dans le sélecteur de ville
        ville = request.form['ville']
        # Faire quelque chose avec la valeur sélectionnée, comme l'afficher
        x = requestsville(ville)
        print (x)
        return render_template('nextrequest.html', ville_request=x)

    else:
        return render_template('request.html')



@app.route('/moon')
def moon():
    return render_template('moon.html', noah='hello world')

@app.route('/base')
def base():
    return render_template('base.html.html', noah='hello world')



if __name__ == "__main__":
    app.run(debug=True)
