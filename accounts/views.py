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
        pass


class UserAddress(View):
    adrs_temp = 'inc/user-address.html'

    def get(self, request):
        user_address = Address.objects.filter(user=request.user).exists()
        if user_address is True:
            user_address = Address.objects.filter(user=request.user)
        return render(request, self.adrs_temp, {'address': user_address})
    
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
        return render(request, self.adrs_temp)