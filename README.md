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

## Validadores do livro

O Model `Book` valida título com `MinLengthValidator(3)`, ano entre 1450 e o ano atual, páginas opcionais entre 1 e 5000 e ISBN opcional com exatamente 13 dígitos. Como o `BookForm` é um `ModelForm`, os validadores declarados no Model também são aplicados no formulário e no Admin durante a validação do Model.

### Perguntas

**a) O `BookForm` mudou?** Os campos novos precisam entrar em `Meta.fields`, mas as regras do Model não precisam ser copiadas para o formulário. O `ModelForm` constrói os campos a partir do Model e o Admin usa o mesmo ciclo de validação, incluindo os validadores do campo.

**b) Validator x `clean_<campo>()`:** um validator recebe um valor e rejeita ou aceita uma regra reutilizável de um campo. `clean_<campo>()` pode transformar o valor antes de salvar e usar o contexto do formulário. Normalizar espaços do título é um exemplo adequado para `clean_title()`.

**c) Estratégias:** título diferente do autor exige `clean()`, porque compara campos; título sem espaços nas pontas usa `clean_title()`; páginas no máximo 5000 usa `MaxValueValidator`; livro indisponível com ISBN exige `clean()`, porque depende de `available` e `isbn` juntos.

## Formulário de livro

As páginas `Novo livro` e `Editar` usam a mesma View e o mesmo `ModelForm`/template. O título é normalizado antes de salvar; espaços repetidos são reduzidos e títulos com menos de três caracteres são rejeitados. O ano não pode ser posterior ao ano atual, calculado no momento da validação. Categorias são opcionais e aparecem como caixas de marcação. Após salvar, o usuário volta à página do autor do livro.

## Upload de capas

`Book.cover` é um `ImageField`: o banco guarda o caminho relativo, e o arquivo fica em `MEDIA_ROOT/capas/`. O formulário usa `enctype="multipart/form-data"`, e a validação limita a capa a 1 MB e às extensões JPG, JPEG e PNG. `Pillow` é necessário para o `ImageField` validar imagens.

Sem `request.FILES`, o arquivo não chega ao `ModelForm`; os demais campos podem continuar válidos, mas a capa fica vazia. Sem `enctype="multipart/form-data"`, o navegador também não envia os bytes; o formulário não mostra aviso automático de upload ausente, apenas salva sem capa se o campo for opcional. Nas CBVs, `ModelFormMixin` monta o formulário POST com `request.POST` e `request.FILES` automaticamente.

Arquivos estáticos são recursos da aplicação, como CSS e JavaScript, e usam `STATICFILES_DIRS` e `{% static %}`. Capas são arquivos enviados pelos usuários, e usam `MEDIA_ROOT` e `{{ livro.cover.url }}`. A mini biblioteca usa mídia para capas.

O Django não remove o arquivo antigo quando um livro é apagado ou quando a capa é trocada; ele remove o registro/caminho, mas não sabe se o arquivo é usado em outro lugar. Isso deixa lixo em `media/capas/`, aumenta o armazenamento e pode expor arquivos antigos. Em produção, uma rotina de limpeza deve remover arquivos sem referência depois de confirmar que não são compartilhados.

A extensão não prova que o conteúdo é uma imagem. O servidor também deve validar conteúdo com Pillow, limitar tamanho e dimensões, gerar nome seguro, impedir travessia de diretórios, armazenar uploads fora do código executável quando possível e servir o arquivo com configuração segura. Uploads nunca devem ser tratados como código executável.

## Class-Based Views

As views usam `ListView`, `DetailView`, `CreateView`, `UpdateView`, `DeleteView` e `TemplateView`. A listagem ordena por título, mantém `lista_livros.html`, e a criação/edição compartilha `book_form.html`. Livro inexistente gera 404 automaticamente. A exclusão usa `livro_confirm_delete.html`, confirma em GET e só apaga em POST. O caminho `sobre/` mostra total de livros e quantidade disponível.

### Perguntas

**a) CreateView:** `ProcessFormView` e `ModelFormMixin` fazem o teste do método HTTP, constroem o formulário e chamam `is_valid()`. Se inválido, a mesma página é renderizada novamente com os dados enviados e os erros junto aos campos; nada é salvo.

**b) Upload na CreateView:** `FormMixin.get_form_kwargs()` inclui `request.FILES` automaticamente em requisições POST. Por isso a capa continua funcionando sem montar o formulário manualmente.

**c) DeleteView:** o GET mostra confirmação e o POST executa a exclusão. Se apagar em GET, um link acessado por robô, pré-carregador ou usuário poderia excluir dados sem confirmação e sem uma ação mutável explícita.

**d) CBVs:** a vantagem é reutilizar fluxo pronto de CRUD e reduzir código repetido; a desvantagem é que a lógica pode ficar menos evidente quando precisa fugir do comportamento padrão. Uma FBV ainda é boa para fluxo curto ou muito específico, com poucas etapas e regra que não se encaixa nos mixins genéricos.

