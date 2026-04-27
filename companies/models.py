from django.db import models
from django.conf import settings
from core.utils import validate_image_size
from .utils import logo_upload_path
from django.core.validators import MinValueValidator


class Company(models.Model):
    owner = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='company'
    )
    name = models.CharField(max_length=255, verbose_name='Название')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    website = models.URLField(blank=True, null=True, verbose_name='Ссылка на сайт')
    logo = models.ImageField(
        upload_to=logo_upload_path,
        blank=True,
        null=True,
        verbose_name='Логотип',
        validators=[validate_image_size],
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Компания'
        verbose_name_plural = 'Компании'
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class Vacancy(models.Model):
    EMPLOYMENT_CHOICES = [
        ('full_time', 'Полная'),
        ('part_time', 'Частичная'),
        ('internship', 'Стажировка'),
        ('contract', 'Контракт'),
        ('remote', 'Удалённая работа'),
    ]
    SCHEDULE_CHOICES = [
        ('day', 'Дневные смены'),
        ('night', 'Ночные смены'),
        ('flexible', 'Гибкий график'),
        ('shift', 'Сменный график'),
        ('remote', 'Удалённо'),
    ]

    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name='vacancies'
    )
    title = models.CharField(max_length=255, verbose_name='Название вакансии')
    description = models.TextField(verbose_name='Общее описание')
    salary = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name='Зарплата',
    )
    experience = models.CharField(
        max_length=255, blank=True, null=True, verbose_name='Опыт работы'
    )
    employment_type = models.CharField(
        max_length=255,
        choices=EMPLOYMENT_CHOICES,
        default='full_time',
        verbose_name='Тип занятости',
    )
    schedule = models.CharField(
        max_length=255,
        choices=SCHEDULE_CHOICES,
        default='day',
        verbose_name='График работы',
    )
    working_hours = models.CharField(
        max_length=255, blank=True, null=True, verbose_name='Рабочие часы'
    )
    responsibilities = models.TextField(
        blank=True, null=True, verbose_name='Обязанности'
    )
    conditions = models.TextField(blank=True, null=True, verbose_name='Условия работы')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Вакансия'
        verbose_name_plural = 'Вакансии'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.title} в {self.company}'
