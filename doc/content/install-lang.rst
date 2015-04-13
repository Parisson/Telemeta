Import ISO 639-3 languages
##########################

:category: Tips
:tags: language, iso
:date: 2014-06-23 11:42

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