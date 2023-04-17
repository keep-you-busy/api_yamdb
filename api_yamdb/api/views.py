from django.core.mail import send_mail
from django.shortcuts import render
from rest_framework import (filters, mixins, permissions, status, views,
                            viewsets)
from rest_framework.response import Response
from reviews.models import User

from .serializers import GetTokenSerializer, SingUpSerializer, UsersSerializer
from .utils import make_token


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = (permissions.IsAuthenticated,
                          permissions.IsAdminUser)
    serializer_class = UsersSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)


class SingUpViewSet(views.APIView):
    permission_classes = (permissions.AllowAny,)
    lookup_field = 'username'

    def post(self, request):
        serializer = SingUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user = User.objects.get(username=request.data.get('username'))
        confirmation_code = make_token(user)
        send_mail(
            subject='Код подтверждения для регистрации',
            message=f'Код подтверждения для пользователя {user.username}:'
                    f' {confirmation_code}',
            from_email='from@example.com',
            recipient_list=[f'{user.email}'],
            fail_silently=False
        )
        return Response(request.data, status=status.HTTP_200_OK)




class GetTokenViewSet(viewsets.ViewSet):
    serializer_class = GetTokenSerializer

