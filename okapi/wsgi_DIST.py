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

# In each string describing a path, you should not use '~' character nor
# os.path.join to transform '/PATH/TO/OKAPI_HOME/' a variable. It is
# repetitive but it avoids bugs.

site.addsitedir('/PATH/TO/OKAPI_HOME/venv_okapi/lib/python3.4/site-packages')

sys.path.append('/PATH/TO/OKAPI_HOME/www')
sys.path.append('/PATH/TO/OKAPI_HOME/www/okapi')

os.environ["DJANGO_SETTINGS_MODULE"] = "okapi.settings"

activate_env = os.path.expanduser('/PATH/TO/OKAPI_VENV/bin/activate_this.py')
execfile(activate_env, dict(__file__=activate_env))

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
