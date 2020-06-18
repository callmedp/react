import logging
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from ...models import AnalyticsVidhyaRecord
from django.conf import settings

class Command(BaseCommand):
    """
        Custom command to update analytics vidhya 
        Enrolled User
    """
    help = "Custom command to update analytics \
            vidhya Enrolled User"
    
    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)

    def handle(self, *args, **options):
        request_url = settings.ANALYTICS_VIDHYA_URL.get('status')
        #do we need a filter
        user_ids = AnalyticsVidhyaRecord.objects.all()
        try:
            for user_id in users_ids:
                av_id = user_id.AV_Id
                url = request_url.format(av_id)
                #add header autherisation
                response = requests.get(url)
                if response.status_code == 200:
                    logging.getLogger('info_log').info('updated status is \
                        recieved from analytics vidhya')
                else:
                    logging.getLogger('info_log').info('updated status not \
                        recieved from analytics vidhya')
                    continue
                data = response.json()
                status = data.get('status')
                if status:
                    user_id.update({
                            'status':av_status_choices.get(status)
                        })
                    user_id.save()




