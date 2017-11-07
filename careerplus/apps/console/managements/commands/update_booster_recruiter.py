from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    def handle(self, *args, **options):
        update_recruiter()


def update_recruiter():
    recruiter_list = settings.BOOSTER_RECRUITERS
    pass