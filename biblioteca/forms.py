from datetime import date

from django import forms

from .models import Author, Book


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ("name", "nationality")
        labels = {
            "name": "Nome",
            "nationality": "Nacionalidade",
        }


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = (
            "title",
            "authors",
            "year",
            "available",
            "categories",
            "pages",
            "isbn",
            "cover",
        )
        labels = {
            "title": "Título",
            "authors": "Autores",
            "year": "Ano",
            "available": "Disponível",
            "categories": "Categorias",
            "pages": "Páginas",
            "isbn": "ISBN",
            "cover": "Capa",
        }
        widgets = {"categories": forms.CheckboxSelectMultiple}

    def clean_title(self):
        title = " ".join(self.cleaned_data["title"].split())
        return title

    def clean_year(self):
        year = self.cleaned_data["year"]
        current_year = date.today().year
        if year > current_year:
            raise forms.ValidationError(
                f"O ano não pode ser posterior a {current_year}."
            )
        return year
