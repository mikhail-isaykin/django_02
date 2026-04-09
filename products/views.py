from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Category, Product


class HomePageView(TemplateView):
    template_name = ''


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Category.objects.filter(is_active=True)
        selected_category = self.request.get.GET('category')
        products = Product.objects.filter(category_name=selected_category)
        context['categories'] = categories
        context['selected_category'] = selected_category
        context['products'] = products
        return context
