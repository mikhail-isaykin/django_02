from django.core.exceptions import ValidationError


def validate_avatar_size(image):
    if image.size / 1024 / 1024 > 8:
        raise ValidationError('Размер файла не должен превышать 8 МБ')


def avatar_upload_path(instance, filename):
    return f'logos/{instance.owner.id}/{filename}'
