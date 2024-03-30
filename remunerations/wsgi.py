"""
WSGI config for remunerations project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'remunerations.settings.local')

application = get_wsgi_application()

application = get_wsgi_application()

from remunerations.data_bases import load_data_base
load_data_base()
