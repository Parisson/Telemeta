Telemeta 1.7 has been released!
###############################

:category: Releases

After months of hard development, I am very pleased to release Telemeta 1.7! It includes many transparent changes, mainly upgrading a lot of dependencies, especially those brought by the audio engine TimeSide which has also been released in its new version.

 * Based on TimeSide 0.9
 * Use Django 1.8
 * Rename some directories
 * Better video streaming
 * Better logging

More details: 

 * https://github.com/Parisson/Telemeta/milestone/5?closed=1
 * https://github.com/Parisson/Telemeta/compare/master...v1.6


Upgrading
---------

.. code:: bash

  git pull origin master
  git submodule update --init --remote
  docker-compose run app /srv/app/bin/upgrade_from_1.6_to_1.7.sh


WARNING
-------

`scripts/` and `app/scripts/` directories has been renamed `bin/` and `app/bin/` respectively. So please adapt your management and maintenance personal scripts.


1.6.x
-----

The 1.6.x branch has been also upgraded to fix various bugs:

 * Setting utf8 database by default
 * Deactivate video.js for now
 * Use mysql:5
 * Fix phpmyadmin config
 * Various bugfixes
 * Based on TimeSide 0.8.3


Get it!
--------

https://github.com/Parisson/Telemeta#install


Thanks to all partners!

Guillaume
