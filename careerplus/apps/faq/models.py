from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models.query import QuerySet

from seo.models import AbstractAutoDate
from partner.models import Vendor
from ckeditor.fields import RichTextField


class FAQuestionQuerySet(QuerySet):
    def active(self):
        """
        Return only "active" (i.e. published) questions.
        """
        return self.filter(status__exact=2)


class FAQuestionManager(models.Manager):
    def get_query_set(self):
        return FAQuestionQuerySet(self.model)

    def active(self):
        return self.get_query_set().active()


class FAQuestion(AbstractAutoDate):

    STATUS_CHOICES = (
        (2, _('Active')),
        (1, _('Inactive')),
        (0, _('Moderation')),)

    text = models.TextField(
        _('question'), help_text=_('The actual question itself.'))
    answer = RichTextField(
        verbose_name=_('answer'), blank=True, help_text=_('The answer text.'))
    status = models.IntegerField(
        _('status'),
        choices=STATUS_CHOICES,
        default=0,
        help_text=_("Only questions with their status set to 'Active' will be "
                    "displayed."))
    sort_order = models.IntegerField(
        _('sort order'), default=0,
        help_text=_('The order you would like the question to be displayed.'))

    vendor = models.ForeignKey(
        Vendor,
        related_name='question_vendor',
        null=True, blank=True)
    objects = FAQuestionManager()
    
    class Meta:
        verbose_name = _("FAQ")
        verbose_name_plural = _("FAQs")
        ordering = ['-modified']
        permissions = (
            ("console_add_faq", "Can Add FAQ From Console"),
            ("console_change_faq", "Can Change FAQ From Console"),
            ("console_moderate_faq", "Can Moderate FAQ From Console"),
            )

    def __str__(self):
        return self.text

    def is_active(self):
        return self.status == 2

    @property
    def get_status(self):
        return dict(self.STATUS_CHOICES).get(self.status)


class Chapter(AbstractAutoDate):
    STATUS_CHOICES = (
        (2, _('Active')),
        (1, _('Inactive')),
        (0, _('Moderation')),)

    heading = models.CharField(_('chapter'), max_length=255)
    parent = models.ForeignKey(
        'self', verbose_name=_('parentchapter'),
        related_name='parentheading', null=True, blank=True)
    answer = RichTextField(
        verbose_name=_('answer'), blank=True, help_text=_('The answer text.'))
    
    ordering = models.PositiveSmallIntegerField(
        _('ordering'), default=1,
        help_text=_(u'An integer used to order the chapter \
            amongst others related to the same chapter. If not given this \
            chapter will be last in the list.'))
    status = models.IntegerField(
        _('status'),
        choices=STATUS_CHOICES,
        default=0,
        help_text=_("Only questions with their status set to 'Active' will be "
                    "displayed."))
    vendor = models.ForeignKey(
        Vendor,
        related_name='chapter_vendor',
        null=True, blank=True)
    
    class Meta:
        ordering = ('heading',)
        verbose_name = _('Chapter')
        verbose_name_plural = _('Chapters')
        permissions = (
            ("console_add_chapter", "Can Add Product Chapter From Console"),
            ("console_change_chapter", "Can Change Product Chapter From Console"),
            ("console_moderate_chapter", "Can Moderate Product Chapter From Console"),
            )
    def __str__(self):
        return self.heading

    @property
    def get_status(self):
        return dict(self.STATUS_CHOICES).get(self.status)


class ScreenFAQ(AbstractAutoDate):

    faq = models.ForeignKey(
        FAQuestion,
        verbose_name=_('Original faq'),
        on_delete=models.SET_NULL,
        related_name='screenfaq',
        null=True)
    
    STATUS_CHOICES = (
        (6, _('Reverted')),
        (5, _('Rejected')),
        (4, _('InActive')),
        (3, _('Active')),
        (2, _('Moderation')),
        (1, _('Changed')),
        (0, _('Added')),)

    text = models.TextField(
        _('question'), help_text=_('The actual question itself.'))
    answer = RichTextField(
        verbose_name=_('answer'), blank=True, help_text=_('The answer text.'))
    status = models.IntegerField(
        _('status'),
        choices=STATUS_CHOICES,
        default=0,
        help_text=_("Only questions with their status set to 'Active' will be "
                    "displayed."))
    sort_order = models.IntegerField(
        _('sort order'), default=0,
        help_text=_('The order you would like the question to be displayed.'))

    vendor = models.ForeignKey(
        Vendor,
        null=True, blank=True)
    objects = FAQuestionManager()
    
    class Meta:
        verbose_name = _("Screen FAQ")
        verbose_name_plural = _("Screen FAQs")
        ordering = ['-modified']

    def __str__(self):
        return self.text

    def is_active(self):
        return self.status == 3

    @property
    def get_status(self):
        return dict(self.STATUS_CHOICES).get(self.status)

    def create_faq(self):
        if self.text and self.answer and self.vendor:
            faq = FAQuestion.objects.create(
                text=self.text,
                answer=self.answer,
                vendor=self.vendor)
            self.faq = faq
            self.save()
            return faq
        return None


class ScreenChapter(AbstractAutoDate):
    STATUS_CHOICES = (
        (2, _('Active')),
        (1, _('Inactive')),
        (0, _('Moderation')),)

    heading = models.CharField(_('chapter'), max_length=255)
    parent = models.ForeignKey(
        'self', verbose_name=_('parentchapter'),
        related_name='parentheading', null=True, blank=True)
    answer = RichTextField(
        verbose_name=_('answer'), blank=True, help_text=_('The answer text.'))
    
    ordering = models.PositiveSmallIntegerField(
        _('ordering'), default=1,
        help_text=_(u'An integer used to order the chapter \
            amongst others related to the same chapter. If not given this \
            chapter will be last in the list.'))
    status = models.IntegerField(
        _('status'),
        choices=STATUS_CHOICES,
        default=0,
        help_text=_("Only questions with their status set to 'Active' will be "
                    "displayed."))
    vendor = models.ForeignKey(
        Vendor,
        null=True, blank=True)
    
    class Meta:
        ordering = ('heading',)
        verbose_name = _('Chapter')
        verbose_name_plural = _('Screen Chapters')
    def __str__(self):
        return self.heading

    @property
    def get_status(self):
        return dict(self.STATUS_CHOICES).get(self.status)

