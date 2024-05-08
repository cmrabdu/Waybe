

from .db import get_db

DATABASE_PATH = 'test2.db'


def total_velo_for_date(): #le total de vélo par jour
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""SELECT DISTINCT strftime('%Y-%m-%d', date), SUM(nb_vehicules) 
    FROM traffic WHERE type_vehicule = "velo" 
    GROUP BY strftime('%Y-%m-%d', date)""")
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
    cursor.execute("""SELECT ville.nom, ville.population, round(SUM(nb_vehicules)/population, 2) 
    FROM traffic 
    JOIN rue on traffic.rue_id = rue.rue_id 
    JOIN ville on rue.code_postal = ville.code_postal 
    WHERE type_vehicule = 'velo' 
    GROUP BY ville.nom 
    ORDER BY SUM(nb_vehicules) DESC;""")
    return cursor.fetchall()

def rue_selection(ville):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""SELECT rue.nom FROM rue 
    JOIN ville ON rue.code_postal = ville.code_postal 
    WHERE ville.nom = ?""",(ville,))
    return cursor.fetchall()

def ville_selection(nom_ville):
    db = get_db()
    cursor = db.cursor()
    type = ["lourd", "pieton", "voiture", "velo"]
    lst = []
    lst_retour = []
    cursor.execute("""SELECT SUM(traffic.nb_vehicules) FROM traffic 
    JOIN rue ON traffic.rue_id = rue.rue_id
    JOIN ville on rue.code_postal = ville.code_postal
    WHERE ville.nom = ?""",(nom_ville,))
    total_vehicule = cursor.fetchall()[0][0]
    for element in type:
        cursor.execute("""SELECT SUM(traffic.nb_vehicules) FROM traffic 
        JOIN rue ON traffic.rue_id = rue.rue_id
        JOIN ville on rue.code_postal = ville.code_postal
        WHERE ville.nom = ? AND type_vehicule = ?""",(nom_ville, element))
        x = cursor.fetchall()
        lst.append(x)
    z = 0
    for shit in lst:
        y = round((shit[0][0]/total_vehicule)*100, 2)
        lst_retour.append(type[z])
        lst_retour.append(y)
        z = z + 1
    return lst_retour
#Fonction optimisée au dessus ^^^^^^^^
'''def ville_selection(x):
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
'''
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


