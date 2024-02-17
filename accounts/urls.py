from django.urls import path
from accounts import views

app_name = 'account'

urlpatterns = [
    path('profile/', views.Profile.as_view(), name='profile'),
    path('address/', views.UserAddress.as_view(), name='address'),
]