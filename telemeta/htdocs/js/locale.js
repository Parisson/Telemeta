/* 
 * javascript file to handle translations between django and javascript
 */
function gettrans(str){
    var loc = localeStrings; //instantiate once for faster lookup
    return str in loc ? loc[str] : str;
}
var localeStrings = {
    'title': gettext('title'),
    'description': gettext('description'),
    'delete the marker permanently?': gettext('delete the marker permanently?'),
    'marker added to selected playlist': gettext('marker added to selected playlist'),
    'item added to selected playlist': gettext('item added to selected playlist'),
    'collection added to selected playlist': gettext('collection added to selected playlist')
};
