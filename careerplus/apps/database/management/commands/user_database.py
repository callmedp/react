import MySQLdb
import csv
from django.conf import settings
from database.models import CPUser
from django.core.management.base import BaseCommand
from django.db import IntegrityError, transaction


class Command(BaseCommand):
    help = ('Get User Database from old Careerplus')

    def handle(self, *args, **options):
        """
            User Migration From OLD Careerplus
            Only Users with email are getting migrated
            User Migrated only for Orders places after "1-04-2014" 
        """
        # db_settings=settings.DATABASES.get('oldDB')
    
        # db_host = db_settings.get('HOST')
        # if db_host is '':
        #     db_host = "localhost"
        # db_name = db_settings.get('NAME')
        # db_pwd = db_settings.get('PASSWORD')
        # db_user = db_settings.get('USER')
        # db = MySQLdb.connect(db_host,db_user,db_pwd,db_name)
        # cursor = db.cursor()

        # sql = """
        #     SELECT auth_user.email, auth_user.username, cart_userprofile.shine_id 
        #     FROM auth_user LEFT OUTER JOIN cart_userprofile ON ( auth_user.id = cart_userprofile.user_id ) 
        #     WHERE auth_user.id IN (SELECT DISTINCT U0.candidate_id FROM cart_order U0 LEFT OUTER JOIN auth_user U1 ON ( U0.candidate_id = U1.id ) WHERE (U0.added_on >= '2014-04-01 00:00:00'  AND U0.candidate_id IS NOT NULL AND NOT (U1.email = ''  AND U1.email IS NOT NULL)))
        # """

        # # sql = """
        # #         SELECT auth_user.email, auth_user.username, cart_userprofile.shine_id 
        # #         FROM auth_user LEFT OUTER JOIN cart_userprofile ON ( auth_user.id = cart_userprofile.user_id ) 
        # #         WHERE (auth_user.email IS NOT NULL AND NOT (auth_user.email = ''))    
        # #     """
        # cursor.execute(sql,{})
        # result = cursor.fetchall()
        # try:
        #     with transaction.atomic():
        #         for row in result:
        #             try:
        #                 CPUser.objects.create(
        #                     username=row[1] if row[1] else '',
        #                     email=row[0] if row[0] else '',
        #                     shine_id=row[2] if row[2] else '')
        #             except:
        #                 continue    
        # except IntegrityError:
        #     pass
        #     print('Fail')
        # cursor.close()
        # db.close()
        
        generated_file = open('check_user.csv', 'w')
        with open('CP_Data.csv', 'r', encoding='utf-8', errors='ignore') as upload:
            uploader = csv.DictReader(upload, delimiter=',', quotechar='"')
            fieldnames = uploader.fieldnames
            fieldnames.append('Matching')
            csvwriter = csv.DictWriter(generated_file, delimiter=',', fieldnames=fieldnames)
            csvwriter.writerow(dict((fn, fn) for fn in fieldnames))
                        
            for row in uploader:
                email = row.get('Email')
                ShineID = row.get('Shine_Id')
                user = CPUser.objects.filter(email=email)[0] if CPUser.objects.filter(email=email) else None
                if user:    
                    if ShineID:    
                        if user.shine_id:    
                            if user.shine_id == ShineID:
                                row['Matching'] = 'Yes'
                            else:
                                row['Matching'] = 'No'
                        else:
                            row['Matching'] = 'Yes'
                    else:
                        row['Matching'] = "Don't Know"
                    csvwriter.writerow(row)
                else:
                    continue
        
        # users = CPUser.objects.all()
        # generated_file = open('order_user.csv', 'w')
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

        