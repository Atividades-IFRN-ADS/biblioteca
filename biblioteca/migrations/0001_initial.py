from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name="Livro",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("titulo", models.CharField(max_length=200)),
                ("autor", models.CharField(max_length=120)),
                ("ano_publicacao", models.IntegerField()),
                ("disponivel", models.BooleanField(default=True)),
            ],
            options={
                "verbose_name": "livro",
                "verbose_name_plural": "livros",
                "ordering": ["titulo"],
            },
        ),
    ]
