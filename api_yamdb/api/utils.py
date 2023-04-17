from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.functional import SimpleLazyObject

make_token = SimpleLazyObject(lambda: PasswordResetTokenGenerator().make_token)
