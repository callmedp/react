from __future__ import unicode_literals
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin, BaseUserManager)
from django.utils import timezone


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

    email = models.EmailField(
        _('email address'),
        max_length=200, unique=True, blank=False)

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

    objects = UserManager()

    def __str__(self):
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
