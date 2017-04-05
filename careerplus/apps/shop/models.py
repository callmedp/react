from django.utils import timezone
from django.db import models


class AbstractAutoDate(models.Model):
    created = models.DateTimeField(editable=False)
    modified = models.DateTimeField()

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(AbstractAutoDate, self).save(*args, **kwargs)

    class Meta:
        abstract = True

