import csv

from django.core.management.base import BaseCommand

from users.models import User


class Command(BaseCommand):
    """Команда загружает данные в БД из csv-файлов.

    Запуск: python manage.py command_test
    """

    def handle(self, *args, **options):
        # Загрузка данных из users.csv в таблицу users_user
        with open('static/data/users.csv') as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=',')
            iterable = iter(csv_reader)

            for row in iterable:
                username = row['username']
                email = row['email']
                role = row['role']
                bio = row['bio']
                first_name = row['first_name']
                last_name = row['last_name']
                user = User(username=username,
                            email=email,
                            role=role,
                            bio=bio,
                            first_name=first_name,
                            last_name=last_name)
                user.save()

        csv_file.close()
