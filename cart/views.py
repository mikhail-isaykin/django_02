"""
apps/cart/views.py
HTMX-вьюхи корзины. Все POST-запросы возвращают
HX-Trigger заголовок для синхронизации Alpine.js.
"""
from __future__ import annotations

import json

from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View
from django.views.generic import TemplateView

from catalog.models import Product
from .cart import Cart


class CartSummaryView(View):
    """GET /cart/summary/ — JSON для Alpine.js initCart()."""

    def get(self, request: HttpRequest) -> JsonResponse:
        cart = Cart(request)
        return JsonResponse(cart.to_summary())


class CartDetailView(TemplateView):
    """
    GET /cart/ — HTML-партиал со списком товаров.
    Подгружается через HTMX при открытии сайдбара.
    """
    template_name = "cart/partials/cart_items.html"

    def get_context_data(self, **kwargs) -> dict:
        ctx = super().get_context_data(**kwargs)
        ctx["cart"] = Cart(self.request)
        return ctx


class CartAddView(View):
    """POST /cart/add/<product_id>/ — добавить товар."""

    def post(self, request: HttpRequest, product_id: int) -> HttpResponse:
        product = get_object_or_404(Product.objects.prefetch_related("images"), pk=product_id)
        cart    = Cart(request)

        # Парсим тело запроса (HTMX отправляет JSON или form-data)
        try:
            body  = json.loads(request.body)
            size  = body.get("size", "")
            color = body.get("color", "")
            qty   = int(body.get("qty", 1))
        except (json.JSONDecodeError, ValueError):
            size  = request.POST.get("size", "")
            color = request.POST.get("color", "")
            qty   = int(request.POST.get("qty", 1))

        cart.add(product, size=size, color=color, qty=qty)

        # HX-Trigger синхронизирует Alpine.js cartStore
        response = HttpResponse(status=204)
        response["HX-Trigger"] = json.dumps({
            "cartUpdated": cart.to_summary()
        })
        return response


class CartUpdateView(View):
    """POST /cart/update/ — изменить количество."""

    def post(self, request: HttpRequest) -> HttpResponse:
        cart = Cart(request)
        data = json.loads(request.body)
        cart.update(
            product_id=data["product_id"],
            size=data["size"],
            color=data["color"],
            qty=int(data["qty"]),
        )
        # Возвращаем обновлённый HTML-партиал + триггер
        response = HttpResponse(status=204)
        response["HX-Trigger"] = json.dumps({"cartUpdated": cart.to_summary()})
        return response


class CartRemoveView(View):
    """POST /cart/remove/ — удалить товар."""

    def post(self, request: HttpRequest) -> HttpResponse:
        cart = Cart(request)
        data = json.loads(request.body)
        cart.remove(data["product_id"], data["size"], data["color"])
        response = HttpResponse(status=204)
        response["HX-Trigger"] = json.dumps({"cartUpdated": cart.to_summary()})
        return response
