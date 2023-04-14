from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import GetTokenViewSet, SingUpViewSet, UsersViewSet

router_v1 = DefaultRouter()

router_v1.register(
    'users', UsersViewSet, basename='users'
)


urlpatterns = [
    path('v1/auth/singup/', SingUpViewSet),
    path('v1/auth/token/', GetTokenViewSet),
    path('v1/', include(router_v1.urls)),
]