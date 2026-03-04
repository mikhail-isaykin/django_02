from django.db import models


from django.db import models

class Note(models.Model):
    title = models.CharField(max_length=100)  # заголовок заметки
    body = models.TextField()                 # текст заметки
    created_at = models.DateTimeField(auto_now_add=True)  # дата создания

    def __str__(self):
        return self.title  # отображение в админке
