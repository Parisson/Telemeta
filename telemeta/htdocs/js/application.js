
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


function PopupDiv(){
    var $J = jQuery;
    var me = this;
    var data = arguments.length && arguments[0] || {};
   
    //var wdw = $J(window);
    var div  = $J('<div/>');
    var header = $J('<div/>').append($J('<input/>').attr('type','text')).append($J('<a/>').attr('href','#').click(function(){
        me.close();
        return false;
    })); //.css('float','right');
    var container = $J('<div/>').css('overflow','auto');
    var footer = $J('<div/>').css({
        'textAlign':'right'
    }).append($J('<a/>').attr('href','#').click(function(){
        me.trigger('ok',true);
        return false;
    }));
    header.find('*').add(footer.find('*')).css('display','none');
    div.append(header).append(container).append(footer);
    //defining immediately the method getDiv (because it is used below)
    this.getDiv = function(){
        return div;
    }
    //setting functions:
    
    var listeners = {};
    this.getListeners = function(){
        return listeners;
    }

    var k;
    //setting static properties, if any:
    for(k in PopupDiv){
        this.__proto__[k] = PopupDiv[k];
        //        consolelog(k+' '+PopupDiv[k]);
        delete PopupDiv[k];
    }

    //setting instance-specific properties:
    for(k in data){
        if(k == 'onOk' || k == 'onShow' || k == 'onClose'){
            this.bind(k,data[k]);
        }else if(k == 'content'){
            this.setContent(data[k]);
        }else {
            this[k] = data[k];
        }
    }

    if(!this.popupCss){
        this.popupCss = {}; //workaround to update css the first time we call show
    //note that {} evaluates to true, but jQueryElement.css({}) is harmless
    }
    

}


(function(p){
    //private static variables
    var $ = jQuery;
    var w_ = window;
    var d_ = document;
    var wdw = $(w_);
    var popupStaticId = 'popup_'+(new Date().getTime());
    //var doc = $(d_);


    //in the functions below, this refers to the new Popup instance, not to the prototype



    p.isClickElement = function(element){
        return element && element.length==1 && element instanceof $ && element[0] !== w_ && element[0] !== d_ &&
        (element.is('a') || element.is('input[type=button]') || element.is('button') ||
            element.is('input[type=submit]'));
    };

    p.getId = function(){
        var div = this.getDiv();
        if(!(div.attr('id'))){
            div.attr('id',popupStaticId+'_'+(new Date().getTime()));
        }
        return div.attr('id');
    };


    //default properties which can be overridden
    p.shadowOffset = 4;
    p.invoker = wdw;
    p.bounds = {
        'top':0.25,
        'left':0.25,
        'right':0.25,
        'bottom':0.25
    }; //note that sepcifying top+bottom>=1 there is undefined behaviour (in chrome, offset is set but height takes all available space)
    p.boundsexact = false;
    p.popupClass = '';
    p.popupCss = {};
    p.showok = false;
    p.showclose=false;
    p.title = "";
    p.okButtonClass =  '';
    p.closeButtonClass =  '';
    p.okButtonTitle =  'Ok';
    p.closeButtonTitle =  'x';
    p.defaultCloseOperation = 'hide';
    p.focusable = false;
    p.fadInTime = 'fast',
    p.fadeOutTime = 0,
    p.shadowOpacity = 0.25;
    p.zIndex = 10000;
    // p.listItemClass = '';

    p.getFormData = function(){
        var elms = this.find('input,select,textarea');
        var ret = {};
        elms.each(function(i,e){
            var ee = $(e);
            var key = ee.attr('name');
            if(key){
                ret[key] = ee.val();
            }
        });
        return ret;
    };

    p.closeLater = function(millseconds){
        var me = this;
        setTimeout(function(){
            me.close();
        },millseconds);
    },

    //methods:
    p.find = function(argumentAsInJQueryFind){
        return $(this.getDiv().children()[1]).find(argumentAsInJQueryFind);
    };

    p.bind = function(eventName, callback){ //eventname: show, close or ok
        var listeners = this.getListeners();
        if(eventName in listeners){
            listeners[eventName].push(callback);
        }else{
            listeners[eventName] = [callback];
        }
    };


    p.unbind = function(eventName){
        var listeners = this.getListeners();
        if(eventName && eventName in listeners){
            delete listeners[eventName];
        }else if(!eventName){
            for(var k in listeners){
                delete listeners[k];
            }
        }
    };

    p.trigger = function(eventName){
        var listeners = this.getListeners();
        var me = this;
        if(eventName in listeners){
            var callbacks = listeners[eventName];
            var i = 0;
            if(eventName == 'ok'){
                var data = this.getFormData();
                for(i=0; i<callbacks.length; i++){
                    callbacks[i].apply(me,[data]);
                }
                if(arguments.length>1 && arguments[1]){
                    //workaround to remove listeners on close:
                    if('close' in listeners){
                        var v = listeners['close'];
                        delete listeners['close'];
                        this.close();
                        listeners['close'] = v;
                    }else{
                        this.close();
                    }

                }
            }else{
                for(i=0; i<callbacks.length; i++){
                    callbacks[i].apply(me);
                }
            }
        }
    };

    p.setContent = function(content){
        var div = this.getDiv();
        var container =   $($(div).children()[1]);
        //div.appendTo('body'); //necessary to properly display the div size
        container.empty();

        if(content instanceof $){
            container.append(content);
        }else if(content instanceof Array){
            var jQ = $;
            var me = this;
            //var name = this.getListItemName();
            var input = $('<input/>').attr('type','hidden').attr('name','selIndex');
            var setEvents = function(idx,anchor,input){
                anchor.click(function(){
                    input.val(idx);
                    me.trigger('ok',true);
                    return false;
                }).focus(function(){ //focus because we need to get the value if ok is present
                    input.val(idx);
                })
            };
            for(var h=0; h<content.length; h++){
                var item = content[h];
                var a = $('<a/>').attr('href','#');
                if('class' in item){
                    a.addClass(item['class']);
                }
                if('html' in item){
                    a.html(item['html']);
                }
                if('name' in item){
                    a.attr('name', item['name']);
                }
                if('id' in item){
                    a.attr('id', item['id']);
                }
                if('css' in item){
                    a.css(item['css']);
                }
                a.css({
                    'display':'block',
                    'margin':'2px'
                }); //margin is used to display the outline (focus)
                setEvents(h,a,input);
                container.append(a);
            }
            container.append(input);
        }else if(content && content.constructor == Object){
            var leftElements = $([]);
            var rightElements = $([]);
            var maxw = [0,0];
            var insert = function(e1,e2){
                var lineDiv = $('<div/>');
                if(!e2){
                    e2=e1;
                    e1 = $('<span/>');
                }
                rightElements = rightElements.add(e2);
                leftElements = leftElements.add(e1);
                container.append(lineDiv.append(e1).append(e2));
                return lineDiv;
            }
            var title, component;

            var max = Math.max; //instantiate once
            var lineDiv = undefined;
            var lineDivs = $([]);
            for(var k in content){
                var val = content[k];
                if(typeof val == 'string' || typeof val == 'number'){
                    title = $('<span/>').html(k);
                    maxw[0] = max(maxw[0],k.length);
                    maxw[1] = max(maxw[1],val.length);
                    component = $('<input/>').attr('type','text').val(val).attr('name',k);
                    lineDivs = lineDivs.add(insert(title,component));
                }else if(val === true || val === false){
                    var id = this.getId()+"_checkbox";
                    title = $('<input/>').attr('type','checkbox').attr('name',k).attr('id',id);
                    if(val){
                        title.attr('checked','checked');
                    }else{
                        title.removeAttr('checked');
                    }
                    component = $('<label/>').attr('for',id).html(k);
                    maxw[1] = max(maxw[1],k.length);
                    lineDivs = lineDivs.add(insert($('<span/>').append(title),component));
                }else if(val instanceof Array){
                    title = $('<span/>').html(k);
                    maxw[0] = max(maxw[0],k.length);
                    component = $('<select/>').attr('size',1);
                    for(var i=0; i< val.length; i++){
                        component.append($('<option/>').val(val[i]).html(val[i]));
                        maxw[1] = max(maxw[1],val[i].length);
                    }
                    lineDivs = lineDivs.add(insert(title,component));
                }
                if(lineDiv){
                    lineDiv.css('marginBottom','1ex');
                }
            }
            lineDivs.css({
                'white-space': 'nowrap',
                'marginBottom':'0.5ex'
            });
            //last div erase marginBottom
            $(lineDivs[lineDivs.length-1]).css('marginBottom','');


            //display: inline-block below assures that width are properly set
            //IE 6/7 accepts the value only on elements with a natural display: inline.
            //(see http://www.quirksmode.org/css/display.html#t03)
            //span and anchors are among them
            //(see http://www.maxdesign.com.au/articles/inline/)
            leftElements.add(rightElements).css({
                'display':'inline-block',
                'margin':'0px',
                'padding':'0px'
            });
            leftElements.css({
                'textAlign':'right',
                'marginRight':'0.5ex',
                'width':Math.round((3/5)*maxw[0])+'em'
            });
            rightElements.css({
                'width':Math.round((3/5)*Math.max(maxw[0], maxw[1]))+'em'
            }); //might be zero if default values are all ""
        }else{
            container.append(""+content);
        }

    };

    p.setFocusCycleRoot = function(value){
        //var value = this.focusable;
        var popup = this.getDiv();
        var focusAttr = this.getFocusAttr();
        var invokerIsClickable = this.isClickElement(this.invoker);
        var children_ = popup.children();
        var topDiv = $(children_[0]);
        var centralDiv = $(children_[1]);
        var bottomDiv = $(children_[2]);
        var elementsWithFocus =  centralDiv.find('input[type!=hidden],select,textarea,a'); //input:not(:hidden),select,textarea,a,

        var ret = elementsWithFocus.length ? $(elementsWithFocus[0]) : popup;
        if(this.showclose){
            elementsWithFocus =elementsWithFocus.add(topDiv.find('a'));
        }
        if(this.showok){
            elementsWithFocus = elementsWithFocus.add(bottomDiv.find('a'));
        }
        elementsWithFocus = elementsWithFocus.add(popup);
        var focusNameSpace = "blur."+this.getId();
        if(!value){
            elementsWithFocus.each(function(i,elm){
                $(elm).unbind(focusNameSpace).removeAttr('tabindex').removeAttr(focusAttr);
            });
            this.getFirstFocusableElement = function(){
                return undefined;
            }
            if(invokerIsClickable){
                this.invoker.removeAttr('tabindex').removeAttr(focusAttr);
            }
            return;
        }
        if(invokerIsClickable){
            this.invoker.attr('tabindex',0).attr(focusAttr,'true');
        }
        var doc_ = d_; //closure (see nested function below)

        //now all elements (including header and footer)

        var me = this;
        //bind the blur to each focusable element:
        elementsWithFocus.each(function(i,e){
            var ee = $(e);
            ee.attr(focusAttr,'true');
            ee.attr('tabindex',i+1);
            ee.unbind(focusNameSpace).bind(focusNameSpace,function(){
                //wait 250msec to see if the focus has been given to another popup focusable element: if yes, do nothing
                //otherwise execute callback
                setTimeout(function(){
                    var v = doc_.activeElement;
                    consolelog(v);
                    if((v && $(v).attr(focusAttr)) || me.isClosing){
                        //if we are closing, we will call back this method which removes the focus attributes, bt meanwhile the
                        //timeout should execute
                        return;
                    }

                    me.close();
                },200)
            }); //set here another time delay. 300 seems to be the good compromise between visual hide and safetiness that
        //meanwhile the focus has already been given to the next component
        });
        this.getFirstFocusableElement = function(){
            return ret;
        }
    };
    p.getFirstFocusableElement = function(){
        return undefined;
    };
    p.show = function(){
        var div = this.getDiv();
        var me = this;


        var cssModified = (this.popupClass || this.popupCss);
        if(this.popupClass){
            //which might be the prototype
            div.removeClass().addClass(this.popupClass);
            this.popupClass = ''; //override prototype property
        }
        if(this.popupCss){
            //which might be the prototype
            div.css(this.popupCss);
            this.popupCss = ''; //override prototype property
        }
        //css modified, restore properties we need to be restored:
        if(cssModified){
            div.css({
                'position':'absolute',
                'zIndex':this.zIndex,
                'margin':'0px',
                'overflow':'hidden'
            });
        }

        //if we have elements of type listitem, add the specified class
        //        var name = this.getListItemName();
        //        var elms = this.find('a[name='+name+']');
        //        if(this.listItemClass){
        //            elms.removeClass().addClass(this.listItemClass);
        //            this.listItemClass = "";
        //        }
        //        elms.css('display','block');


        this.setFocusCycleRoot(this.focusable);
        this.setSizable();//this means the popupdiv is display: !none and visibility:hidden, so every element
        //inside it should be visible and therefore sizable. Being visible means that jQuery.is(':visible') returns true
        //start with showing top and bottom if some elements are visible

        var subdiv = div.children();

        //configure buttons. Text and classes are added here cause might have been changed
        var topDiv = $(subdiv[0]);
        var titleInput = topDiv.find(':text'); //$(':text') is equivalent to $('[type=text]') (selects all <input type="text"> elements)
        var closeBtn = topDiv.find('a');
        //if title doesn't exist or is hidden, set them to undefined (same for closeBtn).
        //to check visibility, we dont use is(:visible) cause apparently
        //width and height as zero mean hidden (I think that is the cause):
        titleInput = titleInput.length ? $(titleInput.get(0)) : undefined;
        closeBtn = closeBtn.length ? $(closeBtn.get(0)) : undefined;
        if(this.showclose || this.title){
            topDiv.css('paddingBottom','0.5ex').show(); //add padding to bottom
            //is(.. return true if at least one of these elements matches the given arguments.
            if(closeBtn){
                if(this.closeButtonClass){
                    closeBtn.addClass(this.closeButtonClass);
                }
                if(this.closeButtonTitle){
                    closeBtn.html(this.closeButtonTitle);
                }
                closeBtn.css({
                    'display':'inline-block'
                }); //in order to set width and height on the element
            }
            if(titleInput){
                titleInput.val(this.title).css({
                    'display':'inline-block',
                    'padding':'0',
                    'margin':'0',
                    'border':'0',
                    'backgroundColor':'transparent',
                    'marginRight' : '1ex'
                }).attr('readonly','readonly');
            }
        }else{
            topDiv.css('padding','0px');
        }

        var bottomDiv = $(subdiv[2]);
        //do the same as above, ok must exist and be visible, otherwise is undefined
        var okButton = bottomDiv.find('a');
        okButton = okButton.length ? $(okButton.get(0)) : undefined;

        //see note above about why we dont use okButton.is(':visible')
        if(this.showok){
            bottomDiv.css('paddingTop','0.5ex').show(); //add padding to bottom
            //is(.. return true if at least one of these elements matches the given arguments.
            if(okButton){
                if(this.okButtonClass){
                    okButton.addClass(this.okButtonClass);
                }
                if(this.okButtonTitle){
                    okButton.html(this.okButtonTitle);
                }
                okButton.css('display','inline-block'); //in order to set width and height on the element
            }
        }else{
            bottomDiv.css('paddingTop','0px');
        }

        var centralDiv = $(subdiv[1]);
        //reset properties of the central div
        centralDiv.css({
            'maxHeight':'',
            'maxWidth':'',
            'minHeight':'',
            'minWidth':'',
            'height':'',
            'width':''
        });


        var invoker = this.invoker;

        var sizeAsPopup = false;
        if(this.isClickElement(invoker)){
            this.setBoundsAsPopup(invoker, true);
            sizeAsPopup = true;
            //storing click events, when showing clicking on an event must give the focus to the popup
            //old handlers will be restored in close()
            this['_tmpHandlers'+this.getId()] = undefined;
            var focusElm = this.getFirstFocusableElement();
            if(focusElm){
                var oldHandlers = [];
                var type = 'click';
                var clickEvents =invoker.data("events")[type];
                $.each(clickEvents, function(key, value) {
                    oldHandlers.push(value);
                })
                invoker.unbind(type); //remove (temporarily) the binding to the event.
                //for instance, if we show the popup by clicking invoker, when the popup is shown do nothing
                //on clicking invoker until popup.hide is called

                this['_tmpHandlers'+this.getId()] = oldHandlers;
                invoker.unbind(type).bind(type,function(evt){
                    //let the invoker have focus and let it be recognized as an element which does not blur the popup:
                    //invoker.attr('tabindex',0).attr(focusAttr,'true');
                    if(div.length && div.is(':visible')){
                        focusElm.focus();
                        return false;
                    }
                    //something wrong: close the popup and restore the hanlers
                    me.close.apply(me);
                    return false;
                });
            }

        }else{
            this.setBoundsInside(invoker, this.bounds, this.boundsexact, true);
        }



        //set central div max height ONLY IF NECESSARY:
        var maxHeight = (div.height()-topDiv.outerHeight(true)-bottomDiv.outerHeight(true)-
            (centralDiv.outerHeight(true)-centralDiv.height()));
        var height = centralDiv.height();
        if(sizeAsPopup && maxHeight<height){
            centralDiv.css('maxHeight',maxHeight+'px');
        }else{
            centralDiv.css({
                'maxHeight': maxHeight+'px',
                'minHeight': maxHeight+'px'
            });
        }
        //set central div max width ONLY IF NECESSARY:
        var maxWidth = div.width();
        var width = $(subdiv[1]).outerWidth(true);
        if(sizeAsPopup && maxWidth<width){
            centralDiv.css('maxWidth',maxWidth+'px');
        }else{
            centralDiv.css({
                'maxWidth': maxWidth+'px',
                'minWidth':maxWidth+'px'
            });
        }

        //set title and close button to span whole width, if necessary
        if(titleInput || closeBtn){
            var titleW = topDiv.width() - (closeBtn ? closeBtn.outerWidth(true) : 0) - (titleInput ? titleInput.outerWidth(true)-titleInput.width() : 0);
            if(titleInput){
                titleInput.css('width',titleW+'px');
            }
        }

        //creating shadow. REmove attributes tabindex (unnecessary) and especially focusAttr,
        //so that clicking tab key and setting the shadow focusable hides the popup. If one wants the shadow not to hide the popup. keep
        //focusAttr BUT insert shadow in the focus cycle root (see method)
        var shadow = div.clone(false,false).empty().css({
            'backgroundColor':'#000',
            'borderColor':'#000',
            'visibility':'visible',
            'zIndex':this.zIndex-1
        }).removeAttr('tabindex').removeAttr(this.getFocusAttr()).fadeTo(0,0).
        attr('id',this.getShadowDivId()) //for use in hide
        .insertAfter(div);


        var postShowFcn = function(){
            me.trigger('show');
            var rect = me.getBounds.apply(me);
            shadow.css({
                'left':(rect.x + me.shadowOffset)+'px',
                'top':(rect.y + me.shadowOffset)+'px',
                'width':(rect.width)+'px',
                'height':(rect.height)+'px'
            }).fadeTo(me.fadInTime,me.shadowOpacity, function(){
                var v = me.getFirstFocusableElement();
                if(v){
                    v.focus();
                }
            });
        }

        div.hide().css('visibility','visible').show(this.fadInTime,function(){

            postShowFcn();


        });
    };

    p.setBoundsAsPopup = function(popupInvoker, isSizable){
        var invoker = popupInvoker;
        var div = this.getDiv();
        var oldCss= isSizable ?  undefined : this.setSizable();

        var windowRectangle = this.getBoundsOf(wdw); //returns the window rectangle

        var invokerOffset = invoker.offset();
        var invokerOuterHeight = invoker.outerHeight();

        //first set the maxwidth,so that we can compute the height according to it:
        this.setMaxSize({
            width: wdw.scrollLeft()+wdw.width()-invokerOffset.left
        },isSizable);


        var spaceAbove = invokerOffset.top - windowRectangle.y;
        var spaceBelow = windowRectangle.height - invokerOuterHeight - spaceAbove;

        var placeAbove = spaceAbove > spaceBelow && div.outerHeight(true) > spaceBelow;
        //note that div.outerHeight() should be  == div.outerHeight(true), as we set margins =0

        //        alert(div.outerHeight(true)+' '+spaceAbove+' '+spaceBelow);
        //        div.css('visibility','');
        //        return;

        this.setMaxSize({
            height : (placeAbove ? spaceAbove : spaceBelow)
        },isSizable); //width will be ignored (for the moment)
        //decrement of one pixel cause when the popup has to be reduced and the shadows bounds "touch" the window right or bottom sides,
        //the window scrolls (and it shouldn't)

        //setting the minimum size to the invoker width, minheight the same as maxHeight (see above)
        this.setMinSize({
            width: invoker.outerWidth()+this.shadowOffset //workaround to NOT consider the shadow, as offset below substracts the shadow
        //height : spaceAbove>spaceBelow ? spaceAbove : spaceBelow //why this? because if we click the popup a
        //computed height CH seems to be set. At subsequent popup show, CH will be the same UNLESS a new maxHeight lower than CH is set
        //however, we want CH to change even if a new maxHeight greater than CH is set
        },isSizable);

        //setting the top and left. This must be done at last because popupDiv.outerHeight(true)
        //must have been computed according to the height set above...
        this.offset({
            'left': invokerOffset.left,
            'top': (placeAbove ? invokerOffset.top -  div.outerHeight(true) :
                invokerOffset.top + invokerOuterHeight)
        },isSizable);
        if(oldCss){
            div.css({
                'display':oldCss['display'],
                'visibility':oldCss['visibility']
            });
        }
    };
    //places and resize the popupdiv inside parent
    //padding is a dict {top:,left:,bottom:..,right:,...} measuring the distance of the popupdiv from the corners, so that
    //padding={top:0.25,left:0.25,bottom:0.25,right:0.25} will place the popupdiv at the center of parent
    //padding={top:25,left:25,bottom:25,right:25} will place the popupdiv at distances 25 px from parent sides
    //in other words, padding keys lower or euqals to 1 will be conbsidered as percentage, otherwise as absolute measures in px
    p.setBoundsInside = function(parent, pd, boundsExact, isSizable){

        var div = this.getDiv();
        var oldCss = isSizable ?  undefined : this.setSizable();

        var bounds = this.getBoundsOf(parent);

        var x=bounds.x;
        var y = bounds.y;
        var w = bounds.width
        var h = bounds.height;
        var pInt = parseInt;
        //rebuilding:

        var padding = {
            top: pd['top'],
            left:pd['left'],
            bottom:pd['bottom'],
            right:pd['right']
        };

        for(var k in padding){
            if(padding[k]<=0){
                padding[k]=0;
            }else if(padding[k]<=1){
                padding[k] = k=='top' || k =='bottom' ? h*padding[k] : w*padding[k];
            }else{
                padding[k] = pInt(padding[k]);
            }
        }

        var maxSize = {
            'width':w-padding['left']-padding['right']+this.shadowOffset,
            'height':h-padding['top']-padding['bottom']+this.shadowOffset
        };

        var vvvv ={
            width:maxSize.width,
            height:maxSize.height
        };
        this._convertSize(div, vvvv);

        if(boundsExact){
            this.setMinSize({
                width:maxSize.width,
                height:maxSize.height
            },isSizable); //a copy cause the argument will be modified
            this.setMaxSize({
                width:maxSize.width,
                height:maxSize.height
            }, isSizable); //a copy cause the argument will be modified

            this.offset({
                'left':x + padding['left'],
                'top': y + padding['top']
            },isSizable);
        }else{
            this.setMaxSize({
                width:maxSize.width,
                height:maxSize.height
            },isSizable); //a copy cause the argument will be modified
            var spanLeft = maxSize.width - div.outerWidth(true);
            var spanTop = maxSize.height - div.outerHeight(true);
            this.offset({
                'left':x + padding['left'] + (spanLeft > 0 ? spanLeft/2 : 0),
                'top': y + padding['top'] +(spanTop > 0 ? spanTop/2 : 0)
            },isSizable);

        }
        //convert to percentage in order to keep same dimensions when zooming


        if(oldCss){
            div.css({
                'display':oldCss['display'],
                'visibility':oldCss['visibility']
            });
        }
    };
    p.getBounds = function(){
        return this.getBoundsOf(this.getDiv());
    };
    //TODO: change argument
    p.getBoundsOf = function(jQueryElement){
        var ret = {
            x:0,
            y:0,
            width:0,
            height:0
        };
        if(!jQueryElement || !(jQueryElement instanceof $)){
            jQueryElement = wdw;
        }
        if(jQueryElement[0] === w_){
            ret.x = jQueryElement.scrollLeft();
            ret.y = jQueryElement.scrollTop();
        }else{
            var offs = jQueryElement.offset();
            ret.x = offs.left;
            ret.y = offs.top;
        }
        ret.width = jQueryElement.width();
        ret.height = jQueryElement.height();
        return ret;
    };

    p.setMaxSize = function(size, isSizable){
        var div = this.getDiv();
        var oldCss = isSizable ?  undefined : this.setSizable();

        this._convertSize(div, size);
        var css = {};
        if('width' in size){
            css.maxWidth = size.width+'px';
        }
        if('height' in size){
            css.maxHeight = size.height+'px';
        }
        if(css){
            div.css(css);
        }
        if(oldCss){
            div.css({
                'display':oldCss['display'],
                'visibility':oldCss['visibility'],
                'top':oldCss['top'],
                'left':oldCss['left']
            });
        }
        return size;
    };
    p.setMinSize = function(size, isSizable){
        var div = this.getDiv();
        var oldCss= isSizable ?  undefined : this.setSizable();

        this._convertSize(div, size);
        var css = {};
        if('width' in size){
            css.minWidth = size.width+'px';
        }
        if('height' in size){
            css.minHeight = size.height+'px';
        }
        if(css){
            div.css(css);
        }
        if(oldCss){
            div.css({
                'display':oldCss['display'],
                'visibility':oldCss['visibility'],
                'top':oldCss['top'],
                'left':oldCss['left']
            });
        }
        return size;
    };
    //div must be display!=hidden. size is a dict with at least one of the fields 'width' and 'height'
    //TODO: check if div is sizable????
    p._convertSize = function(div, size){
        var eD = {
            'width': div.outerWidth(true)-div.width(),
            'height':div.outerHeight(true)-div.height()
        };

        if('width' in size){
            size.width -= (eD.width + this.shadowOffset);
        }
        if('height' in size){
            size.height -= (eD.height + this.shadowOffset);
        }
    };

    p.offset = function(offs, isSizable){
        var div = this.getDiv();
        var oldCss= isSizable?  undefined : this.setSizable();
        //offset does NOT consider margins. Do we have top and left?

        this.getDiv().offset(offs);
        if(oldCss){
            div.css({
                'display':oldCss['display'],
                'visibility':oldCss['visibility'],
                'maxWidth':oldCss['maxWidth'],
                'maxHeight':oldCss['maxHeight'],
                'minWidth':oldCss['minWidth'],
                'minHeight':oldCss['minHeight']
            });
        }
    };

    p.isClosing = false;
    p.close = function(){
        this.isClosing = true;
        this.setFocusCycleRoot(false);
        var div = this.getDiv();
        var shadow = $('#'+this.getShadowDivId());
        shadow.remove();
        var me = this;
        var remove = this.defaultCloseOperation == 'remove';
        div.hide(this.fadeOutTime, function(){

            if(remove){
                div.remove();
            //this is because all bindings will be removed, including blur events
            //we remove this.getFocusAttr() to reupdate focus cycle root when calling show again
            }

            //restore event data on invoker, if any
            var id = '_tmpHandlers'+me.getId();
            if(me[id]){
                var oldHandlers = me[id];
                delete  me[id];
                me.invoker.unbind('click');
                for(var k =0; k< oldHandlers.length; k++){
                    var h = oldHandlers[k];
                    me.invoker.bind(h.type+(h.namespace ? "."+h.namespace : ""),h.handler);
                }
            }

            me.isClosing = false;
            me.trigger('close');
        });

    };


    p.setSizable = function(){
        //if false, just update the flag
        var div = this.getDiv();

        if(!div.parent().length){
            div.appendTo('body');
        }
        var keys = ['display','visibility','left','top','maxWidth','maxHeight','minWidth','minHeight'];
        var css = {};
        for(var i=0; i<keys.length; i++){
            css[keys[i]] = div.css(keys[i]);
        }
        div.offset({
            'left':wdw.scrollLeft(),
            'top':wdw.scrollTop()
        });
        //set the div invisible but displayable to calculate the size (callbackPreShow)
        div.css({
            'visibility':'hidden',
            'maxWidth':'',
            'maxHeight':'',
            'minWidth':'',
            'minHeight':'',
            'height':'',
            'width':''
        }).show();


        return css;
    }
    p.getShadowDivId = function(){
        return this.getId()+"_shadow";
    }

    p.getFocusAttr = function(){
        return this.getId()+"_focus";
    }


})(PopupDiv.prototype);