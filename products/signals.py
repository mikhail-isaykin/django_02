from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Product, Photo, Article

User = get_user_model()
import os
from django.utils.text import slugify


@receiver(pre_save, sender=User)
def normalize_username(sender, instance, **kwargs):
    instance.username = instance.username.lower()


@receiver(post_delete, sender=Photo)
def delete_photo_file(sender, instance, **kwargs):
    if os.path.isfile(instance.image.path):
        os.remove(instance.image.path)
        print('Файл удален')


@receiver(pre_save, sender=Article)
def auto_generate_article_slug(sender, instance, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.title)


@receiver(post_save, sender=Article)
def notify_order_status(sender, instance, created, **kwargs):
    if created:
        print('Создан новый объект')
    else:
        print('Объект обновлен')
