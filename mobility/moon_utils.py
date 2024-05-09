from datetime import datetime
from enum import Enum

from .table import total_velo_for_date


class MoonPhase(Enum):  # classe Moon Phase, cours chap 9
    NEW_MOON = 0
    WAXING_CRESCENT = 1
    FIRST_QUARTER = 2
    WAXING_GIBBOUS = 3
    FULL_MOON = 4
    WANING_GIBBOUS = 5
    LAST_QUARTER = 6
    WANING_CRESCENT = 7


date_reference = datetime(2000, 1, 5)


def age(date_voulu, date_reference):
    diff_jour = (date_voulu - date_reference).days  # jour demandé - jour de pleine lune connue
    age_lune = diff_jour % 29.53059  # nmbr de jour entre chaque pleine lune, cours chap 9 (algo proposé)
    return age_lune


def phase(age_lune):  # 7.38 --> différence de jours entre chaque cycle, mais a affiner pour etre plus précis
    if 0 <= age_lune < 1.38:
        return MoonPhase.NEW_MOON
    if 1.38 <= age_lune < 2.78:
        return MoonPhase.WAXING_CRESCENT
    elif 2.78 <= age_lune < 3.76:
        return MoonPhase.FIRST_QUARTER
    elif 3.76 <= age_lune < 4.14:
        return MoonPhase.WAXING_GIBBOUS
    elif 4.14 <= age_lune < 5.78:
        return MoonPhase.FULL_MOON
    elif 5.78 <= age_lune < 6.38:
        return MoonPhase.WANING_GIBBOUS
    elif 6.38 <= age_lune < 7.58:
        return MoonPhase.LAST_QUARTER
    else:
        return MoonPhase.WANING_CRESCENT



def calcul_moonpahse():
    data = total_velo_for_date()
    print(data)
    # Initialisation des listes
    pleine_lune = []
    pas_pleine_lune = []

    # Parcourir les données et classer en fonction de la pleine lune
    for date, velo in data:
        year, month, day = date.split('-')
        date_voulu = datetime(int(year), int(month), int(day))

        ager = age(date_voulu, date_reference)
        phase_lune = phase(ager)
        if phase_lune == MoonPhase.FULL_MOON:
            pleine_lune.append((date, velo))

        else:
            pas_pleine_lune.append((date, velo))

    sumt=0
    for date, velo in data:
        sumt = sumt + velo

    # jour ou y a la lune
    sump = 0
    for date, velo in pleine_lune:
        sump = sump + velo
    sump = round(sump / len(pleine_lune))

    sumr = 0
    for date, velo in pas_pleine_lune:
        sumr = sumr + velo


    sumr = round(sumr / len(pas_pleine_lune))

    return sump, sumr
