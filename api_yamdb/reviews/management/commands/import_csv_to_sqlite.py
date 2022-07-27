import csv

from django.core.management.base import BaseCommand

from users.models import User


class Command(BaseCommand):
    """Команда загружает данные в БД из csv-файлов.

    Запуск: python manage.py command_test
    """

    def handle(self, *args, **options):
        # Загрузка данных из users.csv в таблицу users_user
        with open('static/data/users.csv', newline='') as csv_file:
            reader = csv.DictReader(csv_file)

            for row in reader:
                user = User(username=row['username'],
                            email=row['email'],
                            role=row['role'],
                            bio=row['bio'],
                            first_name=row['first_name'],
                            last_name=row['last_name'])
                user.save()

        csv_file.close()
