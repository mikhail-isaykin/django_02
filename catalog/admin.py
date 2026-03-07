from django.contrib import admin
from .models import Category, Product, ProductImage


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_at', 'updated_at']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['name']

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'category', 'frame_color', 'lens_color', 'created_at']
    list_filter = ['category', 'is_polarized', 'shape', 'created_at']
    search_fields = ['name', 'description', 'frame_color', 'lens_color']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['price']
    raw_id_fields = ['category']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
    inlines = [ProductImageInline]
    
    fieldsets = (
        ('General', {
            'fields': ('name', 'slug', 'category', 'price')
        }),
        ('Eyewear Properties', {
            'fields': (
                'frame_color', 'lens_color', 'frame_material', 
                'shape', 'is_polarized'
            )
        }),
        ('Details', {
            'fields': ('description', 'details')
        }),
        ('Dimensions (Size & Fit)', {
            'fields': (
                'lens_width_mm', 'bridge_mm', 'frame_front_mm', 
                'temple_length_mm', 'lens_height_mm',
                'fit_narrow_wide', 'fit_low_high'
            )
        }),
    )


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['product', 'image', 'order']
    list_filter = ['product']
    list_editable = ['order']
    ordering = ['product', 'order']
