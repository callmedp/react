#python imports
import logging
from datetime import datetime, timedelta
import os,django,sys,pytz

#Settings imports
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "careerplus.config.settings")
ROOT_FOLDER = os.path.realpath(os.path.dirname(__file__))
ROOT_FOLDER = ROOT_FOLDER[:ROOT_FOLDER.rindex('/')]
if ROOT_FOLDER not in sys.path:
    sys.path.insert(1, ROOT_FOLDER + '/')
django.setup()

#django imports

#local imports

#inter app imports
from shared.utils import DiscountReportUtil

#third party imports

def get_file_obj(file_name_suffix):
    file_name = "reports/discount_report_" + datetime.strftime(datetime.now(),"%Y_%m_%d") + \
             "_" + file_name_suffix + ".csv"

    if settings.IS_GCP:
        generated_file_obj = GCPPrivateMediaStorage().open(file_name, 'wb')
    else:
        generated_file_obj = open(settings.MEDIA_ROOT + '/' + file_name, 'w')
    return generated_file_obj


if __name__=="__main__":
    utc=pytz.UTC
    days_diff = int(sys.argv[1] if len(sys.argv) > 1 else 1)
    today = datetime.now()
    edt = datetime(today.year,today.month,today.day,0,0,0)
    sdt = edt - timedelta(days=days_diff)
    file_name_suffix = "daily" if days_diff == 1 else "monthly"
    file_name = "reports/discount_report_" + datetime.strftime(datetime.now(),"%Y_%m_%d") + \
             "_" + file_name_suffix + ".csv"

    logging.getLogger('info_log').info("Disount Report Cron Started for {},{}".format(sdt,edt))
    util_obj = DiscountReportUtil(start_date=sdt,end_date=edt,file_name=file_name)
    util_obj.generate_report()
    logging.getLogger('info_log').info("Disount Report Cron Complete for {},{}".format(sdt,edt))


    