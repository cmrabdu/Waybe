import sqlite3
import os
from flask import current_app, g
filename = os.path.join('ugly.csv')
def get_db():

    """Returns the database connection. Create the connection if needed.

    Returns:
        db: The db connection to be used for SQL functions
    """
    # g is the shorthand for "globals" and allows registering available in the whole Flask app
    if 'db' not in g:
        # If it's not there, let's create the db connection
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES)
        # Instead of getting "tuple" out of queries, we'll get dictionaries of column->value
        g.db.row_factory = sqlite3.Row
    print("db")
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()






def init_data():
    db = get_db()
    cursor = db.cursor()
    print("test1")
    try:
        print("testok")
        # Création de la table "ville" dans la base de données
        cursor.execute("DROP TABLE IF EXISTS ville;")
        cursor.execute(""" CREATE TABLE IF NOT EXISTS ville (
                   code_postal INTEGER NOT NULL PRIMARY KEY ,
                   nom TEXT NOT NULL,
                   population INTEGER NOT NULL
                   );""")

        # Création de la table "rue" dans la base de données
        cursor.execute("DROP TABLE IF EXISTS rue;")
        cursor.execute("""CREATE TABLE IF NOT EXISTS rue (
            rue_id INTEGER NOT NULL PRIMARY KEY,
            nom TEXT NOT NULL,
            code_postal INTEGER NOT NULL,
            FOREIGN KEY (code_postal) REFERENCES ville(code_postal)
        );""")

        # Création de la table "vitesse" dans la base de données
        cursor.execute("DROP TABLE IF EXISTS vitesse;")
        cursor.execute("""CREATE TABLE IF NOT EXISTS vitesse (
            rue_id INTEGER NOT NULL,
            date TEXT NOT NULL, 
            tranche_de_vitesse INTEGER NOT NULL,
            proportion REAL NOT NULL,
            PRIMARY KEY (rue_id,tranche_de_vitesse,date),
            FOREIGN KEY(rue_id) REFERENCES rue(rue_id)
        );""")

        # Création de la table "v85" dans la base de données
        cursor.execute("DROP TABLE IF EXISTS v85;")
        cursor.execute("""CREATE TABLE IF NOT EXISTS v85 (
            rue_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            v85 REAL,
            PRIMARY KEY(rue_id,date),
            FOREIGN KEY (rue_id) REFERENCES rue(rue_id)
        );""")

        # Création de la table "traffic" dans la base de données
        cursor.execute("DROP TABLE IF EXISTS traffic;")
        cursor.execute("""CREATE TABLE IF NOT EXISTS traffic (
            rue_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            type_vehicule TEXT NOT NULL,
            nb_vehicules INTEGER NOT NULL,
            FOREIGN KEY (rue_id) REFERENCES rue(rue_id),
            PRIMARY KEY (rue_id,type_vehicule,date)
        );""")
        start = 0
        # Ouverture et traitement du fichier CSV
        with open(filename) as fichier:
            populationdico = {"Liege": 197325, "Bruxelles": 1208542, "Namur": 113174, "Charleroi": 203845,
                              "Grobbendonk": 11442,
                              "Herzele": 19000, "Jambes": 20125, "Courtrai": 78841, "beveren": 48000}
            tranches_par_5 = [
                "0-5", "5-10", "10-15", "15-20", "20-25",
                "25-30", "30-35", "35-40", "40-45", "45-50",
                "50-55", "55-60", "60-65", "65-70", "70-75",
                "75-80", "80-85", "85-90", "90-95", "95-100",
                "100-105", "105-110", "110-115", "115-120"
            ]
            for line in fichier:
                if start != 0:
                    list1 = line.split(",")
                    histoliste = list1[18:42]
                    histoliste[-1] = histoliste[-1].strip("""""[']""")
                    population = populationdico[list1[0]]

                    # Vérification de l'existence de la rue dans la base de données et insertion si elle n'existe pas
                    cursor.execute("SELECT rue_id FROM rue WHERE rue_id = ?", (list1[3],))
                    existing_rue = cursor.fetchone()
                    if existing_rue is None:
                        cursor.execute("""INSERT INTO rue('rue_id','nom','code_postal')
                        VALUES(?,?,?);""", (list1[3], list1[2], list1[1]))

                    # Vérification de l'existence de la ville dans la base de données et insertion si elle n'existe pas
                    cursor.execute("SELECT code_postal FROM ville WHERE code_postal = ?", (list1[1],))
                    existing_ville = cursor.fetchone()
                    if existing_ville is None:
                        cursor.execute("""INSERT INTO ville('code_postal','nom','population')
                                    VALUES(?,?,?);""", (list1[1], list1[0], population))

                    # Insertion des données de vitesse dans la table "vitesse"
                    for tranche in range(0, 24):
                        cursor.execute(
                            "SELECT rue_id AND date AND tranche_de_vitesse FROM vitesse WHERE rue_id = ? AND date = ? AND tranche_de_vitesse = ?",
                            (list1[3], list1[4], tranches_par_5[tranche]))
                        existing_vitesse = cursor.fetchone()
                        if existing_vitesse is None:
                            cursor.execute("""INSERT INTO vitesse('rue_id','date','tranche_de_vitesse', 'proportion')
                            VALUES(?,?,?,?);""", (list1[3], list1[4], tranches_par_5[tranche], float(histoliste[tranche])))

                    # Insertion des données de v85 dans la table "v85"
                    cursor.execute("SELECT rue_id AND date FROM v85 WHERE rue_id = ? AND date = ?", (list1[3], list1[4]))
                    existing_v85 = cursor.fetchone()
                    if existing_v85 is None:
                        cursor.execute("""INSERT INTO v85('rue_id','date','v85')
                        VALUES(?,?,?);""", (list1[3], list1[4], list1[-1]))

                    # Insertion des données de trafic dans la table "traffic"
                    types_vehicules = ["lourd", "voiture", "velo", "pieton"]
                    valeur_vehicules = list1[5:9]
                    for select in range(0, 4):
                        cursor.execute(
                            "SELECT rue_id AND date AND type_vehicule FROM traffic WHERE rue_id = ? AND date = ? AND type_vehicule = ?",
                            (list1[3], list1[4], types_vehicules[select]))
                        existing_traffic = cursor.fetchone()
                        if existing_traffic is None:
                            cursor.execute("""INSERT INTO traffic('rue_id','date','type_vehicule', 'nb_vehicules')
                            VALUES(?,?,?,?);""", (list1[3], list1[4], types_vehicules[select], valeur_vehicules[select]))
                start = 1
        db.commit()
    except Exception as e:
        pass
    finally:
        db.close()
        cursor.close()



