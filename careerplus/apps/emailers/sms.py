import logging
import requests

from django.conf import settings
from django.template.loader import render_to_string


class SendSMS(object):
    def __init__(self):
        super(SendSMS, self).__init__()

    def base_send_sms(self, mob, message):
        try:
            payload = {
                'accesskey': settings.ACCESSKEY, 'to': mob, 'text': message}
            resp = requests.get(settings.HTMSL_URL, params=payload)
        except Exception as e:
            logging.getLogger('sms_log').error("%s - %s" % (str(mob), str(e)))

    def render_template(self, template, context):
        return render_to_string(template, context)

    def process(self, send_dict=None, data=None):
        if data.get('mobile', None) and not len(data.get('mobile', '')) < 10:
            mobile = data.get('mobile', '')
            if len(mobile) > 10:
                mobile = str(mobile)[-10:]
            try:
                self.base_send_sms(mobile, self.render_template(
                    send_dict.get('template'), data))
            except Exception as e:
                logging.getLogger('sms_log').error("%s - %s" % (
                    str(mobile), str(e)))
        else:
            return False

    def send(self, sms_type=None, data=None):
        send_dict = {}
        if sms_type == "Writer_Information":
            template_name = data.get('template_name', 'writer_info.html')
            send_dict['template'] = 'sms/' + template_name
            self.process(send_dict, data)

        elif sms_type == "REMINDER":
            template_name = data.get('template_name', 'draft_reminder.html')
            send_dict['template'] = 'sms/' + template_name
            self.process(send_dict, data)

        elif sms_type == "AUTO_CLOSER":
            template_name = data.get('template_name', 'auto_closer.html')
            send_dict['template'] = 'sms/' + template_name
            self.process(send_dict, data)

        elif sms_type == "MIDOUT":
            template_name = data.get('template_name', 'midout_sms.html')
            send_dict['template'] = 'sms/' + template_name
            self.process(send_dict, data)
