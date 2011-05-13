
//Class for global functions.
//Note that the dollar sign is a reserved keyword in some browsers
//(see http://davidwalsh.name/dollar-functions)
//which might be in conflict with jQuery dollar sign

//PENDING: use static method?
//adds a move function to the array object.
//moves the element at position from into to position
//returns from if no move was accomplished, ie when either:
//1) from or to are not integers
//2) from==to or from==to-1 (also in this latter case there is no need to move)
//3) from or to are lower than zero or greater than the array length
//in any other case, returns to
//Array.prototype.move = function(from, to){
//    var pInt = parseInt;
//    if(pInt(from)!==from || pInt(to)!==to){
//        return from;
//    }
//    var len = this.length;
//    if((from<0 || from>len)||(to<0 || to>len)){
//        return from;
//    }
//    //if we moved left to right, the insertion index is actually
//    //newIndex-1, as we must also consider to remove the current index markerIndex, so:
//    if(to>from){
//        to--;
//    }
//    if(from != to){
//        var elm = this.splice(from,1)[0];
//        this.splice(to,0,elm);
//        return to;
//    }
//    return from;
//}

function foldInfoBlocks() {
    var $J = jQuery;
    var extra = $J('.extraInfos');
    extra.find('.folded dl, .folded table').css('display', 'none');
    extra.find('a').click(function() { 
        $J(this).parents('.extraInfos').children().toggleClass('folded').find('dl, table').toggle(100);
        return false; 
    });
}
//returns the full path of the current url location removing the last slash '/' followed by one or more '#', if any
function urlNormalized(){
    var sPath = window.location.href;
    sPath = sPath.replace(/\/#*$/,"");
    return sPath;
}

/**
 * Global telemeta function to set the current selected menu active according toi the current url
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


jQuery(document).ready(function() {
    foldInfoBlocks();
    setSelectedMenu();
});

//****************************************************************************
//json(param, method, onSuccesFcn(data, textStatus, jqXHR), onErrorFcn(jqXHR, textStatus, errorThrown))
//global function to senbd/retrieve data with the server
//
//param: the data to be sent or retrieved.
//  param will be converted to string, escaping quotes newlines and backslashes if necessary.
//  param can be a javascript string, boolean, number, dictionary and array.
//      If dictionary or array, it must contain only the above mentioned recognized types.
//      So, eg, {[" a string"]} is fine, {[/asd/]} not
//
//method: the json method, eg "telemeta.update_marker". See base.py
//
//onSuccesFcn(data, textStatus, jqXHR) OPTIONAL --IF MISSING, NOTHING HAPPENS --
//   A function to be called if the request succeeds with the same syntax of jQuery's ajax onSuccess function.
//   The function gets passed three arguments 
//      The data returned from the server, formatted according to the dataType parameter;
//      a string describing the status;
//      and the jqXHR (in jQuery 1.4.x, XMLHttpRequest) object
//
//onErrorFcn(jqXHR, textStatus, errorThrown) OPTIONAL. --IF MISSING, THE DEFAULT ERROR DIALOG IS SHOWN--
//    A function to be called if the request fails with the same syntax of jQuery ajax onError function..
//    The function receives three arguments:
//      The jqXHR (in jQuery 1.4.x, XMLHttpRequest) object,
//      a string describing the type of error that occurred and
//      an optional exception object, if one occurred.
//      Possible values for the second argument (besides null) are "timeout", "error", "abort", and "parsererror".
//****************************************************************************

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
    //var g = 9;
    //creating the string to send. We use array join and string concatenation with +=
    //as it is more efficient
    var param2string = toString_(param);
    var data2send = '{"id":"jsonrpc", "params":';
    data2send+=param2string;
    data2send+=', "method":"'
    data2send+=method;
    data2send+='","jsonrpc":"1.0"}';
    //        var data2send = '{"id":"jsonrpc", "params":[{"item_id":"'+ s(itemid)+
    //            '", "public_id": "'+s(marker.id)+'", "time": "'+s(offset)+
    //            '", "author": "'+s(marker.author)+
    //            '", "title": "'+s(marker.title)+
    //            '","description": "'+s(marker.desc)+'"}], "method":"'+method+'","jsonrpc":"1.0"}';
    var $J = jQuery;
    $J.ajax({
        type: "POST",
        url: '/json/',
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
var uniqid = function() {
    var d = new Date();
    return new String(d.getTime() + '' + Math.floor(Math.random() * 1000000)).substr(0, 18);
};

/**
 * Loads scripts asynchronously
 * can take up to four arguments:
 * root (optional): a string specifying the root (such as '/usr/local/'). Must end with slash, otherwise
 *      each element in scriptArray must begin with a slash
 * scriptArray: a string array of js script filenames, such as ['script1.js','script2.js']
 * callback (optional): callback to be executed when ALL scripts are succesfully loaded
 * loadInSeries (optional): if true scripts are loaded in synchronously, ie each script is loaded only once the
 *      previous has been loaded. The default (argument missing) is false
 *
 * Examples. Given scripts = ['s1.js', 's2.js']
 *  loadScripts(scripts)                          //loads (asynchronously) scripts
 *  loadScripts('/usr/', scripts)                 //loads (asynchronously) ['/usr/s1.js', '/usr/s2.js']
 *  loadScripts(scripts, callback)                //loads (asynchronously) scripts. When loaded, executes callback
 *  loadScripts('/usr/', scripts, callback)       //loads (asynchronously) ['/usr/s1.js', '/usr/s2.js']. When loaded, executes callback
 *  loadScripts(scripts, callback, true)          //loads (synchronously) scripts. When loaded, executes callback
 *  loadScripts('/usr/', scripts, callback, true) //loads (synchronously) ['/usr/s1.js', '/usr/s2.js']. When loaded, executes callback
 *
 */
function loadScripts(){
    var optionalRoot='', scriptArray=[], callback=undefined, loadInSeries=false;
    var len = arguments.length;
    if(len==1){
        scriptArray = arguments[0];
    }else if(len==2){
        if(typeof arguments[0] == 'string'){
            optionalRoot = arguments[0];
            scriptArray = arguments[1];
        }else{
            scriptArray = arguments[0];
            callback = arguments[1];
        }
    }else if(len>2){
        if(typeof arguments[0] == 'string'){
            optionalRoot = arguments[0];
            scriptArray = arguments[1];
            callback = arguments[2];
            if(len>3){
                loadInSeries = arguments[3];
            }
        }else{
            scriptArray = arguments[0];
            callback = arguments[1];
            loadInSeries = arguments[2];
        }
    }
    
    if(!scriptArray){
        if(callback){
            callback();
        }
        return;
    }
    len = scriptArray.length;
    var i=0;
    if(optionalRoot){
        for(i =0; i<len; i++){
            scriptArray[i] = optionalRoot+scriptArray[i];
        }
    }

    var $J = jQuery;
    //var time = new Date().getTime();
    if(loadInSeries){
        var load = function(index){
            if(index<len){
                //consolelog("loading "+scriptArray[index]+" "+new Date().getTime());
                $J.getScript(scriptArray[index],function(){
                    load(index+1);
                });
            }else if(callback){
                //consolelog("EXECUTING CALLBACK ELAPSED TIME:"+(new Date().getTime()-time));
                callback();
            }
        };
        load(0);
    }else{
        var count=0;
        var s;
        for(i=0; i <len; i++){
            s = scriptArray[i];
            //consolelog("loading "+s+" "+new Date().getTime());
            $J.getScript(s, function(){
                count++;
                if(count==len && callback){
                    //consolelog("EXECUTING CALLBACK ELAPSED TIME:"+(new Date().getTime()-time));
                    callback();
                }
            });
        }
    }
}



function consolelog(text){
    if(typeof console != 'undefined'){
        var c = console;
        if (c.log) {
            c.log(text);
        }
    }
}