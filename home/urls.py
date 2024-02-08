from django.urls import path
from home import views

app_name = 'home'

urlpatterns = [
    path('',views.Home.as_view(), name='home'),
    path('register/',views.Register.as_view(), name='register'),
]