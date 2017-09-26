from django.conf import settings

def pytest_configure():
    settings.configure(#SECRET_KEY = 'test_key'
        INSTALLED_APPS=('django.contrib.auth',
                        'django.contrib.contenttypes',
                        'django.contrib.sessions',
                        'django.contrib.sites',
                        'django.contrib.messages',
                        'suit',
                        'django.contrib.admin',
                        'django.contrib.staticfiles',
                        'django_extensions',
                        'telemeta',),
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:'
            },
        }
    )
