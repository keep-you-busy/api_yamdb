from rest_framework import serializers
from django.core.exceptions import ValidationError
from reviews.models import Comment, Review, Title
from rest_framework.serializers import ModelSerializer, SlugRelatedField
from django.shortcuts import get_object_or_404


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
