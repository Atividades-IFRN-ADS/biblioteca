# Relatório: SQLite para PostgreSQL

## 1. SQLite x PostgreSQL

O SQLite é um banco embutido, sem processo servidor separado: os dados ficam em um arquivo local e a configuração é mínima. Ele atende bem protótipos, testes, estudos e aplicações pequenas de uma máquina.

O PostgreSQL é um SGBD cliente-servidor, com usuários, permissões, conexões concorrentes e operação pela rede. É mais adequado para produção, equipes e aplicações que precisam de controles de acesso, concorrência e crescimento.

A escolha depende do cenário. SQLite reduz a infraestrutura; PostgreSQL exige um servidor, mas oferece recursos de operação e concorrência mais apropriados para uma aplicação publicada.

## 2. Driver

O Django usa o driver `psycopg` para PostgreSQL. A instalação usada neste projeto é:

```bash
python -m pip install "psycopg[binary]"
```

`psycopg[binary]` instala os binários necessários para desenvolvimento local. A dependência está registrada em `requirements.txt`.

## 3. Configuração do `DATABASES`

- `ENGINE`: backend do Django; aqui, `django.db.backends.postgresql`.
- `NAME`: nome do banco PostgreSQL.
- `USER`: usuário usado pela aplicação.
- `PASSWORD`: senha desse usuário.
- `HOST`: endereço do servidor PostgreSQL.
- `PORT`: porta de conexão, normalmente `5432`.

### Antes

O projeto usava SQLite e mantinha a chave secreta no código:

```python
SECRET_KEY = "<valor fixo escrito no código>"
DEBUG = True

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
```

### Depois

`config/settings.py` lê tudo do ambiente com `python-decouple`:

```python
from decouple import Csv, config

SECRET_KEY = config("DJANGO_SECRET_KEY")
DEBUG = config("DJANGO_DEBUG", cast=bool)
ALLOWED_HOSTS = config("DJANGO_ALLOWED_HOSTS", cast=Csv())

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("POSTGRES_DB"),
        "USER": config("POSTGRES_USER"),
        "PASSWORD": config("POSTGRES_PASSWORD"),
        "HOST": config("POSTGRES_HOST"),
        "PORT": config("POSTGRES_PORT"),
    }
}
```

Não há valor padrão para credenciais no `settings.py`. Sem `.env` ou variáveis equivalentes, o projeto falha cedo em vez de escolher uma senha implícita.

## 4. Banco e usuário da aplicação

O usuário administrador do PostgreSQL pode criar um papel restrito e o banco pertencente a ele:

```sql
CREATE ROLE biblioteca_app
    LOGIN
    PASSWORD 'troque-esta-senha'
    NOSUPERUSER
    NOCREATEDB
    NOCREATEROLE;

CREATE DATABASE biblioteca OWNER biblioteca_app;
```

O Django conecta com `biblioteca_app`, não com o superusuário `postgres`. O usuário administrativo só é necessário para a criação inicial do papel e do banco.

## 5. Variáveis de ambiente e arquivos locais

Variáveis de ambiente são valores fornecidos pelo sistema ao processo. A senha não fica no código nem no histórico do Git; cada ambiente pode usar credenciais diferentes sem alterar o projeto.

O `python-decouple` procura um arquivo `.env` local e expõe seus valores por `config()`. O arquivo `.env` está no `.gitignore`. O arquivo `.env.example` contém apenas nomes das variáveis e valores fictícios para orientar a configuração:

```bash
cp .env.example .env
# editar .env com os valores do PostgreSQL local
```

O `.gitignore` impede o envio acidental do `.env` e do `db.sqlite3`. O `.env.example` permanece versionado porque não contém segredo real.

Além do banco, `SECRET_KEY`, `DEBUG` e `ALLOWED_HOSTS` também saíram do código. `SECRET_KEY` é sensível; `DEBUG` e hosts mudam entre desenvolvimento e produção e não devem depender de uma constante esquecida no repositório.

## 6. Migração dos dados

O dump foi criado antes da troca do backend:

```bash
python manage.py dumpdata biblioteca --indent 2 \
    --output biblioteca/fixtures/biblioteca_sqlite_dump.json
```

Depois de configurar o `.env` para PostgreSQL:

```bash
python manage.py migrate
python manage.py loaddata biblioteca_sqlite_dump
python manage.py runserver
```

O fixture versionado contém os dados existentes no SQLite durante a migração: 3 autores e 10 livros. O `loaddata` preserva as chaves primárias e os vínculos `Book.authors`.

## 7. Validação e evidências

Foi usado um cluster PostgreSQL temporário na porta `55432`, com o usuário restrito `biblioteca_app`:

- `python manage.py check`: passou.
- `python manage.py migrate`: todas as migrações passaram.
- `python manage.py loaddata biblioteca_sqlite_dump`: 13 objetos carregados.
- Listagem: 10 livros exibidos.
- Cadastro, edição e exclusão: validados contra o PostgreSQL.
- Duas categorias de teste foram criadas no banco temporário para tornar os checkboxes visíveis na captura do formulário.
- `livros-postgresql.png`: listagem funcionando sobre PostgreSQL.
- `novo-livro-postgresql.png`: formulário funcionando sobre PostgreSQL, incluindo categorias como caixas de marcação.

## 8. Repositório

<https://github.com/Atividades-IFRN-ADS/biblioteca>

O `.env` real não deve ser enviado ao repositório. Apenas `.env.example` acompanha o projeto.

## Fontes consultadas

- Django — Databases: <https://docs.djangoproject.com/en/5.2/ref/databases/>
- Django — DATABASES: <https://docs.djangoproject.com/en/5.2/ref/settings/#databases>
- Django — Deployment checklist: <https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/>
- PostgreSQL — CREATE ROLE: <https://www.postgresql.org/docs/current/sql-createrole.html>
- PostgreSQL — CREATE DATABASE: <https://www.postgresql.org/docs/current/sql-createdatabase.html>
- SQLite — About SQLite: <https://www.sqlite.org/about.html>
- python-decouple — documentação: <https://python-decouple.readthedocs.io/en/latest/>
- Git — gitignore: <https://git-scm.com/docs/gitignore>
