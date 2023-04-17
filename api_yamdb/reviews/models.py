from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """A custom user model. With user, admin and moderator roles."""

    USER = 'user'
    ADMIN = 'admin'
    MODERATOR = 'moderator'

    CHOICES = [
        (USER, 'Аутентифицированный пользователь'),
        (ADMIN, 'Администратор'),
        (MODERATOR, 'Модератор'),
    ]
    email = models.EmailField(
        unique=True,
        blank=False,
        null=False
    )
    first_name = models.CharField(
        'Имя',
        max_length=150,
        blank=True
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=150,
        blank=True
    )
    bio = models.TextField(
        'Биография',
        blank=True
    )
    role = models.CharField(
        'Роль',
        max_length=20,
        choices=CHOICES,
        default=USER
    )

    @property
    def is_user(self):
        return self.role == self.USER

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    class Meta:
        verbose_name = 'Пользователь',
        verbose_name_plural = 'Пользователи',

    def __str__(self) -> str:
        return self.username
