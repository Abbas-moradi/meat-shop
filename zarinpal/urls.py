from django.urls import path
from zarinpal import views

app_name = 'zarinpal'

urlpatterns = [
    path('request/', views.Zarinpal.as_view(), name='request'),
    path('verify/', views.CallbackUrl.as_view() , name='verify'),
]