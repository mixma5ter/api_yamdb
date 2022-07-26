from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, username=None, password=None):
        if not email:
            raise ValueError('У пользователя обязан быть адрес эл. почты')
        if username is None:
            username = email.split('@')[0]
        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )
        
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username=None, password=None):
        if not email:
            raise ValueError('У пользователя обязан быть адрес эл. почты')
        if username is None:
            username = email.split('@')[0]
        user = self.create_user(
            email,
            username=username,
        )
        
        user.role = user.UserRoles.ADMIN
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):

    class UserRoles(models.TextChoices):
        USER = 'user', ('User')
        MODERATOR = 'moderator', ('Moderator')
        ADMIN = 'admin', ('Admin')

    username = models.CharField(
        max_length=100,
        null=False,
        blank=False,
        unique=True,
        verbose_name='Никнейм'
    )
    email = models.EmailField(
        unique=True,
        blank=False,
        verbose_name='Email'
    )
    first_name = models.CharField(max_length=100, verbose_name='Имя')
    last_name = models.CharField(max_length=100, verbose_name='Фамилия')
    bio = models.TextField(max_length=100, verbose_name='О себе')
    role = models.CharField(
        max_length=50,
        choices=UserRoles.choices,
        default=UserRoles.USER,
        verbose_name='Уровень прав доступа'
    )

    @property
    def is_moderator(self):
        return self.role == self.UserRoles.MODERATOR

    @property
    def is_admin(self):
        return self.role == self.UserRoles.ADMIN

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email', ]

    objects = UserManager()

    class Meta:
        ordering = ['username']