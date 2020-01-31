from django.core.management.base import BaseCommand
from emailers.feedback import feedback_emailer


class Command(BaseCommand):
    """
        Daily Cron for feedback after close orderitem send mail
    """

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)

    def handle(self, *args, **options):
        feedback_emailer('feedback_emailer')