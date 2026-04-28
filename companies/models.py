from django.db import models
from django.conf import settings
from core.utils import validate_image_size
from .utils import logo_upload_path
from django.core.validators import MinValueValidator
from professions.models import Profession


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

    @property
    def average_rating(self):
        feedbacks = self.feedbacks.values_list('rating', flat=True)
        if feedbacks:
            return round(sum(feedbacks) / len(feedbacks), 1)
        return 0


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
    SALARY_TYPE_CHOICES = [
        ('weekly', 'Раз в неделю'),
        ('monthly', 'Раз в месяц'),
        ('twice_monthly', '2 раза в месяц'),
        ('daily', 'Ежедневно'),
        ('hourly', 'По часам'),
        ('negotiable', 'Договорная'),
    ]
    EXPERIENCE_CHOICES = [
        ('with_experience', 'С опытом'),
        ('without_experience', 'Без опыта'),
    ]
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name='vacancies',
    )
    profession = models.ForeignKey(
        Profession, on_delete=models.CASCADE, related_name='vacancies'
    )
    title = models.CharField(max_length=255, verbose_name='Название вакансии')
    description = models.TextField(verbose_name='Общее описание')
    salary = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name='Зарплата',
    )
    salary_type = models.CharField(
        max_length=255,
        choices=SALARY_TYPE_CHOICES,
        verbose_name='Тип зарплаты',
    )
    experience = models.CharField(
        max_length=255, blank=True, null=True, verbose_name='Опыт работы'
    )
    experience_required = models.CharField(
        max_length=50,
        choices=EXPERIENCE_CHOICES,
        verbose_name='Требуемый опыт',
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


class FeedbackCompany(models.Model):
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name='feedbacks'
    )
    comment = models.TextField(verbose_name='Отзыв')
    rating = models.PositiveSmallIntegerField(
        choices=[(i, str(i)) for i in range(1, 6)], verbose_name='Рейтинг'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Отзыв о компании'
        verbose_name_plural = 'Отзывы о компаниях'
        ordering = ['-created_at']

    def __str__(self):
        return f'Отзыв о {self.company} — {self.rating}/5'
