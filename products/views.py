from django.views.generic import TemplateView, DetailView
from .models import Category, Product
from django.contrib import messages
from django.shortcuts import render


class HomePageView(TemplateView):
    template_name = 'products/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Category.objects.filter(is_active=True)
        selected_category = self.request.GET.get('category')
        products = Product.objects.filter(
            category__slug=selected_category, is_active=True
        )
        context['categories'] = categories
        context['selected_category'] = selected_category
        context['products'] = products
        return context
