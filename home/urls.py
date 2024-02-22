from django.urls import path
from home import views

app_name = 'home'

urlpatterns = [
    path('',views.Home.as_view(), name='home'),
    path('register/',views.Register.as_view(), name='register'),
    path('otp_confirm/',views.OtpConfirm.as_view(), name='otp_confirm'),
    path('login/',views.Login.as_view(), name='login'),
    path('about/',views.About.as_view(), name='about'),
    path('contactus/',views.Contactus.as_view(), name='contactus'),
    path('forgot/',views.Forgot.as_view(), name='forgot'),
    path('logout/',views.UserLogout.as_view(), name='logout'),
]