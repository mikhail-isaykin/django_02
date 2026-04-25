from django.contrib import admin
from .models import Article, Profile, Author, Book


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

#
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'published_date']
    list_filter = ['published_date']
    search_fields = ['title', 'author__name']
    ordering = ['-published_date']
    readonly_fields = ['created_at']
    fields = ['title', 'description', 'author', 'published_date']


class BookTabularInline(admin.TabularInline):
    model = Book
    fields = ['author', 'title', 'description', 'published_date', 'internal_notes', 'created_at']
    readonly_fields = ['created_at']
    extra = 1
    can_delete = True


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Основная информация', {'fields': ['name', 'birth_date']}),
        ('Контакт', {'fields': ['email']}),
    ]
    inlines = [BookTabularInline]
