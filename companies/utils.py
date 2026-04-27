def logo_upload_path(instance, filename):
    return f'logos/{instance.owner.id}/{filename}'
