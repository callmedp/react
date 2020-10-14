import MySQLdb
import json
import pandas as pd
import numpy as np
from decimal import Decimal
from django.utils import timezone
from datetime import datetime
from django.conf import settings
from django.core.management.base import BaseCommand
from wallet.models import *
import logging


class Command(BaseCommand):
    help = ('Expires Wallet Points Daily')

    def handle(self, *args, **options):
        logging.getLogger('info_log').info("OK")
        today = timezone.now()
        today = timezone.make_aware(datetime(today.year, today.month, today.day, 0,0,0), timezone.get_current_timezone())
        points_exp = RewardPoint.objects.filter(status=1, expiry__lte=today).values_list('wallet', flat=True).distinct()
        wallet = Wallet.objects.filter(pk__in=points_exp)

        for wall in wallet:
            points = wall.point.filter(status=1, expiry__lte=today)
            total = Decimal(0)
            for pt in points:
                total += pt.current
            points.update(status=3)
            txn = WalletTransaction.objects.create(
                wallet=wall,
                txn_type=4,
                status=1,
                notes='expired from cron',
                point_value=total,
                current_value=wall.get_current_amount()
            )
            for pt in points:
                PointTransaction.objects.create(
                    transaction=txn,
                    point=pt,
                    point_value=pt.current,
                    txn_type=4)
            logging.getLogger('info_log').info("{}".format(wall))
        # points_df = pd.DataFrame(list(points_exp))
        # cur_df = points_df.groupby('wallet')['current'].sum().reset_index()
        # pt_df = points_df.groupby('wallet')['pk'].apply(list).reset_index()
        # pt_df = pd.merge(pt_df, cur_df, how='left', on='wallet')
        # del points_df
        # for i, row in pt_df.iterrows():
        #     amount = row['current']
        #     wallet = Wallet.objects.get(pk=row['wallet'])
        #     pt_list = RewardPoint.objects.filter(pk__in=row['pk'])
        #     pt_list.update(status=3)
        #     txn = WalletTransaction.objects.create(
        #         wallet=wallet,
        #         txn_type=4,
        #         status=1,
        #         notes='expired from cron',
        #         point_value=amount,
        #         current_value=wallet.get_current_amount()
        #         )
        #     for pt in pt_list:
        #         PointTransaction.objects.create(
        #             transaction=txn,
        #             point=pt,
        #             point_value=pt.current,
        #             txn_type=4)
        logging.getLogger('info_log').info("Finish")
