def logo_upload_path(instance, filename):
    return f'avatars/{instance.user.id}/{filename}'
