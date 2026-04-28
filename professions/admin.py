from django.contrib import admin
from .models import CategoryProfession, Profession


@admin.register(Profession)
class ProfessionAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    list_filter = ('category',)
    search_fields = ('name', 'category__name')


class ProfessionInline(admin.StackedInline):
    model = Profession
    can_delete = True
    extra = 0


@admin.register(CategoryProfession)
class CategoryProfessionAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name',)
    search_fields = ('name',)
    inlines = [ProfessionInline]
