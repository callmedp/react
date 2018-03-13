import logging
from django.core.management.base import BaseCommand

from shop.mixins import CourseCatalogueMixin


class Command(BaseCommand, CourseCatalogueMixin):
    """
    Custom command to Update course catalogue list in cache.
    """
    help = 'Update course catalogue in cache'

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)

    def handle(self, *args, **options):
        self.get_course_catalogue_context()
        print ('course catalogue updated in cache.')
        logging.getLogger('info_log').info("course catalogue updated in cache.")
