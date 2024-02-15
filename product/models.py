from django.db import models
from django.urls import reverse


class Product(models.Model):
    name = models.CharField(max_length = 200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField()
    price = models.PositiveIntegerField()
    inventory = models.PositiveIntegerField()
    number = models.PositiveSmallIntegerField(default=1)
    pic = models.ImageField(upload_to='product/')
    discount = models.PositiveSmallIntegerField()
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='products')
    economic = models.BooleanField(default=False)
    status = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'product'
        verbose_name_plural = 'products'
        ordering = ('created',)
    
    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        return reverse('product:product_detail', args=[self.slug,])
    
    
class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(null=True, blank=True)
    pic = models.ImageField(upload_to='category/')
    created = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'
        ordering = ('created',)

    def __str__(self) -> str:
        return f'{self.name}'