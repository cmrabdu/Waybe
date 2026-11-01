"""Requêtes SQL sur les données Telraam (test2.db).

Toutes les requêtes sont paramétrées. Les fonctions « historiques » (utilisées
par les tests de 2024) sont conservées en bas du fichier, réécrites proprement.
"""
from datetime import datetime

from .db import get_db

# Ordre d'affichage et libellés des types de véhicules
TYPES = ("voiture", "velo", "pieton", "lourd")
LABELS = {
    "voiture": "Voitures",
    "velo": "Vélos",
    "pieton": "Piétons",
    "lourd": "Poids lourds",
}
# Tables autorisées pour les comptages (jamais de nom de table venant de l'utilisateur)
TABLES = ("ville", "rue", "traffic", "vitesse", "v85")

# Préfixe des images de cartes du jeu, par ville (clé en minuscules)
CARD_PREFIX = {
    "bruxelles": "bx",
    "charleroi": "chr",
    "courtrai": "cou",
    "beveren": "bev",
    "grobbendonk": "gro",
    "herzele": "her",
    "jambes": "jmb",
    "liege": "lie",
    "namur": "nam",
}

ISO_FMT = "%Y-%m-%dT%H:%M:%S.000Z"


def _rows(sql, params=()):
    return get_db().execute(sql, params).fetchall()


def _one(sql, params=()):
    return get_db().execute(sql, params).fetchone()


def display_city(nom):
    """« beveren » -> « Beveren » (les noms sont stockés tels quels)."""
    return nom[:1].upper() + nom[1:] if nom else nom


# ---------------------------------------------------------------------------
# Villes et rues
# ---------------------------------------------------------------------------

def villes():
    """Liste des villes avec population et nombre de rues équipées."""
    return [dict(r) for r in _rows(
        """SELECT v.nom, v.code_postal, v.population, COUNT(r.rue_id) AS nb_rues
           FROM ville v LEFT JOIN rue r ON r.code_postal = v.code_postal
           GROUP BY v.code_postal ORDER BY v.nom COLLATE NOCASE""")]


def ville(nom):
    """Une ville par son nom (insensible à la casse), ou None."""
    if not nom:
        return None
    row = _one("""SELECT nom, code_postal, population FROM ville
                  WHERE nom = ? COLLATE NOCASE""", (nom.strip(),))
    return dict(row) if row else None


def rues(code_postal):
    """Rues d'une ville avec leur période de mesure disponible."""
    return [dict(r) for r in _rows(
        """SELECT r.rue_id, r.nom,
                  substr(MIN(t.date), 1, 10) AS debut,
                  substr(MAX(t.date), 1, 10) AS fin
           FROM rue r LEFT JOIN traffic t ON t.rue_id = r.rue_id
           WHERE r.code_postal = ?
           GROUP BY r.rue_id ORDER BY r.nom COLLATE NOCASE""", (code_postal,))]


def rue(rue_id):
    """Une rue (avec sa ville) par identifiant, ou None."""
    try:
        rue_id = int(rue_id)
    except (TypeError, ValueError):
        return None
    row = _one("""SELECT r.rue_id, r.nom, v.nom AS ville, v.code_postal,
                         substr(MIN(t.date), 1, 10) AS debut,
                         substr(MAX(t.date), 1, 10) AS fin
                  FROM rue r JOIN ville v ON v.code_postal = r.code_postal
                  LEFT JOIN traffic t ON t.rue_id = r.rue_id
                  WHERE r.rue_id = ? GROUP BY r.rue_id""", (rue_id,))
    return dict(row) if row and row["rue_id"] is not None else None


def periode_globale():
    row = _one("SELECT substr(MIN(date), 1, 10), substr(MAX(date), 1, 10) FROM traffic")
    return (row[0], row[1]) if row else (None, None)


# ---------------------------------------------------------------------------
# Agrégats
# ---------------------------------------------------------------------------

def _repartition(rows):
    """[(type, total)] -> {totaux, pourcentages, total} dans l'ordre de TYPES."""
    totaux = {t: 0.0 for t in TYPES}
    for t, s in rows:
        if t in totaux:
            totaux[t] = float(s or 0)
    total = sum(totaux.values())
    pct = {t: (round(v / total * 100, 2) if total else 0.0) for t, v in totaux.items()}
    return {"totaux": {t: round(v) for t, v in totaux.items()}, "pct": pct, "total": round(total)}


def repartition_ville(code_postal):
    """Part de chaque type de véhicule dans une ville (une seule requête)."""
    return _repartition(_rows(
        """SELECT t.type_vehicule, SUM(t.nb_vehicules)
           FROM traffic t JOIN rue r ON r.rue_id = t.rue_id
           WHERE r.code_postal = ? GROUP BY t.type_vehicule""", (code_postal,)))


def parse_bounds(start_date, end_date, heure_debut=None, heure_fin=None):
    """Construit les bornes ISO à partir du formulaire.

    Renvoie (debut, fin) au format des données, ou lève ValueError avec un
    message lisible.
    """
    try:
        d1 = datetime.strptime((start_date or "").strip(), "%Y-%m-%d")
        d2 = datetime.strptime((end_date or "").strip(), "%Y-%m-%d")
    except ValueError:
        raise ValueError("Dates invalides : utilise le format AAAA-MM-JJ.")
    try:
        h1 = datetime.strptime((heure_debut or "00:00").strip() or "00:00", "%H:%M")
        h2 = datetime.strptime((heure_fin or "23:59").strip() or "23:59", "%H:%M")
    except ValueError:
        raise ValueError("Heures invalides : utilise le format HH:MM.")
    debut = d1.replace(hour=h1.hour, minute=h1.minute)
    fin = d2.replace(hour=h2.hour, minute=h2.minute, second=59)
    if fin < debut:
        raise ValueError("La fin de la période est avant le début.")
    return debut.strftime(ISO_FMT), fin.strftime(ISO_FMT)


def analyse_rue(rue_id, debut, fin):
    """Tout ce qu'il faut pour la page de résultats d'une rue sur une période."""
    params = (rue_id, debut, fin)
    where = "WHERE rue_id = ? AND date BETWEEN ? AND ?"

    rep = _repartition(_rows(
        f"SELECT type_vehicule, SUM(nb_vehicules) FROM traffic {where} GROUP BY type_vehicule",
        params))

    # Série temporelle : par heure si période courte (<= 3 jours), sinon par jour
    span_days = (datetime.strptime(fin, ISO_FMT) - datetime.strptime(debut, ISO_FMT)).days
    par_heure = span_days < 3
    bucket = "substr(date, 1, 13)" if par_heure else "substr(date, 1, 10)"
    serie_rows = _rows(
        f"""SELECT {bucket} AS b, type_vehicule, SUM(nb_vehicules)
            FROM traffic {where} GROUP BY b, type_vehicule ORDER BY b""", params)
    buckets = sorted({r[0] for r in serie_rows})
    index = {b: i for i, b in enumerate(buckets)}
    serie = {t: [0] * len(buckets) for t in TYPES}
    for b, t, s in serie_rows:
        if t in serie:
            serie[t][index[b]] = round(s or 0)
    labels = [b.replace("T", " ") + "h" if par_heure else b for b in buckets]

    # Profil horaire moyen (heure UTC des données)
    prof_rows = _rows(
        f"""SELECT CAST(substr(date, 12, 2) AS INTEGER) AS h, type_vehicule, AVG(nb_vehicules)
            FROM traffic {where} GROUP BY h, type_vehicule""", params)
    profil = {t: [0] * 24 for t in TYPES}
    for h, t, a in prof_rows:
        if t in profil and 0 <= h < 24:
            profil[t][h] = round(a or 0, 1)

    v85 = _one(
        f"""SELECT ROUND(AVG(v85), 1), ROUND(MAX(v85), 1) FROM v85
            {where} AND v85 <> '' AND v85 IS NOT NULL""", params)

    heure_pointe = None
    totals_h = [sum(profil[t][h] for t in TYPES) for h in range(24)]
    if any(totals_h):
        heure_pointe = max(range(24), key=lambda h: totals_h[h])

    return {
        "repartition": rep,
        "serie": {"labels": labels, "data": serie, "par_heure": par_heure},
        "profil": profil,
        "v85_moy": v85[0] if v85 else None,
        "v85_max": v85[1] if v85 else None,
        "heure_pointe": heure_pointe,
        "nb_mesures": len(buckets),
    }


def stats_globales():
    """Données de la page Stats."""
    counts = {t: _one(f"SELECT COUNT(*) FROM {t}")[0] for t in TABLES}  # noms whitelistés

    rep = _repartition(_rows("SELECT type_vehicule, SUM(nb_vehicules) FROM traffic GROUP BY type_vehicule"))

    par_ville_rows = _rows(
        """SELECT v.nom, v.population, t.type_vehicule, SUM(t.nb_vehicules)
           FROM traffic t JOIN rue r ON r.rue_id = t.rue_id
           JOIN ville v ON v.code_postal = r.code_postal
           GROUP BY v.code_postal, t.type_vehicule""")
    par_ville = {}
    for nom, pop, t, s in par_ville_rows:
        v = par_ville.setdefault(nom, {"nom": display_city(nom), "population": pop,
                                       **{k: 0 for k in TYPES}})
        if t in TYPES:
            v[t] = round(s or 0)
    for v in par_ville.values():
        tot = sum(v[k] for k in TYPES)
        v["total"] = tot
        v["pct_velo"] = round(v["velo"] / tot * 100, 1) if tot else 0
        v["pct_voiture"] = round(v["voiture"] / tot * 100, 1) if tot else 0
        v["velo_par_hab"] = round(v["velo"] / v["population"], 2) if v["population"] else 0
    villes_list = sorted(par_ville.values(), key=lambda v: v["pct_velo"], reverse=True)

    # Profil horaire moyen tous capteurs confondus
    profil = {t: [0] * 24 for t in TYPES}
    for h, t, a in _rows(
            """SELECT CAST(substr(date, 12, 2) AS INTEGER), type_vehicule, AVG(nb_vehicules)
               FROM traffic GROUP BY 1, 2"""):
        if t in profil and 0 <= h < 24:
            profil[t][h] = round(a or 0, 1)

    # Jour de la semaine (0 = dimanche en SQLite) -> lundi en premier
    semaine = {t: [0] * 7 for t in TYPES}
    for d, t, a in _rows(
            """SELECT CAST(strftime('%w', substr(date, 1, 19)) AS INTEGER), type_vehicule,
                      AVG(nb_vehicules)
               FROM traffic GROUP BY 1, 2"""):
        if t in semaine and d is not None:
            semaine[t][(d + 6) % 7] = round(a or 0, 1)

    top_rues = [dict(r) for r in _rows(
        """SELECT r.nom, v.nom AS ville, r.rue_id, ROUND(SUM(t.nb_vehicules)) AS total
           FROM traffic t JOIN rue r ON r.rue_id = t.rue_id
           JOIN ville v ON v.code_postal = r.code_postal
           WHERE t.type_vehicule = 'velo'
           GROUP BY r.rue_id ORDER BY total DESC LIMIT 5""")]
    for r in top_rues:
        r["ville"] = display_city(r["ville"])

    v85_ville = [(display_city(n), a) for n, a in _rows(
        """SELECT v.nom, ROUND(AVG(s.v85), 1)
           FROM v85 s JOIN rue r ON r.rue_id = s.rue_id
           JOIN ville v ON v.code_postal = r.code_postal
           WHERE s.v85 <> '' AND s.v85 IS NOT NULL
           GROUP BY v.code_postal ORDER BY 2 DESC""")]

    debut, fin = periode_globale()
    return {
        "counts": counts,
        "repartition": rep,
        "villes": villes_list,
        "profil": profil,
        "semaine": semaine,
        "top_rues": top_rues,
        "v85_ville": v85_ville,
        "debut": debut,
        "fin": fin,
    }


# ---------------------------------------------------------------------------
# Fonctions historiques (API de 2024, gardées pour les tests)
# ---------------------------------------------------------------------------

def total_velo_for_date():
    """Total de vélos par jour."""
    return _rows("""SELECT strftime('%Y-%m-%d', substr(date, 1, 19)), SUM(nb_vehicules)
                    FROM traffic WHERE type_vehicule = 'velo'
                    GROUP BY 1 ORDER BY 1""")


def entre_tableau(x):
    """Nombre de lignes d'une table (whitelistée, plus d'injection SQL)."""
    if x not in TABLES:
        raise ValueError(f"Table inconnue : {x!r}")
    return _rows(f"SELECT COUNT(*) FROM {x}")


def nb_rues_par_ville():
    return _rows("""SELECT ville.nom, COUNT(rue_id) FROM rue
                    JOIN ville ON ville.code_postal = rue.code_postal GROUP BY ville.nom""")


def cyclable():
    return _rows("""SELECT ville.nom, ville.population,
                           ROUND(SUM(nb_vehicules) * 1.0 / population, 2)
                    FROM traffic
                    JOIN rue ON traffic.rue_id = rue.rue_id
                    JOIN ville ON rue.code_postal = ville.code_postal
                    WHERE type_vehicule = 'velo'
                    GROUP BY ville.nom ORDER BY SUM(nb_vehicules) DESC""")


def rue_selection(nom_ville):
    return lst_rue(nom_ville)


def lst_ville():
    return _rows("SELECT nom FROM ville")


def lst_rue(nom_ville):
    return _rows("""SELECT rue.nom FROM rue
                    JOIN ville ON rue.code_postal = ville.code_postal
                    WHERE ville.nom = ?""", (nom_ville,))


def ville_selection(nom_ville):
    """['lourd', %, 'pieton', %, 'voiture', %, 'velo', %] (format d'origine)."""
    v = ville(nom_ville)
    pct = repartition_ville(v["code_postal"])["pct"] if v else {t: 0.0 for t in TYPES}
    out = []
    for t in ("lourd", "pieton", "voiture", "velo"):
        out += [t, pct[t]]
    return out


def selection_date(nom_ville, nom_rue, date_debut, date_fin):
    """['lourd', n, 'voiture', n, 'velo', n, 'pieton', n] (format d'origine)."""
    rows = dict(_rows("""SELECT t.type_vehicule, SUM(t.nb_vehicules) FROM traffic t
                         JOIN rue r ON r.rue_id = t.rue_id
                         JOIN ville v ON v.code_postal = r.code_postal
                         WHERE v.nom = ? AND r.nom = ? AND t.date BETWEEN ? AND ?
                         GROUP BY t.type_vehicule""", (nom_ville, nom_rue, date_debut, date_fin)))
    out = []
    for t in ("lourd", "voiture", "velo", "pieton"):
        out += [t, rows.get(t) or 0]
    return out
