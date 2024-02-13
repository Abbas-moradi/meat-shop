from django.urls import path
from . import views


app_name = 'order'

urlpatterns = [
    path('shoping_card/', views.ShopingCard.as_view(), name='card'),
]