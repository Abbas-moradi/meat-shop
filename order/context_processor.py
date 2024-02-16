from .card import Card

def card_number(request):
    return {'item_number': Card(request)}