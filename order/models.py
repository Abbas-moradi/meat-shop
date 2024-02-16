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