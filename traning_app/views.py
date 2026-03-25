from django.http import HttpResponse, JsonResponse
from .models import Product, Category
from django.template import Template, Context
from decimal import Decimal
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.views.decorators.csrf import csrf_exempt


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


def product_detail_api(request, pk):
    try:
        data = get_object_or_404(Product, pk=pk)
        return JsonResponse({
            'id': data.pk,
            'name': data.name,
            'category': data.category.name,
            'price': data.price,
            'discount': data.discount,
            'rating': data.rating,
            'created_at': data.created_at.isoformat(),
        })
    except Http404:
        return JsonResponse({'error': 'Продукт не найден.'}, status=404)


@csrf_exempt
def update_price(request, product_id):
    if request.method == 'POST':
        new_price = request.POST.get('new_price')
        if not new_price:
            return JsonResponse(
                {'error': 'введите данные'},
                  status=400
            )
        product = Product.objects.filter(pk=product_id).update(price=new_price)
        if product == 0:
            return JsonResponse(
            {'error': 'такого продукта не существует'},
              status=404
        )
        return JsonResponse(
            {'success': True,
             'new_price': new_price}
        )
    return JsonResponse(
            {'error': 'отправьте POST запрос'},
            status=405
        )


def product_list_by_price(request):
    filters = {}
    min_price = request.GET.get('min_price')
    if min_price:
        filters['price__gte'] = min_price
    max_price = request.GET.get('max_price')
    if max_price:
        filters['price__lte'] = max_price
    data = Product.objects.filter(**filters)
    if data:
        html = '''
            <h1>Продукты по цене</h1>
            <p>Фильтры: {% if min_price and max_price %}От ${{ min_price }} До ${{ max_price }}
                        {% elif min_price %}От ${{ min_price }}
                        {% elif max_price %}До ${{ max_price }}
                        {% else %}Фильтров нет
                        {% endif %}</p>
            <ul>
            {% for product in data %}
                <li>{{ product.name }} (Категория: {{ product.category.name }}, Цена: ${{ product.price }}, Рейтинг: {{ product.rating }})</li>
            {% endfor %}
            </ul>
        '''
        template = Template(html)
        context = Context(
            {'min_price': min_price,
            'max_price': max_price,
            'data': data
            })
        return HttpResponse(template.render(context))
    return HttpResponse('Продуктов нет')
