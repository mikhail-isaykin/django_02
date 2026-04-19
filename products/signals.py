from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Product, Photo
User = get_user_model()
import os


@receiver(pre_save, sender=User)
def normalize_username(sender, instance, **kwargs):
    instance.username = instance.username.lower()

@receiver(post_delete, sender=Photo)
def delete_photo_file(sender, instance, **kwargs):
    if os.path.isfile(instance.image.path):
        os.remove(instance.image.path)
        print('Файл удален')
