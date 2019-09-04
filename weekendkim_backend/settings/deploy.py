from .base import *

config_secret_deploy = json.loads(open(CONFIG_SECRET_DEPLOY_FILE).read())

DEBUG = False
ALLOWED_HOSTS = config_secret_deploy['django']['allowed_hosts']

# WSGI application
WSGI_APPLICATION = 'weekendkim_backend.wsgi.deploy.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': config_secret_deploy['django']['databases']['user'],
        'PASSWORD': config_secret_deploy['django']['databases']['password'],
        'HOST': 'weekendkimblog.cmi32gylznob.ap-northeast-2.rds.amazonaws.com',
        'PORT': '5432',
    }
}
