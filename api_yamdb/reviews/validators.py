from datetime import datetime
from django.core.exceptions import ValidationError


def validate_creation_year(value):
    MINIMUM_TITLE_YEAR = -45500  # Первое известное произведение искусства
    if value < MINIMUM_TITLE_YEAR or value > datetime.now().year:
        raise ValidationError(f'Значение года должно быть между '
                              f'{MINIMUM_TITLE_YEAR} и {datetime.now().year}')
