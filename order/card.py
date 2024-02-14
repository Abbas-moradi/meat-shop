CARD_SESSION_ID = 'card'

class Card:
    def __init__(self, request):
        self.session = request.session
        card = self.session.get[CARD_SESSION_ID]
        if not card:
            card = self.session[CARD_SESSION_ID]={}
        self.card = card