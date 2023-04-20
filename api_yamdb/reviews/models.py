from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .validators import validate_creation_year


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
        'Адрес электронной почты',
        unique=True,
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


class CommonCategoryGenre(models.Model):
    """Абстрактная модель для хранения общих данных."""
    name = models.CharField(
        "Название",
        max_length=250
    )
    slug = models.SlugField(
        "slug",
        max_length=50,
        unique=True,
        db_index=True
    )

    class Meta:
        abstract = True
        ordering = ('name',)

    def __str__(self):
        return self.name[:settings.CHARS_LENGTH]


class Category(CommonCategoryGenre):
    """Модель категории."""

    class Meta(CommonCategoryGenre.Meta):
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(CommonCategoryGenre):
    """Модель жанра."""

    class Meta(CommonCategoryGenre.Meta):
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    """Модель произведения искусства."""
    name = models.CharField(
        "Название",
        max_length=250,
        default="Неизвестно"
    )
    description = models.TextField(
        "Описание",
        null=True,
        blank=True
    )
    category = models.ForeignKey(
        Category,
        related_name="titles",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Категория",
        help_text="Категория, к которой относится произведение")
    genre = models.ManyToManyField(
        Genre,
        related_name="titles",
        verbose_name="Жанр",
        help_text="Жанр, к которому относится произведение"
    )
    year = models.IntegerField(
        "Год создания",
        db_index=True,
        validators=[validate_creation_year]
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('name',)

    def __str__(self):
        return self.name[:settings.CHARS_LENGTH]


class GenreTitle(models.Model):
    """Модель жанров и произведений."""

    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name="Произведение",
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        verbose_name="Жанр",
    )

    def __str__(self):
        return f"{self.title}, жанр - {self.genre}"

    class Meta:
        verbose_name = "Произведение и жанр"
        verbose_name_plural = "Произведения и жанры"


class Review(models.Model):
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField()
    score = models.SmallIntegerField(
        validators=(MinValueValidator(1),
                    MaxValueValidator(10)),
        error_messages={'validators': 'Оценка должна быть от 1 до 10'}
    )
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)
    
    class Meta:
        ordering = ['-pub_date']
        constraints = [
            models.UniqueConstraint(
                fields=["author", "title"], name="unique_review"
            )
        ]

    def __str__(self):
        return self.text


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)

    class Meta:
        ordering = ["-pub_date"]

    def __str__(self):
        return self.text
