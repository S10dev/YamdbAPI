from django.db import models

# Create your models here.
class Title(models.Model):
    name = models.CharField(max_length=20, verbose_name='Название')
    year = models.IntegerField(verbose_name='Год', null=True, blank=True)
    # rating =
    description = models.TextField(verbose_name='Описание', null=True, blank=True)
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE, verbose_name='Жанр', null=True, blank=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name='Категория', null=True, blank=True)


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



