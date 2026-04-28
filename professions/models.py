from django.db import models


class CategoryProfession(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name='Название категории')
    description = models.TextField(blank=True, null=True, verbose_name='Описание категории')

    class Meta:
        verbose_name = 'Категория профессии'
        verbose_name_plural = 'Категории профессий'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Profession(models.Model):
    category = models.ForeignKey(CategoryProfession, on_delete=models.PROTECT, related_name='professions')
    name = models.CharField(max_length=255, verbose_name='Название профессии')
    description = models.TextField(blank=True, null=True, verbose_name='Описание профессии')

    class Meta:
        unique_together = ['category', 'name']
        verbose_name = 'Профессия'
        verbose_name_plural = 'Профессии'
        ordering = ['name']
    
    def __str__(self):
        return self.name
