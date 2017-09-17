#from telemeta.settings_base import SECRET_KEY, INSTALLED_APPS


SECRET_KEY = 'test_key'
INSTALLED_APPS = ('django.contrib.auth',
                  'django.contrib.contenttypes',
                  'django.contrib.sessions',
                  'django.contrib.sites',
                  'django.contrib.messages',
                  'suit',
                  'django.contrib.admin',
                  'django.contrib.staticfiles',
                  'django_extensions',
                  'telemeta',)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:'
    },
}
