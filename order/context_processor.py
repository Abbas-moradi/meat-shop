from .card import Card
from jdatetime import date as jdate
import datetime


def convert_to_jalali(gregorian_date):
    gregorian_date = datetime.datetime.now()
    jalali_date = jdate.fromgregorian(date=gregorian_date)

    weekday = jalali_date.strftime('%A')
    day = jalali_date.day
    month = jalali_date.strftime('%B')
    year = jalali_date.year

    jalali_str = f"{weekday} {day} {month} {year}"

    return {'jalali': jalali_str}


def card_number(request):
    return {'item_number': Card(request)}