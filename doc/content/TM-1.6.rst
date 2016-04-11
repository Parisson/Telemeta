    Telemeta 1.6 is finally out!
############################

:category: Releases

Telemeta is now usable on **any OS**, ready for development and for production in 5 mn! B-)

* Provide a docker image and composition for the full Telemeta application bundle.
  One month after the publication of docker-compose around march 2015, we had managed to build a prototyped composition which bundled all the dependencies of Telemeta and TimeSide. It took almost one year to deeply investigate all the capabilities of Docker and various images to finally release a propoer composition which bundles all the necessary applications and modules.
* Full refactoring of the search engine and interface using django-haystack and ElasticSearch with new faceting and smart filtering features
* Add an automatic EPUB3 ebook exporter for corpus and collections embedding metadata, image and audio materials.
* More inline forms and functional buttons
* Install new useful tools and modules like Conda, Jupyter notebook and `many others <https://github.com/Parisson/TimeSide/blob/master/conda-requirements.txt>`_
* Add resource sharing links
* Switch to Affero GPL licence
* Upgrade of every dependency bundle in the composition
* Many, many `bugfixes <https://github.com/Parisson/Telemeta/issues?q=is%3Aissue+is%3Aclosed>`_
* Thanks to all partners for this **huge** release!

Get it: https://github.com/Parisson/Telemeta#install
