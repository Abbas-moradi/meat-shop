from django.contrib import admin
from order.models import Order, OrderItem


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'paid', 'total_price', 'created', 'shamsi','status', 'address', 'ref_id')

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'created', 'shamsi', 'status')