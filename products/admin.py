from django.contrib import admin
from .models import Product, Category, Gallery


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('id', 'name', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('name',)
    readonly_fields = ('created_at', 'updated_at')


'''@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = (
        'id',
        'name',
        'sku',
        'category',
        'price',
        'stock',
        'is_active',
        'created_at',
    )
    list_filter = ('category', 'is_active')
    search_fields = ('name',)
    readonly_fields = ('created_at', 'updated_at')'''

@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ('id',)
