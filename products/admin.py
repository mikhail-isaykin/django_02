from django.contrib import admin
from .models import Article, Profile


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'published_date']
    readonly_fields = ['slug']
    list_filter = ['author']
    search_fields = ['title']

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'bio', 'website', 'location']
    fieldsets = [
        ('Личная информация', {'fields': ['user', 'bio']}),
        ('Дополнительно', {'fields': ['website', 'location']}),
    ]
