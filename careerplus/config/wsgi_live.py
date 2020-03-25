"""
WSGI config for careerplus project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
"""

import os,socket
from django.core.wsgi import get_wsgi_application

os.environ["DJANGO_SETTINGS_MODULE"] = "careerplus.config.settings_live"



#NewRelic
if socket.gethostname().startswith('learning-web-od'):
    import newrelic.agent
    newrelic.agent.initialize('/var/www/site/learning/current/careerplus/deploy/newrelic.ini')

application = get_wsgi_application()
