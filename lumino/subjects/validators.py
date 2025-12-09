from django.core.exceptions import ValidationError


def MinValueValidator(value: int):
    if value < 1:
        raise ValidationError(f'{value} is not in mark range')

def MaxValueValidator(value: int):
    if value > 10:
        raise ValidationError(f'{value} is not in mark range')