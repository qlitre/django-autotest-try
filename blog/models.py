from django.db import models
from django.utils import timezone


class Post(models.Model):
    title = models.CharField('タイトル', max_length=32)
    text = models.TextField('本文')
    created_at = models.DateTimeField('作成日', default=timezone.now)
    updated_at = models.DateTimeField('更新日', auto_now=True)

    def __str__(self):
        return self.title
