import MySQLdb
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import IntegrityError, transaction


class Command(BaseCommand):
    help = ('Get User Database from old Careerplus')

    def handle(self, *args, **options):
        db_settings=settings.DATABASES.get('oldDB')
        db_host = db_settings.get('HOST')
        if db_host is '':
            db_host = "localhost"
        db_name = db_settings.get('NAME')
        db_pwd = db_settings.get('PASSWORD')
        db_user = db_settings.get('USER')
        db = MySQLdb.connect(db_host,db_user,db_pwd,db_name)
        cursor = db.cursor()

        sql = """
            """
        cursor.execute(sql,{})

        result = cursor.fetchall()
        try:
            with transaction.atomic():
                count = 0
                for row in result:
                    print(row)
        except IntegrityError:
            pass
            print('Fail')
        cursor.close()
        db.close()
