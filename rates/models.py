from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    class Roles(models.TextChoices):
        USER = 'user', 'User'
        MODERATOR = 'moderator', 'Moderator'
        ADMIN = 'admin', 'Admin'

    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=25)
    role = models.CharField(
        max_length=9,
        choices=Roles.choices,
        default=Roles.USER
        )
    bio = models.TextField(null=True, blank=True, verbose_name='О себе')
    first_name = models.CharField(max_length=10)
    last_name = models.CharField(max_length=10)
    confirmation_code = models.CharField(max_length=10, null=True, blank=True)


user = get_user_model()


class Title(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    year = models.IntegerField(verbose_name='Год', null=True, blank=True)
    description = models.TextField(
        verbose_name='Описание',
        null=True,
        blank=True
        )
    category = models.ForeignKey(
        'Category',
        on_delete=models.SET_NULL,
        verbose_name='Категория',
        null=True,
        blank=True
        )

    def __str__(self):
        return self.name


class genre_title(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='title'
        )
    genre = models.ForeignKey(
        'Genre',
        on_delete=models.CASCADE,
        related_name='genre'
        )


class Genre(models.Model):
    name = models.CharField(max_length=20)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=20)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Review(models.Model):
    text = models.TextField()
    author = models.ForeignKey(
        user, on_delete=models.CASCADE, verbose_name='Автор'
        )
    score = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name='Оценка'
        )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
        )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='review'
        )

    class Meta:
        unique_together = ['author', 'title']

    def __str__(self):
        return self.text


class Comment(models.Model):
    text = models.TextField()
    author = models.ForeignKey(
        user, on_delete=models.CASCADE, verbose_name='Автор'
        )
    pub_date = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата публикации'
        )
    review = models.ForeignKey(Review, on_delete=models.CASCADE)

    def __str__(self):
        return self.text
