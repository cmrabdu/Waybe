

from .db import get_db

DATABASE_PATH = 'test2.db'


def total_velo_for_date():
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        """SELECT DISTINCT strftime('%Y-%m-%d', date), SUM(nb_vehicules) FROM traffic WHERE type_vehicule = "velo" GROUP BY strftime('%Y-%m-%d', date)""")
    return cursor.fetchall()


def entre_tableau(x):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(f"""SELECT COUNT(*) FROM '{x}' """)
    return cursor.fetchall()


def nb_rues_par_ville():
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        """SELECT ville.nom, COUNT(rue_id) FROM rue JOIN ville on ville.code_postal = rue.code_postal GROUP BY ville.nom""")
    return cursor.fetchall()


def cyclable():
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        """SELECT ville.nom, ville.population, round(SUM(nb_vehicules)/population, 2) FROM traffic JOIN rue on traffic.rue_id = rue.rue_id JOIN ville on rue.code_postal = ville.code_postal WHERE type_vehicule = 'velo' GROUP BY ville.nom ORDER BY SUM(nb_vehicules) DESC;""")
    return cursor.fetchall()


def interval_total(city, street, date_start, date_end):
    db = get_db()
    cursor = db.cursor()
    return_list = []
    type = ['lourd', 'pieton', 'voiture', 'velo']
    for types in type:
        cursor.execute(
            """SELECT SUM(traffic.nb_vehicules) FROM traffic JOIN rue ON rue.rue_id = traffic.rue_id JOIN ville ON rue.code_postal = ville.code_postal WHERE ville.nom = ? AND rue.nom = ? AND traffic.type_vehicule = ? AND date BETWEEN strftime('%Y-%m-%d', date) = ? AND strftime('%Y-%m-%d', date) = ? """,
            (city, street, types, date_start, date_end))
        return_list.append(cursor.fetchall())
    return return_list


def rue_selection(ville):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""SELECT rue.nom FROM rue JOIN ville ON rue.code_postal = ville.code_postal WHERE ville.nom = ?""",
                   (ville,))
    return cursor.fetchall()


def ville_selection(x):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""SELECT code_postal FROM ville WHERE nom = ?""", (x,))
    cprequest = cursor.fetchall()
    cprequest = cprequest[0][0]
    cursor.execute("""SELECT rue_id FROM rue WHERE rue.code_postal = ?""", (cprequest,))
    totallourd = 0
    totalvelo = 0
    totalpieton = 0
    totalvoiture = 0
    listeRI = cursor.fetchall()
    for i in range(len(listeRI)):
        cursor.execute(
            """SELECT SUM(nb_vehicules) FROM traffic WHERE traffic.rue_id = ? AND traffic.type_vehicule = 'lourd'""",
            (listeRI[i][0],))
        x = cursor.fetchall()
        totallourd = totallourd + x[0][0]
        cursor.execute(
            """SELECT SUM(nb_vehicules) FROM traffic WHERE traffic.rue_id = ? AND traffic.type_vehicule = 'pieton'""",
            (listeRI[i][0],))
        x = cursor.fetchall()
        totalpieton = totalpieton + x[0][0]
        cursor.execute(
            """SELECT SUM(nb_vehicules) FROM traffic WHERE traffic.rue_id = ? AND traffic.type_vehicule = 'voiture'""",
            (listeRI[i][0],))
        x = cursor.fetchall()
        totalvoiture = totalvoiture + x[0][0]
        cursor.execute(
            """SELECT SUM(nb_vehicules) FROM traffic WHERE traffic.rue_id = ? AND traffic.type_vehicule = 'velo'""",
            (listeRI[i][0],))
        x = cursor.fetchall()
        totalvelo = totalvelo + x[0][0]
    total = totalvelo + totallourd + totalpieton + totalvoiture
    totallourd = round((totallourd / total) * 100, 2)
    totalpieton = round((totalpieton / total) * 100, 2)
    totalvoiture = round((totalvoiture / total) * 100, 2)
    totalvelo = round((totalvelo / total) * 100, 2)
    return "totallourd", totallourd, "totalpieton", totalpieton, "totalvoiture", totalvoiture, "totalvelo", totalvelo


def stats_rue(nom_rue, nom_ville):
    db = get_db()
    cursor = db.cursor()
    nom_ville = str(nom_ville)
    type = ['lourd', 'pieton', 'voiture', 'velo']
    cursor.execute("""SELECT code_postal FROM ville WHERE nom = ?""", (nom_ville,))
    omp = cursor.fetchall()
    CP = omp[0][0]
    cursor.execute("""SELECT rue_id FROM rue WHERE nom = ? AND code_postal = ?""", (nom_rue, CP))
    IDderue = cursor.fetchall()[0][0]
    stock = []
    total = []
    for i in range(7):
        for j in type:
            cursor.execute(
                f"""SELECT '{i}', type_vehicule, SUM(nb_vehicules) FROM traffic WHERE rue_id = ? AND CAST(strftime('%w', date) AS INTEGER) = ? AND type_vehicule = '{j}' """,
                (IDderue, i))
            stock.append(cursor.fetchall())
    # nbr vehicule separe
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


def lst_ville():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""SELECT nom FROM ville""")
    return cursor.fetchall()


def lst_rue(ville):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""SELECT rue.nom FROM rue JOIN ville ON rue.code_postal = ville.code_postal WHERE ville.nom = ?""",
                   (ville,))
    return cursor.fetchall()

def selection_date(nom_ville, nom_rue, date_debut, date_fin):
    print(date_debut,date_fin)
    db = get_db()
    cursor = db.cursor()
    lstV = ["lourd", "voiture", "velo", "pieton"]  # Correction des éléments de la liste
    listeFinal = []
    for element in lstV:
        cursor.execute("""SELECT traffic.type_vehicule, SUM(traffic.nb_vehicules) FROM traffic 
            JOIN rue ON rue.rue_id = traffic.rue_id 
            JOIN ville ON ville.code_postal = rue.code_postal 
            WHERE traffic.type_vehicule = ? AND ville.nom = ? AND rue.nom = ? AND traffic.date BETWEEN ? AND ?""",
            (element, nom_ville, nom_rue, date_debut, date_fin))
        # Ajout des résultats à la liste finale
        get = cursor.fetchall()[0]
        get1 = get[0]
        get2 = get[1]
        listeFinal.append(get1)
        listeFinal.append(get2)
    return listeFinal



