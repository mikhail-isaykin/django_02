from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    is_published = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Photo(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='photo')
    image = models.ImageField(upload_to='gallery/')
    uploaded_at = models.DateTimeField(auto_now_add=True)


class Article(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True, null=True)
    content = models.TextField()

    def __str__(self):
        return self.title

class Category(models.Model):
    name = models.CharField(max_length=100)

class Item(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='item')
    name = models.CharField(max_length=100)


class FailedLogin(models.Model):
    username = models.CharField()
    ip = models.GenericIPAddressField()


class Group(models.Model):
    name = models.CharField()
