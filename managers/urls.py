from django.urls import path
from managers import views


app_name = 'manager'

urlpatterns = [
    path('manage/', views.Manage.as_view(), name='manage'),
]