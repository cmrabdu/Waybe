import unittest
from .moon_utils import age, phase, MoonPhase
from datetime import datetime

class MoonUtilsTestCase(unittest.TestCase):

    def test_1(self):
        date_reference = datetime(2000, 1, 5)
        my_fixture = datetime(2019, 1, 21, 5, 16, 0)
        expected = MoonPhase.WANING_CRESCENT
        self.assertEqual(phase(age(my_fixture, date_reference)), expected,
                         msg=f'My error message on pl.f({my_fixture}) different than {expected}')

    def test_2(self):
        date_reference = datetime(2000, 1, 5)
        my_fixture = datetime(2020, 2, 10, 7, 33, 0)
        expected = MoonPhase.WANING_CRESCENT
        self.assertEqual(phase(age(my_fixture, date_reference)), expected,
                         msg=f'My error message on pl.f({my_fixture}) different than {expected}')

    def test_3(self):
        date_reference = datetime(2000, 1, 5)
        my_fixture = datetime(2020, 2, 24, 15, 33, 0)
        expected = MoonPhase.WAXING_CRESCENT
        self.assertEqual(phase(age(my_fixture, date_reference)), expected,
                         msg=f'My error message on pl.f({my_fixture}) different than {expected}')

    def test_4(self):
        date_reference = datetime(2000, 1, 5)
        my_fixture = datetime(2020, 2, 10, 7, 33, 0)
        expected = MoonPhase.WANING_CRESCENT
        self.assertEqual(phase(age(my_fixture, date_reference)), expected,
                         msg=f'My error message on pl.f({my_fixture}) different than {expected}')

    def test_5(self):
        date_reference = datetime(2000, 1, 5)
        my_fixture = datetime(2020, 2, 2)
        expected = MoonPhase.WANING_CRESCENT
        self.assertEqual(phase(age(my_fixture, date_reference)), expected,
                         msg=f'My error message on pl.f({my_fixture}) different than {expected}')

    def test_6(self):
        date_reference = datetime(2000, 1, 5)
        my_fixture = datetime(2020, 2, 23)
        expected = MoonPhase.NEW_MOON
        self.assertEqual(phase(age(my_fixture, date_reference)), expected,
                         msg=f'My error message on pl.f({my_fixture}) different than {expected}')

    def test_7(self):
        date_reference = datetime(2000, 1, 5)
        my_fixture = datetime(2020, 2, 16)
        expected = MoonPhase.WANING_CRESCENT
        self.assertEqual(phase(age(my_fixture, date_reference)), expected,
                         msg=f'My error message on pl.f({my_fixture}) different than {expected}')

    def test_8(self):
        date_reference = datetime(2000, 1, 5)
        my_fixture = datetime(2020, 2, 19)
        expected = MoonPhase.WANING_CRESCENT
        self.assertEqual(phase(age(my_fixture, date_reference)), expected,
                         msg=f'My error message on pl.f({my_fixture}) different than {expected}')

    def test_9(self):
        date_reference = datetime(2000, 1, 5)
        my_fixture = datetime(2020, 2, 3)
        expected = MoonPhase.WANING_CRESCENT
        self.assertEqual(phase(age(my_fixture, date_reference)), expected,
                         msg=f'My error message on pl.f({my_fixture}) different than {expected}')

    def test_10(self):
        date_reference = datetime(2000, 1, 5)
        my_fixture = datetime(2020, 2, 13)
        expected = MoonPhase.WANING_CRESCENT
        self.assertEqual(phase(age(my_fixture, date_reference)), expected,
                         msg=f'My error message on pl.f({my_fixture}) different than {expected}')

    def test_11(self):
        date_reference = datetime(2000, 1, 5)
        my_fixture = datetime(2020, 2, 29)
        expected = MoonPhase.LAST_QUARTER
        self.assertEqual(phase(age(my_fixture, date_reference)), expected,
                         msg=f'My error message on pl.f({my_fixture}) different than {expected}')

    def test_12(self):
        date_reference = datetime(2000, 1, 5)
        my_fixture = datetime(2022, 6, 15)
        expected = MoonPhase.WANING_CRESCENT
        self.assertEqual(phase(age(my_fixture, date_reference)), expected,
                         msg=f'Expected phase for date {my_fixture} is {expected}')

    def test_13(self):
        date_reference = datetime(2000, 1, 5)
        my_fixture = datetime(2024, 6, 1)
        expected = MoonPhase.WANING_CRESCENT
        self.assertEqual(phase(age(my_fixture, date_reference)), expected,
                         msg=f'Expected phase for date {my_fixture} is {expected}, but got a different phase')



    def test_14(self):

        date_reference = datetime(2000, 1, 5)
        my_fixture = datetime(2023, 3, 15)
        expected = MoonPhase.WANING_CRESCENT
        self.assertEqual(phase(age(my_fixture, date_reference)), expected,
                         msg=f'Expected phase for date {my_fixture} is {expected}, but got a different phase')

    def test_15(self):
        # Teste une date avec une phase de lune incorrecte
        date_reference = datetime(2000, 1, 5)
        my_fixture = datetime(2014, 2, 1)
        expected = MoonPhase.WAXING_CRESCENT
        self.assertEqual(phase(age(my_fixture, date_reference)), expected,
                         msg=f'My custom error message on phase function call')


if __name__ == '__main__':
    unittest.main(verbosity=2)
