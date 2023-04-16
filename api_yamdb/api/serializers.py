from rest_framework import serializers

from reviews.models import Category, Genre, Title


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор категорий"""

    class Meta:
        model = Category
        fields = (
            "name",
            "slug",
        )


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор жанров"""

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
