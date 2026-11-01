"""Phases de la lune et lien avec le trafic vélo.

Méthode (cours chap. 9) : on compte les jours écoulés depuis une nouvelle lune
connue, modulo la durée d'une lunaison. L'âge obtenu (0 = nouvelle lune,
~14.8 = pleine lune) donne la phase, découpée en 8 parts égales.
"""
from datetime import datetime, timedelta
from enum import Enum
from math import cos, pi

from .table import total_velo_for_date

LUNAISON = 29.530588853  # durée moyenne d'un cycle synodique, en jours

# Nouvelle lune de référence : 6 janvier 2000, 18h14 UTC.
# (L'ancienne référence, 5 janvier 2000, était présentée comme une pleine lune :
#  c'était en fait une nouvelle lune, ce qui décalait toutes les phases.)
date_reference = datetime(2000, 1, 6, 18, 14)


class MoonPhase(Enum):  # classe Moon Phase, cours chap 9
    NEW_MOON = 0
    WAXING_CRESCENT = 1
    FIRST_QUARTER = 2
    WAXING_GIBBOUS = 3
    FULL_MOON = 4
    WANING_GIBBOUS = 5
    LAST_QUARTER = 6
    WANING_CRESCENT = 7


LABELS = {
    MoonPhase.NEW_MOON: "Nouvelle lune",
    MoonPhase.WAXING_CRESCENT: "Premier croissant",
    MoonPhase.FIRST_QUARTER: "Premier quartier",
    MoonPhase.WAXING_GIBBOUS: "Gibbeuse croissante",
    MoonPhase.FULL_MOON: "Pleine lune",
    MoonPhase.WANING_GIBBOUS: "Gibbeuse décroissante",
    MoonPhase.LAST_QUARTER: "Dernier quartier",
    MoonPhase.WANING_CRESCENT: "Dernier croissant",
}


def age(date_voulu, date_ref=None):
    """Âge de la lune en jours (0 <= age < LUNAISON) à la date donnée.

    `date_ref` est gardé pour compatibilité avec l'ancienne signature mais
    n'est plus utilisé : la référence est toujours une nouvelle lune connue.
    """
    jours = (date_voulu - date_reference).total_seconds() / 86400
    return jours % LUNAISON


def phase(age_lune):
    """Phase (8 parts égales de la lunaison, centrées sur chaque phase)."""
    index = int((age_lune / LUNAISON) * 8 + 0.5) % 8
    return MoonPhase(index)


def illumination(age_lune):
    """Fraction éclairée du disque (0 à 1)."""
    return (1 - cos(2 * pi * age_lune / LUNAISON)) / 2


def moon_svg_path(age_lune, r=90, cx=100, cy=100):
    """Chemin SVG de la partie éclairée (hémisphère nord : croissant à droite)."""
    frac = age_lune / LUNAISON
    if illumination(age_lune) < 0.005:
        return ""
    rx = abs(cos(2 * pi * frac)) * r
    top, bottom = f"{cx} {cy - r}", f"{cx} {cy + r}"
    waxing = frac < 0.5
    gibbous = 0.25 < frac < 0.75
    outer_sweep = 1 if waxing else 0
    if waxing:
        term_sweep = 1 if gibbous else 0
    else:
        term_sweep = 0 if gibbous else 1
    return (f"M {top} A {r} {r} 0 0 {outer_sweep} {bottom} "
            f"A {rx:.2f} {r} 0 0 {term_sweep} {top} Z")


def prochaine(date_depart, cible_age):
    """Prochaine date (à partir de date_depart) où la lune atteint l'âge `cible_age`."""
    delta = (cible_age - age(date_depart)) % LUNAISON
    return date_depart + timedelta(days=delta)


def infos_lune(date_voulu):
    """Tout ce qu'il faut pour afficher la lune d'une date."""
    a = age(date_voulu)
    p = phase(a)
    return {
        "date": date_voulu,
        "age": a,
        "phase": p,
        "key": p.name,
        "label": LABELS[p],
        "illumination": illumination(a),
        "path": moon_svg_path(a),
        "prochaine_pleine": prochaine(date_voulu, LUNAISON / 2),
        "prochaine_nouvelle": prochaine(date_voulu, 0),
    }


def cycle_miniatures():
    """Les 8 phases avec leur dessin, pour la frise."""
    return [{"phase": p, "key": p.name, "label": LABELS[p],
             "path": moon_svg_path(p.value * LUNAISON / 8 + (0.0001 if p.value == 0 else 0))}
            for p in MoonPhase]


def velos_par_phase():
    """Moyenne de vélos par jour, pour chaque phase, et pleine lune vs autres jours."""
    data = total_velo_for_date()
    groupes = {p: [] for p in MoonPhase}
    for jour, velo in data:
        if not jour or velo is None:
            continue
        y, m, d = (int(x) for x in jour.split("-"))
        groupes[phase(age(datetime(y, m, d, 21)))].append(velo)  # 21h : la lune du soir

    def moyenne(valeurs):
        return round(sum(valeurs) / len(valeurs)) if valeurs else None

    pleine = groupes[MoonPhase.FULL_MOON]
    autres = [v for p, vals in groupes.items() if p != MoonPhase.FULL_MOON for v in vals]
    return {
        "phases": [{"phase": p, "label": LABELS[p], "moyenne": moyenne(v), "jours": len(v)}
                   for p, v in groupes.items()],
        "pleine": moyenne(pleine), "jours_pleine": len(pleine),
        "autres": moyenne(autres), "jours_autres": len(autres),
        "jours": len(pleine) + len(autres),
    }


def calcul_moonpahse():
    """Compat : (moyenne vélos jours de pleine lune, moyenne autres jours)."""
    v = velos_par_phase()
    return v["pleine"] or 0, v["autres"] or 0
