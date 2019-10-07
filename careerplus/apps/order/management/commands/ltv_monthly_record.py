# import python module
import logging
import sys
from datetime import datetime,date

# import django module
from django.core.management.base import BaseCommand

# import apps module
from order.utils import LTVReportUtil






class Command(BaseCommand):
    def handle(self, *args, **options): 
        year = options.get('year','')
        month = options.get('month','')
        ltv_monthly_record(year,month)

    def add_arguments(self, parser):
        parser.add_argument('year', type=str)
        parser.add_argument('month', type=str)

def ltv_monthly_record(year,month):
    if not (year and month):
        today_date = datetime.now()
        year = today_date.year
        month = today_date.month
    
    LTVReportUtil().create_monthly_ltv_record(year,month)
    


