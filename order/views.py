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
from django.contrib.auth.mixins import UserPassesTestMixin
from meatshop import settings
import json
import requests
from django.http import HttpResponse , JsonResponse



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
    

class OrderPay(View):

    CallbackURL = 'http://127.0.0.1:8000/order/verify/'
    currency = "IRR"
    description = "فروشگاه گوشت دامیران"

    def get(self, request, order_id):
        order = Order.objects.get(id=order_id, paid=False)
        request.session['order_pay'] = {
            'order_id': order.id,
        }

        metadata = {
            "mobile": request.user.phone_number,  # Buyer phone number Must start with 09
            "email": request.user.email,  # Buyer Email
            "order_id": str(order.id),  # Order Id
        }

        data = {
            "merchant_id": settings.MERCHANT,
            "amount": order.finally_price*10,
            "currency": self.currency,
            "description": self.description,
            "callback_url": self.CallbackURL,
            "metadata": metadata
        }

        data = json.dumps(data)
        # set content length by data
        headers = {'content-type': 'application/json', 'accept': 'application/json'}

        try:
            response = requests.post(
                settings.ZP_API_REQUEST, data=data, headers=headers, timeout=10)
            response = response.json()
            err = response["errors"]
            if err:
                return JsonResponse(err, content_type="application/json",safe=False)
            if response['data']['code'] == 100:
                url = settings.ZP_API_STARTPAY + str(response['data']['authority'])
                return redirect(url)
            else:
                return JsonResponse(json.dumps({'status': False, 'code': str(response['data']['code'])}), safe=False)
            return JsonResponse(response)

        except requests.exceptions.Timeout:
            data = json.dumps({'status': False, 'code': 'timeout'})
            return HttpResponse(data)
        except requests.exceptions.ConnectionError:
            data = json.dumps({'status': False, 'code': 'اتصال برقرار نشد'})
            return HttpResponse(data)


class OrderPayVerify(View):

    def get(self, request):
        authority = request.GET.get('Authority')
        status = request.GET.get('Status')
        order_id = request.session['order_pay']['order_id']
        order = Order.objects.get(id=order_id, paid=False)

        if status == "NOK":
            return HttpResponse(json.dumps({'status': "پرداخت ناموفق"}))
        data = {
            "merchant_id": settings.MERCHANT,
            "amount": order.total_price,
            "authority": authority,
        }
        data = json.dumps(data)
        headers = {'content-type': 'application/json', 'accept': 'application/json'}
        try:
            response = requests.post(settings.ZP_API_VERIFY, data=data, headers=headers)
            response = response.json()
            err = response["errors"]
            if err:
                return JsonResponse(err, content_type="application/json",safe=False)
            if response['data']['code'] == 100:
                data = json.dumps({'status': True, 'first_time_verify': True, 'ref_id': response['data']['ref_id']})
                order.paid = True
                order.save()
                user = User.objects.get(phone_number=request.user)
                try:
                    msg_sender('09126818407', f' سفارشی با این کد ثبت شد {order.id} ، مبلغ سفارش  {order.finally_price}')
                    msg_sender(user.phone_number, f'{user.full_name} عزیز ، سفارش شما بدست ما رسید ، در اسرع وقت برای آماده سازی و ارسال آن اقدام و به شما اطلاع میدهیم.\n www.qasaab.ir')
                except:
                    print('An error occurred while sending the message')

            else:
                data = json.dumps({'status': False, 'data': response})
            return JsonResponse(data, safe=False)

        except requests.exceptions.ConnectionError:
            data = json.dumps({'status': False, 'code': 'اتصال برقرار نشد'})
            return HttpResponse(data)