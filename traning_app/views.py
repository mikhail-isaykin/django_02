from django.http import HttpResponse, JsonResponse
from .models import Product, Category
from django.template import Template, Context
from decimal import Decimal
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.utils.decorators import method_decorator
from datetime import datetime


def product_list_by_category(request, category_name=None):
    if Category.objects.filter(name=category_name).exists():
        data = Product.objects.filter(category__name=category_name)
        if data:
            html = '''
                <h1>Продукты в категории {{ category_name }}</h1>
                <ul>
                {% for product in data %}
                    <li>{{ product.name }} (Цена: {{ product.price }})</li>
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


class HomePageCBV(View):
    def get(self, request):
        return HttpResponse('Добро пожаловать на главную страницу, используя Классовое Представление!')


@method_decorator(csrf_exempt, name='dispatch')
class ContactFormCBV(View):
    def get(self, request):
        return HttpResponse('Это страница контактов. Отправьте форму методом POST.')
    

    def post(self, request):
        email = request.POST.get('email')
        if email:
            return HttpResponse(f'Спасибо за ваше сообщение от: {email}')
        return HttpResponse('Пожалуйста, укажите ваш email.', status=400)


class ProductDetailCBV(View):
    def get(self, request, product_id):
        return HttpResponse(f'Вы просматриваете продукт с ID: {product_id}')


class SystemInfoCBV(View):
    def get(self, request):
        data = {
            'status': 'active',
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'message': 'Система работает нормально'
        }
        return JsonResponse(data, status=200)


    def post(self, request):
        return JsonResponse({
            'error': 'POST-запросы не разрешены.',
        }, status=405)


class AuthCheckCBV(View):
    def dispatch(self, request, *args, **kwargs):
        if not (auth_key := request.GET.get('auth_key')) or auth_key != 'secret123':
            return HttpResponse('Доступ запрещен: Неверный или отсутствующий auth_key.',
                                status=403)
        return super().dispatch(request, *args, **kwargs)
    

    def get(self, request):
        return HttpResponse('Привет! Вы успешно прошли проверку авторизации.')
    

class ProductRatingView(View):
    def get(self, request, product_id, user_rating):
        return HttpResponse(f'Продукт ID: {product_id}, получена оценка пользователя: {user_rating} (GET запрос)')
    

    def post(self, request, product_id):
        try:
            new_rating = int(request.POST.get('new_rating', 0))
            if new_rating and 1 <= new_rating <= 5:
                return HttpResponse(f'Продукт ID: {product_id}, новая оценка сохранена: {new_rating} (POST запрос)')
            return HttpResponse('Укажите оценку от 1 до 5.',
                                 status=400)
        except (ValueError, TypeError):
            return HttpResponse(f'Ошибка: Укажите корректную оценку от 1 до 5.',
                                 status=400)
