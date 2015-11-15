# -*- coding: utf-8 -*-

"""
WSGI config for okapi project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os
import sys
import site

okapi_home = '~okapi/'

site.addsitedir(os.path.join(
    okapi_home,
    'venv_okapi/local/lib/python2.7/site-packages'))

sys.path.append(os.path.join(okapi_home, 'www'))
sys.path.append(os.path.join(okapi_home, 'www/okapi'))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "okapi.settings")

activate_env = os.path.expanduser(os.path.join(
    okapi_home,
    'venv_okapi/bin/activate_this.py'))
execfile(activate_env, dict(__file__=activate_env))

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
