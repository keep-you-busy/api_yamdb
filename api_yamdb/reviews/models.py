from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings

from .validators import validate_creation_year

User = get_user_model()


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
