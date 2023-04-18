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
    def import_users_from_csv():
        """Импортирует пользователей из файла CSV в базу данных."""
        with open(settings.CSV_FILES_DIR / "users.csv", "rt") as file:
            file.readline()
            objects = []
            for row in csv.reader(file, dialect="excel"):
                objects.append(
                    User(
                        id=row[0],
                        username=row[1],
                        email=row[2],
                        role=row[3],
                        bio=row[4],
                        first_name=row[5],
                        last_name=row[6],
                    ),
                )
        User.objects.bulk_create(objects)

    @staticmethod
    def import_categories_from_csv():
        """Импортирует категории из файла CSV в базу данных"""
        with open(settings.CSV_FILES_DIR / "category.csv", "rt") as file:
            file.readline()
            objects = []
            for row in csv.reader(file, dialect="excel"):
                objects.append(
                    Category(
                        id=row[0],
                        name=row[1],
                        slug=row[2],
                    ),
                )
            Category.objects.bulk_create(objects)

    @staticmethod
    def import_comments_from_csv():
        """Импортирует комментарии из CSV-файла в базу данных."""
        with open(settings.CSV_FILES_DIR / "comments.csv", "rt") as file:
            file.readline()
            objects = []
            for row in csv.reader(file, dialect="excel"):
                objects.append(
                    Comment(
                        id=row[0],
                        review=Review.objects.get(id=row[1]),
                        text=row[2],
                        author=User.objects.get(id=row[3]),
                        pub_date=row[4],
                    ),
                )
            Comment.objects.bulk_create(objects)

    @staticmethod
    def import_genres_from_csv():
        """Импортирует жанры из файла CSV в базу данных"""
        with open(settings.CSV_FILES_DIR / "genre.csv", "rt") as file:
            file.readline()
            objects = []
            for row in csv.reader(file, dialect="excel"):
                objects.append(
                    Genre(
                        id=row[0],
                        name=row[1],
                        slug=row[2],
                    ),
                )
            Genre.objects.bulk_create(objects)

    @staticmethod
    def import_titles_from_csv():
        """Импортирует заголовки из CSV-файла в базу данных."""
        with open(settings.CSV_FILES_DIR / "titles.csv", "rt") as file:
            file.readline()
            objects = []
            for row in csv.reader(file, dialect="excel"):
                objects.append(
                    Title(
                        id=row[0],
                        name=row[1],
                        year=row[2],
                        category=Category.objects.get(id=row[3]),
                    ),
                )
            Title.objects.bulk_create(objects)

    @staticmethod
    def import_reviews_from_csv():
        """Импортирует отзывы из файла CSV в базу данных"""
        with open(settings.CSV_FILES_DIR / "review.csv", "rt") as file:
            file.readline()
            objects = []
            for row in csv.reader(file, dialect="excel"):
                objects.append(
                    Review(
                        id=row[0],
                        title=Title.objects.get(id=row[1]),
                        text=row[2],
                        author=User.objects.get(id=row[3]),
                        score=row[4],
                        pub_date=row[5],
                    ),
                )
            Review.objects.bulk_create(objects)

    @staticmethod
    def import_genre_titles_from_csv():
        """Импортирует названия жанров из CSV-файла в базу данных."""
        with open(settings.CSV_FILES_DIR / "genre_title.csv", "rt") as file:
            file.readline()
            objects = []
            for row in csv.reader(file, dialect="excel"):
                objects.append(
                    GenreTitle(
                        id=row[0],
                        title=Title.objects.get(id=row[1]),
                        genre=Genre.objects.get(id=row[2]),
                    ),
                )
            GenreTitle.objects.bulk_create(objects)

    def handler(self, *args, **kwargs):
        """Начинает импортировать и записывать данные в базу данных."""
        try:
            self.import_users_from_csv()
            self.import_categories_from_csv()
            self.import_titles_from_csv()
            self.import_reviews_from_csv()
            self.import_genres_from_csv()
            self.import_comments_from_csv()
            self.import_genre_titles_from_csv()
        except Exception as err:
            self.stdout.write(self.style.ERROR(err))
            raise err
        self.stdout.write(
            self.style.SUCCESS("Данные CSV успешно импортированы!")
        )
