/**
 * TimeSide - Web Audio Components
 * Copyright (c) 2011 Parisson
 * Author: Riccardo Zaccarelli <riccardo.zaccarelli gmail.com>
 * License: GNU General Public License version 2.0
 */

/**
 * Class for managing translations in telemeta.
 */

var localeStrings = {
    'title': gettext('title'),
    'description': gettext('description'),
    'delete the marker permanently?': gettext('delete the marker permanently?'),
    'marker added to the selected playlist': gettext('marker added to the selected playlist'),
    'item added to the selected playlist': gettext('item added to the selected playlist'),
    'collection added to the selected playlist': gettext('collection added to the selected playlist'),
    'there is at least one unsaved marker': gettext('there is at least one unsaved marker'),
    'If you exit the page you will loose your changes' : gettext('If you exit the page you will loose your changes'),
    'author' : gettext('author')
};

function gettrans(str){
    var loc = localeStrings; //instantiate once for faster lookup
    return str in loc ? loc[str] : str;
}
