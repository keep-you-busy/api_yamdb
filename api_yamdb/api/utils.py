from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework_simplejwt.tokens import RefreshToken

token_generator = PasswordResetTokenGenerator()


def make_token(user):
    """Function allows to manually make a token for the user."""
    return token_generator.make_token(user)


def check_token(user, token):
    """Function allows to manually check a token for the user."""
    return token_generator.check_token(user, token)


def get_token_for_user(user):
    """Function allows to manually make a jwt token for the user."""
    refresh = RefreshToken.for_user(user)

    return str(refresh.access_token)
