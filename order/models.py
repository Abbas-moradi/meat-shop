from django.db import models
from accounts.models import User


class Order(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name='orders')
    paid = models.BooleanField(default=False)
    total_price = models.PositiveBigIntegerField()
    product_number = models.PositiveIntegerField()
    created = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)
    on_delete = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'order'
        verbose_name_plural = 'orders'
        ordering = ('created',)
    
    def __str__(self) -> str:
        return self.id
    

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_products')
    product_id = models.CharField(max_length=150)
    product_price = models.PositiveIntegerField()
    product_quantity = models.PositiveSmallIntegerField()
    total_price = models.PositiveIntegerField()
    created = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'orderproduct'
        verbose_name_plural = 'orderproducts'
        ordering = ('created',)
    
    def __str__(self) -> str:
        return self.id
