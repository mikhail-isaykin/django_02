from django.contrib import admin
from .models import Article


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'published_date']
    list_filter = ['author']
    search_fields = ['title']
    readonly_fields = ['slug', 'published_date'] 
