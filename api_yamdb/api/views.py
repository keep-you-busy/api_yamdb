from django.conf.global_settings import DEFAULT_FROM_EMAIL
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, views, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from reviews.models import Category, Genre, Review, Title, User

from .filters import TitleFilter
from .mixins import CustomMixin
from .permissions import IsAdministrator, IsAdminOrReadOnly, IsOwnerOrReadOnly
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, GetTokenSerializer,
                          NotAdminSerializer, ReviewSerializer,
                          SingUpSerializer, TitleReadSerializer,
                          TitleWriteSerializer, UsersSerializer)
from .utils import check_token, get_token_for_user, make_token


class UsersViewSet(viewsets.ModelViewSet):
    """Пользователи."""

    queryset = User.objects.all()
    permission_classes = (IsAdministrator,)
    pagination_class = PageNumberPagination
    serializer_class = UsersSerializer
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    http_method_names = ['get', 'post', 'patch', 'delete']

    @action(
        methods=['GET', 'PATCH'],
        detail=False,
        permission_classes=(IsAuthenticated,),
        url_path='me')
    def get_current_user_info(self, request):
        serializer = UsersSerializer(request.user)
        if request.method == 'PATCH':
            if request.user.is_admin:
                serializer = UsersSerializer(
                    request.user,
                    data=request.data,
                    partial=True)
            else:
                serializer = NotAdminSerializer(
                    request.user,
                    data=request.data,
                    partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.data)


class SignUpView(views.APIView):
    """Регистрация пользователя."""

    permission_classes = (AllowAny,)

    @staticmethod
    def send_confirmation_code(user):
        confirmation_code = make_token(user)
        send_mail(
            subject='Код подтверждения для регистрации',
            message=f'Код подтверждения для пользователя {user.username}:'
                    f' {confirmation_code}',
            from_email=DEFAULT_FROM_EMAIL,
            recipient_list=[f'{user.email}'],
            fail_silently=False
        )

    def post(self, request):
        if User.objects.filter(username=request.data.get('username'),
                               email=request.data.get('email')).exists():
            self.send_confirmation_code(
                User.objects.get(username=request.data.get('username'))
            )
            return Response(request.data, status=status.HTTP_200_OK)
        else:
            serializer = SingUpSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            self.send_confirmation_code(user)
            return Response(request.data, status=status.HTTP_200_OK)


class GetTokenView(views.APIView):
    """Получение токена."""

    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = GetTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        try:
            user = User.objects.get(username=data.get('username'))
        except User.DoesNotExist:
            return Response(
                {'username': 'Пользователь не найден!'},
                status=status.HTTP_404_NOT_FOUND)
        if check_token(user=user, token=data.get('confirmation_code')):
            return Response({'token': get_token_for_user(user)},
                            status=status.HTTP_201_CREATED)
        return Response(
            {'confirmation_code': 'Неверный код подтверждения!'},
            status=status.HTTP_400_BAD_REQUEST)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    pagination_class = PageNumberPagination
    permission_classes = (IsOwnerOrReadOnly,)

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    """Комментарии."""

    serializer_class = CommentSerializer
    pagination_class = PageNumberPagination
    permission_classes = (IsOwnerOrReadOnly,)

    def get_queryset(self):
        review = get_object_or_404(
            Review,
            pk=self.kwargs.get('review_id'),
            title__id=self.kwargs.get('title_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review,
            pk=self.kwargs.get('review_id'),
            title__id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, review=review)


class CategoryViewSet(CustomMixin):
    """Категории."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = PageNumberPagination


class GenreViewSet(CustomMixin):
    """Жанры."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = PageNumberPagination


class TitleViewSet(viewsets.ModelViewSet):
    """Произведения."""

    queryset = (
        Title.objects.all()
        .annotate(rating=Avg("reviews__score"))
        .order_by("-id")
    )
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = [DjangoFilterBackend]
    pagination_class = PageNumberPagination
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method in ["POST", "PATCH"]:
            return TitleWriteSerializer
        return TitleReadSerializer
