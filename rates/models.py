from django.db import models

# Create your models here.
class Title(models.Model):
    name = models.CharField(max_length=20, verbose_name='Название')
    year = models.IntegerField(verbose_name='Год')
    # rating =
    description = models.TextField(verbose_name='Описание')
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE, verbose_name='Жанр')
    category = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name='Категория')


class Genre(models.Model):
    name = models.CharField(max_length=20)
    slug = models.SlugField(unique = True)


    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=20)
    slug = models.SlugField(unique = True)



