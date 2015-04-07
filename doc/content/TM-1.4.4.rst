Telemeta 1.4.4 is out !
########################

:category: Release
:date: 2012-10-04 16:52

Changes:

* no new fancy functions
* full using of static files which are now in static/ (htdocs/ is now deprecated)
* IMPORTANT : upgrade TimeSide to 0.4.1, add 'timeside' to INSTALLED_APPS and do: ./manage.py collectstatic
* add various buttons, various bugfixes
* after upgrading, always do: ./manage.py migrate

Upgrade::

    sudo pip install --upgrade telemeta

Please first read README.rst and INSTALL.rst to get all informations about the news. Apply new rules, dependencies, modules and settings from your old version to the new one.

or `download <​​http://pypi.python.org/packages/source/T/Telemeta/Telemeta-1.4.4.tar.gz>`_ (MD5: 47b8d7a6fa8340388ff72be58aaff59c)

Enjoy ;)
