from django.contrib import admin
from .models import Company, Vacancy, FeedbackCompany


@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Компания', {'fields': ('company',)}),
        ('Основное', {'fields': ('title', 'description', 'salary', 'experience')}),
        ('Условия', {'fields': ('employment_type', 'schedule', 'working_hours')}),
        ('Подробности', {'fields': ('responsibilities', 'conditions')}),
        ('Даты', {'fields': ('created_at', 'updated_at')}),
    )
    readonly_fields = ('created_at', 'updated_at')
    list_display = (
        'id',
        'title',
        'company',
        'employment_type',
        'schedule',
        'salary',
        'created_at',
    )
    list_filter = ('employment_type', 'schedule', 'created_at')
    search_fields = ('title', 'company__name')


class VacancyInline(admin.StackedInline):
    model = Vacancy
    can_delete = True
    extra = 0


@admin.register(FeedbackCompany)
class FeedbackCompanyAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'updated_at')
    list_display = ('company', 'rating', 'company_average_rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('company__name', 'comment')

    def company_average_rating(self, obj):
        return obj.company.average_rating

    company_average_rating.short_description = 'Средний рейтинг компании'


class FeedbackCompanyInline(admin.StackedInline):
    model = FeedbackCompany
    can_delete = True
    extra = 0


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Владелец', {'fields': ('owner',)}),
        ('Основное', {'fields': ('name', 'description', 'website', 'logo')}),
        ('Даты', {'fields': ('created_at',)}),
    )
    readonly_fields = ('created_at',)
    list_display = ('name', 'owner', 'created_at')
    search_fields = ('name', 'owner__username', 'owner__email')
    list_filter = ('created_at',)
    inlines = (VacancyInline, FeedbackCompanyInline)
