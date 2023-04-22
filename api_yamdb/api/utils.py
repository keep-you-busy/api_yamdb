from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework_simplejwt.tokens import RefreshToken

token_generator = PasswordResetTokenGenerator()


def make_token(user):
    """Функция для создания токена."""
    return token_generator.make_token(user)


def check_token(user, token):
    """Функция для проверки токена."""
    return token_generator.check_token(user, token)


def get_token_for_user(user):
    """Функция для создания JWT для пользователя."""
    refresh = RefreshToken.for_user(user)

    return str(refresh.access_token)
