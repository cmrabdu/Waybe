from flask import Flask, render_template
import os
import sqlite3

app = Flask(__name__)

# Configuration
app.config.from_mapping(
    SECRET_KEY='dev',
    DATABASE=os.path.join(app.root_path, 'poudlard.sqlite'),
)

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
def base():
    return render_template('base.html')


@app.route('/about')
def about():
    return render_template('about.html', HelloWorld='Hello World')


@app.route('/stats')
def stats():
    return render_template('stats.html', stats='hello world')


@app.route('/request')
def request():
    return render_template('request.html', abdullah='hello world')


if __name__ == "__main__":
    app.run(debug=True)
