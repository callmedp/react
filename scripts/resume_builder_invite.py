import os, django, sys, csv, math
import multiprocessing as mp
from django.core.mail import (EmailMessage, get_connection)
from django.conf import settings

from django.template.loader import render_to_string


def get_emails(user_details):
    mail_list = []
    for row in user_details:
        name = row['name']
        email = row['email']
        token_gen = AutoLogin()
        login_token = token_gen.encode(email, '5c4ede4da4d7330573d8c79b', None)
        upload_url = "http://127.0.0.1:8000/autologin/%s/?next=/resume-builder/register/" % (
            login_token)
        context_data = {
            'first_name': name,
            'upload_url': upload_url
        }
        msg = EmailMessage(
            subject="New Message",
            body=render_to_string('emailers/candidate/resume_builder_invite.html', context_data),
            to=[email],
            from_email=settings.DEFAULT_FROM_EMAIL
        )
        msg.content_subtype = 'html'
        mail_list.append(msg)
    return mail_list


def bulk_email_send(file_id, output_method):
    csv_file = open('file_{}.csv'.format(file_id), 'r')
    reader = csv.DictReader(csv_file)
    candidate_info = [row for row in reader]
    csv_file.close()
    if not (len(candidate_info)):
        return
    connection = get_connection()
    emails = get_emails(candidate_info)
    connection.send_messages(emails)
    output_method.put(emails)


if __name__ == '__main__':

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "careerplus.config.settings_staging")

    ROOT_FOLDER = os.path.realpath(os.path.dirname(__file__))
    ROOT_FOLDER = ROOT_FOLDER[:ROOT_FOLDER.rindex('/')]

    if ROOT_FOLDER not in sys.path:
        sys.path.insert(1, ROOT_FOLDER + '/')

    django.setup()
    # import inter apps
    from linkedin.autologin import AutoLogin

    # Define an output queue
    output = mp.Queue()

    # Setup a list of processes that we want to run
    processes = [mp.Process(target=bulk_email_send, args=(x, output)) for x in range(1, 9)]

    # Run processes
    for p in processes:
        p.start()

    # Exit the completed processes
    for p in processes:
        p.join()
