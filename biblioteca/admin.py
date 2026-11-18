from django.contrib import admin

from .models import Author, Book, Category


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "display_authors", "year", "available")
    search_fields = ("title", "authors__name")
    list_filter = ("available", "categories")
    filter_horizontal = ("authors", "categories")

    @admin.display(description="Autores")
    def display_authors(self, book):
        return ", ".join(author.name for author in book.authors.all())


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    search_fields = ("name",)


admin.site.register(Category)
