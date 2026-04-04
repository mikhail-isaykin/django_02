from django.views import View
from django.shortcuts import get_object_or_404
from .models import Manufacturer, Product
from django.http import HttpResponse, JsonResponse
from django.template import Template, Context
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, RedirectView, ListView, DetailView, FormView
from datetime import date
from django.db.models import Count, Q, F
from django.urls import reverse, reverse_lazy
from django.db.models.functions import Abs
from .forms import ContactForm, FeedbackForm, NewsletterSignupForm, ShippingCalculatorForm, ProductSearchForm, AskQuestionForm
from decimal import Decimal

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


'''class ManufacturerListView(TemplateView):
    template_name = 'webshop/manufacturer_list.html'


    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        country = self.request.GET.get('country')
        manufacturers = Manufacturer.objects.all()
        if country:
            manufacturers = manufacturers.filter(country__icontains=country)
        manufacturers = manufacturers.annotate(active_product_count=Count('products', filter=Q(products__is_available=True)))
        context['manufacturers'] = manufacturers
        context['country'] = country
        return context'''


class RedirectToHomeView(RedirectView):
    pattern_name = 'project_home'


class OldProductURLRedirectView(RedirectView):
    pattern_name = 'product_detail'
    permanent = True


    def get_redirect_url(self, *args, **kwargs):
        old_sku = kwargs.get('old_sku')
        return reverse('product_detail', kwargs={'product_sku': old_sku})


'''class ProductSearchView(ListView):
    model = Product
    template_name = 'webshop/product_search.html'
    context_object_name = 'products'

    def get_queryset(self):
        queryset = Product.objects.all()
        q = self.request.GET.get('q')
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')

        if q:
            queryset = queryset.filter(name__icontains=q)
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        return queryset'''


class LegacySearchRedirectView(RedirectView):
    pattern_name = 'product_search'
    query_string = True


class ManufacturerLookupRedirectView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        name = self.request.GET.get('name')
        manufacturer = Manufacturer.objects.filter(name__iexact=name).first()
        if manufacturer:
            return reverse('manufacturer_products', kwargs={'manufacturer_id': manufacturer.id})
        return reverse('manufacturer_list')


class ProductUnavailableView(TemplateView):
    template_name = 'webshop/product_unavailable.html'
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        product_sku = self.request.GET.get('product_sku')
        context['product_sku'] = product_sku
        return context


class ProductAvailabilityRedirectView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        product_sku = kwargs.get('product_sku')
        product = Product.objects.filter(sku=product_sku).first()
        if product and product.is_available == True and product.stock_quantity > 0:
            return reverse('product_detail', kwargs={'product_sku': product_sku})
        return f"{reverse('product_unavailable')}?product_sku={product_sku}"


class ManufacturerDetailView(DetailView):
    model = Manufacturer
    template_name = 'webshop/manufacturer_detail.html'


class ProductDetailBySkuView(DetailView):
    model = Product
    template_name = 'webshop/product_detail.html'
    slug_field = 'sku'
    slug_url_kwarg = 'product_sku'


class ManufacturerProductsDetailView(DetailView):
    model = Manufacturer
    template_name = 'webshop/manufacturer_detail_with_products.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = self.object.products.all()
        context['products'] = products
        return context


class ProductDetailWithViewCount(DetailView):
    model = Product
    template_name = 'webshop/product_detail.html'
    slug_field = 'sku'
    slug_url_kwarg = 'product_sku'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.object
        product_views = self.request.session.setdefault(product.sku, 0) + 1
        context['view_count_in_session'] = self.request.session[product.sku] = product_views
        self.request.session.modified = True
        return context


class ProductDetailWithSimilarPriceView(DetailView):
    model = Product
    template_name = 'webshop/product_detail.html'
    slug_field = 'sku'
    slug_url_kwarg = 'product_sku'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.object
        similar_products = Product.objects.filter(manufacturer=product.manufacturer).exclude(pk=product.pk)
        similar_price_products = similar_products.annotate(
            diff_price=Abs(F('price') - product.price)
            ).filter(diff_price__lte=750).order_by('diff_price')
        context['similar_price_products'] = similar_price_products
        return context


class ManufacturerListView(ListView):
    model = Manufacturer
    template_name = 'webshop/manufacturer_list.html'
    context_object_name = 'manufacturer_list'
    paginate_by = 5 


class ProductFilteredListView(ListView):
    template_name = 'webshop/product_list_filtered.html'
    paginate_by = 5 


    def get_queryset(self):
        queryset = Product.objects.filter(is_available=True)
        self.manufacturer_name = self.request.GET.get('manufacturer_name')
        if self.manufacturer_name:
            queryset = queryset.filter(manufacturer__name=self.manufacturer_name)
        return queryset.order_by('name')
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_manufacturer_name'] = self.manufacturer_name
        return context


class ProductSortableListView(ListView):
    template_name = 'webshop/product_list_sortable.html'
    context_object_name = 'product_list'
    paginate_by = 15


    def get_queryset(self):
        valid_fields = ['name', '-name', 'price', '-price', 'stock_quantity', '-stock_quantity']
        sort_by = self.request.GET.get('sort_by')
        self.sort_by = 'name' if sort_by not in valid_fields else sort_by
        queryset = Product.objects.all().order_by(self.sort_by)
        return queryset
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_sort_by'] = self.sort_by
        return context


class ManufacturerStatsListView(ListView):
    template_name = 'webshop/manufacturer_list_with_stats.html'
    context_object_name = 'manufacturer_list'
    paginate_by = 5


    def get_queryset(self):
        queryset = Manufacturer.objects.annotate(
            available_count = Count('products', filter=Q(products__is_available=True)),
            unavailable_count = Count('products', filter=Q(products__is_available=False))
        )
        return queryset


class ProductAdvancedFilterListView(ListView):
    template_name = 'webshop/product_list_advanced_filter.html'
    context_object_name = 'product_list'
    paginate_by = 10


    def get_queryset(self):
        queryset = Product.objects.all()
        self.available_raw = self.request.GET.get('available')
        available = self.available_raw
        if available in ('true', 'false'):
            available = available == 'true'
        self.min_price = self.request.GET.get('min_price', 0)
        if isinstance(available, bool):
            queryset = queryset.filter(is_available=available)
        queryset = queryset.filter(price__gte=self.min_price)
        return queryset


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_available'] = self.available_raw
        context['current_min_price'] = self.min_price
        return context


class ContactFormView(FormView):
    form_class = ContactForm
    template_name = 'webshop/contact_form.html'
    success_url = reverse_lazy('contact_success')


    def form_valid(self, form):
        name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        message = form.cleaned_data['message']
        print(f'Отправлено сообщение от {name} ({email}): {message}')
        return super().form_valid(form)


class FeedbackFormView(FormView):
    form_class = FeedbackForm
    template_name = 'webshop/feedback_form.html'


    def form_valid(self, form):
        self.form = form
        rating = form.cleaned_data['rating']
        comment = form.cleaned_data['comment']
        email = form.cleaned_data['email']
        print(f'Рейтинг: {rating}, Комментарий: {comment}, Почта: {email}')
        return super().form_valid(form)


    def get_success_url(self):
        rating = self.form.cleaned_data.get('rating')
        return reverse('feedback-thank-you') + f'?rating={rating}'
    

class FeedbackThankYouView(TemplateView):
    template_name = 'webshop/feedback_thank_you.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        rating = self.request.GET.get('rating')
        context['rating'] = rating
        return context


class NewsletterSignupView(FormView):
    form_class = NewsletterSignupForm
    template_name = 'webshop/newsletter_signup.html'
    success_url = reverse_lazy('newsletter_success')


    def form_valid(self, form):
        email = form.cleaned_data['email']
        print(email)
        return super().form_valid(form)


class ShippingCalculatorView(FormView):
    form_class = ShippingCalculatorForm
    template_name = 'webshop/shipping_calculator.html'
    success_url = reverse_lazy('shipping_calculator_page')


    def form_valid(self, form):
        weight = form.cleaned_data['weight']
        distance = form.cleaned_data['distance']
        shipping_cost = (weight * 50) + (distance * 10)
        self.request.session['shipping_cost'] = str(shipping_cost)
        self.request.session.modified = True
        return super().form_valid(form)
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        shipping_cost = Decimal(self.request.session.get('shipping_cost'))
        context['shipping_cost'] = shipping_cost
        if 'shipping_cost' in self.request.session:
            del self.request.session['shipping_cost']
        return context


class ProductSearchView(FormView):
    form_class = ProductSearchForm
    template_name = 'webshop/product_search.html'
    

    def get_form_kwargs(self, **kwargs):
        kwargs = super().get_form_kwargs(**kwargs)
        kwargs['data'] = self.request.GET
        return kwargs
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = context['form']
        filters = {}
        if form.is_valid():
            query = form.cleaned_data['query']
            if query is not None:
                filters['name__icontains'] = query
            max_price = form.cleaned_data['max_price']
            if max_price is not None:
                filters['price__lte'] = max_price
        products = Product.objects.filter(**filters)
        context['products'] = products
        return context


class AskQuestionView(FormView):
    form_class = AskQuestionForm
    template_name = 'webshop/ask_question_form.html'
    success_url = reverse_lazy('ask_sent_page')


    def form_valid(self, form):
        name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        question = form.cleaned_data['question']
        print(f'--- Новый вопрос ---')
        print(f'От: {name} <{email}>')
        print(f'Вопрос: {question}')
        print(f'--------------------')
        return super().form_valid(form)


class QuestionSentView(TemplateView):
    template_name = 'webshop/question_sent.html'
