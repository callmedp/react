import logging
from django.conf import settings
from django.core.mail import EmailMessage
from django.template import Context
from django.template.loader import render_to_string
from linkedin.autologin import AutoLogin


class SendMail():

    def base_send_mail(self, subject, body, to=None, from_email=settings.DEFAULT_FROM_EMAIL, headers=None, cc=None, bcc=None, fail_silently=False, attachments=[], mimetype='application/pdf'):
        '''
            Base function to send email. If debug_mode is true the cc will be shinecp@hindustantimes.com
        '''  
        emsg = EmailMessage(subject, body=body, to=to, from_email=from_email, headers=headers, cc=cc, bcc=bcc, attachments=[])

        emsg.content_subtype = "html"

        emsg.send()

    def render_template(self, template, context):
        return render_to_string(template, context)

    def process(self, to=None, send_dict=None, data=None):
        import ipdb; ipdb.set_trace()
        try:
            body = self.render_template(send_dict['template'], data)
        except Exception as e:
            logging.getLogger('email_log').error("%s - %s" % (str(to), str(e)))

        self.base_send_mail(subject=send_dict.get('subject', 'Shine Career Plus'), body=body, to=to, from_email=send_dict.get('from_email', None), headers=send_dict.get('header', None), bcc=send_dict.get('bcc_list', None), fail_silently=False, attachments=[])
                
    def send(self, to=None, mail_type=None, data={}):
        send_dict = {}

        if str(mail_type) == "1":
            send_dict['subject'] = "Your shine payment confirmation"
            send_dict['template'] = 'emailers/payment_confirm.html'
            send_dict['from_email'] = settings.DEFAULT_FROM_EMAIL
            data['email'] = to[0]
            data['token'] = AutoLogin().encode(
                'upender.singh@hindustantimes.com', '592be7a753c034509597de71')
            data['button_text'] = "click here to dashboard"
        self.process(to, send_dict, data)


# context_dict['LOGIN_URL'] = 'http://' + str(settings.SITE_DOMAIN)\
#                 + reverse('cp_login', kwargs={'token': token})+'?next='
# <a href="{{ LOGIN_URL }}/dashboard/" style="color:#555555; text-decoration:none;"> <img src="http://static1.shine.com/shinecp/images/version1/mailer/feedback/order_icon.gif" style="vertical-align:middle; margin-right:8px;" />View your orders </a>
# <a href="{{SITE_DOMAIN_EMAIL}}/user/login/{{token}}/?next=/dashboard/{{campaign_string}}" style="text-decoration: none;">
#                                                 <P style="font-family:Arial, Helvetica, sans-serif; font-size:20px; color:#ffffff; line-height:22px; border: 1px solid #1e3e6b; border-radius: 3px; padding: 7px; text-align: center; background: -webkit-linear-gradient(top,#1e3e6b,#1e3e6b); background: transparent -moz-linear-gradient(center top , #1e3e6b,#1e3e6b) repeat scroll 0% 0%;">{{ button_text }}</P>
#                                             </a>