from django.db import models


class Product(models.Model):
    name = models.CharField(max_length = 100)
    description = models.TextField()
    price = models.PositiveIntegerField()
    inventory = models.PositiveIntegerField()
    pic = models.ImageField(upload_to='product/')
    discount = models.PositiveSmallIntegerField()
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    economic = models.BooleanField(default=False)
    status = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'product'
        verbose_name_plural = 'products'
        ordering = ('created',)
    
    def __str__(self) -> str:
        return f'{self.name}-{self.status}'


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    pic = models.ImageField(upload_to='category/')
    created = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'
        ordering = ('created',)

    def __str__(self) -> str:
        return f'{self.name}-{self.status}'