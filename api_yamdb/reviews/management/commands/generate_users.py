from django.core.management.base import BaseCommand
from django.utils.crypto import get_random_string

from users.models import User


class Command(BaseCommand):
    """Создает рандомных пользователей.

    Пример запуска команды: python manage.py generate_users 5
    Эта команда создаст 5 рандомных пользователей.
    """

    def add_arguments(self, parser):
        parser.add_argument(
            'count',
            type=int,
            help='Количество пользователей, которые будут созданы'
        )

    def handle(self, *args, **kwargs):
        try:
            count = kwargs['count']
            for i in range(count):
                username = get_random_string(
                    length=8,
                    allowed_chars='abcdefgiklmnoprstvw'
                )
                user = User.objects.create_user(
                    username=username,
                    email=f'{username}@yamdb.com'
                )
                user.save()
        except Exception as exc:
            raise Exception(exc)
        else:
            print('Создание пользователей прошло успешно')
