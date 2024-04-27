import unittest
from website.mobility.moon_utils import  age, phase, MoonPhase
from datetime import datetime

class MoonUtilsTestCase(unittest.TestCase):

    def test_waning_crescent(self):
        date_reference = datetime(2000, 1, 5)
        my_fixture = datetime(2019, 1, 21, 5, 16, 0)
        expected = MoonPhase.WANING_CRESCENT
        self.assertEqual(phase(age(my_fixture, date_reference)), expected,
                         msg=f'Expected phase for date {my_fixture} is {expected}')

    def test_waning_crescent2(self):
        date_reference = datetime(2000, 1, 5)
        my_fixture = datetime(2020, 2, 10, 7, 33, 0)
        expected = MoonPhase.WANING_CRESCENT
        self.assertEqual(phase(age(my_fixture, date_reference)), expected,
                         msg=f'Expected phase for date {my_fixture} is {expected}')

    def test_waxing_crescent(self):
        date_reference = datetime(2000, 1, 5)
        my_fixture = datetime(2020, 2, 24, 15, 33, 0)
        expected = MoonPhase.WAXING_CRESCENT
        self.assertEqual(phase(age(my_fixture, date_reference)), expected,
                         msg=f'Expected phase for date {my_fixture} is {expected}')

    def test_waning_crescent3(self):
        date_reference = datetime(2000, 1, 5)
        my_fixture = datetime(2020, 2, 10, 7, 33, 0)
        expected = MoonPhase.WANING_CRESCENT
        self.assertEqual(phase(age(my_fixture, date_reference)), expected,
                         msg=f'Expected phase for date {my_fixture} is {expected}')

    def test_waning_crescent4(self):
        date_reference = datetime(2000, 1, 5)
        my_fixture = datetime(2020, 2, 2)
        expected = MoonPhase.WANING_CRESCENT
        self.assertEqual(phase(age(my_fixture, date_reference)), expected,
                         msg=f'Expected phase for date {my_fixture} is {expected}')

    def test_new_moon(self):
        date_reference = datetime(2000, 1, 5)
        my_fixture = datetime(2020, 2, 23)
        expected = MoonPhase.NEW_MOON
        self.assertEqual(phase(age(my_fixture, date_reference)), expected,
                         msg=f'Expected phase for date {my_fixture} is {expected}')

    def test_waning_crescent5(self):
        date_reference = datetime(2000, 1, 5)
        my_fixture = datetime(2020, 2, 16)
        expected = MoonPhase.WANING_CRESCENT
        self.assertEqual(phase(age(my_fixture, date_reference)), expected,
                         msg=f'Expected phase for date {my_fixture} is {expected}')

    def test_waning_crescent6(self):
        date_reference = datetime(2000, 1, 5)
        my_fixture = datetime(2020, 2, 19)
        expected = MoonPhase.WANING_CRESCENT
        self.assertEqual(phase(age(my_fixture, date_reference)), expected,
                         msg=f'Expected phase for date {my_fixture} is {expected}')

    def test_waning_crescent7(self):
        date_reference = datetime(2000, 1, 5)
        my_fixture = datetime(2020, 2, 3)
        expected = MoonPhase.WANING_CRESCENT
        self.assertEqual(phase(age(my_fixture, date_reference)), expected,
                         msg=f'Expected phase for date {my_fixture} is {expected}')

    def test_waning_crescent8(self):
        date_reference = datetime(2000, 1, 5)
        my_fixture = datetime(2020, 2, 13)
        expected = MoonPhase.WANING_CRESCENT
        self.assertEqual(phase(age(my_fixture, date_reference)), expected,
                         msg=f'Expected phase for date {my_fixture} is {expected}')

    def test_last_quarter(self):
        date_reference = datetime(2000, 1, 5)
        my_fixture = datetime(2020, 2, 29)
        expected = MoonPhase.LAST_QUARTER
        self.assertEqual(phase(age(my_fixture, date_reference)), expected,
                         msg=f'Expected phase for date {my_fixture} is {expected}')

    def test_waning_crescent9(self):
        date_reference = datetime(2000, 1, 5)
        my_fixture = datetime(2022, 6, 15)
        expected = MoonPhase.WANING_CRESCENT
        self.assertEqual(phase(age(my_fixture, date_reference)), expected,
                         msg=f'Expected phase for date {my_fixture} is {expected}')

    def test_waning_crescent10(self):
        date_reference = datetime(2000, 1, 5)
        my_fixture = datetime(2024, 6, 1)
        expected = MoonPhase.WANING_CRESCENT
        self.assertEqual(phase(age(my_fixture, date_reference)), expected,
                         msg=f'Expected phase for date {my_fixture} is {expected}')

    def test_waning_crescent11(self):
        date_reference = datetime(2000, 1, 5)
        my_fixture = datetime(2023, 3, 15)
        expected = MoonPhase.WANING_CRESCENT
        self.assertEqual(phase(age(my_fixture, date_reference)), expected,
                         msg=f'Expected phase for date {my_fixture} is {expected}')

    def test_invalid_phase(self):
        date_reference = datetime(2000, 1, 5)
        my_fixture = datetime(2014, 2, 1)
        expected = MoonPhase.WAXING_CRESCENT
        self.assertEqual(phase(age(my_fixture, date_reference)), expected,
                         msg=f'Expected phase for date {my_fixture} is {expected}, but got a different phase')


if __name__ == '__main__':
    unittest.main(verbosity=2)
