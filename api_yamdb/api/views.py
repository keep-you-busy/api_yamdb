from django.shortcuts import render
from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from .filters import TitleFilter
from .mixins import CustomMixin
from reviews.models import (Category,
                            Genre,
                            Title)
from .serializers import (CategorySerializer,
                          GenreSerializer,
                          TitleReadSerializer,
                          TitleWriteSerializer)


class CategoryViewSet(CustomMixin):
    """Категории"""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)


class GenreViewSet(CustomMixin):
    """Жанры"""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)


class TitleViewSet(viewsets.ModelViewSet):
    """Произведения"""

    queryset = (
        Title.objects.all()
        .annotate(rating=Avg("reviews__score"))
        .order_by("-id")
    )
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method in ["POST", "PATCH"]:
            return TitleWriteSerializer
        return TitleReadSerializer
