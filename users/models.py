from django.db import models
from django.conf import settings
from .utils import validate_avatar_size, avatar_upload_path


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile'
    )
    avatar = models.ImageField(upload_to=avatar_upload_path, blank=True, null=True, validators=[validate_avatar_size])
    bio = models.TextField(blank=True, null=True)
    phone = models.CharField(
        max_length=20, blank=True, null=True, verbose_name='Телефон'
    )
    date_of_birth = models.DateField(
        blank=True, null=True, verbose_name='Дата рождения'
    )
    location = models.CharField(
        max_length=100, blank=True, null=True, verbose_name='Город'
    )
    is_verified = models.BooleanField(default=False, verbose_name='Верифицирован')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'
        ordering = ['-updated_at']

    def __str__(self):
        return self.user.username
