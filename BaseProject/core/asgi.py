"""
ASGI config for BaseProject.core.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os
import json

from django.core.asgi import get_asgi_application
from django.conf import settings


with open(settings.BASE_DIR / '.config_project/conf.json') as json_file:
  confs = json.loads(json_file.read())

os.environ.setdefault('DJANGO_SETTINGS_MODULE', confs['generals']['settings'])

application = get_asgi_application()
