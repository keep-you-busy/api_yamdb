from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, SlugRelatedField
from reviews.models import Comment, Review, Title, User


class UsersSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'

class SingUpSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'username',)

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                f'{value}: запрещенное имя пользователя!'
            )
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
    author = SlugRelatedField(
        read_only=True, slug_field='username'
    )
    title = SlugRelatedField(
        read_only=True, slug_field='name'
    )

    class Meta:
        fields = '__all__'
        model = Review

    def score_valid(self, value):
        if (value < 1) or (value > 10):
            raise ValidationError('Оценка должна быть от 1 до 10')
        return value

    def validate(self, data):
        request = self.context['request']
        author = request.user
        title = get_object_or_404(Title)
        if (request.method == 'POST'
            and Review.objects.filter(title=title, author=author).exists()
            ):
            raise ValidationError('Одно произведение - один отзыв!')
        return data


class CommentSerializer(ModelSerializer):
    author = SlugRelatedField(
        read_only=True, slug_field='username'
    )
    review = SlugRelatedField(
        read_only=True, slug_field='text'
    )

    class Meta:
        fields = '__all__'
        model = Comment
