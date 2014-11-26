import os
import sys
path = '/home/ldl/mycode/mysite'
if path not in sys.path:
    sys.path.insert(0, '/home/ldl/mycode/mysite')
os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
