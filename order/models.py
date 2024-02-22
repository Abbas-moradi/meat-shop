from django.db import models
from accounts.models import User


class Order(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name='orders')
    total_price = models.PositiveBigIntegerField()
    product_number = models.PositiveIntegerField()
    tax = models.PositiveIntegerField()
    finally_price = models.PositiveIntegerField()
    address = models.TextField()
    paid = models.BooleanField(default=False)
    deliver = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    shamsi = models.CharField(max_length=150)
    status = models.BooleanField(default=True)
    on_delete = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'order'
        verbose_name_plural = 'orders'
        ordering = ('created',)
    
    def __str__(self) -> str:
        return str(self.id)
    

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_products')
    product_id = models.CharField(max_length=150)
    product_price = models.PositiveIntegerField()
    product_quantity = models.PositiveSmallIntegerField()
    total_price = models.PositiveIntegerField()
    created = models.DateTimeField(auto_now_add=True)
    shamsi = models.CharField(max_length=150)
    status = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'orderitem'
        verbose_name_plural = 'orderitems'
        ordering = ('created',)
    
    def __str__(self) -> str:
        return str(self.id)
