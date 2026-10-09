from django.db import migrations, models
import django.db.models.deletion


def move_authors(apps, schema_editor):
    Book = apps.get_model("biblioteca", "Book")
    Author = apps.get_model("biblioteca", "Author")
    database = schema_editor.connection.alias

    for book in Book.objects.using(database).all():
        author, _ = Author.objects.using(database).get_or_create(name=book.autor)
        book.author_id = author.pk
        book.save(using=database, update_fields=["author"])


class Migration(migrations.Migration):
    dependencies = [("biblioteca", "0001_initial")]

    operations = [
        migrations.RenameModel(old_name="Livro", new_name="Book"),
        migrations.RenameField(model_name="book", old_name="titulo", new_name="title"),
        migrations.RenameField(model_name="book", old_name="ano_publicacao", new_name="year"),
        migrations.RenameField(model_name="book", old_name="disponivel", new_name="available"),
        migrations.AlterModelOptions(name="book", options={"ordering": ["title"]}),
        migrations.CreateModel(
            name="Author",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=120)),
                ("nationality", models.CharField(blank=True, max_length=80)),
            ],
            options={"ordering": ["name"], "verbose_name_plural": "autores"},
        ),
        migrations.CreateModel(
            name="Category",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name="book",
            name="author",
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name="books", to="biblioteca.author"),
        ),
        migrations.RunPython(move_authors, migrations.RunPython.noop),
        migrations.RemoveField(model_name="book", name="autor"),
        migrations.AlterField(
            model_name="book",
            name="author",
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="books", to="biblioteca.author"),
        ),
        migrations.AddField(
            model_name="book",
            name="categories",
            field=models.ManyToManyField(blank=True, related_name="books", to="biblioteca.category"),
        ),
    ]
