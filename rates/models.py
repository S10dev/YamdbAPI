from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Title(models.Model):
    name = models.CharField(max_length=20, verbose_name='Название')
    year = models.IntegerField(verbose_name='Год', null=True, blank=True)
    description = models.TextField(verbose_name='Описание', null=True, blank=True)
    genre = models.ForeignKey('Genre', on_delete=models.PROTECT, verbose_name='Жанр', null=True, blank=True)
    category = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name='Категория', null=True, blank=True)


    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=20)
    slug = models.SlugField(unique = True)


    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=20)
    slug = models.SlugField(unique = True)

    
    def __str__(self):
        return self.name


class Review(models.Model):
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name = 'Автор')
    score = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)], verbose_name = 'Оценка')
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name = 'Дата публикации')
    title = models.ForeignKey(Title, on_delete=models.CASCADE, related_name='review')


    class Meta:
        unique_together = ['author', 'title']

    def __str__(self):
        return self.text



class Comment(models.Model):
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name = 'Автор')
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name = 'Дата публикации')
    review = models.ForeignKey(Review, on_delete=models.CASCADE)


    def __str__(self):
        return self.text
