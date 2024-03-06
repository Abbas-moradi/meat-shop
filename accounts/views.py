from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views import View
from .models import User, Address
from order.models import Order, OrderItem
from utils import convert_to_toman


class Profile(View):
    prof_temp = 'inc/profile.html'

    def get(self, request):
        user = User.objects.get(phone_number=request.user.phone_number)
        order = Order.objects.filter(status=True, on_delete=False, user=request.user).reverse()
        return render(request, self.prof_temp, {'user': user, 'order': order})
    
    def post(self, request):
        email_checker = User.objects.filter(email=request.POST['email']).exists()
        if email_checker:
            user = User.objects.get(email=request.POST['email'])
            if user != request.user:
                return render(request, self.prof_temp, {'alert': 'ایمیل وارد شده تکراری است، یک ایمیل دیگر وارد کنید'})
        user = request.user
        user.full_name = request.POST['full_name']
        user.phone_number = request.POST['phone_number']
        user.email = request.POST['email']
        if len(request.POST['password']) > 8:
            user.set_password(request.POST['password'])
        user.save()
        messages.success(request, 'اطلاعات کاربری با موفقیت بروزرسانی شد')
        return render(request, self.prof_temp)


class UserAddress(View):
    adrs_temp = 'inc/user-address.html'

    def get(self, request):
        user_address = Address.objects.filter(user=request.user).exists()
        if user_address is True:
            user_address = Address.objects.filter(user=request.user)
            return render(request, self.adrs_temp, {'address': user_address})
        return render(request, self.adrs_temp)
    
    def post(self, request):
        ex_address = Address.objects.filter(user=request.user).exists()
        if ex_address:
            Address.objects.create(
                user = request.user,
                city = ' شهر '+ request.POST.get('city'),
                neighbourhood = ' محله '+ request.POST['neighbourhood'],
                street = ' خیابان '+ request.POST['street'],
                alley = ' کوچه '+ request.POST['alley'],
                building = ' ساختمان '+ request.POST['building']
            )
        else:
                Address.objects.create(
                    user = request.user,
                    city = ' شهر '+ request.POST.get('city'),
                    neighbourhood = ' محله '+ request.POST['neighbourhood'],
                    street = ' خیابان '+ request.POST['street'],
                    alley = ' کوچه '+ request.POST['alley'],
                    building = ' ساختمان '+ request.POST['building'],
                    main = True
                )
        messages.success(request, 'آدرس شما با موفقیت ثبت شد')
        user_address = Address.objects.filter(user=request.user)
        return render(request, self.adrs_temp, {'address': user_address})
    

class ChangeAddress(View):
    adrs_temp = 'inc/user-address.html'

    def post(self, request):
        user_address = Address.objects.filter(user=request.user)
        for addr in user_address:
            if int(addr.id) == int(request.POST['flexRadioDefault']):
                addr.main = True
            else:
                addr.main = False
            addr.save()
        messages.success(request, 'آدرس اصلی برای ارسال مرسولات پستی تغییر کرد.')
        return redirect('account:address')


class ProfileReceipt(View):
    rec_temp = 'inc/profile_receipt.html'

    def get(self, request, id):
        order = Order.objects.get(id=id)
        items = OrderItem.objects.filter(order=order)
        toman = convert_to_toman(int(order.finally_price))
        return render(request, self.rec_temp, {'order': order, 'items': items, 'toman': toman})
    

class DeleteAddress(View):
    adrs_temp = 'inc/user-address.html'

    def post(self, request, id):
        print(id)
        # Address.objects.get(id=request.POST['id'])
        # user_address = Address.objects.filter(user=request.user)
        messages.success(request, 'آدرس مورد نظر حذف شد.')
        return redirect('account:address')