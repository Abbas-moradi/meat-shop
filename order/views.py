from django.shortcuts import render
from django.views import View


class ShopingCard(View):
    card_temp = 'inc/shoping-card.html'
    home_temp = 'index.html'

    def get(self, request):
        return render(request, self.card_temp)
    

class CardAddProduct(View):
    temp = ''

    def get(self, request):
        pass
    
    def post(self, request, product_id):
        pass
