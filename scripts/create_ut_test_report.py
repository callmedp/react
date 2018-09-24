#python imports
import os,django,sys,subprocess

#Settings imports
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "careerplus.config.settings_staging")
ROOT_FOLDER = os.path.realpath(os.path.dirname(__file__))
ROOT_FOLDER = ROOT_FOLDER[:ROOT_FOLDER.rindex('/')]
if ROOT_FOLDER not in sys.path:
    sys.path.insert(1, ROOT_FOLDER + '/')
django.setup()

#django imports
from django.conf import settings
from django.core.mail import EmailMessage

#local imports

#inter app imports

#third party imports

#Global Constants
TEAM_EMAILS = [
    "Animesh Sharma<animesh.sharma@hindustantimes.com>",
    "Amarnath Kumar<amar.kumar@hindustantimes.com>",
    "Amardeep Vishwakarma<amardeep.vishwakarma@hindustantimes.com>",
    "Shubham Dwivedi<shubham.dwivedi@hindustanimes.com>",
    "Ritesh Bisht<ritesh.bisht@hindustantimes.com>"]



def send_email_to_team_members():
    html_content = "<html><title></title><body>The UT coverage report for Shine Learning is ready.<br><br>\
        You can check it out <a href='{}/dev/ut-coverage/index.html' >here.</a> <br><br>\
        In case of any doubt, please feel free to contact.</body></html>".format(
            settings.MAIN_DOMAIN_PREFIX)

    email = EmailMessage(
        subject="Shine Learning UT Coverage Report", body=html_content,
        from_email=settings.DEFAULT_FROM_EMAIL, to=TEAM_EMAILS)
    email.content_subtype = "html"
    return email.send(fail_silently=False)


def create_index_template(app_names):
    index_dynamic_content = ["<a href='{}/dev/ut-coverage/coverage-{}/index.html' target='_blank'>{}</a><br><br>".\
        format(
            settings.MAIN_DOMAIN_PREFIX,
            app_name,
            app_name.title()) for app_name in app_names]

    index_content = "<html><title></title><body><h1>Learning UT Coverage Report</h1>{}</body></html>".\
        format(" ".join(index_dynamic_content))
    index_file_obj = open("{}/ut-coverage/index.html".format(settings.PROJECT_DIR),"wt",encoding="utf-8")
    index_file_obj.write(index_content)
    index_file_obj.close()


if __name__=="__main__":
    local_apps = settings.LOCAL_APPS
    app_names = local_apps

    for app_name in app_names:
        #Run command to generate coverage for each app.
        #Note the file naming concerned with app handling.

        coverage_shell_command = "export COVERAGE_FILE=.coverage-{} && cd {} && \
            coverage run --source={} manage.py test --keepdb".\
            format(app_name, settings.PROJECT_DIR, app_name)

        subprocess.call(coverage_shell_command, shell=True)

        #Run command to create HTML folders.
        html_shell_command = "export COVERAGE_FILE=.coverage-{} && cd {} && \
            coverage html -d ut-coverage/coverage-{}".\
            format(app_name, settings.PROJECT_DIR, app_name)

        subprocess.call(html_shell_command, shell=True)

        #Delete coverage files once the beautification is complete.
        delete_shell_command = "cd {} && rm -rf .coverage-{}".format(
            settings.PROJECT_DIR, app_name)
        subprocess.call(delete_shell_command, shell=True)

    #Create a common index for all apps. 
    create_index_template(app_names)
    send_email_to_team_members()
