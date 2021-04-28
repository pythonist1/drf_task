from django.db import models

# Create your models here.


# Пост - заголовок, дата создания (авто), текст;
# Комментарий - дата создания (авто), текст;

class Post(models.Model):
    heading = models.CharField(verbose_name='Заголовок', max_length=200, db_index=True)
    date = models.DateField(auto_now_add=True, editable=False)
    text = models.TextField(verbose_name='Текст')

class Comment(models.Model):
    date = models.DateField(auto_now_add=True, editable=False)
    text = models.TextField(verbose_name='Текст')
    post = models.ForeignKey(Post, on_delete=models.PROTECT)