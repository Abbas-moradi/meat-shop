from django.shortcuts import render, redirect
from django.views import View
from accounts.models import User, OtpCode
from django.utils import timezone
import random

class Home(View):
    home_temp = 'index.html'
    def get(self, request):
        temp = self.home_temp
        return render(request, temp)
    
    def post(self, request):
        pass


class Register(View):
    reg_temp = 'inc/register.html'
    otp_temp = 'inc/otp-input.html'
    success_tem = 'inc/reg-done.html'

    def get(self, request):
        return render(request, self.reg_temp)
    
    def post(self, request):
        email_checker = User.objects.filter(email=request.POST['email']).exists()
        phone_number_checker = User.objects.filter(phone_number=request.POST['phone']).exists()
        
        if email_checker:
            return render(request, self.reg_temp, {'alert':'ایمیل تکراری ! ، لطفا یک ایمیل دیگر برای ثبت نام وارد کنید.'})
        
        if phone_number_checker:
            return render(request, self.reg_temp, {'alert': 'شماره تلفن تکراری! ، لطفا شماره دیگری را وارد کنید.'})
        if request.POST['password1'] != request.POST['password2']:
            return render(request, self.reg_temp, {'alert': 'رمز هایی که وارد کرده اید با هم برابر نیستند.'})
        
        otp_code = random.randint(10000, 99999)
        subject = 'کد تایید ثبت نام'
        body = f'کد تایید شما \n code:{otp_code}'
        user_code_exists = OtpCode.objects.filter(phone_number=request.POST['phone']).exists()
        if user_code_exists:
            user_code_created_time = OtpCode.objects.filter(phone_number=request.POST['phone']).values_list('created', flat=True).first()
            current_time = timezone.now()
            time_difference = current_time - user_code_created_time

            if time_difference.total_seconds() > 120:
                user_code_exists = OtpCode.objects.filter(phone_number=request.POST['phone']).delete()
                OtpCode.objects.create(phone_number=request.POST['phone'],
                                       email=request.POST['email'],
                                       code=otp_code)

            else:
                otp_code = OtpCode.objects.filter(phone_number=request.POST['phone']).values_list('code', flat=True).first()
            
        else:
            OtpCode.objects.create(phone_number=request.POST['phone'],
                                       email=request.POST['email'],
                                       code=otp_code)
        return render(request, self.otp_temp)