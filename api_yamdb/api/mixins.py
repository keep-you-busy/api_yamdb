from rest_framework import filters, mixins, viewsets
from rest_framework.pagination import LimitOffsetPagination

from .permissions import IsAdminOrReadOnly


class CreateListViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                        viewsets.GenericViewSet):
    pass

class CustomMixin(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    filter_backends = [filters.SearchFilter]
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAdminOrReadOnly,)
    lookup_field = "slug"
    search_fields = ["=name"]
