from django.db import models


class Product(models.Model):
    name = models.CharField(max_length = 100)
    description = models.TextField()
    price = models.PositiveIntegerField()
    inventory = models.PositiveIntegerField()
    pic = models.ImageField(upload_to='product/')
    discount = models.PositiveSmallIntegerField()
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    economic = models.BooleanField(defualt=False)
    status = models.BooleanField(defualt=True)
    created = models.DateTimeField(auto_add_now=True)

    class Meta:
        verbose_name = 'product'
        verbose_name_plural = 'products'
        ordering = ('created',)
    
    def __str__(self) -> str:
        return f'{self.name}-{self.status}'
