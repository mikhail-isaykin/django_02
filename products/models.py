from django.db import models
from django.utils.text import slugify
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.conf import settings


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ('name',)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Product(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, related_name='products'
    )
    name = models.CharField(max_length=100)
    sku = models.CharField(max_length=15, unique=True)
    slug = models.SlugField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    price = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0)]
    )
    stock = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ('name',)
        unique_together = ('category', 'slug')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Feedback(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField()
    message = models.TextField()

    class Meta:
        verbose_name = 'feedback'
        verbose_name_plural = 'feedback'
        ordering = ['name']

    def __str__(self):
        return self.name


"""class Order(models.Model):
    customer = models.ForeignKey(Сustomer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        verbose_name = 'order'
        verbose_name_plural = 'orders'
        ordering = ['customer__name']

    def __str__(self):
        return f'Order {self.pk} - {self.customer.name}'
"""


"""class Event(models.Model):
    title = models.CharField(max_length=30)
    date = models.DateField()


    class Meta:
        verbose_name = 'event'
        verbose_name_plural = 'events'
        ordering = ['title']
    
    def __str__(self):
        return self.title"""


class Resume(models.Model):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if type(self).is_resume not in (validators := type(self)._meta.get_field('resume').validators):
            validators.append(type(self).is_resume)
        
    username = models.CharField(max_length=100)
    resume = models.FileField(upload_to='resumes/')

    @staticmethod
    def is_resume(resume):
        if not resume.name.endswith('.png'):
            raise ValidationError('Можно загружать только .png')
        return resume


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
