#python imports
import os,django,sys,imaplib,email,smtplib,logging

from re import search
from datetime import datetime,timedelta,date

#Settings imports
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "careerplus.config.settings_staging")
ROOT_FOLDER = os.path.realpath(os.path.dirname(__file__))
ROOT_FOLDER = ROOT_FOLDER[:ROOT_FOLDER.rindex('/')]
if ROOT_FOLDER not in sys.path:
    sys.path.insert(1, ROOT_FOLDER + '/')
django.setup()

#app imports
from order.models import Order

#django imports
from django.core.cache import cache

ORG_EMAIL   = "@gmail.com"
USER  = "hiteshrexwal003" + ORG_EMAIL
PASSWD    = "hidden@leaf"
IMAP_SERVER = "imap.gmail.com"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT   = 587
TO_ADDRESS = 'hitesh.rexwal@hindustantimes.com'

def auto_forward_emails():
    try:
        #login in imap and smtp
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        smtp = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        smtp.starttls()
        smtp.login(USER, PASSWD)
        mail.login(USER,PASSWD)
        mail.select('inbox')
        # searching query
        current_date = date.today().strftime('%d-%b-%Y')
        status, data = mail.uid('SEARCH',None, 'ON '+current_date)
    except Exception as e:
        logging.getLogger('error_log').error("login in imap or smtp/quering mailbox failed - %s" % (str(e)))
        return
    
    mail_ids = data[0] 
    # in cache we store a set of all message uid's done on that day
    all_day_ids = mail_ids.split()
    id_list = list(set(mail_ids.split())- cache.get('message_uids_done',set()))

    #varaibles for logging
    total_msg_forwarded = 0
    total_msg_forward_failed = 0

    for id in id_list:
        try:
            mail_status, mail_data = mail.uid('FETCH',id, '(RFC822)' ) #fetching mail from uid
        except Exception as e:
            logging.getLogger('error_log').error("mail fetch failed - %s" % (str(e)))
            continue
        
        for response_part in mail_data:
            if not isinstance(response_part, tuple): # response of message coming in tuple so a check here
                continue
            
            msg = email.message_from_string(response_part[1].decode('utf-8'))
            email_from =  search('<(.+)>', msg['from']).group(1) if search('<(.+)>', msg['from']) is not None else None
            msg_datetime = datetime.strptime(msg['date'],'%a, %d %b %Y %H:%M:%S %z')

            if not email_from:
                continue

            #checking if email from has any order in 90 days
            start_date = datetime.today().date()-timedelta(days=90)
            count = Order.objects.filter(email=email_from,payment_date__gte=start_date).count()

            if count:
                mail.uid('STORE',id,'+FLAGS','\SEEN') #make email seen as it will be forwarded
                msg.replace_header("From", USER)
                msg.replace_header("To", TO_ADDRESS)
                msg.add_header('reply-to', email_from) 

                try:
                    smtp.sendmail(USER, TO_ADDRESS, msg.as_string()) #Forward mail to resume@shine.com
                    total_msg_forwarded += 1
                except Exception as e:
                    total_msg_forward_failed +=1
                    logging.getLogger('error_log').error("Forward mail to resume@shine.com failed - %s" % (str(e)))
                    mail.uid('STORE',id,'-FLAGS','\SEEN')
                    continue
            else:
                mail.uid('STORE',id,'-FLAGS','\SEEN')

    
    cache.set('message_uids_done',set(all_day_ids),3600)
    mail.close()
    mail.logout()
    smtp.quit()
    logging.getLogger('error_log').error("total messages forwarded - %s" % (str(total_msg_forwarded)))
    logging.getLogger('error_log').error("total messages forward failed - %s" % (str(total_msg_forward_failed)))

auto_forward_emails()

