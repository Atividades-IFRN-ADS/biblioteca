from django.contrib import admin

from .models import Author, Book, Category


class BookInline(admin.TabularInline):
    model = Book
    extra = 0
    fields = ("title", "year", "available", "categories")


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "year", "available")
    search_fields = ("title", "author__name")
    list_filter = ("available", "categories")
    filter_horizontal = ("categories",)


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    inlines = (BookInline,)
    search_fields = ("name",)


admin.site.register(Category)
