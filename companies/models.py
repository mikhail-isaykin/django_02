from django.db import models
from django.conf import settings
from .utils import logo_upload_path


class Company(models.Model):
    owner = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='company'
    )
    name = models.CharField(max_length=255, verbose_name='Название')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    website = models.URLField(blank=True, null=True, verbose_name='Ссылка на сайт')
    logo = models.ImageField(
        upload_to=logo_upload_path, blank=True, null=True, verbose_name='Логотип'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Компания'
        verbose_name_plural = 'Компании'
        ordering = ['-created_at']

    def __str__(self):
        return self.name
