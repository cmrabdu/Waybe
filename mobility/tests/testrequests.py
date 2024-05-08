from ..table import *
import os
import tempfile
import unittest
from flask import current_app
from mobility import create_app
filename = "mobility/tests/test.csv"
class TestUser(unittest.TestCase):

    def setUp(self):
        # generate a temporary file for the test db
        self.db_fd, self.db_path = tempfile.mkstemp()
        # create the testapp with the temp file for the test db
        self.app = create_app({'TESTING': True, 'DATABASE': self.db_path})
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.db = get_db()

        # read in SQL for populating test data
        with open(os.path.join(os.path.dirname(__file__), "schema_test.sql"), "rb") as f:
            self.db.executescript(f.read().decode("utf8"))
        file_path = os.path.join("tests/test.csv")
        cursor = self.db.cursor()
        start = 0
        with current_app.open_resource(file_path, "r") as f:
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
                                VALUES(?,?,?,?);""", (
                                list1[3], list1[4], tranches_par_5[tranche], float(histoliste[tranche])))

                        # Insertion des données de v85 dans la table "v85"
                        cursor.execute("SELECT rue_id AND date FROM v85 WHERE rue_id = ? AND date = ?",
                                       (list1[3], list1[4]))
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
                                VALUES(?,?,?,?);""",
                                               (list1[3], list1[4], types_vehicules[select], valeur_vehicules[select]))
                    start = 1

    def test_ville_selection(self):
        self.assertEqual(ville_selection("Liege")[0][0],
        ('totallourd', 100.0, 'totalpieton', 0.0, 'totalvoiture', 0.0, 'totalvelo', 0.0))

    def tearDown(self):
        # closing the db and cleaning the temp file
        self.db.commit()
        self.db.close()
        os.close(self.db_fd)
        os.unlink(self.db_path)
"""
    
    def test_selection_date(self):
        self.assertEqual(selection_date("Liege", "Avenue Rogier", "2024-01-05T16:00:00.000Z", "2024-01-05T18:00:00.000Z"), ['lourd', 30, 'voiture', 2, 'velo', 70, 'pieton', 20])
    
    def test_total_velo_for_date(self):
        self.assertEqual(total_velo_for_date()[0][0], "2023-12-16")
        self.assertEqual(total_velo_for_date()[1][0], "2023-12-20")
        self.assertEqual(total_velo_for_date()[2][0], "2024-01-05")
        self.assertEqual(total_velo_for_date()[0][1], 0)
        self.assertEqual(total_velo_for_date()[1][1], 0)
        self.assertEqual(total_velo_for_date()[2][1], 70)
    def test_entre_tableau(self):
        self.assertEqual(entre_tableau("vitesse")[0][0], 216)
        self.assertEqual(entre_tableau("v85")[0][0], 9)
        self.assertEqual(entre_tableau("traffic")[0][0], 36)
        self.assertEqual(entre_tableau("rue")[0][0], 3)
        self.assertEqual(entre_tableau("ville")[0][0], 2)

    def test_nb_rues_par_ville(self):
        self.assertEqual(nb_rues_par_ville()[0][0], "Bruxelles")
        self.assertEqual(nb_rues_par_ville()[1][0], "Liege")
    def test_cyclable(self):
        respond = ["Liege", 197325, 0.0, "Bruxelles", 1208542, 0.0]
        inc = 0
        for element in range(0,2):
            for element2 in range(0,3):
                self.assertEqual(cyclable()[element][element2], respond[inc])
                inc = inc + 1

    def test_rue_selection(self):
        respond = ["Bogaardenstraat", "Avenue Rogier"]
        for element, number in zip(respond, range(len(respond))):
            self.assertEqual(rue_selection("Bruxelles")[number][0], respond[number])
        self.assertEqual(rue_selection("Liege")[0][0], "Avenue Rogier")
"""




if __name__ == '__main__':
    unittest.main(verbosity=2)




