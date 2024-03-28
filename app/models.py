import datetime
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class Article(models.Model):
    article_title = models.CharField('назва новини', max_length=200)
    article_text = models.TextField('текст новини')
    pub_date = models.DateTimeField('дата публікації')

    def __str__(self):
        return self.article_title

    def was_published_recently(self):
        return self.pub_date >= (timezone.now() - datetime.timedelta(days=7))

    class Meta():
      verbose_name = 'Новина'
      verbose_name_plural = 'Новини'


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comment_text = models.TextField('текст коментаря')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.author.username

    def can_edit_or_delete(self, user):
        return self.author == user or user.is_superuser

    class Meta:
        verbose_name = 'Коментар'
        verbose_name_plural = 'Коментарі'


class User(AbstractUser):
    money = models.IntegerField('Респани', blank=True, default=0)
    profession = models.CharField('професія', blank=False, max_length=50, default="Шановний Пан")
    date_birth = models.DateTimeField(blank=True, null=True, verbose_name="День народження")


class UserMessage(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} ({self.created_at}): {self.message}'