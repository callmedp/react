import logging
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from linkedin.autologin import AutoLogin
from core.mixins import TokenGeneration


class SendMail():

    def base_send_mail(self, subject, body, to=None, from_email=settings.CONSULTANTS_EMAIL, headers=None, cc=None, bcc=None, fail_silently=False, attachments=[], mimetype='application/pdf'):
        '''
            Base function to send email. If debug_mode is true the cc will be shinecp@hindustantimes.com
        '''

        if settings.DEBUG:
            subject = "Test Mail " + subject
            to = ['priya.kharb@hindustantimes.com']
            cc = []
            bcc = []

        emsg = EmailMessage(subject, body=body, to=to, from_email=from_email, headers=headers, cc=cc, bcc=bcc, attachments=[])

        emsg.content_subtype = "html"

        emsg.send()

    def render_template(self, template, context):
        return render_to_string(template, context)

    def process(self, to=None, send_dict=None, data=None):
        try:
            body = self.render_template(send_dict['template'], data)
        except Exception as e:
            logging.getLogger('email_log').error("%s - %s" % (str(to), str(e)))

        self.base_send_mail(subject=send_dict.get('subject', 'Shinelearning'), body=body, to=to, from_email=send_dict.get('from_email', settings.DEFAULT_FROM_EMAIL), headers=send_dict.get('header', None), bcc=send_dict.get('bcc_list', None), fail_silently=False, attachments=[])
                
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

        if str(mail_type) == "2":
            send_dict['subject'] = "Linkedin Profile"
            send_dict['template'] = 'emailers/payment_confirm.html'
            send_dict['from_email'] = settings.DEFAULT_FROM_EMAIL
            send_dict['cc_list'] = [data.get('cc')]
            data['email'] = [to]
            data['token'] = AutoLogin().encode(to, data.get('candidateid'), data.get('orderitem'))
            data['button_text'] = "click here to dashboard"
            self.process(to, send_dict, data)

        elif mail_type == "ASSIGNMENT_ACTION":
            send_dict['subject'] = data.get('subject', 'Details of your services')
            template_name = data.get('template_name', 'assignment_action.html')
            send_dict['template'] = 'emailers/' + template_name
            send_dict['from_email'] = settings.DEFAULT_FROM_EMAIL
            self.process(to, send_dict, data)

        elif mail_type == "REMINDER":
            send_dict['subject'] = data.get('subject', "Your developed document has been uploaded")
            template_name = data.get('template_name', 'draft_reminder.html')
            send_dict['template'] = 'emailers/' + template_name

            # for 2nd draft
            if data.get('draft_level') == 2:
                send_dict['subject'] = "Your modified document is awaiting for approval"

            send_dict['from_email'] = settings.DEFAULT_FROM_EMAIL
            self.process(to, send_dict, data)

        elif mail_type == "AUTO_CLOSER":
            send_dict['subject'] = data.get('subject', "Auto Closer Your Order item")
            template_name = data.get('template_name', 'auto_closer.html')
            send_dict['template'] = 'emailers/' + template_name

            send_dict['header'] = {'Reply-To': settings.REPLY_TO}
            send_dict['bcc_list'] = [settings.CONSULTANTS_EMAIL]
            send_dict['from_email'] = settings.CONSULTANTS_EMAIL

            self.process(to, send_dict, data)

        elif mail_type == "MIDOUT":
            send_dict['subject'] = data.get('subject', "Upload your resume")
            template_name = data.get('template_name', 'midout_mail.html')
            send_dict['template'] = 'emailers/' + template_name
            send_dict['from_email'] = settings.DEFAULT_FROM_EMAIL
            self.process(to, send_dict, data)

        elif mail_type == "RESUME_CRITIQUE":
            send_dict['subject'] = data.get('subject', "Sharing of Evaluated Resume")
            template_name = data.get('template_name', 'critique_mail.html')
            send_dict['template'] = 'emailers/' + template_name
            send_dict['from_email'] = settings.DEFAULT_FROM_EMAIL
            self.process(to, send_dict, data)

        elif mail_type == "BOOSTER_RECRUITER":
            send_dict['subject'] = data.get('subject', "Candidate Resume")
            template_name = data.get('template_name', 'booster_recruiter.html')
            send_dict['template'] = 'emailers/' + template_name

            send_dict['header'] = {'Reply-To': settings.REPLY_TO}
            send_dict['bcc_list'] = [settings.CONSULTANTS_EMAIL]
            send_dict['from_email'] = settings.CONSULTANTS_EMAIL

            self.process(to, send_dict, data)

        elif mail_type == "BOOSTER_CANDIDATE":
            send_dict['subject'] = data.get('subject', "shine booster confirmation")
            template_name = data.get('template_name', 'booster_candidate.html')
            send_dict['template'] = 'emailers/' + template_name

            send_dict['header'] = {'Reply-To': settings.REPLY_TO}
            send_dict['bcc_list'] = [settings.CONSULTANTS_EMAIL]
            send_dict['from_email'] = settings.CONSULTANTS_EMAIL

            self.process(to, send_dict, data)

        elif mail_type == "FEATURED_UPDATE_MAIL":
            send_dict['subject'] = data.get('subject', "your profile updated")
            template_name = data.get('template_name', 'featured_profile.html')
            send_dict['template'] = 'emailers/' + template_name

            send_dict['header'] = {'Reply-To': settings.REPLY_TO}
            send_dict['bcc_list'] = [settings.CONSULTANTS_EMAIL]
            send_dict['from_email'] = settings.CONSULTANTS_EMAIL

            self.process(to, send_dict, data)

        elif mail_type == "COURSE_CLOSER_MAIL":
            send_dict['subject'] = data.get('subject', "Your service has been processed")
            template_name = data.get('template_name', 'course-closer.html')
            send_dict['template'] = 'emailers/' + template_name

            send_dict['header'] = {'Reply-To': settings.REPLY_TO}
            send_dict['bcc_list'] = [settings.CONSULTANTS_EMAIL]
            send_dict['from_email'] = settings.CONSULTANTS_EMAIL

            self.process(to, send_dict, data)

        elif mail_type == "INTERNATIONATIONAL_PROFILE_UPDATE_MAIL":
            send_dict['subject'] = data.get('subject', "your profile updated")
            template_name = data.get('template_name', 'featured_profile.html')
            send_dict['template'] = 'emailers/' + template_name

            send_dict['header'] = {'Reply-To': settings.REPLY_TO}
            send_dict['bcc_list'] = [settings.CONSULTANTS_EMAIL]
            send_dict['from_email'] = settings.CONSULTANTS_EMAIL

            self.process(to, send_dict, data)

        elif mail_type == "AUTO_REGISTER":
            send_dict['subject'] = data.get('subject', "Your login credential on shinelearning")
            template_name = data.get('template_name', 'auto-register.html')
            send_dict['template'] = 'emailers/' + template_name

            send_dict['header'] = {'Reply-To': settings.REPLY_TO}
            send_dict['bcc_list'] = [settings.CONSULTANTS_EMAIL]
            send_dict['from_email'] = settings.CONSULTANTS_EMAIL

        elif mail_type == "FORGOT_PASSWORD":

            send_dict['subject'] = "Forgot Password"
            send_dict['template'] = 'emailers/payment_confirm.html'
            send_dict['from_email'] = settings.CONSULTANTS_EMAIL
            send_dict['header'] = {'Reply-To': settings.REPLY_TO}
            token = TokenGeneration().encode(data.get("email", ''), '1', 1)
            data['reset_url'] = "http://%s/user/update/password/?token=%s" % (settings.SITE_DOMAIN, token)
            data['button_text'] = "Click Here To Reset Password"
            self.process(to, send_dict, data)
