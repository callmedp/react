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
            # cc = ['upenders379@gmail.com']
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

        self.base_send_mail(subject=send_dict.get('subject', 'Shinelearning'), body=body, to=to, from_email=send_dict.get('from_email', settings.DEFAULT_FROM_EMAIL), headers=send_dict.get('header', None), cc=send_dict.get('cc_list', None), bcc=send_dict.get('bcc_list', None), fail_silently=False, attachments=[])
                
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

        elif mail_type == "REGISTRATION":
            send_dict['template'] = 'emailers/candidate/register.html'
            send_dict['subject'] = "Welcome to Shine"
            send_dict['header'] = {'Reply-To': settings.REPLY_TO}
            send_dict['bcc_list'] = [settings.CONSULTANTS_EMAIL]
            send_dict['from_email'] = settings.CONSULTANTS_EMAIL
            self.process(to, send_dict, data)

        elif mail_type == "PAYMENT_PENDING":
            send_dict['template'] = 'emailers/candidate/payment_pending.html'
            send_dict['subject'] = data.get('subject', '')
            send_dict['header'] = {'Reply-To': settings.REPLY_TO}
            send_dict['bcc_list'] = [settings.CONSULTANTS_EMAIL]
            send_dict['from_email'] = settings.CONSULTANTS_EMAIL
            self.process(to, send_dict, data)
            
        elif str(mail_type) == "2":
            send_dict['subject'] = "Linkedin Profile"
            send_dict['template'] = 'emailers/payment_confirm.html'

        elif mail_type == "PROCESS_MAILERS":
            send_dict['subject'] = data.get('subject', '')
            send_dict['template'] = 'emailers/candidate/process_mailers.html'
            if data.get('type_flow') == 1:
                send_dict['upload_url'] = "http://%s/dashboard" % (settings.SITE_DOMAIN)
            elif data.get('type_flow') == 8:
                send_dict['counselling_form'] = "http://%s/linkedin/counsellingform/%s" % (settings.SITE_DOMAIN, data.get('pk'))
            elif data.get('type_flow') == 9:
                send_dict['complete_profile'] = "http://%s/dashboard/roundone/profile/" % (settings.SITE_DOMAIN)
            elif data.get('type_flow') == 10:
                pass
            send_dict['from_email'] = settings.DEFAULT_FROM_EMAIL
            data['email'] = [to]
            self.process(to, send_dict, data)

        elif mail_type == "ALLOCATED_TO_WRITER":
            send_dict['subject'] = data.get('subject', '')
            template_name = data.get('template_name', 'assignment_mail.html')
            send_dict['template'] = 'emailers/candidate/' + template_name
            send_dict['header'] = {'Reply-To': settings.REPLY_TO}
            send_dict['bcc_list'] = [settings.CONSULTANTS_EMAIL]
            if data.get('writer_email', None):
                send_dict['cc_list'] = []
                send_dict['cc_list'].append(data.get('writer_email'))
            send_dict['from_email'] = settings.CONSULTANTS_EMAIL
            self.process(to, send_dict, data)

        elif mail_type == "DRAFT_UPLOAD":
            # for first draft
            if data.get('draft_level') == 1:
                send_dict['template'] = 'emailers/candidate/initial_document.html'
                send_dict['subject'] = "Your developed document has been uploaded"
            # for 2nd draft
            elif data.get('draft_level') == 2:
                send_dict['template'] = 'emailers/candidate/revised_document.html'
                send_dict['subject'] = "Your developed document is ready"
            # for 3rd draf
            elif data.get('draft_level') == 3:
                send_dict['template'] = 'emailers/candidate/final_document.html'
                send_dict['subject'] = "Your final document is ready"
            token = AutoLogin().encode(data.get('email', ''), data.get('candidateid', ''))
            data['autologin'] = "http://%s/autologin/%s/" % (settings.SITE_DOMAIN, token)
            send_dict['from_email'] = settings.DEFAULT_FROM_EMAIL
            self.process(to, send_dict, data)

        elif mail_type == "REMINDER":
            send_dict['template'] = 'emailers/candidate/draft_reminder.html'
            send_dict['subject'] = "Reminder:Your developed document has been uploaded"
            send_dict['from_email'] = settings.DEFAULT_FROM_EMAIL
            self.process(to, send_dict, data)

        elif mail_type == "WRITING_SERVICE_CLOSED":
            send_dict['subject'] = data.get('subject', "")
            template_name = data.get('template_name', 'writing_service_closed.html')
            send_dict['template'] = 'emailers/candidate/' + template_name

            send_dict['header'] = {'Reply-To': settings.REPLY_TO}
            send_dict['bcc_list'] = [settings.CONSULTANTS_EMAIL]
            send_dict['from_email'] = settings.CONSULTANTS_EMAIL

            self.process(to, send_dict, data)

        elif mail_type == "PENDING_ITEMS":
            send_dict['subject'] = data.get('subject', "To initiate your services fulfil these details")
            template_name = data.get('template_name', 'pending_item.html')
            send_dict['template'] = 'emailers/candidate/' + template_name
            send_dict['from_email'] = settings.DEFAULT_FROM_EMAIL
            self.process(to, send_dict, data)

        elif mail_type == "RESUME_CRITIQUE_CLOSED":
            send_dict['subject'] = data.get('subject', "Your developed document has been uploaded")
            send_dict['template'] = 'emailers/candidate/resume_critique_closed.html'
            token = AutoLogin().encode(data.get('email', ''), data.get('candidateid', ''))
            data['autologin'] = "http://%s/autologin/%s/" % (settings.SITE_DOMAIN, token)
            send_dict['from_email'] = settings.DEFAULT_FROM_EMAIL
            self.process(to, send_dict, data)

        elif mail_type == "BOOSTER_RECRUITER":
            send_dict['subject'] = data.get('subject', "Resumes of active candidates seeking jobs")
            template_name = data.get('template_name', 'booster_recruiter.html')
            send_dict['template'] = 'emailers/candidate/' + template_name

            send_dict['header'] = {'Reply-To': settings.REPLY_TO}
            send_dict['bcc_list'] = [settings.CONSULTANTS_EMAIL]
            send_dict['from_email'] = settings.CONSULTANTS_EMAIL

            self.process(to, send_dict, data)

        elif mail_type == "BOOSTER_CANDIDATE":
            send_dict['subject'] = data.get('subject', "Your resume has been shared with relevant consultants")
            template_name = data.get('template_name', 'booster_candidate.html')
            send_dict['template'] = 'emailers/candidate/' + template_name

            send_dict['header'] = {'Reply-To': settings.REPLY_TO}
            send_dict['bcc_list'] = [settings.CONSULTANTS_EMAIL]
            send_dict['from_email'] = settings.CONSULTANTS_EMAIL

            self.process(to, send_dict, data)

        elif mail_type == "YOUR_RESUME_FEATURED_SERVICE_STARTED":
            send_dict['subject'] = data.get('subject', "Your featured profile service has been started")
            template_name = data.get('template_name', 'featured_profile.html')
            send_dict['template'] = 'emailers/candidate/' + template_name

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

        elif mail_type == "INTERNATIONATIONAL_PROFILE_UPDATED":
            send_dict['subject'] = data.get('subject', "Your International Profile is updated")
            template_name = data.get('template_name', 'international_profile.html')
            send_dict['template'] = 'emailers/candidate/' + template_name

            send_dict['header'] = {'Reply-To': settings.REPLY_TO}
            send_dict['bcc_list'] = [settings.CONSULTANTS_EMAIL]
            send_dict['from_email'] = settings.CONSULTANTS_EMAIL

            self.process(to, send_dict, data)

        elif mail_type == "AUTO_REGISTER":
            send_dict['subject'] = data.get('subject', "Your login credential on shine.com")
            template_name = data.get('template_name', 'auto-register.html')
            send_dict['template'] = 'emailers/' + template_name

            send_dict['header'] = {'Reply-To': settings.REPLY_TO}
            send_dict['bcc_list'] = [settings.CONSULTANTS_EMAIL]
            send_dict['from_email'] = settings.CONSULTANTS_EMAIL

        elif mail_type == "FORGOT_PASSWORD":
            send_dict['subject'] = "Your Shine.com password"
            send_dict['template'] = 'emailers/candidate/email_forgot_pass.html'
            send_dict['from_email'] = settings.CONSULTANTS_EMAIL
            send_dict['header'] = {'Reply-To': settings.REPLY_TO}
            token = TokenGeneration().encode(data.get("email", ''), '1', 1)
            data['reset_url'] = "http://%s/user/update/password/?token=%s" % (settings.SITE_DOMAIN, token)
            self.process(to, send_dict, data)

        elif mail_type == "CART_DROP_OUT":
            send_dict['subject'] = "PMI Agile is ready to checkout"
            send_dict['template'] = 'emailers/candidate/cart_drop_out.html'
            send_dict['from_email'] = settings.CONSULTANTS_EMAIL
            send_dict['header'] = {'Reply-To': settings.REPLY_TO}
            self.process(to, send_dict, data)

        elif mail_type == "SHINE_PAYMENT_CONFIRMATION":
            send_dict['subject'] = "Your Shine Payment Confirmation"
            send_dict['template'] = 'emailers/candidate/payment_realisation.html'
            send_dict['from_email'] = settings.CONSULTANTS_EMAIL
            send_dict['header'] = {'Reply-To': settings.REPLY_TO}
            self.process(to, send_dict, data)
