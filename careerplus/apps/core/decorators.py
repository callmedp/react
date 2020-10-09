from core.utils import send_failure_mail

def run_cron(func):
    def inner(cron_name):
        try:
            func(cron_name)
        except Exception as e:
            send_failure_mail(cron_name,e)
    return inner