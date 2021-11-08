"""
WSGI config for fcs project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os, sys

sys.path.append('/home/iiitd/fcs')

# add the virtualenv site-packages path to the sys.path
sys.path.append('/home/iiitd/fcs/env/lib/python3.6/site-packages')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fcs.settings')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
