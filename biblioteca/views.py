from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
)

from .forms import AuthorForm, BookForm
from .models import Author, Book


class BookListView(ListView):
    model = Book
    template_name = "biblioteca/lista_livros.html"
    context_object_name = "livros"
    ordering = ("title",)

    def get_queryset(self):
        return Book.objects.prefetch_related("authors").order_by(*self.ordering)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_livros"] = Book.objects.count()
        context["livros_disponiveis"] = Book.objects.filter(available=True).count()
        return context


class AuthorDetailView(DetailView):
    model = Author
    template_name = "biblioteca/author_detail.html"
    context_object_name = "author"

    def get_queryset(self):
        return Author.objects.prefetch_related("books")


class AuthorCreateView(CreateView):
    form_class = AuthorForm
    template_name = "biblioteca/author_form.html"
    context_object_name = "author"
    success_url = reverse_lazy("listar_livros")

    def get_success_url(self):
        return reverse("author_detail", kwargs={"pk": self.object.pk})


class BookFormMixin:
    form_class = BookForm
    template_name = "biblioteca/book_form.html"
    context_object_name = "book"
    success_url = reverse_lazy("listar_livros")

    def get_success_url(self):
        author = self.object.authors.order_by("pk").first()
        if author is None:
            return self.success_url
        return reverse("author_detail", kwargs={"pk": author.pk})


class BookCreateView(BookFormMixin, CreateView):
    pass


class BookUpdateView(BookFormMixin, UpdateView):
    model = Book


class BookDeleteView(DeleteView):
    model = Book
    template_name = "biblioteca/livro_confirm_delete.html"
    context_object_name = "livro"
    success_url = reverse_lazy("listar_livros")


class AboutView(TemplateView):
    template_name = "biblioteca/sobre.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_livros"] = Book.objects.count()
        context["livros_disponiveis"] = Book.objects.filter(available=True).count()
        return context
