from django.urls import path

from . import views

urlpatterns = [
    path("", views.listar_livros, name="listar_livros"),
    path("autores/<int:pk>/", views.author_detail, name="author_detail"),
]
