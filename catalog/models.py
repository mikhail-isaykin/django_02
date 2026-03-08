"""
apps/catalog/models.py
Модели каталога: Category, Product, ProductImage.
Принципы: ООП, DRY (абстрактная модель TimeStampedModel), type hints.
"""
from __future__ import annotations

import json
from decimal import Decimal

from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class TimeStampedModel(models.Model):
    """Абстрактная модель: created_at и updated_at для всех дочерних."""
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at  = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(TimeStampedModel):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120, unique=True)

    class Meta:
        verbose_name_plural = "categories"
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs) -> None:
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Product(TimeStampedModel):
    name        = models.CharField(max_length=200)
    slug        = models.SlugField(max_length=220, unique=True)
    price       = models.DecimalField(max_digits=8, decimal_places=2)
    category    = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="products")
    description = models.TextField(blank=True, help_text="Example: Wraparound Sunglasses in Blue Nylon")
    details     = models.JSONField(default=list, help_text='List of details, e.g. ["Blue Nylon Frame", "Blue Mirror Lenses"]')
    # Size and Fit
    lens_width_mm    = models.PositiveIntegerField(null=True, blank=True, help_text="Lens width: 59 mm")
    bridge_mm        = models.PositiveIntegerField(null=True, blank=True, help_text="Bridge: 14 mm")
    frame_front_mm   = models.PositiveIntegerField(null=True, blank=True, help_text="Frame front: 155 mm")
    temple_length_mm = models.PositiveIntegerField(null=True, blank=True, help_text="Temple length: 111 mm")
    lens_height_mm   = models.PositiveIntegerField(null=True, blank=True, help_text="Lens height: 30 mm")
    
    # Fit percentages (0-100)
    fit_narrow_wide  = models.PositiveIntegerField(default=50, help_text="Fit Narrow (0) to Wide (100)")
    fit_low_high     = models.PositiveIntegerField(default=50, help_text="Fit Low (0) to High (100)")

    # Specific Eyewear Fields
    frame_color    = models.CharField(max_length=100, blank=True)
    lens_color     = models.CharField(max_length=100, blank=True)
    frame_material = models.CharField(max_length=100, blank=True, help_text="e.g. Acetate, Metal, Nylon")
    shape          = models.CharField(max_length=100, blank=True, help_text="e.g. Square, Round, Cat-eye, Wraparound")
    is_polarized   = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self) -> str:
        return reverse("catalog:product_detail", kwargs={"slug": self.slug})

    @property
    def main_image(self):
        """Возвращает главное изображение товара."""
        images = list(self.images.all())
        if not images:
            return None
        return next((img for img in images if img.order == 0), images[0])

    @property
    def images_json(self) -> str:
        """Список URL изображений для Alpine.js (JSON)."""
        urls = [img.image.url for img in self.images.all()]
        return json.dumps(urls)

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image   = models.ImageField(upload_to="products/")
    order   = models.PositiveSmallIntegerField(default=0, db_index=True)

    class Meta:
        ordering = ["order"]
