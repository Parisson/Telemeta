var localeStrings = {
    'title': gettext('title'),
    'description': gettext('description'),
    'delete the marker permanently?': gettext('delete the marker permanently?'),
    'marker added to the selected playlist': gettext('marker added to the selected playlist'),
    'item added to the selected playlist': gettext('item added to the selected playlist'),
    'collection added to the selected playlist': gettext('collection added to the selected playlist'),
    'there are unsaved or modified markers': gettext('there are unsaved or modified markers'),
    'If you exit the page you will loose your changes' : gettext('If you exit the page you will loose your changes'),
    'author' : gettext('author'),
    'Paste HTML to embed player in website': gettext('Paste HTML to embed player in website'),
    'delete the item permanently?' : gettext('delete the item permanently?'),
    'delete the collection permanently?' : gettext('delete the collection permanently?'),
    'delete the playlist permanently?' : gettext('delete the playlist permanently?'),
    'delete the resource from the playlist permanently?' : gettext('delete the resource from the playlist permanently?'),
};

function gettrans(str){
    var loc = localeStrings; //instantiate once for faster lookup
    return str in loc ? loc[str] : str;
}

/*
 * Copyright (C) 2007-2011 Parisson
 * Copyright (c) 2011 Riccardo Zaccarelli <riccardo.zaccarelli@gmail.com>
 * 
 * This file is part of TimeSide.
 *
 * TimeSide is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 2 of the License, or
 * (at your option) any later version.
 *
 * TimeSide is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with TimeSide.  If not, see <http://www.gnu.org/licenses/>.
 *
 * Author: Riccardo Zaccarelli <riccardo.zaccarelli@gmail.com>
 */

/**
 * Class for managing translations in telemeta.
 */


