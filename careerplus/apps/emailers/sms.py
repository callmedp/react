import logging
import requests

from django.conf import settings
from django.template.loader import render_to_string
from linkedin.autologin import AutoLogin


class SendSMS(object):
    def __init__(self):
        super(SendSMS, self).__init__()

    def base_send_sms(self, mob, message):
        try:
            if settings.DEBUG:
                mob = '9654947449'
                pass
            payload = {
                'api_key': settings.ACCESSKEY, 'to': mob, 'message': message,
                "method": "sms", 'sender': 'SHINEM'}
            resp = requests.get(settings.HTMSL_URL, params=payload)
        except Exception as e:
            logging.getLogger('error_log').error("%s - %s" % (str(mob), str(e)))

    def render_template(self, template, context):
        return render_to_string(template, context)

    def process(self, send_dict=None, data=None):
        from .tasks import send_sms_for_base_task
        if data.get('mobile', None) and not len(data.get('mobile', '')) < 10:
            mobile = data.get('mobile', '')
            if len(mobile) > 10:
                mobile = str(mobile)[-10:]
            send_sms_for_base_task.delay(mobile, self.render_template(
                send_dict.get('template'), data))
        else:
            return False

    def send(self, sms_type=None, data=None):
        send_dict = {}
        if sms_type == "OFFLINE_PAYMENT":
            template_name = data.get('template_name', 'offline_payment.html')
            send_dict['template'] = 'sms/' + template_name
            self.process(send_dict, data)

        elif sms_type == "ALLOCATED_TO_WRITER":
            template_name = data.get('template_name', 'assignment_action.html')
            send_dict['template'] = 'sms/' + template_name
            self.process(send_dict, data)

        elif sms_type == "DRAFT_UPLOAD":
            draft = data.get('draft_level', 1)
            if draft == 1:
                send_dict['template'] = 'emailers/sms/draft1.html'
            elif draft == 2:
                send_dict['template'] = 'emailers/sms/draft2.html'
            elif draft == 3:
                send_dict['template'] = 'emailers/sms/draft3.html'
            token = AutoLogin().encode(data.get('email', ''), data.get('candidateid', ''), data.get('order_id', ''))
            data['autologin'] = "%s://%s/autologin/%s/?next=/dashboard" % (settings.SITE_PROTOCOL, settings.SITE_DOMAIN, token)
            self.process(data, send_dict)

        elif sms_type == "REMINDER":
            template_name = data.get('template_name', 'draft_reminder.html')
            send_dict['template'] = 'sms/' + template_name
            self.process(send_dict, data)

        elif sms_type == "WRITING_SERVICE_CLOSED":
            template_name = data.get('template_name', 'auto_closer.html')
            send_dict['template'] = 'sms/' + template_name
            self.process(send_dict, data)

        elif sms_type == "PENDING_ITEMS":
            template_name = data.get('template_name', 'pending_item_sms.html')
            send_dict['template'] = 'sms/' + template_name
            self.process(send_dict, data)

        elif sms_type == "BOOSTER_CANDIDATE":
            template_name = data.get('template_name', 'booster_candidate.html')
            send_dict['template'] = 'sms/' + template_name
            self.process(send_dict, data)

        elif sms_type == "COURSE_CLOSER_MAIL":
            template_name = data.get('template_name', 'course-closer.html')
            send_dict['template'] = 'sms/' + template_name
            self.process(send_dict, data)

        elif sms_type == "RESUME_CRITIQUE_CLOSED":
            template_name = data.get('template_name', 'resume_critique_closed.html')
            send_dict['template'] = 'sms/' + template_name
            self.process(send_dict, data)

        elif sms_type == "SERVICE_INITIATION":
            template_name = data.get('template_name', 'service_initiation.html')
            send_dict['template'] = 'sms/' + template_name
            self.process(send_dict, data)

        elif sms_type == "WELCOME_CALL_BACK":
            template_name = data.get('template_name','welcome_call_back.html')
            send_dict['template'] = 'sms/' + template_name
            self.process(send_dict, data)
