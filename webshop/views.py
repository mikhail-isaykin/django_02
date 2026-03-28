from django.views import View
from django.shortcuts import get_object_or_404
from .models import Manufacturer, Product
from django.http import HttpResponse, JsonResponse
from django.template import Template, Context
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from datetime import date


class ManufacturerProductsView(View):
    def get(self, request, manufacturer_id):
        manufacturer = get_object_or_404(Manufacturer, pk=manufacturer_id)
        data = Product.objects.filter(manufacturer=manufacturer)
        data_count = data.count()
        items_per_page = 2
        while items_per_page > data_count:
            items_per_page -= 1
        page = int(request.GET.get('page', 1))
        total_pages = (data_count + items_per_page - 1) // items_per_page  # округление вверх
        if page < 1 or page > total_pages:
            return HttpResponse('Страница не найдена', status=404)
        start = (page - 1) * items_per_page
        end = start + items_per_page
        current_page_data = data[start:end]
        html = '''
            <h1>Производитель: {{ manufacturer.name }}</h1>
            <p>Продукты:</p>
            <ul>
            {% for product in current_page_data %}
                <li>{{ product.name }} (Цена: {{ product.price }})</li>
            {% endfor %}
            </ul>
            <p>Страница {{ page }} из {{ total_pages }}</p>
        '''
        template = Template(html)
        context = Context({'manufacturer': manufacturer,
                           'current_page_data': current_page_data,
                           'total_pages': total_pages,
                           'page': page})
        
        return HttpResponse(template.render(context))


@method_decorator(csrf_exempt, name='dispatch')
class UpdateProductAvailabilityView(View):
    def dispatch(self, request, *args, **kwargs):
        if not request.method =='POST':
            return JsonResponse({
                'error': 'Метод не разрешен.'
            }, status=405)
        sku = kwargs['sku']
        try:
            product = Product.objects.get(sku=sku)
        except Product.DoesNotExist:
            return JsonResponse({
                'error': 'Продукт не найден.'
            }, status=404)
        self.product = product
        return super().dispatch(request, *args, **kwargs)
    

    def post(self, request, sku):
        new_status = request.POST.get('status')
        if new_status in ('true', 'false'):
            self.product.is_available = new_status == 'true'
            self.product.save()
            return JsonResponse({
                'message': 'Статус обновлен.',
                'is_available': self.product.is_available
            })
        return JsonResponse({
            'error': 'Недопустимое значение статуса.'
            }, status=400)


class AboutUsView(TemplateView):
    template_name = 'webshop/about.html'


class WelcomeHomeView(TemplateView):
    template_name = 'webshop/home.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_year'] = date.today().year
        name = self.request.GET.get('name', 'Гость')
        context['username'] =  name
        return context


class FAQView(TemplateView):
    template_name = 'webshop/faq.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['faq_items'] = [{'question': 'Что вы продаете?', 'answer': 'Электроника, книги, одежда.'},
                                {'question': 'Как сделать заказ?', 'answer': 'Добавьте товары в корзину и оформите заказ.'}]
        return context


class ProductDetailWithRelatedView(TemplateView):
    template_name = 'webshop/product_detail_with_related.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product_sku = kwargs.get('product_sku')
        product = get_object_or_404(Product, sku=product_sku)
        related_products = Product.objects.filter(manufacturer=product.manufacturer).exclude(pk=product.pk)
        context['product'] = product
        context['related_products'] = related_products
        return context
