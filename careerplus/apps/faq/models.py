from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models.query import QuerySet
from seo.models import AbstractAutoDate

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

    objects = FAQuestionManager()
    
    class Meta:
        verbose_name = _("Frequent asked question")
        verbose_name_plural = _("Frequently asked questions")
        ordering = ['sort_order', 'created']

    def __str__(self):
        return self.text

    def is_active(self):
        return self.status == 2


class Chapter(AbstractAutoDate):
    heading = models.CharField(_('chapter'), max_length=255)
    parent = models.ForeignKey(
        'self', verbose_name=_('parentchapter'),
        related_name='parentheading', null=True, blank=True)
    answer = RichTextField(
        verbose_name=_('answer'), blank=True, help_text=_('The answer text.'))
    
    ordering = models.PositiveSmallIntegerField(
        _('ordering'), blank=True,
        help_text=_(u'An integer used to order the chapter \
            amongst others related to the same chapter. If not given this \
            chapter will be last in the list.'))
    
    class Meta:
        ordering = ('heading',)
        verbose_name = _('chapter')
        verbose_name_plural = _('chapters')

    def __str__(self):
        return self.heading


class Topic(AbstractAutoDate):
    name = models.CharField(_('name'), max_length=255)
    description = RichTextField(
        verbose_name=_('description'), blank=True,
        help_text=_('A short description of this topic.'))
    chapters = models.ManyToManyField(
        Chapter,
        verbose_name=_('Topic Chapter'),
        through='TopicChapter',
        through_fields=('topic', 'chapter'),
        blank=True)

    class Meta:
        ordering = ('name',)
        verbose_name = _('topic')
        verbose_name_plural = _('topics')

    def __str__(self):
        return self.name


class TopicChapter(AbstractAutoDate):
    topic = models.ForeignKey(
        Topic,
        related_name='topics',
        on_delete=models.CASCADE)
    chapter = models.ForeignKey(
        Chapter,
        related_name='chapters',
        on_delete=models.CASCADE)
    sort_order = models.PositiveIntegerField(
        _('Sort Order'), default=1)
    active = models.BooleanField(default=True)

    def __str__(self):
        return _("%(top)s to '%(cp)s'") % {
            'top': self.topic,
            'cp': self.chapter}
