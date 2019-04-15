import logging
import json
from datetime import datetime
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
        if settings.DEBUG and settings.TEST_EMAIL:
            subject = "Test Mail " + subject
            to = ['priya.kharb@hindustantimes.com']
            cc = []
        else:
            bcc = [settings.DEFAULT_FROM_EMAIL]
        emsg = EmailMessage(subject, body=body, to=to, from_email=from_email, headers=headers, cc=cc, bcc=bcc, attachments=[])
        emsg.content_subtype = "html"
        if attachments:
            try:
                emsg.attach(
                    filename=attachments[0], content=attachments[1],
                    mimetype=mimetype)
            except Exception as e:
                logging.getLogger('error_log').error(
                    "%s - %s" % (str(to), str(e)))
        emsg.send()

    def render_template(self, template, context):
        return render_to_string(template, context)

    def process(self, to=None, send_dict=None, data=None):
        try:
            body = self.render_template(send_dict['template'], data)
        except Exception as e:
            logging.getLogger('error_log').error("%s - %s" % (str(to), str(e)))

        self.base_send_mail(subject=send_dict.get('subject', 'Shinelearning'), body=body, to=to, from_email=send_dict.get('from_email', settings.DEFAULT_FROM_EMAIL), headers=send_dict.get('header', None), cc=send_dict.get('cc_list', None), bcc=send_dict.get('bcc_list', None), fail_silently=False, attachments=[])

    def send(self, to=None, mail_type=None, data={}):
        send_dict = {}

        if mail_type == "REGISTRATION":
            send_dict['template'] = 'emailers/candidate/register.html'
            send_dict['subject'] = "Welcome to Shine"
            headers_dict = {'Reply-To': settings.REPLY_TO}
            if settings.TAG_MAILER:
                headers_dict.update({
                    'X-APIHEADER': json.dumps({'X-Uid': 'SLRegistration'}),
                    'X-TAGS': 'SLRegistration',
                    'X-MailerTag': 'SLRegistration',
                    'X-SentDate': datetime.now(),
                })
            send_dict['header'] = headers_dict
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

        elif mail_type == "PROCESS_MAILERS":
            send_dict['subject'] = data.get('subject', '')
            send_dict['template'] = 'emailers/candidate/process_mailers.html'
            send_dict['from_email'] = settings.DEFAULT_FROM_EMAIL
            send_dict['header'] = {'Reply-To': settings.REPLY_TO}
            send_dict['bcc_list'] = [settings.CONSULTANTS_EMAIL]
            self.process(to, send_dict, data)

        elif mail_type == "ALLOCATED_TO_WRITER":
            send_dict['subject'] = data.get('subject', '')
            template_name = data.get('template_name', 'assignment_mail.html')
            send_dict['template'] = 'emailers/candidate/' + template_name
            headers_dict = {'Reply-To': settings.REPLY_TO}
            if settings.TAG_MAILER:
                headers_dict.update({
                    'X-APIHEADER': json.dumps({'X-Uid': 'SLServiceInitiated'}),
                    'X-TAGS': 'SLServiceInitiated',
                    'X-MailerTag': 'SLServiceInitiated',
                    'X-SentDate': datetime.now(),
                })
            send_dict['header'] = headers_dict
            send_dict['bcc_list'] = [settings.CONSULTANTS_EMAIL]

            if data.get('writer_email', None):
                send_dict['cc_list'] = []
                send_dict['cc_list'].append(data.get('writer_email'))
            send_dict['from_email'] = settings.CONSULTANTS_EMAIL
            self.process(to, send_dict, data)

        elif mail_type == "DRAFT_UPLOAD":
            # for first draft
            headers_dict = None
            if data.get('draft_level') == 1:
                send_dict['template'] = 'emailers/candidate/initial_document.html'
                send_dict['subject'] = "Your developed document has been uploaded"
                if settings.TAG_MAILER:
                    headers_dict = {
                        'Reply-To': settings.REPLY_TO,
                        'X-APIHEADER': json.dumps({'X-Uid': 'SLDevelopedDocumentUploaded'}),
                        'X-TAGS': 'SLDevelopedDocumentUploaded',
                        'X-MailerTag': 'SLDevelopedDocumentUploaded',
                        'X-SentDate': datetime.now(),
                    }
            # for 2nd draft
            elif data.get('draft_level') == 2:
                send_dict['template'] = 'emailers/candidate/revised_document.html'
                send_dict['subject'] = "Your developed document is ready"
                if settings.TAG_MAILER:
                    headers_dict = {
                        'Reply-To': settings.REPLY_TO,
                        'X-APIHEADER': json.dumps({'X-Uid': 'SLDevelopedDocumentUploaded'}),
                        'X-TAGS': 'SLDevelopedDocumentUploaded',
                        'X-MailerTag': 'SLDevelopedDocumentUploaded',
                        'X-SentDate': datetime.now(),
                    }
            # for 3rd draf
            elif data.get('draft_level') == 3:
                send_dict['template'] = 'emailers/candidate/final_document.html'
                send_dict['subject'] = "Your final document is ready"
                if settings.TAG_MAILER:
                    headers_dict = {
                        'Reply-To': settings.REPLY_TO,
                        'X-APIHEADER': json.dumps({'X-Uid': 'SLDevelopedDocumentReady'}),
                        'X-TAGS': 'SLDevelopedDocumentReady',
                        'X-MailerTag': 'SLDevelopedDocumentReady',
                        'X-SentDate': datetime.now(),
                    }
            send_dict['header'] = headers_dict
            send_dict['from_email'] = settings.DEFAULT_FROM_EMAIL
            send_dict['bcc_list'] = [settings.CONSULTANTS_EMAIL]
            self.process(to, send_dict, data)

        elif mail_type == "REMINDER":
            send_dict['template'] = 'emailers/candidate/draft_reminder.html'
            send_dict['subject'] = "Reminder:Your developed document has been uploaded"
            send_dict['from_email'] = settings.DEFAULT_FROM_EMAIL
            send_dict['header'] = {'Reply-To': settings.REPLY_TO}
            send_dict['bcc_list'] = [settings.CONSULTANTS_EMAIL]
            self.process(to, send_dict, data)

        elif mail_type == "WRITING_SERVICE_CLOSED":
            send_dict['subject'] = data.get('subject', "")
            template_name = data.get('template_name', 'writing_service_closed.html')
            send_dict['template'] = 'emailers/candidate/' + template_name
            headers_dict = {'Reply-To': settings.REPLY_TO}
            if settings.TAG_MAILER:
                headers_dict.update({
                    'X-APIHEADER': json.dumps({'X-Uid': 'SLServiceClosed'}),
                    'X-TAGS': 'SLServiceClosed',
                    'X-MailerTag': 'SLServiceClosed',
                    'X-SentDate': datetime.now(),
                })
            send_dict['header'] = headers_dict
            send_dict['bcc_list'] = [settings.CONSULTANTS_EMAIL]
            send_dict['from_email'] = settings.CONSULTANTS_EMAIL

            self.process(to, send_dict, data)

        elif mail_type == "PENDING_ITEMS":
            send_dict['subject'] = data.get('subject', "To initiate your services fulfil these details")
            template_name = data.get('template_name', 'pending_item.html')
            send_dict['template'] = 'emailers/candidate/' + template_name
            send_dict['from_email'] = settings.DEFAULT_FROM_EMAIL
            send_dict['header'] = {'Reply-To': settings.REPLY_TO}
            send_dict['bcc_list'] = [settings.CONSULTANTS_EMAIL]
            self.process(to, send_dict, data)

        elif mail_type == "RESUME_CRITIQUE_CLOSED":
            send_dict['subject'] = data.get('subject', "Your developed document has been uploaded")
            send_dict['template'] = 'emailers/candidate/resume_critique_closed.html'
            send_dict['from_email'] = settings.DEFAULT_FROM_EMAIL
            send_dict['header'] = {'Reply-To': settings.REPLY_TO}
            send_dict['bcc_list'] = [settings.CONSULTANTS_EMAIL]
            self.process(to, send_dict, data)

        elif mail_type == "BOOSTER_RECRUITER":
            send_dict['subject'] = data.get('subject', "Resumes of active candidates seeking jobs")
            template_name = data.get('template_name', 'booster_recruiter.html')
            send_dict['template'] = 'emailers/candidate/' + template_name
            headers_dict = {'Reply-To': settings.REPLY_TO}
            if settings.TAG_MAILER:
                headers_dict.update({
                    'X-APIHEADER': json.dumps({'X-Uid': 'SLResumeBoosterRecruiter'}),
                    'X-TAGS': 'SLResumeBoosterRecruiter',
                    'X-MailerTag': 'SLResumeBoosterRecruiter',
                    'X-SentDate': datetime.now(),
                })
            send_dict['header'] = headers_dict
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

        elif mail_type == "FEATURED_PROFILE_UPDATED":
            send_dict['subject'] = data.get('subject', "Your Featured Profile Is Updated")
            template_name = data.get('template_name', 'feature_profile.html')
            send_dict['template'] = 'emailers/candidate/' + template_name

            send_dict['header'] = {'Reply-To': settings.REPLY_TO}
            send_dict['bcc_list'] = [settings.CONSULTANTS_EMAIL]
            send_dict['from_email'] = settings.CONSULTANTS_EMAIL

            self.process(to, send_dict, data)

        elif mail_type == "PRIORITY_APPLICANT_MAIL":
            send_dict['subject'] = data.get('subject', "Congratulations, you are now Shine’s Priority Applicant")
            template_name = data.get('template_name', 'priority_applicant.html')
            send_dict['template'] = 'emailers/candidate/' + template_name

            send_dict['header'] = {'Reply-To': settings.REPLY_TO}
            send_dict['bcc_list'] = [settings.CONSULTANTS_EMAIL]
            send_dict['from_email'] = settings.CONSULTANTS_EMAIL

            self.process(to, send_dict, data)

        elif mail_type == "COURSE_CLOSER_MAIL":
            send_dict['subject'] = data.get('subject', "Your service(s) has been initiated")
            template_name = data.get('template_name', 'candidate/course_closure.html')
            send_dict['template'] = 'emailers/' + template_name
            send_dict['header'] = {'Reply-To': settings.REPLY_TO}
            send_dict['bcc_list'] = [settings.CONSULTANTS_EMAIL]
            send_dict['from_email'] = settings.CONSULTANTS_EMAIL
            if settings.TAG_MAILER:
                headers_dict = {
                    'X-APIHEADER': json.dumps({'X-Uid': 'SLServiceInitiated'}),
                    'X-TAGS': 'SLServiceInitiated',
                    'X-MailerTag': 'SLServiceInitiated',
                    'X-SentDate': datetime.now(),
                }
                send_dict['header'] = headers_dict
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
            template_name = data.get('template_name', 'register.html')
            send_dict['template'] = 'emailers/candidate/' + template_name
            send_dict['header'] = {'Reply-To': settings.REPLY_TO }
            send_dict['bcc_list'] = [settings.CONSULTANTS_EMAIL]
            send_dict['from_email'] = settings.CONSULTANTS_EMAIL

            self.process(to, send_dict, data)

        elif mail_type == "FORGOT_PASSWORD":
            send_dict['subject'] = "Your Shine.com password"
            send_dict['template'] = 'emailers/candidate/email_forgot_pass.html'
            send_dict['from_email'] = settings.CONSULTANTS_EMAIL
            send_dict['header'] = {'Reply-To': settings.REPLY_TO}
            token = TokenGeneration().encode(data.get("email", ''), '1', 1)
            data['reset_url'] = "%s://%s/user/update/password/?token=%s" % (settings.SITE_PROTOCOL, settings.SITE_DOMAIN, token)
            send_dict['bcc_list'] = [settings.CONSULTANTS_EMAIL]
            self.process(to, send_dict, data)

        elif mail_type == "CART_DROP_OUT":
            send_dict['subject'] = data.get('subject', "")
            send_dict['template'] = 'emailers/candidate/cart_drop_out.html'
            send_dict['from_email'] = settings.CONSULTANTS_EMAIL
            send_dict['header'] = {'Reply-To': settings.REPLY_TO}
            send_dict['bcc_list'] = [settings.CONSULTANTS_EMAIL]
            self.process(to, send_dict, data)

        elif mail_type == "SHINE_PAYMENT_CONFIRMATION":
            send_dict['subject'] = "Your Shine Payment Confirmation"
            send_dict['template'] = 'emailers/candidate/payment_realisation.html'
            send_dict['from_email'] = settings.CONSULTANTS_EMAIL
            headers_dict = {'Reply-To': settings.REPLY_TO}
            if settings.TAG_MAILER:
                headers_dict.update({
                    'X-APIHEADER': json.dumps({'X-Uid': 'SL_PaymentConfirmation'}),
                    'X-TAGS': 'SL_PaymentConfirmation',
                    'X-MailerTag': 'SL_PaymentConfirmation',
                    'X-SentDate': datetime.now(),
                })
            send_dict['header'] = headers_dict

            send_dict['bcc_list'] = [settings.CONSULTANTS_EMAIL]
            self.process(to, send_dict, data)
