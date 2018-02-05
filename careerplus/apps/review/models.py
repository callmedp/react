from django.conf import settings
from decimal import Decimal
from django.contrib.contenttypes import fields
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext, ugettext_lazy as _
from seo.models import AbstractAutoDate
from ckeditor.fields import RichTextField

DEFAULT_CHOICES = (
    ('5', '5'),
    ('4', '4'),
    ('3', '3'),
    ('2', '2'),
    ('1', '1'),
)


STATUS_CHOICES = (
    (0, _("Requires moderation")),
    (1, _("Approved")),
    (2, _("Rejected")),
)
    

class Review(AbstractAutoDate):
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    reviewed_item = fields.GenericForeignKey('content_type', 'object_id')
    user_name = models.CharField(
        max_length=100,
        verbose_name=_("User Name"),)
    user_email = models.CharField(
        max_length=100,
        verbose_name=_("User Email"),)
    user_id = models.CharField(
        max_length=100,
        verbose_name=_("User ID"),)

    content = RichTextField(
        max_length=1500,
        verbose_name=_('Content'),
        blank=True,
    )

    average_rating = models.FloatField(
        verbose_name=_('Average rating'),
        default=0,
    )

    status = models.SmallIntegerField(
        _("Status"), choices=STATUS_CHOICES, default=0)

    # GFK 'extra_item' If required let say linking review to orderitem and product. if required
    extra_content_type = models.ForeignKey(
        ContentType,
        related_name='reviews_attached',
        null=True, blank=True,
    )
    extra_object_id = models.PositiveIntegerField(null=True, blank=True)
    extra_item = fields.GenericForeignKey(
        'extra_content_type', 'extra_object_id')

    class Meta:
        ordering = ['-created']
        permissions = (
            #  review queue permission
            ("can_change_review_queue", "Can Change Review Queue"),
        )

    def __str__(self):
        return '{0} - {1}'.format(self.reviewed_item, self.get_user())

    def get_user(self):
        if self.user_email:
            return self.user_email
        return ugettext('Anonymous')

    def get_ratings(self):
        pure_rating = int(self.average_rating)
        decimal_part = self.average_rating - pure_rating
        final_score = ['*' for i in range(pure_rating)]
        rest_part = int(5.0 - self.average_rating)
        res_decimal_part = 5.0 - self.average_rating - rest_part
        if decimal_part >= 0.75:
            final_score.append("*")
        elif decimal_part >= 0.25:
            final_score.append("+")
        if res_decimal_part >= 0.75:
            final_score.append('-')
        for i in range(rest_part):
            final_score.append('-')
        return final_score

    def get_remarks(self):
        remarks = ''
        if self.average_rating >= 4.0:
            remarks = "Excellent!"
        elif self.average_rating >= 3.0:
            remarks = "Good!"
        elif self.average_rating >= 2.0:
            remarks = "Average!"
        else:
            remarks = "Bad!"

        return remarks


