import sqlite3
import ast
import csv

# Connexion à la base de données SQLite
connexion = sqlite3.connect('test2.db')
db = connexion.cursor()

# Création de la table "ville" dans la base de données
db.execute("DROP TABLE IF EXISTS ville;")
db.execute(""" CREATE TABLE IF NOT EXISTS ville (
           code_postal INTEGER NOT NULL PRIMARY KEY ,
           nom TEXT NOT NULL,
           population INTEGER NOT NULL
           );""")

# Création de la table "rue" dans la base de données
db.execute("DROP TABLE IF EXISTS rue;")
db.execute("""CREATE TABLE IF NOT EXISTS rue (
    rue_id INTEGER NOT NULL PRIMARY KEY,
    nom TEXT NOT NULL,
    code_postal INTEGER NOT NULL,
    FOREIGN KEY (code_postal) REFERENCES ville(code_postal)
);""")

# Création de la table "vitesse" dans la base de données
db.execute("DROP TABLE IF EXISTS vitesse;")
db.execute("""CREATE TABLE IF NOT EXISTS vitesse (
    rue_id INTEGER NOT NULL,
    date TEXT NOT NULL, 
    tranche_de_vitesse INTEGER NOT NULL,
    proportion REAL NOT NULL,
    PRIMARY KEY (rue_id,tranche_de_vitesse,date),
    FOREIGN KEY(rue_id) REFERENCES rue(rue_id)
);""")

# Création de la table "v85" dans la base de données
db.execute("DROP TABLE IF EXISTS v85;")
db.execute("""CREATE TABLE IF NOT EXISTS v85 (
    rue_id INTEGER NOT NULL,
    date TEXT NOT NULL,
    v85 REAL,
    PRIMARY KEY(rue_id,date),
    FOREIGN KEY (rue_id) REFERENCES rue(rue_id)
);""")

# Création de la table "traffic" dans la base de données
db.execute("DROP TABLE IF EXISTS traffic;")
db.execute("""CREATE TABLE IF NOT EXISTS traffic (
    rue_id INTEGER NOT NULL,
    date TEXT NOT NULL,
    type_vehicule TEXT NOT NULL,
    nb_vehicules INTEGER NOT NULL,
    FOREIGN KEY (rue_id) REFERENCES rue(rue_id),
    PRIMARY KEY (rue_id,type_vehicule,date)
);""")

# Chemin vers le fichier CSV contenant les données
filename = "mobility/ugly.csv"
start = 0

# Ouverture et traitement du fichier CSV
with open(filename) as fichier:
    populationdico = {"Liege": 197325, "Bruxelles": 1208542, "Namur": 113174, "Charleroi": 203845, "Grobbendonk": 11442,
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
            list = line.split(",")
            histoliste = list[18:42]
            histoliste[-1] = histoliste[-1].strip("""""[']""")
            population = populationdico[list[0]]

            # Vérification de l'existence de la rue dans la base de données et insertion si elle n'existe pas
            db.execute("SELECT rue_id FROM rue WHERE rue_id = ?", (list[3],))
            existing_rue = db.fetchone()
            if existing_rue is None:
                db.execute("""INSERT INTO rue('rue_id','nom','code_postal')
                VALUES(?,?,?);""", (list[3], list[2], list[1]))

            # Vérification de l'existence de la ville dans la base de données et insertion si elle n'existe pas
            db.execute("SELECT code_postal FROM ville WHERE code_postal = ?", (list[1],))
            existing_ville = db.fetchone()
            if existing_ville is None:
                db.execute("""INSERT INTO ville('code_postal','nom','population')
                            VALUES(?,?,?);""", (list[1], list[0], population))

            # Insertion des données de vitesse dans la table "vitesse"
            for tranche in range(0, 24):
                db.execute(
                    "SELECT rue_id AND date AND tranche_de_vitesse FROM vitesse WHERE rue_id = ? AND date = ? AND tranche_de_vitesse = ?",
                    (list[3], list[4], tranches_par_5[tranche]))
                existing_vitesse = db.fetchone()
                if existing_vitesse is None:
                    db.execute("""INSERT INTO vitesse('rue_id','date','tranche_de_vitesse', 'proportion')
                    VALUES(?,?,?,?);""", (list[3], list[4], tranches_par_5[tranche], float(histoliste[tranche])))

            # Insertion des données de v85 dans la table "v85"
            db.execute("SELECT rue_id AND date FROM v85 WHERE rue_id = ? AND date = ?", (list[3], list[4]))
            existing_v85 = db.fetchone()
            if existing_v85 is None:
                db.execute("""INSERT INTO v85('rue_id','date','v85')
                VALUES(?,?,?);""", (list[3], list[4], list[-1]))

            # Insertion des données de trafic dans la table "traffic"
            types_vehicules = ["lourd", "voiture", "velo", "pieton"]
            valeur_vehicules = list[5:9]
            for select in range(0, 4):
                db.execute("SELECT rue_id AND date AND type_vehicule FROM traffic WHERE rue_id = ? AND date = ? AND type_vehicule = ?",
                    (list[3], list[4], types_vehicules[select]))
                existing_traffic = db.fetchone()
                if existing_traffic is None:
                    db.execute("""INSERT INTO traffic('rue_id','date','type_vehicule', 'nb_vehicules')
                    VALUES(?,?,?,?);""", (list[3], list[4], types_vehicules[select], valeur_vehicules[select]))
        start = 1


def all(x):
    if x == "nb_rues_par_ville":
        db.execute("""SELECT ville.nom, COUNT(rue.rue_id) FROM ville JOIN rue on ville.code_postal = rue.code_postal GROUP BY ville.nom""")
        return db.fetchall()
    if x == "nbr_entreVille":
        db.execute("""SELECT COUNT(*) FROM ville""")
        return db.fetchall()
    if x == "nbr_entreVitesse":
        db.execute("""SELECT COUNT(*) FROM vitesse""")
        return db.fetchall()
    if x == "nbr_entreV85":
        db.execute("""SELECT COUNT(*) FROM v85""")
        return db.fetchall()
    if x == "nbr_entreTraffic":
        db.execute("""SELECT COUNT(*) FROM traffic""")
        return db.fetchall()
    if x == "nbr_entreRue":
        db.execute("""SELECT COUNT(*) FROM rue""")
        return db.fetchall()
    if x == "nb_rues_par_ville":
        db.execute("""SELECT ville.nom, COUNT(rue.rue_id) FROM ville JOIN rue on ville.code_postal = rue.code_postal GROUP BY ville.nom""")
        return db.fetchall()
    if x == "cyclable":
        db.execute("""SELECT ville.nom, ville.population, SUM(nb_vehicules)/population FROM traffic JOIN rue on traffic.rue_id = rue.rue_id JOIN ville on rue.code_postal = ville.code_postal WHERE type_vehicule = 'velo' GROUP BY ville.nom""")
        return db.fetchall()

connexion.commit()