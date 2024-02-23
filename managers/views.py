from django.shortcuts import render
from django.views import View
from order.models import Order, OrderItem
from accounts.models import User, Address
from django.contrib.auth.mixins import UserPassesTestMixin


class Manage(UserPassesTestMixin, View):
    manage_temp = 'manage.html'

    def get(self, request):
        return render(request, self.manage_temp)

    def post(self, request):
        pass

    def test_func(self) -> bool | None:
        return self.request.user.is_authenticated and self.request.user.is_admin