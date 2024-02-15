from django.urls import path
from order import views


app_name = 'order'

urlpatterns = [
    path('shoping_card/', views.ShopingCard.as_view(), name='shoping_card'),
    path('shoping_card/add/<str:product>/', views.ShopingCardUpdate.as_view(), name='shoping_card_update'),
    path('card/add/<int:product_id>/', views.CardAddProduct.as_view(), name='card_add'),
    path('receipt/', views.UserReceipt.as_view(), name='receipt'),
]