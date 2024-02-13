from django.shortcuts import render
from django.views import View


class ShopingCard(View):
    card_temp = 'inc/shoping-card.html'
    home_temp = 'index.html'

    def get(self, request):
        return render(request, self.card_temp)
