from rest_framework.exceptions import ValidationError


def check_name(value=None, name=None):
    """Декоратор валидирует значение поля username."""
    name = ['me'] if (name is None) else name
    name = [name.lower() for name in name]

    if value.lower() in name:
        raise ValidationError({'me': 'Запрещенное имя пользователя!'})
