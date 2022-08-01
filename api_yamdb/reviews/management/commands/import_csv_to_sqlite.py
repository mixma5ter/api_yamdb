import csv
import sqlite3 as sq

from django.core.management import BaseCommand

DIR = 'static/data/'
SQL_TEMP = 'INSERT INTO {table} ({fields}) VALUES ({values});'

CSV_FILES = {
    'category.csv': {'table_name': 'reviews_category',
                     'table_fields': ['id', 'name', 'slug'],
                     'fields': 'id,name,slug'},
    'genre.csv': {'table_name': 'reviews_genre',
                  'table_fields': ['id', 'name', 'slug'],
                  'fields': 'id,name,slug'},
    'titles.csv': {'table_name': 'reviews_title',
                   'table_fields': ['id', 'name', 'year', 'category'],
                   'fields': 'id,name,year,category_id'},
    'review.csv': {'table_name': 'reviews_review',
                   'table_fields': ['id', 'title_id', 'text', 'author',
                                    'score', 'pub_date'],
                   'fields': 'id,title_id,text,author_id,score,pub_date'},
    'comments.csv': {'table_name': 'reviews_comment',
                     'table_fields': ['id', 'review_id', 'text', 'author',
                                      'pub_date'],
                     'fields': 'id,review_id,text,author_id,pub_date'},
}


class Command(BaseCommand):
    """Копирует данные из csv-файлов в БД.

    Запуск команды: python manage.py import_csv_to_sqlite
    """

    def handle(self, *args, **kwargs):
        con = sq.connect('db.sqlite3')
        cur = con.cursor()
        for file_name, table_meta in CSV_FILES.items():
            try:
                with open(f'{DIR}{file_name}', encoding='utf-8') as csv_file:
                    reader = csv.DictReader(csv_file)
                    to_db = [
                        [k[i] for i in table_meta['table_fields']]
                        for k in reader
                    ]
                cur.executemany(SQL_TEMP.format(
                    table=table_meta['table_name'],
                    fields=table_meta['fields'],
                    values=','.join(['?'] * len(table_meta['table_fields']))),
                    to_db)
                con.commit()
                csv_file.close()
            except Exception:
                raise Exception
            else:
                print(f'Загрузка данных из {file_name} прошла успешно')
        con.close()
