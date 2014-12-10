--------
Install
--------

Telemeta is designed first to run on Linux platforms.

* On Debian and Ubuntu operating systems, please install all binary dependencies like this::

    sudo aptitude install gcc python python-dev python-pip python-django python-xml \
        python-ctypes python-setuptools python-support python-docutils \
        python-libxml2 python-django-registration python-lxml python-numpy \
        python-scipy python-imaging python-mutagen python-gobject python-gst0.10 \
        python-django-south

 then do::

    sudo pip install telemeta

* On other Linux platforms:

    Please install all the equivalent dependencies above thanks to your application manager.

* OSX install procedure will be soon provided.

* Windows plaforms are not officialy supported but possible.

-------------------------
Fast testing (sandbox)
-------------------------

If you just want to test Telemeta just now, a sandbox is available in the example/ directory::

    cd example/sandbox
    ./manage.py syncdb
    ./manage.py migrate
    ./manage.py runserver 9000

Now browse http://localhost:9000

-------------------------------
Create a new Telemeta project
-------------------------------

Start your project
------------------

For example::

    cd ~/projects
    django-admin startproject newproject

Create the database
------------------------

Telemeta needs MySQL to work well and fast in production. So you need to create a MySQL database before trying it. But you can also use SQLite, PostgreSQL or Oracle DB.

Configure the project
----------------------------------

Edit the file newproject/settings.py in a text editor.

You can find and even copy the example in the sandbox (example/sandbox/settings.py)

Modifiy the following variables::

    ADMINS =            telemeta requires that you indicate an administrator here
    DATABASES =         your database setting dict (don't forget to create the database if needed)
    MEDIA_ROOT =        absolute path to the media directory you just created

Set the app lists as follow::

    INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',
    'telemeta',
    'timeside',
    'jsonrpc',
    'south',
    'sorl.thumbnail',
    'timezones',
    'jqchat',
    )

Set the following languages::

    LANGUAGES = [ ('fr', 'French'),
                  ('en', 'English'),
    ]

Set the following Middlewares::

    MIDDLEWARE_CLASSES = (
        'django.middleware.common.CommonMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.locale.LocaleMiddleware',
    )

and the following processors::

    TEMPLATE_CONTEXT_PROCESSORS = (
        'django.core.context_processors.request',
        'django.contrib.auth.context_processors.auth',
        'django.core.context_processors.i18n',
        'django.core.context_processors.media',
        'django.core.context_processors.static',)

Add the following variables::

    TELEMETA_ORGANIZATION =         name of the organization which hosts this installation
    TELEMETA_SUBJECTS =             tuple of subject keywords (used for Dublin Core), such as "Ethnology", etc...
    TELEMETA_DESCRIPTION =          the description of the site
    TELEMETA_CACHE_DIR =            absolute path to the cache directory that you just created
    TELEMETA_GMAP_KEY =             your Google Map API key
    TELEMETA_DOWNLOAD_ENABLED =     True to enable raw audio data download
    TELEMETA_STREAMING_FORMATS =    tuple of authorized streaming formats. Ex: ('mp3', 'ogg')
    TELEMETA_DOWNLOAD_FORMATS =     tuple of authorized download formats. Ex: ('wav', 'mp3', 'webm')
    TELEMETA_PUBLIC_ACCESS_PERIOD = number of years above which item files are automagically published
    EMAIL_HOST =                    your default SMTP server
    DEFAULT_FROM_EMAIL =            the default sending email address

Just paste the lines below::

    LOGIN_URL = '/login'
    LOGIN_REDIRECT_URL = '/'
    AUTH_PROFILE_MODULE = 'telemeta.userprofile'
    TELEMETA_EXPORT_CACHE_DIR = TELEMETA_CACHE_DIR + "/export"
    TELEMETA_DATA_CACHE_DIR = TELEMETA_CACHE_DIR + "/data"
    CACHE_BACKEND = "file://" + TELEMETA_CACHE_DIR + "/data"

Optional: if you want some personal templates, for example::

    TEMPLATE_DIRS = (
    '/home/dev/telemeta/sandboxes/sandbox_generic/templates/',
    )


Configure your urls
----------------------

You can find (even copy) an example of url.py there::

    example/sandbox/urls.py

Add this dictionary to get Javascript translation::

    js_info_dict = {
        'packages': ('telemeta',),
    }

The simplest case is to have telemeta running at public root. To do so, add this url in urls.py::

    # Telemeta
    (r'^', include('telemeta.urls')),

    # Languages
    (r'^i18n/', include('django.conf.urls.i18n')),
    (r'^jsi18n/$', 'django.views.i18n.javascript_catalog', js_info_dict),

You should also bring the django admin::

    (r'^admin/django/', include(admin.site.urls)),

Please also uncomment::

    from django.contrib import admin
    admin.autodiscover()


Initialize the database
--------------------------

This synchronizes the DB with the model::

    ./manage.py syncdb

If you want tu use the data schema migration system (South needed, see previous paragraph)::

    ./manage.py migrate telemeta

Then::

    ./manage.py collectstatic


Start the project
--------------------

We are ready to start the telemeta server::

    python manage.py runserver

By default, the server starts on the port 8000. You can override this with, for example::

    python manage.py runserver 9000

To get it on your network interface::

    python manage.py runserver 192.168.0.10:9000


Test it
-----------

Go to this URL with your browser::

    http://localhost:8000

or::

    http://localhost:9000

or::

    http://192.168.0.10:9000


Configure the site domain name in admin > general admin > sites

Test it and enjoy it !


--------------------------
Template customization
--------------------------

Please see ::

    http://telemeta.org/wiki/InterfaceCustomization


--------------------------
Deploy it with Apache 2
--------------------------

If you want to use Telemeta through a web server, it is highly recommended to use Apache 2
with the mod_wsgi module as explained in the following page ::

    http://docs.djangoproject.com/en/1.1/howto/deployment/modwsgi/#howto-deployment-modwsgi

This will prevent Apache to put some audio data in the cache memory as it is usually the case with mod_python.

You can find an example of an Apache2 VirtualHost conf file there::

    example/apache2/telemeta.conf


-------------------------
IP based authorization
-------------------------

It is possible to login automatically an IP range of machines to Telemeta thanks to the django-ipauth module::

    sudo pip install django-ipauth

See http://pypi.python.org/pypi/django-ipauth/ for setup.


----------------------------
Import ISO 639-3 languages
----------------------------

From Telemeta 1.4, an ISO 639-3 language model has been implemented.

The ISO language table content can be initialized with the official code set.
Here is a import example where telemeta_crem5 is the SQL database::

    wget http://www.sil.org/iso639-3/iso-639-3_20110525.tab
    mysql -u root -p
    load data infile 'iso-639-3_20110525.tab' into table telemeta_crem5.languages CHARACTER SET UTF8 ignore 1 lines (identifier, part2B, part2T, part1, scope, type, name, comment);

If you upgraded Telemeta from a version previous or equal to 1.3, please update the media_items table as follow::

    mysql -u root -p
    use telemeta_crem5
    ALTER TABLE media_items ADD COLUMN 'language_iso_id' integer;
    ALTER TABLE 'media_items' ADD CONSTRAINT 'language_iso_id_refs_id_80b221' FOREIGN KEY ('language_iso_id') REFERENCES 'languages' ('id');

-------------------------
Contact / More infos
-------------------------

See README.rst and http://telemeta.org.
