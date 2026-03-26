from django.views import View
from django.shortcuts import get_object_or_404
from .models import Manufacturer, Product
from django.http import HttpResponse
from django.template import Template, Context


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
