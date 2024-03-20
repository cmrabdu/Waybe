# moon_utils.py
from datetime import datetime
from decimal import Decimal, getcontext
from enum import Enum
import unittest

class MoonPhase(Enum):
    NEW_MOON = 0  # Nouvelle lune
    FIRST_QUARTER = 1  # Premier quartier
    FULL_MOON = 2  # Pleine lune
    LAST_QUARTER = 3  # Dernier quartier

def age(date: datetime) -> Decimal:
    # Utiliser une date de nouvelle lune de référence pour calculer l'âge de la lune
    getcontext().prec = 9
    new_moon_reference = datetime(1900, 1, 1)  # Ou toute autre date de nouvelle lune de référence connue
    days_since_new_moon_reference = (date - new_moon_reference).days
    age = Decimal(days_since_new_moon_reference) % Decimal('29.53059')
    return age

def phase(age: Decimal) -> MoonPhase:
    # Détermination de la phase de la lune basée sur l'âge (genre en tranche de jours)
    if 0 <= age < 7.4:
        return MoonPhase.NEW_MOON
    elif 7.4 <= age < 14.8:
        return MoonPhase.FIRST_QUARTER
    elif 14.8 <= age < 22.1:
        return MoonPhase.FULL_MOON
    else:  # 22.1 <= age < 29.53059
        return MoonPhase.LAST_QUARTER

class MoonUtilsTestCase(unittest.TestCase):

    def test_phase_full_moon(self):
        # Exemple de date pour tester la pleine lune, en supposant la cohérence avec la date de référence utilisée dans `age`
        my_fixture = datetime(2020, 10, 1)
        expected_phase = MoonPhase.FULL_MOON
        calculated_age = age(my_fixture)
        self.assertEqual(phase(calculated_age), expected_phase,
                         msg=f'Phase attendue {expected_phase}, mais obtenue {phase(calculated_age)} pour la date {my_fixture}')

if __name__ == '__main__':
    unittest.main(verbosity=2)
