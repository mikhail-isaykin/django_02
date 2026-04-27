from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator


class Resume(models.Model):
    GENDER_CHOICES = [
        ('male', 'Мужчина'),
        ('female', 'Женщина'),
]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='resumes')
    first_name = models.CharField(max_length=255, verbose_name='Имя')
    last_name = models.CharField(max_length=255, verbose_name='Фамилия')
    middle_name = models.CharField(max_length=255, blank=True, null=True, verbose_name='Отчество')
    gender = models.CharField(max_length=255, choices=GENDER_CHOICES, blank=True, null=True, verbose_name='Пол')
    phone = models.CharField(max_length=255, unique=True, verbose_name='Номер телефона')
    date_of_birth = models.DateField(verbose_name='Дата рождения')
    desired_salary = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], verbose_name='Желаемая зарплата')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Резюме'
        verbose_name_plural = 'Резюме'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
