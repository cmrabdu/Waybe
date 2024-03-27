from datetime import datetime
from enum import Enum
from .table import abdu


class MoonPhase(Enum): #classe Moon Phase, cours chap 9
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
    diff_jour = (date_voulu - date_reference).days #jour demandé - jour de pleine lune connue
    age_lune = diff_jour % 29.53059 #nmbr de jour entre chaque pleine lune, cours chap 9 (algo proposé)
    return age_lune

def phase(age_lune): #7.38 --> différence de jours entre chaque cycle, mais a affiner pour etre plus précis
    if 0 <= age_lune < 7.38:
        return MoonPhase.NEW_MOON
    elif 7.38 <= age_lune < 14.76:
        return MoonPhase.FIRST_QUARTER
    elif 14.76 <= age_lune < 22.14:
        return MoonPhase.FULL_MOON
    else:
        return MoonPhase.LAST_QUARTER

#manque plus que :
#1 ---> #identifer jours de pleine lune sur la période demandé (easy)
#2 ---> #receuille nmbre de vélo en fonctions des jours (pleine lune ou pas) (easy mais je dois voir comment demander a php)
#3 ---> #faire une moyenne de vélos des jours (genre additions total de vélos par jours puis diviser par le nombre de jours) (easy, c'est juste un calcul de golmon)
#4 ---> #puis afficher les résultats (easy)
#5 ---> #faire les testes.. (sah jsp, j'vais voir avec la team)
#6 ---> #toujours rester bg car je le suis en sah (vrmt trop bgggg)


###################



data=abdu()

# Initialisation des listes
pleine_lune = []
pas_pleine_lune = []

# Parcourir les données et classer en fonction de la pleine lune
for date, velo in data:
    year, month, day = date.split('-')
    date_voulu= datetime(int(year), int(month), int(day))

    ager=age(date_voulu,date_reference)
    phase_lune = phase(ager)
    if phase_lune == MoonPhase.FULL_MOON:
        pleine_lune.append((date, velo))

    else:
        pas_pleine_lune.append((date, velo))


#jour ou y a la lune
sump = 0
for date, velo in pleine_lune:
    sump = sump + velo

sump= sump / len(pleine_lune)
print(sump)

sumr=0
for date, velo in pas_pleine_lune:
    sumr = sumr + velo

sumr= sumr / len(pas_pleine_lune)

print(sumr)

