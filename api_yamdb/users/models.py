from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Класс, описывающий пользователя."""

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

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_superuser or self.is_staff

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    class Meta:
        ordering = ('username',)
