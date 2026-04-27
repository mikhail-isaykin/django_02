from django.core.exceptions import ValidationError


def validate_image_size(image):
    if image.size / 1024 / 1024 > 8:
        raise ValidationError('Размер файла не должен превышать 8 МБ')
