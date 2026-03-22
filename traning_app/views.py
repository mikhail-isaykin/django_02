from django.http import HttpResponse
from .models import Product, Category
from django.template import Template, Context
from decimal import Decimal


def product_list_by_category(request, category_name=None):
    if Category.objects.filter(name=category_name).exists():
        data = Product.objects.filter(category__name=category_name)
        if data:
            html = '''
                <h1>Продукты в категории {{ category_name }}</h1>
                <ul>
                {% for product in data %}
                    <li>{{ product.name }} (Цена: {{ product.price }}, Рейтинг: {{ product.rating }})</li>
                {% endfor %}
                </ul>
            '''
            template = Template(html)
            context = Context({'category_name': category_name, 'data': data})
            return HttpResponse(template.render(context))
        return HttpResponse('Продуктов нет')
    return HttpResponse('Такой категории нет')


def  top_products(request):
    min_rating = float(request.GET.get('min_rating', 0))
    min_discount = Decimal(request.GET.get('min_discount', 0))
    data = Product.objects.filter(rating__gte=min_rating, discount__gte=min_discount).order_by('-rating')
    if data:
        html = '''
                <h1>Лучшие Продукты:</h1>
                <p>Минимальный рейтинг: {{ min_rating }}</p>
                <p>Минимальная скидка: {{ min_discount }}</p>
                <ul>
                {% for product in data %}
                    <li>{{ product.name }} (Категория: {{ product.category.name }}, Цена: ${{ product.price }}, Скидка: {{ product.discount }}%, Рейтинг: {{ product.rating }})</li>
                {% endfor %}
                </ul>
            '''
        template = Template(html)
        context = Context({'min_rating': min_rating, 'min_discount': min_discount, 'data': data})
        return HttpResponse(template.render(context))
    return HttpResponse('Продуктов нет')
