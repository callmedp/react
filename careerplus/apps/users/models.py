#python imports
from __future__ import unicode_literals
import logging,os
from base64 import b64encode

#django imports
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin, BaseUserManager)
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save


#local imports
from .choices import WRITER_TYPE
from .functions import get_upload_path_user_invoice

#inter app imports

#third party imports


class UserManager(BaseUserManager):

    def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
        """
            Creates and saves a User with the given email and password and
            contact_number.
        """
        now = timezone.now()
        email = self.normalize_email(email)
        user = self.model(
            email=email, is_staff=is_staff, is_active=True,
            is_superuser=is_superuser, last_login=now,
            date_joined=now, **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, contact_number=None, **extra_fields):
        """
            Creates and saves a User with the given email and password and contact_number.
        """
        user = self._create_user(email, password, False, False, **extra_fields)

        return user

    def create_superuser(self, email, password, **extra_fields):
        """
            creates super user when using command >> createsuperuser.
        """

        user = self._create_user(email, password, True, True, **extra_fields)

        return user


class User(AbstractBaseUser, PermissionsMixin):

    USERNAME_FIELD = 'email'

    name = models.CharField(_('Name'), max_length=100)
    cp_id = models.CharField(_('CPID'), max_length=20, blank=True)

    email = models.EmailField(
        _('email address'),
        max_length=200, unique=True, blank=False)

    contact_number = models.CharField(max_length=15, blank=True, null=True)

    is_staff = models.BooleanField(
        _('staff status'), default=False,
        help_text=_(
            'Designates whether the user can log into this admin site.'))
    is_active = models.BooleanField(
        _('active'), default=True,
        help_text=_(
            'Designates whether this user should be treated as active. Unselect this instead of deleting accounts.')
    )

    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    alt = models.CharField(max_length=128,null=True,blank=True)

    objects = UserManager()

    def __str__(self):
        if self.name:
            return self.name + '  (' + str(self.email) + ')'
        return "%s" % str(self.email)

    def get_short_name(self):
        """
            Returns the short name for the user.
        """
        return self.name

    def get_full_name(self):
        """
            Returns the short name for the user.
        """
        return self.name

    def get_vendor(self):
        vendor_list = self.vendor_set.all()
        if vendor_list:
            return vendor_list[0]
        return None

    def get_vendor_list(self):
        return self.vendor_set.all() if self.vendor_set.all() else []

    def generate_alt(self):
        return b64encode(os.urandom(64)).decode('utf-8')

    def get_console_reset_password_endpoint(self):
        if not self.alt:
            return ""
        
        return "{}://{}/console/reset-password/?alt={}".format(\
            settings.SITE_PROTOCOL,settings.SITE_DOMAIN,self.alt)


class UserProfile(models.Model):
    """
    Currently there is no relation between the user and userprofile in the
    sql database , it will only return the user_ids of user model.

    """
    user = models.OneToOneField(User)
    writer_type = models.PositiveIntegerField(
        choices=WRITER_TYPE,
        default=0)
    pan_no = models.CharField(
        max_length=100, null=True, blank=True)
    gstin = models.CharField(
        max_length=255, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    po_number = models.CharField(
        max_length=255, unique=True,
        null=True, blank=True)
    valid_from = models.DateField(null=True, blank=True)
    valid_to = models.DateField(null=True, blank=True)
    user_invoice = models.FileField(
        upload_to=get_upload_path_user_invoice,
        max_length=255,
        blank=True, null=True)
    invoice_date = models.DateField(null=True, blank=True)

    last_writer_type = models.PositiveIntegerField(
        choices=WRITER_TYPE,
        default=1)

    wt_changed_date = models.DateField(
        "Writer Type Update Date",
        blank=True, null=True)

    def __str__(self):
        if self.user.name:
            return self.user.name + ' (' + str(self.user.email) +')'
        return "%s" % str(self.user.email)

    def __init__(self, *args, **kwargs):
        super(UserProfile, self).__init__(*args, **kwargs)
        self.initial_writer_type = self.writer_type
        self.initial_wt_changed_date = self.wt_changed_date

    def clean(self, *args, **kwargs):
        super(UserProfile, self).clean(*args, **kwargs)
        today_date = timezone.now().date()
        if self.initial_writer_type != self.writer_type:
            if not self.initial_wt_changed_date:
                self.wt_changed_date = today_date
                if self.initial_writer_type != 0:
                    self.last_writer_type = self.initial_writer_type
                elif self.writer_type != 0:
                    self.last_writer_type = self.writer_type

            elif self.initial_wt_changed_date.month == today_date.month and self.initial_wt_changed_date.year == today_date.year:
                self.wt_changed_date = today_date

            else:
                if self.initial_writer_type != 0:
                    self.last_writer_type = self.initial_writer_type
                else:
                    self.last_writer_type = self.writer_type
                self.wt_changed_date = today_date


def create_user_profile(sender, instance, created, **kwargs):
    # when user is created
    # if created:
    # this code run on every save of user object
    try:
        UserProfile.objects.get_or_create(user=instance)
    except Exception as e:
        logging.getLogger('error_log').error('unable to get/create userprofile object %s' % str(e))

        pass
post_save.connect(create_user_profile, sender=User)


# class UserEmail(models.Model):
#     """
#     This is to record of all emails sent to a user.
#     """
#     user = models.ForeignKey(User, related_name='emails',
#                              verbose_name=_("User"))
#     subject = models.TextField(_('Subject'), max_length=255)
#     body_text = models.TextField(_("Body Text"))
#     body_html = models.TextField(_("Body HTML"), blank=True)
#     date_sent = models.DateTimeField(_("Date Sent"), auto_now_add=True)

#     class Meta:
#         abstract = True
#         verbose_name = _('Email')
#         verbose_name_plural = _('Emails')

#     def __str__(self):
#         return _(u"Email to %(user)s with subject '%(subject)s'") % {
#             'user': self.user.get_username(), 'subject': self.subject}
