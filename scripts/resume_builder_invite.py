import os, django, sys, csv, math
import multiprocessing as mp
from django.core.mail import EmailMessage
from django.core import mail
from django.conf import settings
from django.template.loader import render_to_string

# from core.mixins import TokenGeneration

sub_lists = []


def get_emails(user_details):
    mail_list = []
    for row in user_details:
        name = row['name']
        email = row['email']
        token_gen = TokenGeneration()
        login_token = token_gen.encode(email, 2)
        msg = EmailMessage(
            subject="New Message",
            body=render_to_string('emailers/candidate/resume_builder_invite.html',
                                  {'first_name': name, 'login_token': login_token,
                                   'upload_url': 'https://learning.shine.com'}),
            to=[email],
            from_email=settings.DEFAULT_FROM_EMAIL
        )
        msg.content_subtype = 'html'
        mail_list.append(msg)
    return mail_list


def bulk_email_send(details, output_method):
    connection = mail.get_connection()
    emails = get_emails(details)
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
    from core.mixins import TokenGeneration

    with open('test_file.csv') as csv_file:
        reader = csv.DictReader(csv_file)
        list_data = [row for row in reader]
        sub_lists_length = math.ceil(len(list_data) / 10)
        for ind in range(0, sub_lists_length):
            sub_lists.append(list_data[ind * 10: ind * 10 + 10])
    # Define an output queue
    output = mp.Queue()

    # Setup a list of processes that we want to run
    processes = [mp.Process(target=bulk_email_send, args=(x, output)) for x in sub_lists]

    # Run processes
    for p in processes:
        p.start()

    # Exit the completed processes
    for p in processes:
        p.join()

    # Get process results from the output queue
    results = [output.get() for p in processes]

    print(results)
