import datetime
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.db import models

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
    author_name = models.CharField('ім\'я автора', max_length=50)
    comment_text = models.CharField('текст коментаря', max_length=200)
    

    def __str__(self):
        return self.author_name

    class Meta():
      verbose_name = 'Коментар'
      verbose_name_plural = 'Коментарі'


class User(AbstractUser):
    money = models.IntegerField('Респани', blank=True, default=0)
    profession = models.CharField('професія', blank=False, max_length=50, default="Шановний Пан")
    date_birth = models.DateTimeField(blank=True, null=True, verbose_name="День народження")