# -*- coding: utf-8 -*-
# Django settings for sandbox project.

import os, sys
from django.core.urlresolvers import reverse_lazy, reverse

import environ
# set default values and casting
env = environ.Env(DEBUG=(bool, False),
                  CELERY_ALWAYS_EAGER=(bool, False),
                  )

# Django settings for server project.
DEBUG = env('DEBUG') # False if not in os.environ
TEMPLATE_DEBUG = DEBUG

sys.dont_write_bytecode = True

ALLOWED_HOSTS = ['*']

ADMINS = (
    ('Guillaume Pellerin', 'yomguy@parisson.com'),
)

MANAGERS = ADMINS

# Full filesystem path to the project.
#PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = '/srv/app/'

DATABASES = {
    'default': {
        'ENGINE': env('ENGINE'),  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'USER': env('MYSQL_USER'),      # Not used with sqlite3.
        'PASSWORD': env('MYSQL_PASSWORD'),  # Not used with sqlite3.
        'NAME': env('MYSQL_DATABASE'),
        'HOST': 'db',      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '3306',   # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Paris'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
#LANGUAGE_CODE = 'fr_FR'

LANGUAGES = [ ('fr', 'French'),
              ('en', 'English'),
              ('de', 'German'),
              ('zh_CN', 'Simplified Chinese'),
              ('ar_TN', 'Arabic'),
              ('pt_BR', 'Portuguese'),
              ('es', 'Spanish'),
]

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
# MEDIA_ROOT = PROJECT_ROOT + '/media/'
#
# if not os.path.exists(MEDIA_ROOT):
#     os.makedirs(MEDIA_ROOT)
MEDIA_ROOT = '/srv/media/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
# STATIC_ROOT = '/var/www/static'
STATIC_ROOT = '/srv/static/'

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
# Put strings here, like "/home/html/static" or "C:/www/django/static".
# Always use forward slashes, even on Windows.
# Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
'django.contrib.staticfiles.finders.FileSystemFinder',
'django.contrib.staticfiles.finders.AppDirectoriesFinder',
'djangobower.finders.BowerFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)
# Make this unique, and don't share it with anybody.
SECRET_KEY = 'a8l7%06wr2k+3=%#*#@#rvop2mmzko)44%7k(zx%lls^ihm9^5'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)


MIDDLEWARE_CLASSES = (
    # Manage Django URLs for AngularJS with django-angular
    'djng.middleware.AngularUrlMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    # 'pagination.middleware.PaginationMiddleware',
)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'suit',
    'django.contrib.admin',
    'django.contrib.staticfiles',
    'django_extensions',
    'telemeta',
    'timeside.player',
    #'timeside.server',
    'jsonrpc',
    'south',
    'sorl.thumbnail',
    'timezones',
    'jqchat',
    'ipauth',
    'extra_views',
    'bootstrap3',
    'bootstrap_pagination',
    'googletools',
    'registration',
    'rest_framework',
    'djcelery',
    'haystack',
    'djangobower',
    'djng',
    'saved_searches',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.request',
    'django.contrib.auth.context_processors.auth',
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    'django.core.context_processors.static',
    'telemeta.context_processors.menu',
    'django.contrib.messages.context_processors.messages',
)

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'ipauth.backend.RangeBackend',
)

SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"


TELEMETA_ORGANIZATION = 'CREM-CNRS'
TELEMETA_SUBJECTS = ('Ethnomusicology', 'Research')
TELEMETA_DESCRIPTION = "Sound archives of the CNRS and the Musee de l'Homme. Research Centre of Ethnomusicology (CREM), University of Paris 10"
TELEMETA_LOGO = STATIC_URL + 'telemeta/images/logo_crem.png'

TELEMETA_GMAP_KEY = 'ABQIAAAArg7eSfnfTkBRma8glnGrlxRVbMrhnNNvToCbZQtWdaMbZTA_3RRGObu5PDoiBImgalVnnLU2yN4RMA'

TELEMETA_CACHE_DIR = os.path.join(MEDIA_ROOT, 'cache')
TELEMETA_EXPORT_CACHE_DIR = os.path.join(MEDIA_ROOT, 'export')
TELEMETA_DATA_CACHE_DIR = os.path.join(TELEMETA_CACHE_DIR, 'data')
FILE_UPLOAD_TEMP_DIR = os.path.join(MEDIA_ROOT, 'tmp')
FILE_UPLOAD_PERMISSIONS = 0o644

TELEMETA_DOWNLOAD_ENABLED = False
TELEMETA_STREAMING_FORMATS = ('mp3', 'ogg')
TELEMETA_DOWNLOAD_FORMATS = ('wav', 'mp3', 'ogg', 'flac')
TELEMETA_PUBLIC_ACCESS_PERIOD = 51

TELEMETA_STRICT_CODE = False
COLLECTION_PUBLISHED_CODE_REGEX = 'CNRSMH_E_[0-9]{4}(?:_[0-9]{3}){2}'
COLLECTION_UNPUBLISHED_CODE_REGEX = 'CNRSMH_I_[0-9]{4}_[0-9]{3}'
ITEM_PUBLISHED_CODE_REGEX = COLLECTION_PUBLISHED_CODE_REGEX + '(?:_[0-9]{2,3}){1,2}'
ITEM_UNPUBLISHED_CODE_REGEX = COLLECTION_UNPUBLISHED_CODE_REGEX + '_[0-9]{2,3}(?:_[0-9]{2,3}){0,2}'
RESOURCE_CODE_REGEX = '[A-Za-z0-9._-]*'

AUTH_PROFILE_MODULE = 'telemeta.userprofile'
SESSION_EXPIRE_AT_BROWSER_CLOSE = False

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/desk/lists/'

EMAIL_HOST = 'localhost'
DEFAULT_FROM_EMAIL = 'webmaster@parisson.com'

TIMESIDE_DEFAULT_GRAPHER_ID = 'waveform_centroid'
TIMESIDE_DEFAULT_WAVEFORM_SIZES = ['346x130', '640x130']
TIMESIDE_AUTO_ZOOM = False

# Settings for django-bootstrap3
BOOTSTRAP3 = {
    'set_required': True,
    'set_placeholder': False,
    'error_css_class': 'has-error',
    'required_css_class': 'has-warning',
    'javascript_in_head': True,
}

PAGINATION_SETTINGS = {
    'PAGE_RANGE_DISPLAYED': 10,
    'MARGIN_PAGES_DISPLAYED': 2,
}

if DEBUG:
    INSTALLED_APPS += ('debug_toolbar',)
    MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)
    DEBUG_TOOLBAR_CONFIG = {
        'SHOW_TOOLBAR_CALLBACK': lambda x : True
    }
    DEBUG_TOOLBAR_PATCH_SETTINGS = False
    DEBUG_TOOLBAR_PANELS = [
        'debug_toolbar.panels.versions.VersionsPanel',
        'debug_toolbar.panels.timer.TimerPanel',
        'debug_toolbar.panels.settings.SettingsPanel',
        'debug_toolbar.panels.headers.HeadersPanel',
        'debug_toolbar.panels.request.RequestPanel',
        'debug_toolbar.panels.sql.SQLPanel',
        'debug_toolbar.panels.staticfiles.StaticFilesPanel',
        'debug_toolbar.panels.templates.TemplatesPanel',
        'debug_toolbar.panels.cache.CachePanel',
        'debug_toolbar.panels.signals.SignalsPanel',
        'debug_toolbar.panels.logging.LoggingPanel',
        'debug_toolbar.panels.redirects.RedirectsPanel',
    ]
    DEBUG_TOOLBAR_CONFIG = {
        'JQUERY_URL': '/static/jquery/dist/jquery.min.js',
    }
    INTERNAL_IPS = ['127.0.0.1', '0.0.0.0', '172.17.0.1']

SUIT_CONFIG = {
        'ADMIN_NAME': 'Telemeta Admin'
}

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

BROKER_URL = env('BROKER_URL')
CELERY_IMPORTS = ("timeside.server.tasks",)
CELERY_RESULT_BACKEND = 'djcelery.backends.database:DatabaseBackend'
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['application/json']

from worker import app

HAYSTACK_CONNECTIONS = {
    'default': {
        #'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
        'ENGINE': 'telemeta.util.backend.CustomElasticEngine',
        'URL': env('HAYSTACK_URL'),
        'INDEX_NAME': env('HAYSTACK_INDEX_NAME'),
        'INLUDE_SPELLING': True,
        'EXCLUDED_INDEXES': ['telemeta.search_indexes.LocationIndex',
                             'telemeta.search_indexes.LocationAliasIndex',
                             'telemeta.search_indexes.InstrumentIndex',
                             'telemeta.search_indexes.InstrumentAliasIndex'
                             ]
    },
    'autocomplete': {
        # 'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
        'ENGINE': 'telemeta.util.backend.CustomElasticEngine',
        'URL': env('HAYSTACK_URL'),
        'INDEX_NAME': env('HAYSTACK_INDEX_NAME_AUTOCOMPLETE'),
        'INLUDE_SPELLING': True,
        'EXCLUDED_INDEXES': ['telemeta.search_indexes.MediaItemIndex',
                             'telemeta.search_indexes.MediaCollectionIndex',
                             'telemeta.search_indexes.MediaCorpusIndex',
                             'telemeta.search_indexes.MediaFondsIndex'
                             ]
    },
}

HAYSTACK_ROUTERS = ['telemeta.util.search_router.AutoRouter', 'haystack.routers.DefaultRouter']
# HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'
HAYSTACK_SIGNAL_PROCESSOR = 'telemeta.util.search_signals.RealTimeCustomSignal'
HAYSTACK_SEARCH_RESULTS_PER_PAGE = 50

BOWER_COMPONENTS_ROOT = '/srv/bower/'
BOWER_PATH = '/usr/local/bin/bower'
BOWER_INSTALLED_APPS = (
    'jquery#2.2.4',
    'jquery-migrate#~1.2.1',
    'underscore#1.8.3',
    'bootstrap#3.3.7',
    'bootstrap-select#1.5.4',
    'font-awesome#4.4.0',
    'angular#1.2.26',
    'angular-bootstrap-select#0.0.5',
    'angular-resource#1.2.26',
    'raphael#2.2.7',
    'soundmanager#V2.97a.20150601',
    'jquery-ui#1.11.4',
    'tablesorter',
    'video.js',
    'sass-bootstrap-glyphicons',
    # 'https://github.com/Parisson/loaders.git',
    # 'https://github.com/Parisson/ui.git',
)
