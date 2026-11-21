# Mini biblioteca

Projeto Django para listar livros e consultar os livros de cada autor.

## Autores e reversão das migrações

`Book.authors` permite vários autores por livro. A migração adiciona a relação muitos-para-muitos, copia para ela o autor que cada livro já tinha e só depois remove a chave estrangeira antiga. `author_detail` continua usando `author.books`, nome preservado pelo `related_name`.

Ao reverter a migração, os vínculos excedentes de coautoria se perdem: uma chave estrangeira só pode guardar um autor por livro. A reversão escolhe um autor para preencher esse campo; os outros vínculos não cabem no modelo antigo.

Se o único autor de um livro for apagado, o livro continua existindo sem autores; o Django apaga apenas o vínculo da tabela intermediária. Para exigir pelo menos um autor, valide os formulários e operações que alteram autores e impeça a remoção do último vínculo. Uma garantia também contra alterações SQL diretas exige uma regra no próprio banco, como um trigger.

## Base de exemplo

Antes da alteração, a base foi copiada para `db.sqlite3.backup-2026-10-09` e completada para conter pelo menos 10 livros.

## Executar

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# preencha o .env com as credenciais do PostgreSQL
python manage.py migrate
python manage.py runserver
```

Os livros da primeira atividade são preservados e convertidos para autores na migração. Em um banco novo e vazio, carregue os exemplos com `python manage.py loaddata livros`.

A lista fica em `http://127.0.0.1:8000/`; os detalhes do autor são acessados pelo link ao lado de cada livro. Para administrar o catálogo, crie um usuário com `python manage.py createsuperuser` e acesse `http://127.0.0.1:8000/admin/`.

O relatório da migração para PostgreSQL está em `RELATORIO_POSTGRES.md`.

## Formulário de autor

O link `Novo autor` abre um `ModelForm` com os campos `Nome` e `Nacionalidade`. O nome é obrigatório; a nacionalidade é opcional. Após salvar, a aplicação redireciona para a página do autor recém-criado, evitando novo cadastro ao atualizar o navegador.

O template usa `{% csrf_token %}`. Em teste, removê-lo e enviar o formulário produz resposta HTTP 403 (`CSRF verification failed. Request aborted.`), porque o `CsrfViewMiddleware` bloqueia a requisição POST antes da View. A proteção deve permanecer no formulário.

## Formulário de livro

As páginas `Novo livro` e `Editar` usam a mesma View e o mesmo `ModelForm`/template. O título é normalizado antes de salvar; espaços repetidos são reduzidos e títulos com menos de três caracteres são rejeitados. O ano não pode ser posterior ao ano atual, calculado no momento da validação. Categorias são opcionais e aparecem como caixas de marcação. Após salvar, o usuário volta à página do autor do livro.
