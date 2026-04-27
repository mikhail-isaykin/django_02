from django.contrib import admin
from .models import Company


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Владелец', {'fields': ['owner']}),
        ('Основное', {'fields': ['name', 'description', 'website', 'logo']}),
        ('Даты', {'fields': ['created_at']}),
    ]
    readonly_fields = ['created_at']
    list_display = ['name', 'owner', 'created_at']
    search_fields = ['name', 'owner__username', 'owner__email']
    list_filter = ['created_at']
