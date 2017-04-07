from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models.query import QuerySet
from seo.models import AbstractAutoDate


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
    
    STATUS_CHOICES = ((2, _('Active')),
        (1, _('Inactive')), (0, _('Moderation')),)

    text = models.TextField(
        _('question'), help_text=_('The actual question itself.'))
    answer = models.TextField(
        _('answer'), blank=True, help_text=_('The answer text.'))
    status = models.IntegerField(
        _('status'),
        choices=STATUS_CHOICES,
        default=0,
        help_text=_("Only questions with their status set to 'Active' will be "
                    "displayed."))
    protected = models.BooleanField(
        _('is protected'),
        default=False,
        help_text=_("Set true if this question is only visible by authenticated users."))
    sort_order = models.IntegerField(
        _('sort order'), default=0,
        help_text=_('The order you would like the question to be displayed.'))

    # created_by = models.ForeignKey(
    #     User, verbose_name=_('created by'),
    #     null=True, related_name="+")
    # updated_by = models.ForeignKey(
    #     User, verbose_name=_('updated by'),
    #     null=True, related_name="+")  
    
    objects = FAQuestionManager()
    
    class Meta:
        verbose_name = _("Frequent asked question")
        verbose_name_plural = _("Frequently asked questions")
        ordering = ['sort_order', 'created']

    def __str__(self):
        return self.text

    def is_active(self):
        return self.status == 2

