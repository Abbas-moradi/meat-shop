from django.shortcuts import render, get_object_or_404
from product.models import Product
from django.views import View
from .card import Card


class ShopingCard(View):
    card_temp = 'inc/shoping-card.html'
    home_temp = 'index.html'

    def get(self, request):
        card = Card(request)
        return render(request, self.card_temp, {'card': card})
    

class CardAddProduct(View):
    home_temp = 'index.html'

    def get(self, request):
        pass
    
    def post(self, request, product_id):
        card = Card(request)
        product = get_object_or_404(Product, id=product_id)
        card.add(product, request.POST['quantity'])
        return render(request, self.home_temp ,{'alert': 'محصول شما با موفقیت به سید خرید افزوده شد.'})
