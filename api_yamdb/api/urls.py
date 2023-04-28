from django.urls import include, path
from rest_framework import routers
from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                    GetTokenView, ReviewViewSet, SignUpView, TitleViewSet,
                    UsersViewSet)

router_v1 = routers.DefaultRouter()
router_v1.register(r'users', UsersViewSet)

auth_urls = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('token/', GetTokenView.as_view(), name='token'),
]
router_v1.register(
    'users',
    UsersViewSet,
    basename='users'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router_v1.register(
    'genres',
    GenreViewSet,
    basename='genres'
)
router_v1.register(
    'categories',
    CategoryViewSet,
    basename='сategories'
)
router_v1.register(
    'titles',
    TitleViewSet,
    basename='titles'
)

urlpatterns = [
    path('v1/auth/', include(auth_urls)),
    path('v1/', include(router_v1.urls)),
]
