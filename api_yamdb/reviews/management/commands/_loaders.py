import csv

from django.contrib.auth import get_user_model
from django.core.management import BaseCommand
from django.conf import settings

from reviews.models import (Category,
                            Comment,
                            Genre,
                            GenreTitle,
                            Review,
                            Title)

User = get_user_model()


class Command(BaseCommand):
    help = "Импортирует данные из файлов CSV в базу данных"

    @staticmethod
    def import_from_csv(file_name, model, field_classes):
        """Импортирует данные из CSV в базу данных для указанной модели."""
        with open(settings.CSV_FILES_DIR / file_name, "rt") as file:
            file.readline()
            objects = []
            for row in csv.reader(file, dialect="excel"):
                obj_kwargs = {}
                # используется защищенный атрибут _meta
                for i, field in enumerate(model._meta.fields):
                    if field.name == "id":
                        obj_kwargs[field.name] = row[i]
                    # важный момент, было сложно реализовать но получилось!
                    elif field.name in field_classes:
                        obj_kwargs[field.name] = \
                            field_classes[field.name].objects.get(id=row[i])
                    else:
                        obj_kwargs[field.name] = row[i]
                objects.append(model(**obj_kwargs))
            model.objects.bulk_create(objects)


    def handler(self, *args, **options):
        """Начинает импортировать и записывать данные в базу данных."""
        field_classes = {
            "author": User,
            "category": Category,
            "genre": Genre,
            "review": Review,
            "title": Title,
        }
        try:
            self.import_from_csv("users.csv", User, {})
            self.import_from_csv("category.csv", Category, {})
            self.import_from_csv("genre.csv", Genre, {})
            self.import_from_csv("comments.csv", Comment, field_classes)
            self.import_from_csv("titles.csv", Title, field_classes)
            self.import_from_csv("review.csv", Review, field_classes)
            self.import_from_csv("genre_title.csv", GenreTitle, field_classes)
        except Exception as err:
            self.stdout.write(self.style.ERROR(err))
            raise err
        self.stdout.write(
            self.style.SUCCESS("Данные CSV успешно импортированы!")
        )
