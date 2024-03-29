from django.shortcuts import render, redirect
from django.views import View
from accounts.models import User, OtpCode
from home.models import ContactUs
from django.utils import timezone
from product.models import Category, Product
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from order.models import OrderItem
from django.db.models import Count
from utils import msg_sender
from django.contrib import messages
import random

class Home(View):
    home_temp = 'index.html'
    def get(self, request):
        temp = self.home_temp
        eco_prod = Product.objects.filter(status=True, inventory__gt=0, economic=True) 
        products = Product.objects.filter(status=True, inventory__gt=0)
        top_items = OrderItem.objects.values('product_id').annotate(total=Count('product_id')).order_by('-total')[:4]
        top_product_ids = [item['product_id'] for item in top_items]
        top_products = Product.objects.filter(name__in=top_product_ids, inventory__gt=0)
        return render(request, temp, {'products': products, 'economic': eco_prod, 'best_sellers': top_products})
    
    def post(self, request):
        pass


class Register(View):
    reg_temp = 'inc/register.html'
    otp_temp = 'inc/otp-input.html'
    success_tem = 'inc/reg-done.html'

    def get(self, request):
        messages.info(request, 'لطفا زبان نوشتن را روی حالت انگلیسی قرار دهید')
        return render(request, self.reg_temp)
    
    def post(self, request):
        phone_number_checker = User.objects.filter(phone_number=request.POST['phone']).exists()
        
        if phone_number_checker:
            return render(request, self.reg_temp, {'alert': 'شماره تلفن تکراری! ، لطفا شماره دیگری را وارد کنید.'})
        if request.POST['password1'] != request.POST['password2']:
            return render(request, self.reg_temp, {'alert': 'رمز هایی که وارد کرده اید با هم برابر نیستند.'})
        
        otp_code = random.randint(10000, 99999)
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
                                       email='register@sample.com',
                                       code=otp_code)
        
        request.session['user_register_info'] = {
                    'phone_number': request.POST['phone'],
                    'full_name': request.POST['name'],
                    'password': request.POST['password2']
                    }
        message = f'کد تایید ثبت نام شما : {otp_code} \n www.Qasaab.ir'
        msg_sender(request.POST['phone'], message)
        return render(request, self.otp_temp)


class OtpConfirm(View):
    otp_temp = 'inc/otp-input.html'
    success_temp = 'inc/reg-done.html'    
    
    def post(self, request):
        user_phone = request.session['user_register_info']['phone_number']
        user_full_name = request.session['user_register_info']['full_name']
        user_password = request.session['user_register_info']['password']
        otp_code = OtpCode.objects.filter(phone_number=user_phone).values_list('code', flat=True).first()
        
        if int(otp_code)==int(request.POST['code']):
            User.objects.create(
                phone_number=user_phone,
                full_name=user_full_name,
                password=user_password
            )
            OtpCode.objects.filter(phone_number=user_phone).delete()
            del request.session['user_register_info']
            return render(request, self.success_temp)
        return render(request, self.otp_temp, {'alert': 'کد یکبار مصرف وارد شده صحیح نمی باشد'})


class Login(View):
    log_temp = 'inc/login.html'
    home_temp = 'index.html'

    def get(self, request):
        return render(request, self.log_temp)
    
    def post(self, request):
        user = authenticate(request, phone_number=request.POST['phone'], 
                            password=request.POST['password'])
        if user is not None:
            login(request, user)
            return redirect('home:home')
        return render(request, self.log_temp, {'alert': 'شماره تلفن و یا رمز وارد شده معتبر نیست.'})

    

class Forgot(View):
    forgot_temp = 'inc/forgot-pass.html'
    login_temp = 'inc/login.html'

    def get(self, request):
        phone = request.GET['phone']
        user_exists = User.objects.filter(phone_number=phone).exists()
        if not user_exists:
            return render(request, self.login_temp, {'alert': 'کاربری با اطلاعات وارد شده در سایت ثبت نام نکرده است'})
        otp_code = random.randint(100000, 999999)
        OtpCode.objects.create(phone_number=phone, email='forgot@mail.com', code=otp_code)
        request.session['user_forgot_password'] = {
            'user_phone': phone
        }
        message = f'اگر شما کد فراموشی رمز را درخواست نداده اید این پیام را نادیده بگیرید. \n کد تایید شما: {otp_code} \n www.Qasaab.ir'
        msg_sender(phone, message)
        return render(request, self.forgot_temp)

    def post(self, request):
        code = request.POST['code']
        pass1 = request.POST['password1']
        pass2 = request.POST['password2']

        code_sent = OtpCode.objects.filter(phone_number=request.session['user_forgot_password']['user_phone']).values_list('code', flat=True).first()
        user_phone = request.session['user_forgot_password']['user_phone']
        user = User.objects.get(phone_number=user_phone)
        code_exist = OtpCode.objects.filter(phone_number=request.session['user_forgot_password']['user_phone'],
                                             email='forgot@mail.com').exists()
        
        if code_exist and int(code_sent)==int(code):
            if str(pass1)==str(pass2):
                user.set_password(pass2)
                user.save()
                OtpCode.objects.filter(phone_number=request.session['user_forgot_password']['user_phone']).delete()
                del request.session['user_forgot_password']
                return render(request, self.login_temp, {'alert': 'رمز با موفقیت تغییر کرد'})
            else:
                return render(request, self.forgot_temp, {'alert': 'رمز اول با تکرار رمز برابر نیست'})
        else:
            return render(request, self.forgot_temp, {'alert': 'کد وارد شده صحیح نیست و یا منقضی شده است'})



class About(View):
    about_temp = 'about.html'

    def get(self, request):
        return render(request, self.about_temp)
    

class Contactus(View):
    cont_temp = 'contactus.html'

    def get(self, request):
        return render(request, self.cont_temp)
    
    def post(self, request):
        ContactUs.objects.create(
            name = request.POST['name'],
            email = request.POST['email'],
            subject = request.POST['subject'],
            message = request.POST['message']
        )
        messages.success(request, 'با تشکر ،پیام شما با موفقیت برای ما ارسال شد.')
        return redirect('home:contactus')


class UserLogout(LoginRequiredMixin, View):
    temp = 'index.html'

    def get(self, request):
        logout(request)
        return redirect('home:home')