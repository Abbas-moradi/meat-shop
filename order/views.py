from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
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
        card.add(product, int(request.POST['quantity']))
        messages.success(request, 'محصول شما با موفقیت به سبد خرید افزوده شد.')
        return redirect('home:home')


class UserReceipt(View):
    receipt_temp = 'inc/order-recipt.html'

    def get(self, request):
        return render(request, self.receipt_temp) 