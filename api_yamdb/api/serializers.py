from django.core.exceptions import ValidationError
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, SlugRelatedField

from reviews.models import Category, Comment, Genre, Review, Title, User
from core.user_validation import check_name


class UsersSerializer(serializers.ModelSerializer):
    """Сериализатор пользователей."""

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role')


class SingUpSerializer(serializers.ModelSerializer):
    """Сериализатор регистрации."""

    class Meta:
        model = User
        fields = ('email', 'username',)

    def validate_username(self, value):
        check_name(name=['me'], value=value)
        return value


class GetTokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True
    )
    confirmation_code = serializers.CharField(
        required=True
    )

    class Meta:
        model = User
        fields = ('username', 'confirmation_code',)


class ReviewSerializer(ModelSerializer):
    """Сериализатор отзывов."""

    author = SlugRelatedField(
        read_only=True, slug_field='username'
    )
    title = SlugRelatedField(
        read_only=True, slug_field='name'
    )

    def validate(self, data):
        if self.context['request'].method == 'POST':
            title_id = self.context.get('view').kwargs.get('title_id')
            user = self.context['request'].user
            if Review.objects.filter(title_id=title_id, author=user).exists():
                raise ValidationError('Одно произведение - один отзыв!')
        return data

    class Meta:
        fields = '__all__'
        model = Review


class CommentSerializer(ModelSerializer):
    """Сериализатор комментариев."""

    author = SlugRelatedField(
        read_only=True, slug_field='username'
    )
    review = SlugRelatedField(
        read_only=True, slug_field='text'
    )

    class Meta:
        fields = '__all__'
        model = Comment


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор категорий."""

    class Meta:
        model = Category
        fields = (
            "name",
            "slug",
        )


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор жанров."""

    class Meta:
        model = Genre
        fields = (
            "name",
            "slug",
        )


class TitleWriteSerializer(serializers.ModelSerializer):
    """Сериализатор произведений."""

    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field="slug",
        many=True
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field="slug"
    )

    class Meta:
        model = Title
        fields = "__all__"


class TitleReadSerializer(serializers.ModelSerializer):
    """Сериализатор произведений."""

    genre = GenreSerializer(
        many=True,
        read_only=True
    )
    category = CategorySerializer(
        read_only=True
    )
    rating = serializers.IntegerField(
        read_only=True
    )

    class Meta:
        model = Title
        fields = "__all__"
