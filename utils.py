from num2words import num2words
from jdatetime import GregorianToJalali
from datetime import datetime
from ippanel import Client, Error, HTTPError, ResponseCode


def convert_to_jalali(gregorian_date):
    jalali_date = GregorianToJalali(gregorian_date.year, gregorian_date.month, gregorian_date.day)
    return f'{jalali_date.jyear}/{jalali_date.jmonth}/{jalali_date.jday}'


def convert_to_toman(number):
    toman_number = number / 1
    toman_string = num2words(toman_number, lang='fa')
    return f'{toman_string} تومان'


def otp_sender(phone, message):
    client = Client("ykD_Lp-isbx9Ka0KJUOjqcKa8OUE6CWdyBR5eOa_vvg=")

    try:
        message_id = client.send("+983000505", [phone], message, "summary")
        print(message_id)
    except Error as e:
        print(f"Error handled => code: {e.code}, message: {e.message}")

        if e.code == ResponseCode.ErrUnprocessableEntity.value:
            for field in e.message:
                print(f"Field: {field} , Errors: {e.message[field]}")
    except HTTPError as e:
        print(f"Error handled => code: {e}")
