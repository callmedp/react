# python imports
import os, django, sys, csv, math, requests

import random, logging
# django imports
from django.core.mail import (EmailMessage, get_connection)
from django.conf import settings
from django.template.loader import render_to_string
from django.core.management.base import BaseCommand

# local imports
from emailers.email import SendMail

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "careerplus.config.settings_staging")

ROOT_FOLDER = os.path.realpath(os.path.dirname(__file__))
ROOT_FOLDER = ROOT_FOLDER[:ROOT_FOLDER.rindex('/')]

if ROOT_FOLDER not in sys.path:
    sys.path.insert(1, ROOT_FOLDER + '/')

#  setup django
django.setup()

# import inter apps
from linkedin.autologin import AutoLogin

COUPON_CODE = "qwerty"
COUPON_VAL = "20"
COUPON_DESC = 'description'


def send_mail_resume(email, candidate_id, name):

    site_domain = "https://resume.shine.com"
    if settings.DEBUG:
        site_domain = "https://resumestage.shine.com"

    token = AutoLogin().encode(email, candidate_id, days=None)

    subjects = [
        "Do you have a job winning resume?",
        "Are you receiving interview calls?",
        "Is your resume getting interview calls?",
        "Why your resume is sabotaging your job search?",
        "Are you impacted by COVID pandemic?",
        "Do you suffer job loss due to COVID?"
    ]

    subject = subjects[random.randint(0, 5)]

    context_data = {
                'token': token,
                'coupon_code':COUPON_CODE,
                'coupon_val' : COUPON_VAL,
                'coupon_desc' : COUPON_DESC,
                'subject': subject,
                'domain_name':site_domain,
                'username': name
            }
    to_email = [email]
    mail_type = "RESUME_BUILDER_PROMOTION"
    SendMail().send(to_email, mail_type, context_data)
    # print(context_data)

def resume_promotion():
    min_exp = 24 #experience = 2 years
    max_exp = '*'       
    row = 100
    start = 0
    loop = True
    sent_mail_count = 0
    testing = False
    query_string = "sMNEx:[{} TO {}]".format(min_exp, max_exp)  
    candidate_solr_url = settings.CANDIDATE_SOLR_URL

    while loop:
        solr_query = '{}?fq={}&rows={}&start={}&indent=on&q=sRST:none&wt=json&fl=id,sEm,sFLN'.format(candidate_solr_url, query_string, row, start)
        response = requests.get(solr_query)

        if response.status_code == 200:
            candidates = response.json()['response']['docs']
            if len(candidates) > 0:
                for cand in candidates:
                    candidate_id = cand.get('id')
                    email = cand.get('sEm')
                    name = cand.get('sFLN')
                    if candidate_id and email and name:
                        sent_mail_count += 1
                        if settings.DEBUG:
                            if not testing:
                                send_mail_resume("kanak.garg@hindustantimes.com","5f9fb6799cbeea23f026f228","kanak")
                                testing = settings.DEBUG
                            break
                        send_mail_resume(email, candidate_id, name)
                start += row
            else:
                loop = False
                break
            logging.getLogger('info_log').info("number of emails sent {}".format(sent_mail_count))
            print("number of emails sent {}".format(sent_mail_count))
        else:
            logging.getLogger('error_log').error("something went wrong"+ str(response.content))
    

class Command(BaseCommand):
    """
    command to send mail
    """
    def handle(self, *args, **options):
        resume_promotion()        