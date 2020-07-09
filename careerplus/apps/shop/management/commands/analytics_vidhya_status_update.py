import logging, requests
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from ...models import AnalyticsVidhyaRecord
from django.conf import settings
from shop.mixins import AnalyticsVidhyaMixin
from shop.choices import av_status_choices

class Command(BaseCommand):
    """
        Custom command to update analytics vidhya 
        Enrolled User
    """
    help = "Custom command to update analytics vidhya Enrolled User"
    
    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)

    def handle(self, *args, **options):
        base_url = settings.ANALYTICS_VIDHYA_URL.get('BASE_URL', '')
        request_url = settings.ANALYTICS_VIDHYA_URL.get('STATUS', '')
        final_url = base_url + request_url
        #status 3 - enrollment_done
        users = AnalyticsVidhyaRecord.objects.exclude(status=3) 
        headers = AnalyticsVidhyaMixin().get_api_header()
        for user in users:
            av_id = user.AV_Id
            url = final_url.format(av_id)
            try:
                response = requests.get(url, headers=headers)
                if response.status_code == 200:
                    logging.getLogger('info_log').info('updated status is \
                        recieved from analytics vidhya')
                elif response.status_code == 401:
                    logging.getLogger('error_log').error('authorization error \
                        check if authorization header is correct')
                    continue
                else:
                    logging.getLogger('error_log').error('Unable to update status\
                        check the api')
                    continue
            except Exception as e:
                logging.getLogger('error_log').error('unable to call api - e'.format(e))
            data = response.json()
            status = data.get('status', '')
            status_msg = data.get('status_msg', '')
            remarks = data.get('remarks', '')
            if not status:
                logging.getLogger('error_log').error('Incorrect response from analytics vidhya')
                continue
            status_code = av_status_choices.get(status, -1)
            if status_code == -1:
                logging.getLogger('error_log').error('Change of status list analytics vidhya')
                continue
            user.status = status_code
            user.status_msg = status_msg
            user.remarks =  remarks
            user.save()




