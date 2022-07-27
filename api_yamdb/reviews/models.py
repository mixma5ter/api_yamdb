from django.db import models

from users.models import User


class Genre(models.Model):
    """Класс, описывающий жанр."""

    pass


class Category(models.Model):
    """Класс, описывающий категорию."""

    pass


class Title(models.Model):
    """Класс, описывающий произведение."""

    pass


class Review(models.Model):
    """Класс, описывающий отзывы."""

    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField('Текст отзыва')
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews')
    score = models.IntegerField('Оценка', default=1)  # TODO
    pub_date = models.DateTimeField(
        'Дата и время публикации', auto_now_add=True)


class Comment(models.Model):
    """Класс, описывающий комментарии."""

    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField('Текст комментария')
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments')
    pub_date = models.DateTimeField(
        'Дата и время публикации', auto_now_add=True)
