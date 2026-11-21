from datetime import date

from django.core.exceptions import ValidationError


def validar_ano_publicacao(value):
    if value > date.today().year:
        raise ValidationError("O ano de publicação não pode ser futuro.")
