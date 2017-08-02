import MySQLdb
import csv
from django.conf import settings
from database.models import CPUser
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

        sql = """SELECT auth_user.email, auth_user.username, cart_userprofile.shine_id
            FROM auth_user
            LEFT OUTER JOIN cart_userprofile ON ( auth_user.id = cart_userprofile.user_id ) 
            WHERE auth_user.id IN (
                SELECT DISTINCT U0.candidate_id
                FROM cart_order U0
                WHERE U0.candidate_id IS NOT NULL)
            """
        cursor.execute(sql,{})
        result = cursor.fetchall()
        try:
            with transaction.atomic():
                for row in result:
                    try:
                        CPUser.objects.create(
                            username=row[1] if row[0] else '',
                            email=row[0] if row[1] else '',
                            shine_id=row[2] if row[2] else '')
                    except:
                        continue    
        except IntegrityError:
            pass
            print('Fail')
        cursor.close()
        db.close()
        # users = CPUser.objects.all()
        # generated_file = open('user.csv', 'w')
        # fieldnames = ['Email', 'ShineID',]
        # csvwriter = csv.DictWriter(generated_file, delimiter=',', fieldnames=fieldnames)
        # csvwriter.writerow(dict((fn, fn) for fn in fieldnames))
                                
        # for user in users:
        #     try:
        #         if user.email:
        #             row = {}
        #             row['Email'] = user.email 
        #             row['ShineID'] = ''
                    
        #             csvwriter.writerow(row)
        #     except:
        #         continue

        # 