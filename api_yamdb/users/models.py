from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Model for user."""

    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    ROLE_CHOICES = [
        (USER, 'пользователь'),
        (MODERATOR, 'модератор'),
        (ADMIN, 'администратор'),
    ]
    email = models.EmailField('E-mail', max_length=254, unique=True)
    bio = models.TextField('Биография', null=True, blank=True)
    role = models.CharField(
        'Тип пользователя',
        max_length=30,
        choices=ROLE_CHOICES,
        default=USER,
    )

    def is_admin(self):
        return self.role == self.ADMIN

    def is_moderator(self):
        return self.role == self.MODERATOR

    class Meta:
        ordering = ['username']
