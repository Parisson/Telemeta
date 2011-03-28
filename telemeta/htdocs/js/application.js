
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
Array.prototype.move = function(from, to){
    var pInt = parseInt;
    if(pInt(from)!==from || pInt(to)!==to){
        return from;
    }
    var len = this.length;
    if((from<0 || from>len)||(to<0 || to>len)){
        return from;
    }
    //if we moved left to right, the insertion index is actually
    //newIndex-1, as we must also consider to remove the current index markerIndex, so:
    if(to>from){
        to--;
    }
    if(from != to){
        var elm = this.splice(from,1)[0];
        this.splice(to,0,elm);
        return to;
    }
    return from;
}

function foldInfoBlocks() {
    var $J = jQuery;
    var extra = $J('.extraInfos');
    extra.find('.folded dl, .folded table').css('display', 'none');
    extra.find('a').click(function() { 
        $J(this).parents('.extraInfos').children().toggleClass('folded').find('dl, table').toggle(100);
        return false; 
    });
}


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
            //of the current paqge
            if(linkHref!=pageOrigin && pageHref.match("^"+linkHref+".*")){
                elm.addClass('active');
            }else{
                elm.removeClass('active');
            }
        }
        
    })
}

$(document).ready(function() {
    foldInfoBlocks();
    setSelectedMenu();
});

//****************************************************************************
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
//onSuccesFcn(data, textStatus, jqXHR) OPTIONAL
//   A function to be called if the request succeeds.
//   The function gets passed three arguments:
//      The data returned from the server, formatted according to the dataType parameter;
//      a string describing the status;
//      and the jqXHR (in jQuery 1.4.x, XMLHttpRequest) object
//
//onErrorFcn(jqXHR, textStatus, errorThrown) OPTIONAL. --If missing, default dialog error is shown--
//    A function to be called if the request fails.
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

var popup={
    _cfg_:{
        jQuery:jQuery,
        div: function(){
            var div = this.jQuery('<div/>').css({ //this is _cfg_
                position: 'absolute',
                overflow:'auto', //necessary to properly display the content
                display: 'none',
                zIndex:1000
            });
            if(this.className){
                div.addClass(this.className);
            }
            return div;
        },
        className: 'component',
        divShadow: function(){
            var divShadow =  this.jQuery('<div/>').css({ //this is _cfg_
                position: 'absolute',
                display: 'none',
                overflow:'visible',
                padding: '0 !important', //otherwise setting divShadow dimension is tricky
                backgroundColor:'#000 !important', //shadow must be black
                zIndex:999
            });
            if(this.className){
                divShadow.addClass(this.className);
            }
            return divShadow;
        },
        //        mouseDownNamespace : "mousedown.popup__",
        //        keyDownNamespace : "keydown.popup__",

        //namespace: 'popup__', //used for namespaces when binding click to document
        handlersToRestore: [],
        event: null,
        divsToDelete:null,
        toggleBind: function(element, functionE){
            var clickNamespace = "click.popup__";
            var keydownNamespace =  "keyup.popup__";
            element.unbind(clickNamespace);
            element.unbind(keydownNamespace);
            if(functionE){
                element.bind(clickNamespace, functionE);
                element.bind(keydownNamespace,functionE);
            }
        }
    },
    
    isShowing: function(){
        return this._cfg_.divsToDelete ? true : false;
    },


    hide: function(){
        var toggleBind = this._cfg_.toggleBind;
       
        var $J = this._cfg_.jQuery;

        toggleBind($J(document));
        if(this._cfg_.divsToDelete){
            for(var i=0; i < this._cfg_.divsToDelete.length; i++){
                this._cfg_.divsToDelete[i].empty().remove();
            }
        }
        if(this._cfg_.event && this._cfg_.handlersToRestore){
            var type = this._cfg_.event.type; //which should be the same as h.type below, without namespaces?
            var invokerElement = this._cfg_.event.target;
            if(invokerElement){
                var e = $J(invokerElement);
                toggleBind(e);
                if(type){
                    //e.unbind(type);
                    for(var i=0; i<this._cfg_.handlersToRestore.length; i++){
                        var h = this._cfg_.handlersToRestore[i];
                        var functionCode = h.handler;
                        var namespace = ""+h.namespace;
                        if(namespace.length>0){
                            namespace="."+namespace;
                        }
                        var what = h.type+ namespace;
                        e.bind(what, functionCode);
                    }
                }
            }
        }
        this._cfg_.event=null;
        this._cfg_.handlersToRestore=null;
    },

    show:function(content, optionalEvent){
        //if showing, hide
        if(this.isShowing()){
            this.hide();
        }

        var $J = this._cfg_.jQuery;
        var div = this._cfg_.div();
        //toggleBind sets the functions to hiding/keep shown the popup when clicking or
        //using the keyboard keys
        var toggleBind = this._cfg_.toggleBind;

        //remove the callback on invoker so that clicking on invoker does nothing
        //moreover, toggleBind on invoker so that clicking invoker doesn't hide the popup
        this.oldCallback = undefined;
        var oldHandlers=[];
        var invokerElement = optionalEvent && optionalEvent.target ? $J(optionalEvent.target) : undefined;
        if(invokerElement){
            optionalEvent.stopPropagation(); //othewrwise the popup hides immediately
            //cause the event is catched from the document click (added later, see below)
            // but apparently as soon as we add it it catches even the current event)
            var type = optionalEvent.type;
            var clickEvents =invokerElement.data("events")[type];
            $J.each(clickEvents, function(key, value) {
                oldHandlers.push(value);
            })
            invokerElement.unbind(type); //remove (temporarily) the binding to the event.
            //for instance, if we show the popup by clicking invoker, when the popup is shown do nothing
            //on clicking invoker until popup.hide is called
            toggleBind(invokerElement,function(e){ //add bindings to stop cancel the popup in case the invoker is clicked again
                e.stopPropagation();
                return false;
            });
        }
        //store the functions removed from invoker, if any, to restore them in this.hide
        this._cfg_.handlersToRestore = oldHandlers;
        this._cfg_.event = optionalEvent;
        
        //toggleBind on each child of content so that clicking and pressing keys on
        //a child doesn't hide the popup
        var children = $J(content).find('*');
        $J(children).each(function(){
            toggleBind($(this),function(e){
                e.stopPropagation();
                return false;
            });
        });
        //showing
        var doc = $J(document);
        $J('body').append(div);
        
        content.css('position','static'); //this is really important to place the content in the normal flow
        //within the div. static is the default
        content.show(); //in case the div is display:none
        div.append(content);

        //positioning div: center of the screen if no invoker, below the invoker otherwise
        var wdow = $J(window); //reference the window object (doing it once speeds up a bit performances)
        var windowH = wdow.height();
        var windowW = wdow.width();
        var position = div.offset();
        var shadowOffset=5;
        var size = {
            width:div.outerWidth(true)+shadowOffset,
            height:div.outerHeight(true)+shadowOffset
        };
        if(invokerElement){
            position = invokerElement.offset();
            position.top+=  invokerElement.outerHeight(true);
        }else{
            position.top = (windowH-size.height)/2;
            position.left = (windowW-size.width)/2;
        }
        //position div. This must be done immediately cause here below we want to get the div  offset
        //(div position in absolute - ie, document's - coordinates)
        div.css({
            'top': position.top,
            'left': position.left,
            'right': 'auto', //in case right has been set by some css class rule
            'bottom': 'auto' //see above...
        });
        //set the maximum size
        //due to overflow:auto a scrollbar will automatically appear
        var max = Math.max; //reference max immediately (speeds up performances a bit)
        var maxSize = {
            width: max(20,windowW +  wdow.scrollLeft() -position.left-shadowOffset),
            height: max(20, (windowH + wdow.scrollTop() -position.top- shadowOffset))
        }
        //position div and size:
        var divPadding = {
            left: div.outerWidth()-div.width(),
            top:div.outerHeight()-div.height()
            }; //setting width on a div means the width(),
        //but calculations here are made according to outerWidth(true), so we need this variable (se below)

        div.css({
            'maxWidth': maxSize.width-divPadding.left,
            'maxHeight': maxSize.height-divPadding.top
        });
        //last thing: if invoker element exist, set width at least invoker element width
        if(invokerElement){
            var iEw = invokerElement.outerWidth(); //no margins considered
            if(iEw<maxSize.width && iEw>div.outerWidth()){
                div.css({
                    'minWidth':iEw-divPadding.left
                });
            }
        }
        var divShadow = this._cfg_.divShadow().insertAfter(div);
        //        //position div shadow:
        //        var divShadow = this._cfg_.divShadow().css({
        //            'top': (position.top+shadowOffset),
        //            'left': (position.left+shadowOffset),
        //            'width': div.outerWidth(true),
        //            'height': div.outerHeight(true)
        //        }).insertAfter(div).fadeTo(0,0.4);
        //
        //        //set focus to the first input component, if any. Otherwise try with anchors, otherwise do nothing
        //        var inputs = $J(div).find(':input');
        //        if(inputs && inputs[0]){
        //            inputs[0].focus();
        //        }else{
        //            inputs = $J(div).find('a');
        //            if(inputs && inputs[0]){
        //                inputs[0].focus();
        //            }
        //        }
        //
        //store the divs to be removed
        this._cfg_.divsToDelete = [div,divShadow];
        //add a listener to the document. If one of the content children is clicked/keypressed,
        //we won't come here. Otherwise hide popup
        var me = this;
        var hide = this.hide;
        toggleBind(doc,function(e){
            hide.apply(me);
            e.stopPropagation();
        });
        div.show(300, function(){ //400: basically in between fast (200) and slow (600)
            //position div shadow:
            divShadow.css({
                'top': (position.top+shadowOffset),
                'left': (position.left+shadowOffset),
                'width': div.outerWidth(true),
                'height': div.outerHeight(true)
            }).fadeTo(0,0.4);

            //set focus to the first input component, if any. Otherwise try with anchors, otherwise do nothing
            var inputs = $J(div).find(':input');
            if(inputs && inputs[0]){
                inputs[0].focus();
            }else{
                inputs = $J(div).find('a');
                if(inputs && inputs[0]){
                    inputs[0].focus();
                }
            }
        });
        return false; //to avoid scrolling if we clicked on an anchor
    },

    //field must be a dictionary of label:defaultValues (both strings)
    //callbackOnOk is the callback to be executed on ok, if null ok will simply hide the dialog
    //otherwise it must be a function accepting
    createDivDialog : function(field,callbackOnOk){

        var $J = this._cfg_.jQuery;
        var table = $J('<table/>');
        var fieldElms = {};
        for(var label in field){
            var input = $('<input/>')
            .attr('type','text').val(field[label]).attr("name",label);
            table.append($J('<tr/>')
                .append($J('<td/>').html(label))
                .append($J('<td/>').append(input)));
            fieldElms[label]=input;
        }

        var p = this;
        var onCancel= function(){
            p.hide();
            return false;
        };
       
        var onOk= function(){
            if(callbackOnOk){
                var ret = {};
                var inputs = table.find("input");
                $J.each(inputs, function(key,value){
                    var v = $J(value);
                    ret[v.attr('name')] = v.val();
                });
                callbackOnOk(ret);
                return false;
            }else{
                return onCancel();
            }
        };
        var subdiv = $J('<div/>').css({'padding':'1ex','float':'right'}).
            append(
            $J('<a/>').
            html('Ok').
            addClass('component_icon').
            addClass('button').
            addClass('icon_ok').
            attr('href','#').
            click(function(){
                return onOk();
            })
            );
        if(callbackOnOk){
            subdiv.append(
                $J('<a/>').
                html('Cancel').
                addClass('component_icon').
                addClass('button').
                addClass('icon_cancel').
                attr('href','#').
                click(function(){
                    return onCancel();
                })
                );
        }
        //popupDialog(element,table,onOk);
        return $J('<div/>').append(table).append(subdiv);
    }

}
