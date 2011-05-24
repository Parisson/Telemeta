==================
Telemeta - INSTALL
==================

-----------------
0. Requirements
-----------------

Telemeta is designed to run on Linux and other UNIX based architectures.
It depends on several python librairies like Django (version >= 1.1.1).
See http://djangoproject.com.

Other needed librairies are listed below.

-----------------------
1. Install the software
-----------------------

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


Install Telemeta
------------------

* On Debian style systems, if you have added our repositories::

    sudo apt-get install telemeta

* Else:

    Download the latest release of telemeta at
    http://telemeta.org

    Uncompress the archive like::

        tar xzvf telemeta_0.5.1.tar.gz

    Go to the main folder of telemeta and run this command
    in a shell as root::

        sudo python setup.py install


--------------------------
2. Create a Django project
--------------------------

If you haven't already done it, start a new django project::

    cd ~/my_projects
    django-admin startproject mysite


-----------------------------------------
3. Create the media and cache directories
-----------------------------------------

We need 2 directories for media and caching::

    cd mysite
    mkdir media cache cache/data cache/export


You might want to place these data directories somewhere else, no pb.


----------------------------------
4. Configure the telemeta project
----------------------------------

Edit the file settings.py in a text editor.
Modifiy the following variables:

    ADMINS =            telemeta requires that you indicate an administrator here
    DATABASES =         your database setting dict (don't forget to create the database if needed)
    MEDIA_ROOT =        absolute path to the media directory you just created
    INSTALLED_APPS =    add 'telemeta' and 'jsonrpc' to the tuple

Set the following languages:
    
    LANGUAGES = [ ('fr', 'French'),
                  ('en', 'English'),
    ]


Set the following Middlewares:
    
    MIDDLEWARE_CLASSES = (
        'django.middleware.common.CommonMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.locale.LocaleMiddleware',
    )

Add the following variables:
    
    TEMPLATE_CONTEXT_PROCESSORS = (
        'django.core.context_processors.request',
        'django.contrib.auth.context_processors.auth',)

    TELEMETA_ORGANIZATION =         name of the organization which hosts this installation
    TELEMETA_SUBJECTS =             tuple of subject keywords (used for Dublin Core), such as "Ethnology", etc...
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
    
You can find an example for settings.py there::
    
    conf/examples/django/settings.py


--------------------------
5. Initialize the database
--------------------------

This synchronizes the DB with the model::

    python manage.py syncdb


----------------------
6. Configure your urls
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

You can find an example for url.py there::
    
    conf/examples/django/urls.py


--------------------
7. Start the project
--------------------

We are ready to start the telemeta server::

    python manage.py runserver

By default, the server starts on the port 8000. You can override this with, for example::

    python manage.py runserver 9000


-----------
8. Test it
-----------

Go to this URL with your browser::

    http://localhost:8000

or::

    http://localhost:9000

Test it and enjoy it !


--------------------------
9. Deploy it with Apache
--------------------------

If you want to use Telemeta through a web server, it is highly recommended to use Apache 2
with the mod_wsgi module as explained in the following page :

    http://docs.djangoproject.com/en/1.1/howto/deployment/modwsgi/#howto-deployment-modwsgi

This will prevent Apache to put some audio data in the cache memory as it is usually the case with mod_python.

You can find an example of an Apache2 VirtualHost conf file there::

    conf/examples/apache2/telemeta.conf


-------------------------
10. Contact / More infos
-------------------------

See README and http://telemeta.org.

