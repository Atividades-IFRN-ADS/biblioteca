from django.db import migrations


def copy_authors(apps, schema_editor):
    Book = apps.get_model("biblioteca", "Book")
    database = schema_editor.connection.alias

    for book in Book.objects.using(database).only("pk", "author_id").iterator():
        book.authors.add(book.author_id)


def restore_author(apps, schema_editor):
    Book = apps.get_model("biblioteca", "Book")
    database = schema_editor.connection.alias

    for book in Book.objects.using(database).only("pk").iterator():
        author_id = book.authors.using(database).order_by("pk").values_list("pk", flat=True).first()
        if author_id:
            Book.objects.using(database).filter(pk=book.pk).update(author_id=author_id)


class Migration(migrations.Migration):
    dependencies = [("biblioteca", "0003_add_book_authors")]

    operations = [migrations.RunPython(copy_authors, restore_author)]
