from django.shortcuts import render
from rest_framework import filters, mixins, permissions, viewsets
from reviews.models import User

from .serializers import GetTokenSerializer, SingUpSerializer, UsersSerializer


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = (permissions.IsAuthenticated,
                          permissions.IsAdminUser)
    serializer_class = UsersSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)


class SingUpViewSet(viewsets.ViewSet):
    serializer_class = SingUpSerializer
    permission_classes = permissions.AllowAny

class GetTokenViewSet(viewsets.ViewSet):
    serializer_class = GetTokenSerializer
