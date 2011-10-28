==================
Telemeta - INSTALL
==================

Don't worry, Telemeta is easy to setup as any other Django app !

-----------------
Requirements
-----------------

Telemeta is designed to run on Linux and other UNIX based architectures.
It depends on several python librairies like Django (version >= 1.1.1).
See http://djangoproject.com.

Other needed librairies are listed below.

-----------------------
Install the software
-----------------------

Install Telemeta
------------------

* Using python package tools (install MANY dependencies automatically)::

    sudo pip install telemeta

  or::

    sudo easy_install telemeta

* Downloading the latest tar archive at http://telemeta.org. Uncompress it and install. For example::

        tar xzf telemeta-1.0.tar.gz
        cd telemeta-1.0
        sudo python setup.py install

        
Install the dependencies
-------------------------

* On Debian (Squeeze recommended) or Ubuntu Lucid:

    Install all dependencies like this::
	
        sudo aptitude install python python-django python-xml python-mysqldb mysql-server \
                              python-ctypes python-setuptools python-support python-docutils \
                              python-libxml2 python-django-registration

    To get MP3 reading and writing, just add these lines to your /etc/apt/sources-list::

        deb http://www.debian-multimedia.org stable main

    Then::

        sudo apt-get update
        sudo aptitude install gstreamer0.10-fluendo-mp3 gstreamer0.10-lame

* On other linux platforms:

    Please install all dependencies thanks to your application manager.


Install TimeSide
-----------------

Telemeta needs the audio processing library named TimeSide (>= 0.3)
You have to download and install it from source.

So, download the last archive at :
http://code.google.com/p/timeside/downloads/list

Uncompress it and see README and INSTALL to install the dependencies 
and then the module.


Install JSON-RPC server
------------------------

In order to use markers on the player, you will need a JSON-RPC server for django::
    
    git clone git://github.com/samuraisam/django-json-rpc.git
    cd django-json-rpc
    python setup.py install

-------------------------
Fast testing (sandbox)
-------------------------

If you just want to test Telemeta, a sandbox is available in the example/ directory.
As Telemeta needs MySQL to work properly and fast, please create a database before editing setting.py

--------------------------
Or create a Django project
--------------------------

If you haven't already done it, start a new django project::

    cd ~/my_projects
    django-admin startproject mysite

-----------------------------------------
Create the media and cache directories
-----------------------------------------

We need 2 directories for media and caching::

    cd mysite
    mkdir media cache cache/data cache/export


You might want to place these data directories somewhere else, no pb.

------------------------
Create the database
------------------------

Telemeta needs MySQL to work well and fast. So you need to create a MySQL database before trying it.

----------------------------------
Configure the telemeta project
----------------------------------

Edit the file settings.py in a text editor.
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
    'jsonrpc',
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

Add the following variables::
    
    TEMPLATE_CONTEXT_PROCESSORS = (
        'django.core.context_processors.request',
        'django.contrib.auth.context_processors.auth',)

    TELEMETA_ORGANIZATION =         name of the organization which hosts this installation
    TELEMETA_SUBJECTS =             tuple of subject keywords (used for Dublin Core), such as "Ethnology", etc...
    TELEMETA_DESCRIPTION =          the description of the site
    TELEMETA_CACHE_DIR =            absolute path to the cache directory that you just created
    TELEMETA_GMAP_KEY =             your Google Map API key
    TELEMETA_DOWNLOAD_ENABLED =     True to enable raw audio data download
    TELEMETA_STREAMING_FORMATS =    tuple of authoized streaming formats. Ex : ('mp3', 'ogg')
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

If you want some personal templates, for example::
    
    TEMPLATE_DIRS = (
    '/home/dev/telemeta/sandboxes/sandbox_generic/templates/',
    )

You can find an example for settings.py there::
    
    example/sandbox/settings.py

--------------------------
Initialize the database
--------------------------

This synchronizes the DB with the model::

    python manage.py syncdb


----------------------
Configure your urls
----------------------

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

You can find an example for url.py there::
    
    example/sandbox/urls.py


--------------------
Start the project
--------------------

We are ready to start the telemeta server::

    python manage.py runserver

By default, the server starts on the port 8000. You can override this with, for example::

    python manage.py runserver 9000


-----------
Test it
-----------

Go to this URL with your browser::

    http://localhost:8000

or::

    http://localhost:9000


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
with the mod_wsgi module as explained in the following page :

    http://docs.djangoproject.com/en/1.1/howto/deployment/modwsgi/#howto-deployment-modwsgi

This will prevent Apache to put some audio data in the cache memory as it is usually the case with mod_python.

You can find an example of an Apache2 VirtualHost conf file there::

    example/apache2/telemeta.conf


-------------------------
Contact / More infos
-------------------------

See README.rst and http://telemeta.org.

