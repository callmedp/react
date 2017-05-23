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
        max_length=1024,
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

    def __str__(self):
        return '{0} - {1}'.format(self.reviewed_item, self.get_user())

    def get_user(self):
        if self.user_email:
            return self.user_email
        return ugettext('Anonymous')

    def get_averages(self, max_value=None):

        """
        Call this if you have multiple rating in a review.
        """
        max_rating_value = 0
        category_maximums = {}
        category_averages = {}
        categories = RatingCategory.objects.filter(counts_for_average=True,
                                                   rating__review=self)
        # find the highest rating possible across all categories
        for category in categories:
            category_max = category.get_rating_max_from_choices()
            category_maximums.update({category: category_max})
            if max_value is not None:
                max_rating_value = max_value
            else:
                if category_max > max_rating_value:
                    max_rating_value = category_max
        # calculate the average of every distinct category, normalized to the
        # recently found max
        for category in categories:
            category_average = None
            ratings = Rating.objects.filter(
                review=self,
                category=category, value__isnull=False).exclude(value='')
            category_max = category_maximums[category]
            for rating in ratings:
                if category_average is None:
                    category_average = float(rating.value)
                else:
                    category_average += float(rating.value)

            if category_average is not None:
                category_average *= float(max_rating_value) / float(
                    category_max)
                category_averages[category] = (
                    category_average / ratings.count())

        # calculate the total average of all categories
        total_average = 0
        for category, category_average in category_averages.items():
            total_average += category_average
        if not len(category_averages):
            return (False, False)
        total_average /= len(category_averages)

        return total_average, category_averages

    def get_average_rating(self, max_value=None):
        """
        Returns the average rating for all categories of this review.
        """
        total_average, category_averages = self.get_averages(
            max_value=max_value)
        return total_average

    def get_category_averages(self, max_value=None):
        """
        Returns the average ratings for every category of this review.
        """
        total_average, category_averages = self.get_averages(
            max_value=max_value)
        return category_averages

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
        remarks= ''
        if self.average_rating >= 4.0:
            remarks = "Excellent!"
        elif self.average_rating >= 3.0:
            remarks = "Good!"
        elif self.average_rating >= 2.0:
            remarks = "Average!"
        else:
            remarks = "Bad!"

        return remarks


class RatingCategory(AbstractAutoDate):
    identifier = models.SlugField(
        max_length=32,
        verbose_name=_('Identifier'),
        blank=True,
        unique=True
    )

    counts_for_average = models.BooleanField(
        verbose_name=_('Count it for average rating'),
        default=True,
    )

    name = models.CharField(
        max_length=100,
        verbose_name=_("Name"),)
    question = models.CharField(
        max_length=100,
        verbose_name=_("Question"),)

    def __str__(self):
        return self.name

    @property
    def required(self):
        """Returns False, if the choices include a None value."""
        if not hasattr(self, '_required'):
            # get_choices sets _required
            self.get_choices()
        return self._required

    def get_choices(self):
        """Returns the tuple of choices for this category."""
        choices = ()
        self._required = True
        for choice in self.choices.all():
            if choice.value is None or choice.value == '':
                self._required = False
            choices += (choice.value, choice.label),
        if not choices:
            return DEFAULT_CHOICES
        return choices

    def get_rating_max_from_choices(self):
        """Returns the maximun value a rating can have in this catgory."""
        return int(list(self.get_choices())[0][0])


class RatingCategoryChoice(AbstractAutoDate):
    ratingcategory = models.ForeignKey(
        RatingCategory,
        verbose_name=_('Rating category'),
        related_name='choices',
    )

    value = models.CharField(
        verbose_name=_('Value'),
        max_length=20,
        blank=True, null=True,
    )

    label = models.CharField(
        verbose_name=_('Label'),
        max_length=128,)
    
    def __str__(self):
        return self.label

    class Meta:
        ordering = ('-value', )


class Rating(models.Model):
    """
    Represents a rating for one rating category.
    :rating: Rating value.
    :review: The review the rating belongs to.
    :category: The rating category the rating belongs to.
    """
    rating_choices = DEFAULT_CHOICES

    value = models.CharField(
        max_length=20,
        verbose_name=_('Value'),
        choices=rating_choices,
        blank=True, null=True,
    )

    review = models.ForeignKey(
        'review.Review',
        verbose_name=_('Review'),
        related_name='ratings',
    )

    category = models.ForeignKey(
        'review.RatingCategory',
        verbose_name=_('Category'),
    )

    class Meta:
        ordering = ['category', 'review']

    def __str__(self):
        return '{0}/{1} - {2}'.format(self.category, self.review, self.value)
