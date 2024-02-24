from django.shortcuts import render
from django.views import View
from order.models import Order, OrderItem
from accounts.models import User, Address
from django.contrib.auth.mixins import UserPassesTestMixin
from datetime import date, timedelta, datetime
from django.db.models import Q, Sum


class Manage(UserPassesTestMixin, View):
    manage_temp = 'manage.html'

    def get(self, request):
        today = date.today()
        yesterday = today - timedelta(days=1)
        last_day_date = [today, yesterday]
        last_month = today.replace(day=1) - timedelta(days=1)

        last_day_orders = Order.objects.filter(paid=True)
        last_day = []
        for order in last_day_orders:
            if order.created.date() in last_day_date:
                last_day.append(order)

        total_price_lasd_day = 0
        for lsd in last_day:
            total_price_lasd_day += int(lsd.total_price)
        last_month_orders = Order.objects.filter(Q(created__year=last_month.year) & 
                                        Q(created__month=last_month.month) & 
                                        Q(status=True) & Q(paid=True))
        total_price_lasd_month = last_month_orders.aggregate(total_price=Sum('total_price'))['total_price']


        return render(request, self.manage_temp ,{'last_day': last_day, 'total_price_lasd_day': total_price_lasd_day,
                                                  'last_month': last_month_orders, 'total_price_lasd_month': total_price_lasd_month})

    def post(self, request):
        pass

    def test_func(self) -> bool | None:
        return self.request.user.is_authenticated and self.request.user.is_admin