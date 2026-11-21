from datetime import date

from django.core.exceptions import ValidationError


def validar_ano_publicacao(value):
    if value > date.today().year:
        raise ValidationError("O ano de publicação não pode ser futuro.")


def validar_tamanho_arquivo(file):
    if file.size > 1 * 1024 * 1024:
        raise ValidationError("A capa deve ter no máximo 1 MB.")
