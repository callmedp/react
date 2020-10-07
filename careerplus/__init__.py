from __future__ import absolute_import, unicode_literals
# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
from careerplus.config.celery import app as celery_app  # noqa
__all__ = ['celery_app']
__version__ = "2.1.2"


### x.y.z:
### x: Major release, y: feature release, z: bugs