/*
 * Copyright (C) 2007-2012 Guillaume Pellerin, Parisson
 * Copyright (c) 2011 Riccardo Zaccarelli <riccardo.zaccarelli@gmail.com>
 * Copyright (c) 2010 Olivier Guilyardi <olivier@samalyse.com>
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
 * Authors: Riccardo Zaccarelli <riccardo.zaccarelli@gmail.com>
 *          Olivier Guilyardi <olivier@samalyse.com>
 */

/**
 * Class for telemeta global functions.
 * Note that the dollar sign is a reserved keyword in some browsers
 * (see http://davidwalsh.name/dollar-functions)
 * which might be in conflict with jQuery dollar sign.
 */

//returns the full path of the current url location removing the last slash '/' followed by one or more '#', if any
function urlNormalized(){
    var sPath = window.location.href;
    sPath = sPath.replace(/\/#*$/,"");
    return sPath;
}
/**
 *sets up few stuff when the page is ready (see functions below it)
 */
jQuery(document).ready(function() {
    foldInfoBlocks();
    setSelectedMenu();
});

/**
 *function inherited from old code, never touched. Guess fixes the click on the left data table, if any
 */
function foldInfoBlocks() {
    var $J = jQuery;
    var extra = $J('.extraInfos');
    extra.find('.folded dl, .folded table').css('display', 'none');
    extra.find('h4').click(function() {
        $J(this).parents('.extraInfos').children().toggleClass('folded').find('dl, table').toggle(100);
        //toggle toggles the visibility of elements
        return false;
    });
}

/**
 * Global telemeta function which sets the current selected menu according to the current url
 */
function setSelectedMenu(){
    var $J = jQuery;
    var menus = $J('#menu a');
    //build collections/items from http:/site/collections/items,
    //being http:/site/ = window.location.origin
    
    //function for normalizing paths (removes last n occurrences of the slash)
    var normalize = function(str){
        return str.replace(/\/+#*$/,"");
    }
    
    var host = window.location.host;
    var protocol = window.location.protocol
    var href = normalize(window.location.href);
     
    if(!(host) || !(protocol) || !(href)){
        return;
    }

    //var pageOrigin = normalize(window.location.origin); //does not exist in FF, so:
    var pageOrigin = normalize(protocol+"//"+host);
    var pageHref = normalize(href);

    menus.each(function(){
        ///if we are at home, the window location href corresponds to window location origin,
        //so we select only links whose link points EXACTLY to the origin (home link)
        var linkHref = normalize(this.href);
        var elm = $J(this);

        if(linkHref.indexOf("#") != -1){
            var reg = new RegExp("[#]+", "g");
            var baseHref = linkHref.split(reg);
            linkHref = pageOrigin + "/" + baseHref[1]
        }

        if(pageOrigin===pageHref){
            if(pageHref == linkHref){
                elm.addClass('active');
            }else{
                elm.removeClass('active');
            }
        }else{
            //here, on the other hand, we select if a link points to a page or super page
            //of the current page
            if(linkHref!=pageOrigin && pageHref.match("^"+linkHref+".*")){
                elm.addClass('active');
            }else{
                elm.removeClass('active');
            }
        }
        
    })
}




/*****************************************************************************
 * json(param, method, onSuccesFcn(data, textStatus, jqXHR), onErrorFcn(jqXHR, textStatus, errorThrown))
 * global function to senbd/retrieve data with the server
 *
 * param: the data to be sent or retrieved.
 *   param will be converted to string, escaping quotes newlines and backslashes if necessary.
 *   param can be a javascript string, boolean, number, dictionary and array.
 *       If dictionary or array, it must contain only the above mentioned recognized types.
 *       So, eg, {[" a string"]} is fine, {[/asd/]} not
 *
 * method: the json method, eg "telemeta.update_marker". See base.py
 *
 * onSuccesFcn(data, textStatus, jqXHR) OPTIONAL --IF MISSING, NOTHING HAPPENS --
 *    A function to be called if the request succeeds with the same syntax of jQuery's ajax onSuccess function.
 *    The function gets passed three arguments
 *       The data returned from the server, formatted according to the dataType parameter;
 *       a string describing the status;
 *       and the jqXHR (in jQuery 1.4.x, XMLHttpRequest) object
 *
 * onErrorFcn(jqXHR, textStatus, errorThrown) OPTIONAL. --IF MISSING, THE DEFAULT ERROR DIALOG IS SHOWN--
 *     A function to be called if the request fails with the same syntax of jQuery ajax onError function..
 *     The function receives three arguments:
 *       The jqXHR (in jQuery 1.4.x, XMLHttpRequest) object,
 *       a string describing the type of error that occurred and
 *       an optional exception object, if one occurred.
 *       Possible values for the second argument (besides null) are "timeout", "error", "abort", and "parsererror".
 * ****************************************************************************/

var json = function(param,method,onSuccessFcn,onErrorFcn){
    //this function converts a javascript object to a string
    var toString_ = function(string){
        if(typeof string == "string"){
            //escapes newlines quotes and backslashes
            string = string.replace(/\\/g,"\\\\")
            .replace(/\n/g,"\\n")
            .replace(/"/g,"\\\"");
        }
        var array; //used for arrays and objects (see below)
        if(typeof string == "boolean" || typeof string== "number" || typeof string == "string"){
            string = '"'+string+'"';
        }else if(string instanceof Array){
            array = [];
            for(var i = 0;i <string.length ; i++){
                array.push(toString_(string[i])); //recursive invocation
            }
            string='[';
            string+=array.join(",");
            string+=']';
        }else{
            array = [];
            for(var k in string){
                array.push(toString_(k)+":"+toString_(string[k])); //recursive invocation
            }
            string='{';
            string+=array.join(",");
            string+='}';
        }
        return string;
    };
    
    //creating the string to send. 
    var param2string = toString_(param);
    var data2send = '{"id":"jsonrpc", "params":';
    data2send+=param2string;
    data2send+=', "method":"'
    data2send+=method;
    data2send+='","jsonrpc":"1.0"}';
    
    var $J = jQuery;
    $J.ajax({
        type: "POST",
        url: 'json/',
        contentType: "application/json",
        data: data2send,
        dataType: "json",
        success: function(data, textStatus, jqXHR){
            if(onSuccessFcn){
                onSuccessFcn(data, textStatus, jqXHR);
            }
        },
        error: function(jqXHR, textStatus, errorThrown){
            if(onErrorFcn){
                onErrorFcn(jqXHR, textStatus, errorThrown);
                return;
            }
            //default:
            var details = "\n(no further info available)";
            if(jqXHR) {
                details="\nThe server responded witha status of "+jqXHR.status+" ("+
                jqXHR.statusText+")\n\nDetails (request responseText):\n"+jqXHR.responseText;
            }
            alert("ERROR: Failed to save"+details);
            
        }
    });

};

/**
 * function for writing to the console. Catches errors, if any (eg, console == undefined) and does nothing in case
 */
function consolelog(text){
    if(typeof console != 'undefined'){
        var c = console;
        if (c.log) {
            c.log(text);
        }
    }
}

// Drop down menus

$(document).ready(function () {
     
    $('#nav li').hover(
        function () {
            //show its submenu
            $('ul', this).slideDown(200);
 
        },
        function () {
            //hide its submenu
            $('ul', this).slideUp(100);        
        }
    );
     
});