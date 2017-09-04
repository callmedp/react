import logging

from django.core.management.base import BaseCommand
from emailers.feedback import feedback_emailer

class Command(BaseCommand):
    """
        Daily Cron for draft reminder mail/Sms
    """

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)

    def handle(self, *args, **options):
        feedback_emailer()