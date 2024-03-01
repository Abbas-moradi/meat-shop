from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from order.models import Order, OrderItem
from accounts.models import User, Address
from django.contrib.auth.mixins import UserPassesTestMixin
from datetime import date, timedelta, datetime
from django.db.models import Q, Sum
from utils import msg_sender, convert_to_toman


class Manage(UserPassesTestMixin, View):
    manage_temp = 'manage.html'

    def get(self, request):
        # Get the current date and the previous date
        today = date.today()
        yesterday = today - timedelta(days=1)
        # Get the last month's date range
        last_month = today.replace(month=1) - timedelta(days=1)
        month_date_list = [last_month + timedelta(days=n) for n in range((today - last_month).days + 1)]
        # Get the orders with status True
        last_orders = Order.objects.filter(status=True)
        # Get the total number of users
        total_user = User.objects.count()
        # Get the total number of unpaid & paid orders
        total_unpaid_order = Order.objects.filter(paid=False).count()
        total_paid_order = Order.objects.filter(paid=True).count()
        # Get the orders from the last day and the last month
        last_day = last_orders.filter(created__date__in=[today, yesterday])
        last_month = last_orders.filter(created__date__in=month_date_list)
        # Get the total price of the paid orders from the last day and the last month
        total_price_lasd_day = last_day.filter(paid=True).aggregate(Sum('total_price'))['total_price__sum'] or 0
        total_price_lasd_month = last_month.filter(paid=True).aggregate(Sum('total_price'))['total_price__sum'] or 0
        # Get the total price of all the paid orders
        total_price_paid = last_orders.filter(paid=True).aggregate(Sum('total_price'))['total_price__sum'] or 0
        toman = convert_to_toman(int(total_price_paid))

        return render(request, self.manage_temp ,{'last_day': last_day, 'total_price_lasd_day': total_price_lasd_day,
                                                  'last_month': last_month, 'total_price_lasd_month': total_price_lasd_month,
                                                  'all_user': total_user, 'total_order_paid': total_paid_order,
                                                  'all_price': total_price_paid, 'total_unpaid_order': total_unpaid_order,
                                                  'toman': toman})

    def post(self, request):
        order = Order.objects.get(id=request.POST['orderid'])
        delivery_status = request.POST.get('delivery_status')
        paid_status = request.POST.get('paid_status')
        delivery_status = True if delivery_status == 'delivered' else False
        paid_status = True if paid_status == 'paid' else False
        order.deliver = delivery_status
        order.paid = paid_status
        order.save()
        if delivery_status == True:
            msg_sender(order.user.phone_number, f'{order.user.full_name} عزیز ، سفارش شما آماده و در حال ارسال است و تا چند ساعت دیگر بدست شما میرسد. \n فروشگاه گوشت دامیران')
       
        messages.success(request, 'تغییرات شما اعمال شد. مدیر محترم لطفا در تغییرات دقت لازم را داشته باشید!')
        return redirect('manager:manage')

    def test_func(self) -> bool | None:
        return self.request.user.is_authenticated and self.request.user.is_admin