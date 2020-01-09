from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator

from seo.models import AbstractAutoDate

from .functions import get_scheduler_upload_path

TASK_TYPE = (
    (0, 'Select_Type'),
    (1, 'AutoLogin Token Genaration'),
    (2, 'Upload Certificate'),
    (3, 'Upload Candidate Certificate'),
    (4, 'Generate Product  List'),
    (5, 'Encrypted URLs for Mailer'),
    (6, 'Generate Compliance Report'),
    (7, 'Pixel Report Generation'),
    (8, "Discount Report Generation")
)

TASK_STATUS = (
    (0, 'Default'),
    (1, 'Failure'),
    (2, 'Success'),
    (3, 'Working'),
)


class Scheduler(AbstractAutoDate):
    task_type = models.PositiveIntegerField(
        choices=TASK_TYPE, default=0)
    status = models.PositiveIntegerField(
        choices=TASK_STATUS, default=0)
    percent_done = models.FloatField(
        default=0.0,
        validators=[MinValueValidator(0.0), MaxValueValidator(100)])
    file_uploaded = models.FileField(
        "Uploaded", max_length=200,
        upload_to=get_scheduler_upload_path,
        blank=True)
    file_generated = models.FileField(
        "Generated", max_length=200,
        upload_to=get_scheduler_upload_path,
        blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True,
        related_name='created_by',on_delete=models.PROTECT)
    completed_on = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "Scheduler"
        verbose_name_plural = "Schedulers"
        permissions = (
            ("can_generate_auto_login_token_task_scheduler", "Can Generate Autologin Token From Console"),
            ("can_view_completed_task_list_scheduler", "Can View All Completed Task List From Console"),
            ("can_download_product_list", "Can Download Product List from Console"),
            ('can_generate_compliance_report','Can Download Compliance Report From Console'),
            ('order.can_download_discount_report','Can Download Discount Report'),
        )

    def __str__(self):
        type_dict = dict(TASK_TYPE)
        return str(type_dict.get(self.task_type, '')) + " - " + str(self.pk)

    @property
    def get_type(self):
        type_dict = dict(TASK_TYPE)
        return type_dict.get(self.task_type, '')

    @property
    def get_status(self):
        status_dict = dict(TASK_STATUS)
        return status_dict.get(self.status, '')

    @property
    def get_complete(self):
        if self.status == 3:
            if self.percent_done:
                if self.percent_done < 100.0:
                    return True
                else:
                    return False
        return False

    @property
    def get_progress(self):
        progress_dict = {
            0: 'progress-bar-info',
            1: 'progress-bar-danger',
            2: 'progress-bar-success',
            3: 'progress-bar-warning'}
        return progress_dict.get(self.status, '')



