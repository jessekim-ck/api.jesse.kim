import os
from django.core.wsgi import get_wsgi_application


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "weekendkim_backend.settings.debug")
application = get_wsgi_application()

