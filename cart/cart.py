"""
apps/cart/cart.py
Класс Cart — ООП-обёртка над Django session.
Принципы: DRY, инкапсуляция, type hints.
"""
from __future__ import annotations

from decimal import Decimal
from typing import Iterator

from django.conf import settings
from django.http import HttpRequest

from catalog.models import Product

CART_SESSION_KEY: str = "eyeshop_cart"


class CartItem:
    """Представляет один элемент корзины."""
    __slots__ = ("product_id", "name", "price", "image_url", "size", "color", "qty")

    def __init__(self, data: dict) -> None:
        self.product_id: str    = data["product_id"]
        self.name:       str    = data["name"]
        self.price:      Decimal = Decimal(data["price"])
        self.image_url:  str    = data.get("image_url", "")
        self.size:       str    = data.get("size", "")
        self.color:      str    = data.get("color", "")
        self.qty:        int    = int(data.get("qty", 1))

    @property
    def total_price(self) -> Decimal:
        return self.price * self.qty

    def to_dict(self) -> dict:
        return {
            "product_id": self.product_id,
            "name":       self.name,
            "price":      str(self.price),
            "image_url":  self.image_url,
            "size":       self.size,
            "color":      self.color,
            "qty":        self.qty,
        }


class Cart:
    """
    Корзина, хранящаяся в Django-сессии.
    Ключ в сессии: CART_SESSION_KEY.
    """

    def __init__(self, request: HttpRequest) -> None:
        self.session = request.session
        self._data: dict[str, dict] = self.session.get(CART_SESSION_KEY, {})

    # ── Внутренние методы ──────────────────────────────────────

    def _key(self, product_id: int | str, size: str, color: str) -> str:
        """Уникальный ключ элемента корзины."""
        return f"{product_id}|{size}|{color}"

    def _save(self) -> None:
        """Сохраняем изменения в сессии."""
        self.session[CART_SESSION_KEY] = self._data
        self.session.modified = True

    # ── Публичный API ──────────────────────────────────────────

    def add(self, product: Product, size: str, color: str, qty: int = 1) -> None:
        """Добавляет товар или увеличивает количество."""
        key = self._key(product.id, size, color)
        if key in self._data:
            self._data[key]["qty"] += qty
        else:
            image_url = ""
            if product.main_image:
                image_url = product.main_image.image.url
            self._data[key] = {
                "product_id": str(product.id),
                "name":       product.name,
                "price":      str(product.price),
                "image_url":  image_url,
                "size":       size,
                "color":      color,
                "qty":        qty,
            }
        self._save()

    def update(self, product_id: int | str, size: str, color: str, qty: int) -> None:
        """Обновляет количество. Удаляет если qty <= 0."""
        key = self._key(product_id, size, color)
        if key not in self._data:
            return
        if qty <= 0:
            self.remove(product_id, size, color)
        else:
            self._data[key]["qty"] = qty
            self._save()

    def remove(self, product_id: int | str, size: str, color: str) -> None:
        key = self._key(product_id, size, color)
        self._data.pop(key, None)
        self._save()

    def clear(self) -> None:
        self._data = {}
        self._save()

    def __iter__(self) -> Iterator[CartItem]:
        for item_data in self._data.values():
            yield CartItem(item_data)

    def __len__(self) -> int:
        return sum(item["qty"] for item in self._data.values())

    @property
    def total(self) -> Decimal:
        return sum(
            Decimal(item["price"]) * item["qty"]
            for item in self._data.values()
        )

    def to_summary(self) -> dict:
        """JSON-ответ для Alpine.js (счётчик и сумма)."""
        return {
            "count": len(self),
            "total": float(self.total),
        }
