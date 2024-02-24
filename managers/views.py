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
        month_date_list = []
        for single_date in (last_month + timedelta(days=n) for n in range((today - last_month).days + 1)):
            month_date_list.append(single_date)

        last_orders = Order.objects.filter(status=True)
        total_paid_order = last_orders.filter(paid=True)
        total_user = len(User.objects.all())
        total_unpaid_order = len(Order.objects.filter(paid=False))

        last_day = []
        for order in last_orders:
            if order.created.date() in last_day_date:
                last_day.append(order)

        last_month = []
        for order in last_orders:
            if order.created.date() in month_date_list:
                last_month.append(order)

        total_price_lasd_day = 0
        for lsd in last_day:
            if lsd.paid:
                total_price_lasd_day += int(lsd.total_price)
        
        total_price_lasd_month = 0
        for lsd in last_month:
            if lsd.paid:
                total_price_lasd_month += int(lsd.total_price)
        
        total_price_paid = 0
        for lsd in total_paid_order:
            total_price_paid += int(lsd.total_price)

        return render(request, self.manage_temp ,{'last_day': last_day, 'total_price_lasd_day': total_price_lasd_day,
                                                  'last_month': last_month, 'total_price_lasd_month': total_price_lasd_month,
                                                  'all_user': total_user, 'total_order_paid': len(total_paid_order),
                                                  'all_price': total_price_paid, 'total_unpaid_order': total_unpaid_order})

    def post(self, request):
        pass

    def test_func(self) -> bool | None:
        return self.request.user.is_authenticated and self.request.user.is_admin