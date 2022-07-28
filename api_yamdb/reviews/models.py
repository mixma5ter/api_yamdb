from django.db import models

from users.models import User
from .validators import validate_year


class Genre(models.Model):
    """Класс, описывающий жанр."""

    name = models.CharField(
        verbose_name='Название',
        default='Название жанра',
        max_length=256
    )
    slug = models.SlugField(
        verbose_name='id жанра',
        max_length=50,
        unique=True
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ['name']

    def __str__(self):
        return self.name


class Category(models.Model):
    """Класс, описывающий категорию."""

    name = models.CharField(
        verbose_name='Название',
        default='Название категории',
        max_length=256
    )
    slug = models.SlugField(
        verbose_name='id категории',
        max_length=50,
        unique=True
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']

    def __str__(self):
        return self.name


class Title(models.Model):
    """Класс, описывающий произведение."""

    name = models.CharField(
        verbose_name='Название',
        default='Название произведения',
        max_length=200
    )
    year = models.IntegerField(
        verbose_name='Дата выхода',
        validators=[validate_year],
        null=True,
        blank=True
    )
    description = models.TextField(
        verbose_name='Описание',
        null=True,
        blank=True
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанр',
        related_name='titles',
    )
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        on_delete=models.SET_NULL,
        related_name='titles',
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ['name']

    def __str__(self):
        return self.name


class Review(models.Model):
    """Класс, описывающий отзывы."""

    title = models.ForeignKey(
        Title,
        verbose_name='Отзыв',
        on_delete=models.CASCADE,
        related_name='reviews')
    text = models.TextField('Текст отзыва')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews')
    score = models.IntegerField(
        'Оценка',
        default=1
    )
    pub_date = models.DateTimeField(
        'Дата и время публикации',
        auto_now_add=True
    )

    def __str__(self):
        return f'Отзыв на {self.title} от {self.author}'


class Comment(models.Model):
    """Класс, описывающий комментарии."""

    review = models.ForeignKey(
        Review,
        verbose_name='Комментарий',
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField('Текст комментария')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    pub_date = models.DateTimeField(
        'Дата и время публикации',
        auto_now_add=True
    )

    def __str__(self):
        return f'Комментарий на {self.review} от {self.author}'
