# Mini biblioteca

Projeto Django para listar livros e consultar os livros de cada autor.

## Decisão sobre exclusão de autores

`Book.author` usa `on_delete=models.PROTECT`. Se um autor tiver livros, o Admin e o ORM impedem sua exclusão. Isso mantém os livros associados a um autor válido; para excluir esse autor, primeiro é necessário reatribuir ou remover seus livros.

## Executar

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Os livros da primeira atividade são preservados e convertidos para autores na migração. Em um banco novo e vazio, carregue os exemplos com `python manage.py loaddata livros`.

A lista fica em `http://127.0.0.1:8000/`; os detalhes do autor são acessados pelo link ao lado de cada livro. Para administrar o catálogo, crie um usuário com `python manage.py createsuperuser` e acesse `http://127.0.0.1:8000/admin/`.
