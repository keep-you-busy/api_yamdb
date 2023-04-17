from django.db.models import Avg
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from .permissions import AdminModeratorAuthorPermission
from reviews.models import Review, Title
from .serializers import (CommentSerializer, ReviewSerializer)


class ReviewViewSet(viewsets.ModelViewSet):
    rating = Review.objects.aggregate(Avg("score"))
    serializer_class = ReviewSerializer
    permission_classes = AdminModeratorAuthorPermission

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = AdminModeratorAuthorPermission

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        return review.comments

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)
