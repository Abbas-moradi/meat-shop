from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from product.models import Product
from accounts.models import User, Address
from order.models import Order, OrderItem
from django.views import View
from datetime import datetime
from .card import Card


class ShopingCard(View):
    card_temp = 'inc/shoping-card.html'
    home_temp = 'index.html'

    def get(self, request):
        card = Card(request)
        finally_price = sum(item['total_price'] for item in card)
        return render(request, self.card_temp, {'card': card,
                                                'finally_price': finally_price})
    

class ShopingCardUpdate(View):
    card_temp = 'inc/shoping-card.html'

    def post(self, request, product):
        card = Card(request)
        product = get_object_or_404(Product, name=product)
        card.update(product, int(request.POST['quantity']))
        messages.success(request, 'کارت خرید شما با موفقیت بروز رسانی شد.')
        return redirect('order:shoping_card')


class RemoveItem(View):
    card_temp = 'inc/shoping-card.html'

    def post(self, request, product):
        card = Card(request)
        product = get_object_or_404(Product, name=product)
        card.delete(product)
        messages.success(request, 'محصول از سبد خرید شما حذف شد')
        return redirect('order:shoping_card')

    

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
        card = Card(request)
        finally_price = sum(item['total_price'] for item in card)
        user = User.objects.get(phone_number=request.user)
        product_item = [item for item in card]
        product_num = len(product_item)
        order = Order.objects.create(
            user=user, total_price=finally_price, 
            product_number=product_num,
        )

        for item in card:
            OrderItem.objects.create(
                order=order, product_id=item['product'], product_price=int(item['price']),
                product_quantity=int(item['quantity']), total_price=int(item['total_price'])
                )
        id = order.id
        time_now = datetime.now()
        user_address = get_object_or_404(Address, user=user)
        if not user_address:
            messages.success(request, ' آدرسی برای شما ثبت نشده، لطفا یک آدرس ثبت کنید')
            return redirect('account:profile')
        return render(request, self.receipt_temp, {'items': card, 'id': id, 'date': time_now,
                                                   'address': user_address,  }) 