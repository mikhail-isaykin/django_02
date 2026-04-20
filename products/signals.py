from django.db.models.signals import post_save, pre_save, post_delete, pre_delete
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Product, Photo, Article, Category, Item
from django.core.exceptions import ValidationError
import os
from django.utils.text import slugify
from django.utils import timezone
from django.conf import settings
User = get_user_model()
PATH = os.path.join(settings.BASE_DIR, 'log.txt')


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

@receiver(pre_delete, sender=Category)
def block_category_delete_if_has_items(sender, instance, **kwargs):
    is_item = Item.objects.filter(category=instance).exists()
    if is_item:
        raise ValidationError('Нельзя удалить категорию, в которой есть товары')

@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    print(f'Пользователь user.username вошёл в систему в {timezone.now()}')


@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    with open('log.txt', 'a', encoding='utf-8') as log:
        if user is None:
            log.write('Неизвестный пользователь вышел из системы\n')
        else:
            log.write(f'Пользователь {user.username} вышел из системы\n')
