from enum import Enum
import datetime


def age(date):

    reference_date = datetime.datetime(1900, 1, 1)


    date = datetime.datetime.strptime(date, "%Y-%m-%d")

    days_since_reference = (date - reference_date).days


    moon_age = days_since_reference % 29.53059

    return moon_age

class MoonPhase(Enum):
    NEW_MOON = 0
    WAXING_CRESCENT = 1
    FIRST_QUARTER = 2
    WAXING_GIBBOUS = 3
    FULL_MOON = 4
    WANING_GIBBOUS = 5
    LAST_QUARTER = 6
    WANING_CRESCENT = 7
