from db import get_db
DATABASE_PATH = 'test2.db'
# Connexion à la base de données SQLite
# Chemin vers le fichier CSV contenant les données





def abdu():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""SELECT DISTINCT strftime('%Y-%m-%d', date), SUM(nb_vehicules) FROM traffic GROUP BY strftime('%Y-%m-%d', date)""")
    return cursor.fetchall()


def all(x):
    db = get_db()
    cursor = db.cursor()
    if x == "nb_rues_par_ville":
        cursor.execute("""SELECT ville.nom, COUNT(rue_id) FROM rue JOIN ville on ville.code_postal = rue.code_postal GROUP BY ville.nom""")
        return cursor.fetchall()
    if x == "nbr_entreVille":
        cursor.execute("""SELECT COUNT(*) FROM ville""")
        return db.fetchall()
    if x == "nbr_entreVitesse":
        cursor.execute("""SELECT COUNT(*) FROM vitesse""")
        return db.fetchall()
    if x == "nbr_entreV85":
        cursor.execute("""SELECT COUNT(*) FROM v85""")
        return db.fetchall()
    if x == "nbr_entreTraffic":
        cursor.execute("""SELECT COUNT(*) FROM traffic""")
        return db.fetchall()
    if x == "nbr_entreRue":
        cursor.execute("""SELECT COUNT(*) FROM rue""")
        return db.fetchall()
    if x == "nb_rues_par_ville":
        cursor.execute(
            """SELECT ville.nom, COUNT(rue.rue_id) FROM ville JOIN rue on ville.code_postal = rue.code_postal GROUP BY ville.nom""")
        return db.fetchall()
    if x == "cyclable":
        cursor.execute(
            """SELECT ville.nom, ville.population, round(SUM(nb_vehicules)/population, 2) FROM traffic JOIN rue on traffic.rue_id = rue.rue_id JOIN ville on rue.code_postal = ville.code_postal WHERE type_vehicule = 'velo' GROUP BY ville.nom ORDER BY SUM(nb_vehicules) DESC;""")
        return db.fetchall()


def requestsville(x):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""SELECT code_postal FROM ville WHERE nom = ?""", (x,))
    cprequest = db.fetchall()
    cprequest = cprequest[0][0]
    cursor.execute("""SELECT rue_id FROM rue WHERE rue.code_postal = ?""", (cprequest,))
    totallourd = 0
    totalvelo = 0
    totalpieton = 0
    totalvoiture = 0
    listeRI = db.fetchall()
    for i in range(len(listeRI)):
        cursor.execute(
            """SELECT SUM(nb_vehicules) FROM traffic WHERE traffic.rue_id = ? AND traffic.type_vehicule = 'lourd'""",
            (listeRI[i][0],))
        x = db.fetchall()
        totallourd = totallourd + x[0][0]
        cursor.execute(
            """SELECT SUM(nb_vehicules) FROM traffic WHERE traffic.rue_id = ? AND traffic.type_vehicule = 'pieton'""",
            (listeRI[i][0],))
        x = db.fetchall()
        totalpieton = totalpieton + x[0][0]
        cursor.execute(
            """SELECT SUM(nb_vehicules) FROM traffic WHERE traffic.rue_id = ? AND traffic.type_vehicule = 'voiture'""",
            (listeRI[i][0],))
        x = db.fetchall()
        totalvoiture = totalvoiture + x[0][0]
        cursor.execute(
            """SELECT SUM(nb_vehicules) FROM traffic WHERE traffic.rue_id = ? AND traffic.type_vehicule = 'velo'""",
            (listeRI[i][0],))
        x = db.fetchall()
        totalvelo = totalvelo + x[0][0]
    total = totalvelo + totallourd + totalpieton + totalvoiture
    totallourd = round((totallourd / total) * 100, 2)
    totalpieton = round((totalpieton / total) * 100, 2)
    totalvoiture = round((totalvoiture / total) * 100, 2)
    totalvelo = round((totalvelo / total) * 100, 2)
    return "totallourd", totallourd, "totalpieton", totalpieton, "totalvoiture", totalvoiture, "totalvelo", totalvelo


def requestsrue(x, y):
    db = get_db()
    cursor = db.cursor()
    y = str(y)
    type = ['lourd', 'pieton', 'voiture', 'velo']
    cursor.execute("""SELECT code_postal FROM ville WHERE nom = ?""", (y,))
    # print(db.fetchall()[0][0])
    CP = db.fetchall()[0][0]
    cursor.execute("""SELECT rue_id FROM rue WHERE nom = ? AND code_postal = ?""", (x, CP))
    IDderue = db.fetchall()[0][0]
    stock = []
    total = []
    for i in range(7):
        for j in type:
            cursor.execute(
                f"""SELECT '{i}', type_vehicule, SUM(nb_vehicules) FROM traffic WHERE rue_id = ? AND CAST(strftime('%w', date) AS INTEGER) = ? AND type_vehicule = '{j}' """,
                (IDderue, i))
            stock.append(db.fetchall())

    for i in range(0, 28, 4):
        groupe = stock[i:i + 4]
        x = 0
        for j in groupe:
            x = x + j[0][2]
        if x == 0:
            total.append(list(j[0]))
        else:
            for j in groupe:
                yo = list(j[0])
                yo[2] = round(((yo[2] / x) * 100), 2)
                total.append(yo)
    return total


def selectrequest():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""SELECT nom FROM ville""")
    return db.fetchall()


def selectruerequest(ville):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""SELECT rue.nom FROM rue JOIN ville ON rue.code_postal = ville.code_postal WHERE ville.nom = ?""",
               (ville,))
    return db.fetchall()


