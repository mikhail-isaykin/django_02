"""
apps/catalog/views.py
CBV-вьюхи каталога. HTMX-запросы получают только партиал,
обычные запросы — полную страницу.
"""
from __future__ import annotations

from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView

from .models import Category, Product


class CatalogView(ListView):
    """Каталог товаров с фильтрацией по категории."""
    model               = Product
    template_name       = "catalog/index.html"
    context_object_name = "products"
    paginate_by         = 20

    # Партиал для HTMX-запросов (только сетка, без base.html)
    htmx_template = "catalog/partials/product_grid.html"

    def get_queryset(self):
        qs = (
            Product.objects
            .select_related("category")
            .prefetch_related("images")
            .distinct()
        )
        category_slug = self.request.GET.get("category")
        if category_slug:
            qs = qs.filter(category__slug=category_slug)
        return qs

    def get_template_names(self) -> list[str]:
        # HTMX-запрос → возвращаем только партиал (без полного layout)
        if self.request.headers.get("HX-Request"):
            return [self.htmx_template]
        return [self.template_name]

    def get_context_data(self, **kwargs) -> dict:
        ctx = super().get_context_data(**kwargs)
        ctx["categories"]       = Category.objects.all()
        ctx["active_category"]  = self.request.GET.get("category", "")
        return ctx


class ProductDetailView(DetailView):
    """Детальная страница товара."""
    model               = Product
    template_name       = "catalog/product_detail.html"
    context_object_name = "product"

    # Партиал для HTMX-запросов (без base.html)
    htmx_template       = "catalog/partials/product_detail_partial.html"

    def get_queryset(self):
        return (
            Product.objects
            .select_related("category")
            .prefetch_related("images")
        )

    def get_template_names(self) -> list[str]:
        if self.request.headers.get("HX-Request"):
            return [self.htmx_template]
        return [self.template_name]

    def get_context_data(self, **kwargs) -> dict:
        ctx = super().get_context_data(**kwargs)
        ctx["tabs"]       = ["Details", "Size & Fit", "Shipping & Returns"]
        # Случайные 2 товара из той же категории для "Complete the Look"
        ctx["look_items"] = (
            Product.objects
            .filter(category=self.object.category)
            .exclude(pk=self.object.pk)
            .prefetch_related("images")[:2]
        )
        return ctx
