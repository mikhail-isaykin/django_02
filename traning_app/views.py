from django.http import HttpResponse
from .models import Product, Category
from django.template import Template, Context


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
