from django.core.validators import (
    FileExtensionValidator,
    MaxValueValidator,
    MinLengthValidator,
    MinValueValidator,
    RegexValidator,
)
from django.db import models

from .validators import validar_ano_publicacao, validar_tamanho_arquivo


class Author(models.Model):
    name = models.CharField(max_length=120)
    nationality = models.CharField(max_length=80, blank=True)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "autores"

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(
        max_length=200,
        validators=[
            MinLengthValidator(
                3,
                message="O título deve ter pelo menos 3 caracteres.",
            )
        ],
    )
    authors = models.ManyToManyField(Author, related_name="books")
    year = models.IntegerField(
        validators=[
            MinValueValidator(1450, message="O ano deve ser a partir de 1450."),
            validar_ano_publicacao,
        ]
    )
    available = models.BooleanField(default=True)
    categories = models.ManyToManyField(Category, blank=True, related_name="books")
    pages = models.IntegerField(
        blank=True,
        null=True,
        validators=[
            MinValueValidator(1, message="O número de páginas deve ser no mínimo 1."),
            MaxValueValidator(
                5000,
                message="O número de páginas não pode passar de 5000.",
            ),
        ],
    )
    isbn = models.CharField(
        max_length=13,
        blank=True,
        validators=[
            RegexValidator(
                r"^\d{13}$",
                message="O ISBN deve conter exatamente 13 dígitos.",
            )
        ],
    )
    cover = models.ImageField(
        upload_to="capas/",
        blank=True,
        null=True,
        validators=[
            validar_tamanho_arquivo,
            FileExtensionValidator(
                allowed_extensions=["jpg", "jpeg", "png"],
                message="A capa deve ser uma imagem JPG, JPEG ou PNG.",
            ),
        ],
    )

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title
