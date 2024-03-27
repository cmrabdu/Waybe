import sqlite3

DATABASE_PATH = 'test2.db'
# Connexion à la base de données SQLite
connexion = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
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
            list1 = line.split(",")
            histoliste = list1[18:42]
            histoliste[-1] = histoliste[-1].strip("""""[']""")
            population = populationdico[list1[0]]

            # Vérification de l'existence de la rue dans la base de données et insertion si elle n'existe pas
            db.execute("SELECT rue_id FROM rue WHERE rue_id = ?", (list1[3],))
            existing_rue = db.fetchone()
            if existing_rue is None:
                db.execute("""INSERT INTO rue('rue_id','nom','code_postal')
                VALUES(?,?,?);""", (list1[3], list1[2], list1[1]))

            # Vérification de l'existence de la ville dans la base de données et insertion si elle n'existe pas
            db.execute("SELECT code_postal FROM ville WHERE code_postal = ?", (list1[1],))
            existing_ville = db.fetchone()
            if existing_ville is None:
                db.execute("""INSERT INTO ville('code_postal','nom','population')
                            VALUES(?,?,?);""", (list1[1], list1[0], population))

            # Insertion des données de vitesse dans la table "vitesse"
            for tranche in range(0, 24):
                db.execute(
                    "SELECT rue_id AND date AND tranche_de_vitesse FROM vitesse WHERE rue_id = ? AND date = ? AND tranche_de_vitesse = ?",
                    (list1[3], list1[4], tranches_par_5[tranche]))
                existing_vitesse = db.fetchone()
                if existing_vitesse is None:
                    db.execute("""INSERT INTO vitesse('rue_id','date','tranche_de_vitesse', 'proportion')
                    VALUES(?,?,?,?);""", (list1[3], list1[4], tranches_par_5[tranche], float(histoliste[tranche])))

            # Insertion des données de v85 dans la table "v85"
            db.execute("SELECT rue_id AND date FROM v85 WHERE rue_id = ? AND date = ?", (list1[3], list1[4]))
            existing_v85 = db.fetchone()
            if existing_v85 is None:
                db.execute("""INSERT INTO v85('rue_id','date','v85')
                VALUES(?,?,?);""", (list1[3], list1[4], list1[-1]))

            # Insertion des données de trafic dans la table "traffic"
            types_vehicules = ["lourd", "voiture", "velo", "pieton"]
            valeur_vehicules = list1[5:9]
            for select in range(0, 4):
                db.execute("SELECT rue_id AND date AND type_vehicule FROM traffic WHERE rue_id = ? AND date = ? AND type_vehicule = ?",
                    (list1[3], list1[4], types_vehicules[select]))
                existing_traffic = db.fetchone()
                if existing_traffic is None:
                    db.execute("""INSERT INTO traffic('rue_id','date','type_vehicule', 'nb_vehicules')
                    VALUES(?,?,?,?);""", (list1[3], list1[4], types_vehicules[select], valeur_vehicules[select]))
        start = 1

def abdu():
    db.execute("""SELECT DISTINCT strftime('%Y-%m-%d', date), SUM(nb_vehicules) FROM traffic GROUP BY strftime('%Y-%m-%d', date)""")
    return db.fetchall()

def all(x):
    if x == "nb_rues_par_ville":
        db.execute("""SELECT ville.nom, COUNT(rue_id) FROM rue JOIN ville on ville.code_postal = rue.code_postal GROUP BY ville.nom""")
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
        db.execute("""SELECT ville.nom, ville.population, SUM(nb_vehicules)/population FROM traffic JOIN rue on traffic.rue_id = rue.rue_id JOIN ville on rue.code_postal = ville.code_postal WHERE type_vehicule = 'velo' GROUP BY ville.nom ORDER BY SUM(nb_vehicules) DESC;""")
        return db.fetchall()
def requestsville(x):
    db.execute("""SELECT code_postal FROM ville WHERE nom = ?""", (x,))
    cprequest = db.fetchall()
    cprequest = cprequest[0][0]
    db.execute("""SELECT rue_id FROM rue WHERE rue.code_postal = ?""",(cprequest,))
    totallourd = 0
    totalvelo = 0
    totalpieton = 0
    totalvoiture = 0
    listeRI = db.fetchall()
    for i in range(len(listeRI)):
        db.execute("""SELECT SUM(nb_vehicules) FROM traffic WHERE traffic.rue_id = ? AND traffic.type_vehicule = 'lourd'""",(listeRI[i][0],))
        x = db.fetchall()
        totallourd = totallourd + x[0][0]
        db.execute("""SELECT SUM(nb_vehicules) FROM traffic WHERE traffic.rue_id = ? AND traffic.type_vehicule = 'pieton'""",(listeRI[i][0],))
        x = db.fetchall()
        totalpieton = totalpieton + x[0][0]
        db.execute("""SELECT SUM(nb_vehicules) FROM traffic WHERE traffic.rue_id = ? AND traffic.type_vehicule = 'voiture'""",(listeRI[i][0],))
        x = db.fetchall()
        totalvoiture = totalvoiture + x[0][0]
        db.execute("""SELECT SUM(nb_vehicules) FROM traffic WHERE traffic.rue_id = ? AND traffic.type_vehicule = 'velo'""",(listeRI[i][0],))
        x = db.fetchall()
        totalvelo = totalvelo + x[0][0]
    total = totalvelo + totallourd + totalpieton + totalvoiture
    totallourd = round((totallourd/total)*100, 2)
    totalpieton = round((totalpieton / total) * 100, 2)
    totalvoiture = round((totalvoiture / total) * 100, 2)
    totalvelo = round((totalvelo / total) * 100, 2)
    return "totallourd", totallourd, "totalpieton", totalpieton, "totalvoiture", totalvoiture, "totalvelo", totalvelo
def requestsrue(x, y):
    y = str(y)
    type = ['lourd', 'pieton', 'voiture', 'velo']
    db.execute("""SELECT code_postal FROM ville WHERE nom = ?""",(y,))
    #print(db.fetchall()[0][0])
    CP = db.fetchall()[0][0]
    db.execute("""SELECT rue_id FROM rue WHERE nom = ? AND code_postal = ?""",(x,CP))
    IDderue = db.fetchall()[0][0]
    stock = []
    total = []
    for i in range(7):
        for j in type:
            db.execute(f"""SELECT '{i}', type_vehicule, SUM(nb_vehicules) FROM traffic WHERE rue_id = ? AND CAST(strftime('%w', date) AS INTEGER) = ? AND type_vehicule = '{j}' """,(IDderue, i))
            stock.append(db.fetchall())
    for i in range(0, 28, 4):
        groupe = stock[i:i+4]
        x = 0
        for j in groupe:
            x = x + j[0][2]
        for j in groupe:
            yo = list(j[0])
            yo[2] = round(((yo[2] / x)*100), 2)
            total.append(yo)
    return total

def selectrequest():
    db.execute("""SELECT nom FROM ville""")
    return db.fetchall()

def selectruerequest(ville):
    db.execute("""SELECT rue.nom FROM rue JOIN ville ON rue.code_postal = ville.code_postal WHERE ville.nom = ?""",(ville,))
    return db.fetchall()

connexion.commit()