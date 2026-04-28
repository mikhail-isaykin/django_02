from django.contrib import admin
from .models import Profile
from django.contrib.auth import get_user_model
from resumes.admin import ResumeInline

User = get_user_model()


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Пользователь', {'fields': ('user', 'is_verified')}),
        (
            'Личные данные',
            {'fields': ('avatar', 'bio', 'phone', 'date_of_birth', 'location')},
        ),
        ('Даты', {'fields': ('created_at', 'updated_at')}),
    )
    readonly_fields = ('created_at', 'updated_at')
    list_display = ('user', 'is_verified', 'created_at')
    search_fields = ('user__username', 'user__email', 'phone', 'location')
    list_filter = ('is_verified', 'created_at')


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    extra = 0


class UserAdmin(admin.ModelAdmin):
    inlines = (ProfileInline, ResumeInline)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
