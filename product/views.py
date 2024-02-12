from django.shortcuts import render, get_object_or_404
from .models import Product
from django.views import  View


class ProductDetail(View):
    detail_temp = 'inc/detail.html'

    def get(self, request, slug):
        product = get_object_or_404(Product, slug=slug)
        totalprice = int(product.price)*(product.inventory)
        return render(request, self.detail_temp, {'product': product,
                                                  'totalprice': totalprice})