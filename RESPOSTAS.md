# Pesquisa: Models e Views

## 1. Investigando os Models

### 1.1. O que é um Model no Django e que problema resolve?

Um Model é uma classe Python que representa um tipo de dado da aplicação. Cada objeto costuma corresponder a um registro do banco, e os campos da classe descrevem os dados armazenados. No MVT, o Model organiza e fornece acesso aos dados, evitando que as regras de persistência fiquem espalhadas pelas Views e pelos Templates.

### 1.2. O que é ORM?

ORM é o mapeamento entre objetos da aplicação e tabelas do banco relacional. No Django, o ORM transforma operações Python em consultas ao banco: por exemplo, `Livro.objects.all()` busca os registros de Livro sem que a aplicação precise montar SQL manualmente.

### 1.3. Como se declara um Model? Cite cinco campos.

Um Model é declarado como uma classe que herda de `django.db.models.Model`. Seus atributos são campos do banco. Exemplos:

- `CharField`: texto curto com tamanho máximo, como nome ou título.
- `TextField`: texto longo, como descrição ou conteúdo.
- `IntegerField`: número inteiro, como quantidade ou ano.
- `BooleanField`: valor verdadeiro ou falso, como ativo/disponível.
- `DateField`: uma data sem horário, como data de nascimento.
- `ForeignKey`: relação de muitos registros para um registro de outro Model, como vários livros de uma mesma categoria.

### 1.4. Para que serve a classe Meta?

A classe interna `Meta` reúne opções que configuram o comportamento e a apresentação do Model. `ordering` define a ordenação padrão das consultas; `verbose_name` e `verbose_name_plural` definem os nomes exibidos no Admin. Também é possível configurar a tabela com `db_table`.

### 1.5. O que são migrations? Diferença entre `makemigrations` e `migrate`.

Migrations são arquivos que registram mudanças na estrutura dos Models e permitem aplicá-las de forma controlada ao banco. `makemigrations` compara os Models com as migrations existentes e cria os arquivos de mudança. `migrate` executa essas mudanças no banco de dados.

## 2. Ligando Models às Views

### 2.1. Como uma View usa um Model?

A View importa a classe do Model e usa o ORM para consultar ou alterar os dados. Por exemplo, `Livro.objects.all()` obtém os livros cadastrados. A View então escolhe quais dados serão enviados à resposta.

### 2.2. O que é um QuerySet? Diferença entre `all()`, `filter()` e `get()`.

QuerySet é uma coleção de objetos resultante de uma consulta ao banco; normalmente sua avaliação é adiada até os dados serem necessários. `all()` seleciona todos os registros. `filter()` retorna os registros que atendem a condições e pode retornar nenhum, um ou vários. `get()` busca um único registro e gera exceção se não encontrar nenhum ou se encontrar mais de um.

### 2.3. Como os dados chegam ao Template?

A View chama `render(request, caminho_do_template, contexto)`. O contexto é um dicionário Python que associa nomes a valores. No Template, as chaves ficam disponíveis como variáveis. Por exemplo, `render(request, "biblioteca/lista_livros.html", {"livros": livros})` permite percorrer a lista usando `{% for livro in livros %}`.

### 2.4. Para que serve `get_object_or_404`?

`get_object_or_404(Model, ...)` busca um objeto e, se ele não existir, encerra a resposta com HTTP 404. É útil em Views porque evita tratar manualmente a exceção `DoesNotExist` e comunica corretamente que o recurso solicitado não foi encontrado. `get()` continua adequado quando a ausência do objeto deve ser tratada de outra forma.

## 3. Desafio prático: Mini biblioteca

O projeto Django está na raiz deste repositório. Os Models `Book`, `Author` e `Category`, a View `listar_livros`, as URLs e o Template `lista_livros.html` estão configurados. A fixture `livros.json` cadastra três exemplos.

Para executar localmente:

Se o banco ainda estiver vazio, carregue os exemplos com `python manage.py loaddata livros` após migrar.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```


