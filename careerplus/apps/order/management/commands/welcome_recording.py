import logging
from django.core.management.base import BaseCommand
from datetime import timezone,timedelta

from .models import WelcomeCallOperation



class Command(BaseCommand):
    def handle(self, *args, **options):
        fetch_call_recording_links()






def fetch_call_recording_links():
    fetched_count = 0
    current_time = timezone.now().replace(hour=00,minute=00,second=00)
    welcome_calls = WelcomeCallOperation.objects.filter(modified__gte=current_time)

