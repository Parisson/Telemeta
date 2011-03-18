
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
        return str.replace(/\/+$/,"");
    }
    var pageOrigin = normalize(window.location.origin);
    var pageHref = normalize(window.location.href);
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

//function to communicate with the server
//param: the data to be sent or retrieved. Recognized types: 
//  string, boolean number, dictionary of recognized types (including sub-dictionaries) and
//  arrays of recognized types (including sub-arrays). param will be converted to string, escaping quotes newlines
//  and backslashes if necessary.
//method: the json method, eg "telemeta.update_marker"
//onSuccesFcn(data, textStatus, jqXHR)
//   A function to be called if the request succeeds.
//   The function gets passed three arguments:
//      The data returned from the server, formatted according to the dataType parameter;
//      a string describing the status;
//      and the jqXHR (in jQuery 1.4.x, XMLHttpRequest) object
//showAlertError: if true, on error a msg dialog box is shown
var json = function(param,method,onSuccessFcn,showAlertOnError){
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
            if(showAlertOnError){
                var details = "\n(no further info available)";
                if(jqXHR) {
                    details="\nThe server responded witha status of "+jqXHR.status+" ("+
                    jqXHR.statusText+")\n\nDetails (request responseText):\n"+jqXHR.responseText;
                }
                alert("ERROR: Failed to save marker"+details);
            }
        }
    });

};
uniqid = function() {
    var d = new Date();
    return new String(d.getTime() + '' + Math.floor(Math.random() * 1000000)).substr(0, 18);
}
popupDialog = function(invokerElement,divContent,callbackOnOk){
    var $J = jQuery;
    var div = $J("<div/>")
    var divShadow = $J('<div/>')
    //    var topDiv = $J('<div/>')
    //    .append($J('<span/>').html(dialogTitle ? dialogTitle : "&nbsp;"))
    //    .append($J('<a/>').
    //        css({'float':'right','padding':'1ex','backgroundImage':'url("/images/del_marker.png")',
    //    'backgroundRepeat':'no-repeat'})
    //        .attr('href','#').bind('click',function(){div.remove();}));
    
    var okB = $J('<a/>')
    .addClass('mediaitem_button')
    .addClass('mediaitem_button_ok')
    .attr('href',"#")
    .html("Ok")
    .css({
        'float':'right',
        'marginLeft':'0.5ex'
    })
    .bind('click',function(){
        div.remove();
        divShadow.remove();
        if(callbackOnOk){
            callbackOnOk();
        }
        return false;
    })
    var cancelB = okB.clone(true,true)
    .html('Cancel')
    .removeClass('mediaitem_button_ok')
    .addClass('mediaitem_button_cancel')
    .unbind('click').bind('click',function(){
        div.fadeOut('fast', function() {
            div.remove();
            divShadow.remove();
        });
        return false;
    })

    var bottomDiv = $J('<div/>').css({
        'marginTop':'0.5ex'
    }).append(cancelB).append(okB);

    div.append(divContent).append(bottomDiv);
    
    var pos = invokerElement.position();
    var top = (invokerElement.outerHeight(true)+pos.top);
    var left = pos.left;
    div.css({
        padding: '1ex',
        border: '1px solid #DDD',
        display: 'none',
        position: 'absolute',
        left: pos.left + 'px',
        top:top+"px",
        zIndex:1000,
        backgroundColor:'#eee'

    });
    div.insertBefore(invokerElement);
    divShadow.css({
        'backgroundColor':'#000',
        position:'absolute',
        zIndex:900,
        width:div.outerWidth(),
        height:div.outerHeight(),
        left: (left + 5)+'px',
        top:(top+5)+"px"
        });
    div.fadeIn('fast', function() {
        divShadow.insertAfter(div);
        divShadow.fadeTo(0,0.4);
        cancelB.focus();
    });
}