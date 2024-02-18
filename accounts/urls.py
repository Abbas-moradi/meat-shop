from django.urls import path
from accounts import views

app_name = 'account'

urlpatterns = [
    path('profile/', views.Profile.as_view(), name='profile'),
    path('profile/receipt/<int:id>/', views.ProfileReceipt.as_view(), name='pro_receipt'),
    path('address/', views.UserAddress.as_view(), name='address'),
    path('address/change/', views.ChangeAddress.as_view(), name='change'),
    path('address/delete/<int:id>/', views.DeleteAddress.as_view(), name='delete'),
]