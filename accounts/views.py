from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views import View
from .models import User, Address


class Profile(View):
    prof_temp = 'inc/profile.html'

    def get(self, request):
        user = User.objects.get(phone_number=request.user.phone_number)
        return render(request, self.prof_temp, {'user': user})
    
    def post(self, request):
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
        Address.objects.create(
            user = request.user,
            city = request.POST['city'],
            neighbourhood = request.POST['neighbourhood'],
            street = request.POST['street'],
            alley = request.POST['alley'],
            building = request.POST['building']
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
