from django.urls import include, path
from rest_framework import routers
from rest_framework.routers import DefaultRouter

from .views import (CommentViewSet, GetTokenView, ReviewViewSet, SignUpView,
                    UsersViewSet)

router_v1 = DefaultRouter()

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




urlpatterns = [
    path('v1/auth/signup/', SignUpView.as_view()),
    path('v1/auth/token/', GetTokenView.as_view()),
    path('v1/', include(router_v1.urls)),
]