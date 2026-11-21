from django.urls import path

from . import views

urlpatterns = [
    path("", views.BookListView.as_view(), name="listar_livros"),
    path("sobre/", views.AboutView.as_view(), name="sobre"),
    path("autores/novo/", views.AuthorCreateView.as_view(), name="author_create"),
    path("autores/<int:pk>/", views.AuthorDetailView.as_view(), name="author_detail"),
    path("livros/novo/", views.BookCreateView.as_view(), name="book_create"),
    path("livros/<int:pk>/editar/", views.BookUpdateView.as_view(), name="book_edit"),
    path("livros/<int:pk>/excluir/", views.BookDeleteView.as_view(), name="book_delete"),
]
