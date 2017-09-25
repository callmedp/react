import MySQLdb
import json
import pandas as pd
import numpy as np
from decimal import Decimal
from django.utils import timezone
from datetime import datetime
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import IntegrityError, transaction
from django.contrib.contenttypes.models import ContentType
from wallet.models import *

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
        
        db2_settings=settings.DATABASES.get('default')
        db2_host = db2_settings.get('HOST')
        if db2_host is '':
            db2_host = "localhost"
        db2_name = db2_settings.get('NAME')
        db2_pwd = db2_settings.get('PASSWORD')
        db2_user = db2_settings.get('USER')
        db2 = MySQLdb.connect(db2_host,db2_user,db2_pwd,db2_name, autocommit=True)
        ww_list = Wallet.objects.all()
        i = 0
        for wal in ww_list:
            txn_list = wal.wallettxn.all().order_by('created')
            total = Decimal(0)
            print('Wallet ', wal.owner_email)
            for txn in txn_list:
                reward = wal.point.filter(status=1).order_by('created')
                if txn.txn_type == 1:
                    total += txn.point_value
                    txn.current_value = total
                    txn.notes = 'Migrated from CP'
                    txn.save()
                elif txn.txn_type == 2:
                    total -= txn.point_value
                    if total < Decimal(0):
                        total = Decimal(0)
                    point = txn.point_value
                    txn.current_value = total
                    txn.notes = 'Migrated from CP'
                    for pts in reward:
                        if point > Decimal(0):    
                            if pts.current > point:
                                pts.current -= point
                                if pts.current == Decimal(0):
                                    pts.status = 1
                                pts.save()
                                PointTransaction.objects.create(
                                    transaction=txn,
                                    point=pts,
                                    point_value=point,
                                    txn_type=2)
                                point = Decimal(0)
                            else:
                                point -= pts.current
                                pts.status = 2
                                PointTransaction.objects.create(
                                    transaction=txn,
                                    point=pts,
                                    point_value=pts.current,
                                    txn_type=2)
                                pts.current = Decimal(0)
                                pts.save()
                    txn.save()
                elif txn.txn_type == 4:
                    total -= txn.point_value
                    if total < Decimal(0):
                        total = Decimal(0)
                    point = txn.point_value
                    txn.current_value = total
                    txn.notes = 'Migrated from CP'
                    for pts in reward:
                        if point > Decimal(0):    
                            if pts.current > point:
                                pts.current -= point
                                if pts.current == Decimal(0):
                                    pts.status = 1
                                pts.save()
                                PointTransaction.objects.create(
                                    transaction=txn,
                                    point=pts,
                                    point_value=point,
                                    txn_type=4)
                                point = Decimal(0)
                            else:
                                point -= pts.current
                                pts.status = 3
                                PointTransaction.objects.create(
                                    transaction=txn,
                                    point=pts,
                                    point_value=pts.current,
                                    txn_type=4)
                                pts.save()
                    txn.save()
                        