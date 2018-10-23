import logging
from django.core.management.base import BaseCommand
from django.db.models import Q
from users.models import UserProfile,User
from users.mixins import WriterInvoiceMixin





class Command(BaseCommand):
    help = "Generates writer's invoice"


    def handle(self, *args, **options):
        result=None
        users_list = list(UserProfile.objects.filter(~Q(
            writer_type=0)).values_list('user',flat=True))
        users = User.objects.filter(id__in=users_list,is_active=True)
        for writ_user in users:
            result = WriterInvoiceMixin().save_writer_invoice_pdf(
                user=writ_user)
            error = result.get('error', None)
            if error:
                logging.getLogger('error_log').error(
                    ",error_msg=" + error+ ',for'+'user='+str(writ_user))














