"""
WSGI config for BaseProject.core.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os
import json

from django.core.wsgi import get_wsgi_application
from django.conf import settings


with open(settings.BASE_DIR / '.config_project/conf.json') as json_file:
  confs = json.loads(json_file.read())

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

application = get_wsgi_application()
