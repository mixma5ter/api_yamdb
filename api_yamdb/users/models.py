from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Класс, описывающий пользователя."""

    USER = "user"
    MODERATOR = "moderator"
    ADMIN = "admin"
    USER_ROLES = (
        (USER, "Пользователь"),
        (MODERATOR, "Модератор"),
        (ADMIN, "Администратор"),
    )
    username = models.CharField(
        verbose_name="Имя пользователя",
        max_length=50,
        unique=True,
        blank=False,
        null=False,
    )
    bio = models.TextField(
        verbose_name="Биография",
        blank=True,
    )
    email = models.EmailField(
        verbose_name="email",
        unique=True,
        null=False,
        max_length=254
    )
    first_name = models.CharField(
        verbose_name="Имя",
        max_length=50,
        blank=True
    )
    last_name = models.CharField(
        verbose_name="Фамилия",
        max_length=50,
        blank=True
    )
    role = models.CharField(
        choices=USER_ROLES,
        max_length=10,
        verbose_name="Роль пользователя",
        default=USER,
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    REQUIRED_FIELDS = ["email"]
    USERNAME_FIELDS = "email"

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_user(self):
        return self.role == self.USER
