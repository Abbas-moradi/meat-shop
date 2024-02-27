from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from product.models import Product
from accounts.models import User, Address
from order.models import Order, OrderItem
from django.views import View
from datetime import datetime
from .card import Card
from utils import convert_to_toman, convert_to_jalali, msg_sender
from datetime import datetime


class ShopingCard(View):
    card_temp = 'inc/shoping-card.html'
    home_temp = 'index.html'

    def get(self, request):
        card = Card(request)
        finally_price = sum(item['total_price'] for item in card)
        toman = convert_to_toman(int(finally_price))
        return render(request, self.card_temp, {'card': card,'finally_price': finally_price,
                                                'toman': toman})
    

class ShopingCardUpdate(View):
    card_temp = 'inc/shoping-card.html'

    def post(self, request, product):
        card = Card(request)
        product = get_object_or_404(Product, name=product)
        if product.inventory < int(request.POST['quantity']):
            messages.info(request, 'مقدار انتخابی شما بیشتر از مقدار باقیمانده محصول است')
            return redirect('order:shoping_card')
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
        if product.inventory < int(request.POST['quantity']):
            messages.info(request, 'مقدار انتخابی شما بیشتر از مقدار باقیمانده محصول است')
            return redirect('home:home')
        card.add(product, int(request.POST['quantity']))
        messages.success(request, 'محصول شما با موفقیت به سبد خرید افزوده شد.')
        return redirect('order:shoping_card')


class UserReceipt(View):
    receipt_temp = 'inc/order-recipt.html'

    def get(self, request):
        user_address = Address.objects.filter(user=request.user).exists()
        if user_address is False:
            messages.success(request, ' آدرسی برای شما ثبت نشده، لطفا یک آدرس ثبت کنید')
            return redirect('account:address')
        
        user_address = Address.objects.filter(user=request.user, main=True)

        card = Card(request)
        item_in_card = 0
        for _ in card:
            item_in_card += 1
        if item_in_card == 0 :
            messages.success(request, 'سبد خرید شما خالی است')
            return redirect('order:shoping_card')
        
        finally_price = sum(item['total_price'] for item in card)
        user = User.objects.get(phone_number=request.user)
        product_item = [item for item in card]
        product_num = len(product_item)
        tax = int(finally_price * 0.00)
        end_price = int(tax) + finally_price
        usadrs = ''
        for adrs in user_address:
            usadrs += str(adrs)
        shamsi_date = convert_to_jalali(datetime.now())
        order = Order.objects.create(
            user=user, total_price=finally_price, finally_price=end_price,
            product_number=product_num,tax=tax,address=usadrs, shamsi=shamsi_date
        )
        try:
            msg_sender('09126818407', f' سفارشی با این کد ثبت شد {order.id} ، مبلغ سفارش  {order.finally_price}')
            msg_sender(user.phone_number, f'{user.full_name} عزیز ، سفارش شما بدست ما رسید ، در اسرع وقت برای آماده سازی و ارسال آن اقدام و به شما اطلاع میدهیم. qasaab.ir')
        except:
            print('An error occurred while sending the message')

        for item in card:
            OrderItem.objects.create(
                order=order, product_id=item['product'], product_price=int(item['price']),
                product_quantity=int(item['quantity']), total_price=int(item['total_price'],),
                shamsi=shamsi_date
                )
            update_product = Product.objects.get(name=item['product'])
            if update_product.inventory >= int(item['quantity']):
                update_product.inventory -= int(item['quantity'])
            else:
                messages.error(request, f'متاسفانه محصول {update_product.name} به مقدار انتخابی شما موجود نیست.')
                return redirect('order:shoping_card')
            update_product.save()

        items = OrderItem.objects.filter(order=order.id)
        del request.session['card']
        toman = convert_to_toman(int(order.finally_price))
        return render(request, self.receipt_temp, {'order': order, 'items': items, 'toman': toman}) 