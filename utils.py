from num2words import num2words


def convert_to_toman(number):
    toman_number = number / 1
    toman_string = num2words(toman_number, lang='fa')
    return f'{toman_string} تومان'