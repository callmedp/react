#python imports
import os,django,sys,imaplib,email,smtplib
from re import search
from datetime import datetime,timedelta

#Settings imports
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "careerplus.config.settings_staging")
ROOT_FOLDER = os.path.realpath(os.path.dirname(__file__))
ROOT_FOLDER = ROOT_FOLDER[:ROOT_FOLDER.rindex('/')]
if ROOT_FOLDER not in sys.path:
    sys.path.insert(1, ROOT_FOLDER + '/')
django.setup()

#app imports
from order.models import Order

ORG_EMAIL   = "@gmail.com"
USER  = "hiteshrexwal003" + ORG_EMAIL
PASSWD    = "hidden@leaf"
IMAP_SERVER = "imap.gmail.com"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT   = 587
TO_ADDRESS = 'hitesh.rexwal@hindustantimes.com'

def auto_forward_emails():
    import ipdb; ipdb.set_trace()
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    smtp = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    smtp.starttls()
    smtp.login(USER, PASSWD)
    mail.login(USER,PASSWD)

    mail.select('inbox')

    status, data = mail.uid('SEARCH',None, 'SINCE 19-Aug-2019')
    mail_ids = data[0]
    id_list = mail_ids.split()   
    first_email_id = int(id_list[0])
    latest_email_id = int(id_list[-1])


    for i in range(latest_email_id,first_email_id, -1):
        mail_status, mail_data = mail.uid('FETCH',str(i), '(RFC822)' )
        for response_part in mail_data:
            if not isinstance(response_part, tuple):
                continue
            msg = email.message_from_string(response_part[1].decode('utf-8'))
            email_from =  search('<(.+)>', msg['from']).group(1) if search('<(.+)>', msg['from']) is not None else None
            if not email_from:
                continue
            start_date = datetime.today().date()-timedelta(days=90)
            if Order.objects.filter(email=email_from,payment_date__gte=start_date).count():
                print('seen')
                mail.uid('STORE',str(i),'+FLAGS','\SEEN')
                msg.replace_header("From", USER)
                msg.replace_header("To", TO_ADDRESS)
                msg.add_header('reply-to', email_from)
                smtp.sendmail(USER, TO_ADDRESS, msg.as_string())
            else:
                print('unseen')
                mail.uid('STORE',str(i),'-FLAGS','\SEEN')
            print(email_from)
    mail.close()
    mail.logout()
    smtp.quit()

auto_forward_emails()

