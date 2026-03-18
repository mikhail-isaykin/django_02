from django.http import HttpResponse
from .models import Product, Category


def product_list_by_category(request, category_name=None):
    if Category.objects.filter(name=category_name).exists()
    data = Product.objects.filter(category__name=category_name)
    if data:
        .....