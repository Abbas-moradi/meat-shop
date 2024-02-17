from num2words import num2words
from jdatetime import GregorianToJalali
from datetime import datetime

def convert_to_jalali(gregorian_date):
    jalali_date = GregorianToJalali(gregorian_date.year, gregorian_date.month, gregorian_date.day)
    return f'{jalali_date.jyear}/{jalali_date.jmonth}/{jalali_date.jday}'


def convert_to_toman(number):
    toman_number = number / 1
    toman_string = num2words(toman_number, lang='fa')
    return f'{toman_string} تومان'