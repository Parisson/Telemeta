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
 * Class for showing non-modal dialogs such as popups or combo lists. Requires jQuery. Works in IE7+, FF, Chrome. In IE7 some dimensions
 * do not span the whole optimized width. Probably due to a bug in calculating the size when scrollbars are present. It works however.
 * This class builds an absolutely positioned div for popup forms, message dialogs or listitem popup (emilating the
 * <select> tag element popup). If you're scared about the doc, scroll below to see some examples.
 * Usage:
 * var p = new PopupDiv(dictionary); p.show(); or simply new PopupDiv(dictionary).show();
 * dictionary is an object with the following parameters (In brackets the default value if missing). None of them is mandatory, but
 * at least the property 'content' should be specified, unless showing an empty div is what you want to get)
 * content (""): the popup content. Can be:
 *      1) a dictionnary of key:val pairs (form filling popup). Each pair represents a row in the popup. The row will be a div with
 *          a <span> with innerHTML=key followed by an <input> with value = val. The popup takes care of <span>s and <input>s horizontal alignement so there should be
 *          no need of extra css). The type of <input> is determined as follows:
 *          a) val is boolean: <input type=checkbox>
 *          b) val is an array of strings: <select> tag (non multi select. Yes, it is not an <input> tag in the strict term...)
 *          c) otherwise: <input type=text> with val.toString as value
 *          If showOk is true (see below), a click on the ok anchor will trigger the popup onOk callback (see below) with
 *          argument a dictionary of (key: <input> value) pairs
 *      2) an array of strings for (list item popup). Each array element (string) S will be represented by a row of the popup (internally, an anchor with innerHTML=S). A click on each anchor triggers the onOk callback (see onOk below), with argument an object of the form {selIndex:N},
 where N is the index of the anchor being clicked
 *      3) a jQuery object: the content will be appended to the popup
 *      4) otherwise: content.toString() will be set as the popup innerHTML
 *        In all of these cases, object inserted in the popup via the content property can be retrieved and manipulated via the popup.find method (same syntax as in jQuery)
 * invoker (jQuery(window)): a jQuery object representing an html element. If invoker is:
 *        a clickable element (anchor, input of type button or submit, button), then the PopupDiv will behave as a <select> popuplist of invoker.
 *          Thus, when showing, the PopupDiv will calculate the available space nearby invoker to show up in the window corner next to invoker which best fits its size. In this case the parameter focusable (see below) is usually set to true
 *        Otherwise, the popupdiv will be centered inside invoker. Note that internally each popupdiv is appended to the body element, so it will
 *            be visually centered in invoker, it does not belong to invoker children (well, unless invoker is the jQuery('body') element). In this case the parameters bounds and/or boundsExact (see below) might be also specified
 * bounds ({'top':0.25, 'left':0.25, 'right':0.25, 'bottom':0.25}): if invoker is a clickable element, it is ignored. Otherwise, specifies the
 *      insets (margins) of the popup within invoker (internally, the popup has no margins, so bounds represent the distances from each window
 *      size: top, left, right, bottom). Each bounds element can be in percentage of invoker size if lower than 1 (eg, bounds.left = 0.25: popup left margin is 25% of invoker width, and so on) or as pixel measure (if greater than 1)
 * boundsExact (false): if invoker is a clickable element, it is ignored. Otherwise, specifies whether bounds (see above) should be a hint
 *      (maximum allowed margins) or an exact measure. In other words, with boundsExact the popup will have the size of the rectangle R
 *      determined by invoker size and bounds. Otherwise, the maximum popup size will be R, and if the popup size is included in R, it
 *      will be centered in R. NOTE: padding margin and border, if set via the property popupClass or popupCss (see below) might alter
 *      the real height and width of the rectangle (those properties are ADDED to the natural height/width of the popup)
 * focusable (false): boolean. When true, the popup gains the focus when shown, and disappears when losses the focus
 *      (popup.close() is called, see below)
 * showOk (false): determines whether or not an ok button should be shown at the bottom of the popup. The ok button is an <a> tag whose
 *      click will trigger the popup.onOk callback (see below). This parameter should always be true for form filling popup (see PopupDiv.content above) and when onOk is specified (see below)
 * okButtonTitle ('Ok') [see note4]: self-explanatory
 * onOk (null): callback. callback to be executed when the ok button is pressed. When specified, showOk must be set to true.
 *        The callback takes as argument a dictionary that the popup will build by retrieving all <input> <select> or <textarea>
 *        elements among its children: each element E whith attribute A = popup.getFormDataAttrName() (static popup method), will denote the property
 *        [A:E_value] of the dictionary. Elements with such attributes are automatically created when content (see above) is
 *        an object (form fill popup) or an array (listItem popup), but the user might provide its own custom implementation, for instance:
 *         popup.setContent("<input type='text' "+popup.getFormDataAttrName()+"='default value'/>");popup.showOk=true;
 *        After each onOk callback has been executed, popup.close() will be always called
 * onShow (null): callback to be executed when the popup shows up
 * defaultCloseOperation ('hide'): specified what to do when popup.close() is called. 'remove' calls jQuery.remove() on the popup, ie it removes the html element from the document, 'hide' or any other value simply call jQuery.hide() on the popup
 * onClose (null): callback to be executed when the popup .close() function is called. The callback must take one argument (string) which
 *        denotes wether the popup is closing  because of 1) the ok button click, 2) a lost of focus, 3) the close button click or 4)
 *        another reason (eg, a custom code call to popup.close()). In these cases, the string argument is
 *        1) "okClicked", 2) "focusLost", 3) "closeClicked" and 4) the empty string ""
 * showClose (false): a parameter specifying whether a close button should appear on the top-right corner of the popup. Clicking the close button
 *      (internally, an <a> tag) will close the popup and trigger popup.close() (and associated callbacks bindings, if any)
 * closeButtonTitle ('x') [see note4]: self-explanatory
 * title (""): a parameter specifying whether the popup should have a title. The title will be placed on the top of the popup.
 * shadowOffset (4): the shadow offset, in pixels. Each popup has a 'shadow' which renders a kind of 3d raised effect. Set to 0 if no shadow must be visualized
 * p.okButtonAlign ('right'): self-explanatory. Takes the same argument as css text-align property. The css property text-align is set on the ok button parent div, so if okButtonClass (see below) is specified it might override the button alignement behaviour
 * popupClass ("") [see note1+2]: the popup class(es). The top and bottom divs (housing title/close and ok buttons respectively) are not affected by this parameter
 * popupCss ({}) [see note1+3]: the popup css. The top and bottom divs (housing title/close and ok buttons respectively) are not affected by this parameter
 * okButtonClass ('') [see note1+2+4]: the ok button class
 * closeButtonClass ('') [see note1+2+4]: the close button class
 * titleClass ('') [see note1+2]: the title class
 * listItemClass ('') [see note1+2]: the list items css, valid only if the popup is a listitem popup (see content above):
 *         it applies to each popup row (internally, an <a> tag with display block)
 * listItemCss ('') [see note1+3]: the list items css, valid only if the popup is a listitem popup (see content above):
 *        it applies to each popup row (internally, an <a> tag with display block)
 * fadeInTime ('fast'): the fade in time when popup.show() is called. See jQuery show for possible values (briefly, a number in milliseconds or the string 'fast' or 'slow')
 * fadeOutTime (0): the fade out time when popup.close() is called. See jQuery show for possible values (briefly, a number in milliseconds or the string 'fast' or 'slow')
 * shadowOpacity (0.25): self-explanatory. 1 means shadow completely black, 0 completely transparent (bascially, no shadow)
 * zIndex (10000): the popup zIndex. Should be left untouched unless there are issues with other component with hight zIndex.
 *
 * [note1] IMPORTANT: For every css or class parameter, some css styles might be overridden before showing the popup because they would interfere with the correct placement and
 *      appearence of the popup: surely, 'display', 'position' and 'visibility' are among them. Usually, also 'size' css properties
 *      such as width, height, left, right ectetera. Css and class parameters are useful for customizing the popup 'visually' (eg, colors, font,
 *      backgrounds etcetera)
 * [note2]: class arguments are in the same form of jQuery.addClass() argument (ie, a string which can denote also multiple classes separated by spaces)
 * [note3]: css arguments are in the same form of jQuery.css() argument (ie, an object of cssName:cssValue pairs)
 * [note4]: to customize ok button (closeButton respectively) with css (eg, with an icon), specify a background image in the class AND an height and a width (or padding),
 * otherwise title and icon might overlap or, if okButtonTitle (closeButtonTitle respectively) is the empty string '', the button will be invisible. Note that the anchor has by default
 * display = inline-block, so dimensions can be specified.
 *
 * And finally, EXAMPLES:
 * Given an anchor <a> (jQuery element)
 *      1) show a popup when clicking <a> leaving the user choose among three oprions: 'banana', 'orange' and 'apple'. The popup will
 *      behave as a default popup hiding when it looses focus
 *      //setup parameters
 *      var choices = ['banana','oranges','apples'];
 *      var dict = {
 *          content: choices,
 *          onOk: function(data){
 *              var fruitChosen = choices[data.selIndex];
 *              //.. do something with the selected fruit....
 *          },
 *          focusable: true,
 *          invoker: a,
 *          defaultCloseOperation: ' remove'
 *      }
 *      //bind the click event of the anchor:
 *      a.click(function(){ new PopupDiv(dict).show();});
 *
 *      1) show a popup when clicking <a> leaving the user choose the fruit as text. The popup will close either when ok or close are clicked
 *      //setup parameters
 *      var choices = {'yourFruit':'banana'}; //banana will be the default value when the popup shows
 *      var dict = {
 *          content: choices,
 *          showClose: true,
 *          showOk: true,
 *          onOk: function(data){
 *              var fruitChosen = data['yourFruit'];
 *              //.. do something with the selected fruit....
 *          },
 *          invoker: a
 *      }
 *      //bind the click event of the anchor:
 *      a.click(function(){ new PopupDiv(dict).show();});
 *
 *      3) show a message dialog which expires after 1500 milliseconds. No invoker specified means the popup will be centered in screen
 *      new PopupDiv.show({
 *          content: "i'm gonna disappear!", //one could also input "<span>i'm gonna disappear!</span>" or jQuery('<span/>').html("i'm gonna disappear!")
 *          onShow: function(){
 *              var me = this; //this refers to the popup
 *              setTimeout(function(){
 *                  this.close();
 *              }, 1500);
 *          }
 *      });
 */
function PopupDiv() {
    var $J = jQuery;
    var me = this;
    var data = {};
    if(arguments.length && arguments[0]){
        data= arguments[0];
    }
    //var wdw = $J(window);
    var div  = $J('<div/>');
    //we use an input rather than a span for two reasons:
    //1: span with overflow:hidden have problems in vertical align with the close button in FF and IE
    //2: if text title overlaps, with a span it is not selectable, with an input it is
    //we however append a span to calculate the input width, not really ortodox I know. See setTitle (below)
    var header = $J('<div/>').append($J('<a/>').attr('href','#').click(function(){
        me.close('closeClicked');
        return false;
    })).append(' ').append($J('<div/>').css('clear','both')); //.css('float','right');
    var container = $J('<div/>').css('overflow','auto');
    var footer = $J('<div/>').append($J('<a/>').attr('href','#').click(function(){
        me.trigger('ok');
        return false;
    }));
    //header.find('*').add(footer.find('*')).css('display','none');
    div.append(header).append(container).append(footer);

    //defining immediately the method getDiv (because it is used below)
    this.getDiv = function(){
        return div;
    };
    //setting functions:

    var listeners = {};
    this.getListeners = function(){
        return listeners;
    };


    //setting static properties, if any.
    //The idea is that static PopupDiv properties SPP (eg, PopupDiv.shadowOffset = 5) must define default PopupDiv properties values
    //and they should be added to the current PopupDiv
    //instance prototype ONCE (properties in the prototype are shared between all PopupDiv instances)
    //and then deleted from the PopupDiv function.
    //The problem is how to access the prototype: nor __proto__ neither Object.getPrototypeOf(this) are cross browser
    //(see http://ejohn.org/blog/objectgetprototypeof/, which suggests to rewrite a global Object.getPrototypeOf(arg), which
    //however does not work if arg constructor has been manipulated). Eventually, we do the following:
    //Find a prototype variable P: P= Object.getPrototypeOf: is it NOT a function? then P = this.__proto__. Is it NOT an object?
    //then P= this.
    //Populate P, if P = this, we are assigning SPP to each new instance and NOT ONCE to the prototype object, which of course
    //means that SPP's cannot be deleted after their first assignment. This requires more work and more memory consumption
    //but it assures cross browser compatibility

    var k;
    var staticProps;
    for(k in PopupDiv){
        var f = PopupDiv[k];
        if(PopupDiv.hasOwnProperty(k) && (typeof f !== 'function')){ //do not assign functions (PopupDiv.function... might be used in future as
            //static functions accessible from outside
            if(!staticProps){
                staticProps = {};
            }
            staticProps[k] = f;
        }
    }
    if(staticProps){
        var remove = true;
        var proto = undefined;
        if ( typeof Object.getPrototypeOf !== "function" ) {
            if (typeof this.__proto__ === "object" ) {
                proto = this.__proto__;
            } else {
                // May break if the constructor has been tampered with:
                // proto =  this.constructor.prototype;
                //so we assign static properties to this instance BUT we DO NOT remove static properties
                proto = this;
                remove = false;
            }
        }else{
            proto = Object.getPrototypeOf(this);
        }
        for(k in staticProps){
            if(staticProps.hasOwnProperty(k)){
                proto[k] = staticProps[k];
                if(remove){
                    delete PopupDiv[k];
                }
            }
        }
    }

    //setting instance-specific properties:
    for(k in data){
        if(data.hasOwnProperty(k)){
            if(k === 'onOk' || k === 'onShow' || k === 'onClose'){
                this.bind(k.substring(2).toLowerCase(),data[k]);
            }else if(k == 'content'){
                this.setContent(data[k]);
            }else {
                this[k] = data[k];
            }
        }
    }

    if(!this.popupCss){
        this.popupCss = {}; //workaround to update css the first time we call show
    //note that {} evaluates to true, but jQueryElement.css({}) is harmless
    }


}

//populating the prototype object:
(function(p){
    //in the functions below, this refers to the new Popup instance, not to the prototype

    //private static variables
    var $ = jQuery;
    var w_ = window;
    var d_ = document;
    var wdw = $(w_);
    var popupStaticId = 'popup_'+(new Date().getTime());

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
    p.shadowOffset = 4; //zero means: no shadow
    p.invoker = wdw;
    p.bounds = {
        'top':0.25,
        'left':0.25,
        'right':0.25,
        'bottom':0.25
    }; //note that sepcifying top+bottom>=1 there is undefined behaviour (in chrome, offset is set but height takes all available space)
    p.boundsExact = false;
    p.popupClass = '';
    p.popupCss = {};
    p.showOk = false;
    p.showClose=false;
    p.title = "";
    p.okButtonClass =  '';
    p.okButtonAlign =  'right';
    p.closeButtonClass =  '';
    p.titleClass =  '';
    p.okButtonTitle =  'Ok';
    p.closeButtonTitle =  'x';
    p.defaultCloseOperation = 'hide';
    p.focusable = false;
    p.fadInTime = 'fast';
    p.fadeOutTime = 0;
    p.shadowOpacity = 0.25;
    p.zIndex = 10000;
    p.listItemClass = '';
    p.listItemCss = '';

    //returns the data associated to this popup. Basically, it searches for all input, select or textarea with attribute
    //this.getFormDataAttrName(). The use of a custom attribute is cross browser, note that some attributes, eg name, are
    //not (name is not safe in IE for instance)
    p.getFormData = function(){
        var elms = this.find('input,select,textarea');
        var ret = {};
        var att = this.getFormDataAttrName();
        elms.each(function(i,e){
            var ee = $(e);
            var key = ee.attr(att);
            if(key){
                ret[key] = ee.val();
            }
        });
        return ret;
    };

    //methods:
    p.find = function(argumentAsInJQueryFind){
        return this.getDiv().children().eq(1).find(argumentAsInJQueryFind);
    };

    p.bind = function(eventName, callback){ //eventname: show, close or ok
        var listeners = this.getListeners();
        if(listeners.hasOwnProperty(eventName)){
            listeners[eventName].push(callback);
        }else{
            listeners[eventName] = [callback];
        }
    };


    p.unbind = function(eventName){
        var listeners = this.getListeners();
        if(eventName && listeners.hasOwnProperty(eventName)){
            delete listeners[eventName];
        }else if(!eventName){
            for(var k in listeners){
                if(listeners.hasOwnProperty(k)){
                    delete listeners[k];
                }
            }
        }
    };

    p.trigger = function(eventName){
        var listeners = this.getListeners();
        var me = this;
        if(listeners.hasOwnProperty(eventName)){
            var callbacks = listeners[eventName];
            var i = 0;
            if(eventName == 'ok'){
                var data = this.getFormData();
                for(i=0; i<callbacks.length; i++){
                    callbacks[i].apply(me,[data]);
                }
                this.close('okClicked');
            }else if(eventName == 'close'){
                var str = "";
                if(arguments && arguments.length>1 && typeof arguments[1] === 'string'){
                    str = arguments[1];
                }
                for(i=0; i<callbacks.length; i++){
                    callbacks[i].apply(me,[str]);
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
        var att = this.getFormDataAttrName();
        if(content instanceof $){
            container.append(content);
        }else if(content instanceof Array){

            var me = this;
            //var name = this.getListItemName();
            var input = $('<input/>').attr('type','hidden').attr(att,'selIndex');
            var setEvents = function(idx,anchor,input){
                anchor.click(function(){
                    input.val(idx);
                    me.trigger('ok');
                    return false;
                }).focus(function(){ //focus because we need to get the value if ok is present
                    input.val(idx);
                })
            };
            var listItems = $([]);
            for(var h=0; h<content.length; h++){
                var item = content[h];
                var a = $('<a/>').attr('href','#').html(""+item); //.css('whiteSpace','nowrap');
                listItems = listItems.add(a);
                setEvents(h,a,input);
                container.append(a);
            }
            //set css and class on all listitem anchor:
            //set margin to properly display the outline (border focus)
            //this css can be overridden (see lines below) as it is not strictly necessary
            listItems.css({
                'margin':'2px'
            });
            if(this.listItemClass){
                listItems.addClass(this.listItemClass);
            }
            if(this.listItemCss){
                listItems.css(this.listItemCss);
            }
            //override css which are necessary to properly display the listItem:
            listItems.css({
                'position' : '',
                'display':'block'
            });
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
            };
            var title, component;

            var max = Math.max; //instantiate once
            var lineDiv = undefined;
            var lineDivs = $([]);
            for(var k in content){
                if(content.hasOwnProperty(k)){
                    var val = content[k];
                    if(typeof val == 'string' || typeof val == 'number'){
                        title = $('<span/>').html(k);
                        maxw[0] = max(maxw[0],k.length);
                        maxw[1] = max(maxw[1],val.length);
                        component = $('<input/>').attr('type','text').val(val).attr(att,k);
                        lineDivs = lineDivs.add(insert(title,component));
                    }else if(val === true || val === false){
                        var id = this.getId()+"_checkbox";
                        title = $('<input/>').attr('type','checkbox').attr(att,k).attr('id',id);
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
                        component = $('<select/>').attr('size',1).attr(att,k);
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
            }
            lineDivs.css({
                'white-space': 'nowrap',
                'marginBottom': '0.5ex'
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
                'width':Math.round((3/5)*max(maxw[0], maxw[1]))+'em' //approximate width
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

        //set the element with focus by default if there is no focusable element inside the popup
        var ret = elementsWithFocus.length ? $(elementsWithFocus[0]) : centralDiv;

        if(this.showClose){
            elementsWithFocus =elementsWithFocus.add(topDiv.find('a'));
        }
        if(this.showOk || this.title){
            elementsWithFocus = elementsWithFocus.add(topDiv.find(':text'));
            if(this.showOk){
                elementsWithFocus = elementsWithFocus.add(bottomDiv.find('a'));
            }
        }
        popup.add(centralDiv).css('outline','#FFF none 0px'); //DO NOT SHOW BORDER FOCUS FOR DIVS (NICER). Doesnt work in IE7
        elementsWithFocus = elementsWithFocus.add(popup).add(centralDiv);
        //we add the popup div cause in case of padding clicking on the popup padding should NOT hide the popup
        //we add the centralDiv cause, if scrollbars are present, then moving the scrollbars sets the focus to the
        //centralDiv in IE and therefore the popup would hide

        
        var focusNameSpace = "blur."+this.getId();
        if(!value){
            elementsWithFocus.each(function(i,elm){
                $(elm).unbind(focusNameSpace).removeAttr('tabindex').removeAttr(focusAttr);
            });
            this.getFirstFocusableElement = function(){
                return undefined;
            };
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
                    
                    if((v && $(v).attr(focusAttr)) || me.__isClosing){
                        //if we are closing, we will call back this method which removes the focus attributes, bt meanwhile the
                        //timeout should execute
                        return;
                    }

                    me.close('focusLost');
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

    p.refresh = function(content, title){
        var showing = this.isShowing();
        var focusable = this.focusable;
        if(content!==undefined){
            this.setContent(content);
            if(showing && focusable){
                this.setFocusCycleRoot(this.focusable);
            }
        }
        if(title!=undefined){
            if(showing){
                this.setTitle(title);
            }else{
                this.title = title;
            }
        }
        if(!showing){
            return; //show(), when called, will update size and other stuff written in this method here bwloe
        }
        this.setBounds();
        
        
        if(focusable){
            this.getFirstFocusableElement().focus();
        }
    };

    p.setTitle = function(title){
        var subdiv = this.getDiv().children().eq(0);


        var text = subdiv.contents().filter(function() {
            return this.nodeType == 3;
        });
        
        var node = text.get(0);
        if(!title){
            //if title is the empty string, apparently the text node seems to be "deleted", so resetting
            //the title later has no effect. Setting a white space is not really perfect, as we could have extra space. However,
            //if assures at least a minimum width if the container is empty
            title=' ';
        }
        if (node.textContent) {
            node.textContent = title;
        } else if (node.nodeValue) {
            node.nodeValue = title;
        }
    };

    p.isShowing = function(){
        return this.getDiv().is(':visible');
    };

    p.show = function(){
        var div = this.getDiv();
        var me = this;
        var invoker = this.invoker;
        var isClickElement = this.isClickElement(invoker);
        this._isClickElement = isClickElement;
        this.setBounds = isClickElement ? this._setBoundsAsPopup : this._setBoundsInside;
        this.setOffset = isClickElement ? this._setOffsetAsPopup : this._setOffsetInside;

        if(this.popupClass){
            //this.popupClass might be in the prototype (not set by user)
            div.removeClass().addClass(this.popupClass);
            this.popupClass = ''; //override prototype property
        }
        if(this.popupCss){
            //this.popupCss might be in the prototype (not set by user)
            div.css(this.popupCss);
            this.popupCss = ''; //override prototype property
        }
        

        this.setFocusCycleRoot(this.focusable);

        var subdiv = div.children();
        //configure buttons. Text and classes are added here cause might have been changed
        var topDiv = $(subdiv[0]);
        var closeBtn = topDiv.find('a').eq(0);

        if(this.showClose || this.title){
            topDiv.css({
                'paddingBottom':'0.25em'
            //,'whiteSpace':'nowrap'
            }); //add padding to bottom
            //warning: do NOT use real numbers such as 0.5ex cause browsers round it in a different manner
            //whiteSpace is FUNDAMENTAL in calculating the popup div in case the title is the longest (max width) element
            //in the popup div. We will set the same whitespace css also on the title (see below)

            if(this.titleClass && this.title){
                topDiv.attr('class',this.titleClass);
                this.titleClass='';
            }


            if(this.showClose){
                closeBtn.css('marginLeft','0.5em').attr('class',this.closeButtonClass).html(this.closeButtonTitle).css({
                    'display':'inline-block',
                    'float':'right'
                //warning: do NOT use real numbers such as 0.5ex cause browsers round it in a different manner
                //inline-block in order to retrieve/set width and height on the element
                });
            }else{
                closeBtn.hide(); //margin:0 is to be sure, as afterwards we must span the title the whole popup width
            }
            this.setTitle(this.title);
        }

        var bottomDiv = $(subdiv[2]);
        var okButton = bottomDiv.find('a').eq(0);
        //see note above about why we dont use okButton.is(':visible')
        if(this.showOk){
            bottomDiv.css({
                'paddingTop':'0.25em',
                'textAlign':this.okButtonAlign
            }); //add padding to bottom
            //warning: do NOT use real numbers such as 0.5ex cause browsers round it in a different manner
            okButton.attr('class', this.okButtonClass); //removes all existing classes, if any
            okButton.html(this.okButtonTitle);
            okButton.css({
                'float':'none',
                'display':'inline-block'
            }); //in order to set width and height on the element
        }

        if(!div.parent().length){ //to be done before setsetBounds
            div.appendTo('body');
        }

        
        if(isClickElement){
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
                });
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

        }
        this.setBounds();
       
        var shadow = this._getShadow();
        var place = this.setOffset;
        var postShowFcn = function(){
            //adding window resize interval to track window changes
            var w = wdw.width();
            var h = wdw.height();
            me._resizeTimeInterval = setInterval(function(){
                var w2 = wdw.width();
                var h2 = wdw.height();
                if(w2!==w || h2 !==h){
                    setTimeout(function(){
                        if(!me.isShowing() || me.__isClosing){
                            return;
                        }
                        if(wdw.width()===w2 && wdw.height()===h2){
                            place.apply(me);
                        }
                    },100);
                }
            },200);


            me.trigger('show');
            if(shadow !== undefined){
                shadow.fadeTo(me.fadInTime,me.shadowOpacity, function(){
                    var v = me.getFirstFocusableElement();
                    if(v){
                        v.focus();
                    }
                });
            }else{
                var v = me.getFirstFocusableElement();
                if(v){
                    v.focus();
                }
            }
            
        };

        div.show(this.fadInTime,function(){
            postShowFcn();
        });
    };
    //div must be visible
    p.refreshShadow = function(){
        var shadow = this._getShadow(); //$('#'+this.getShadowDivId());
        var so = this.shadowOffset;
        if(!so && shadow !== undefined){
            shadow.remove();
        //shadow = undefined;
        }else if(so){
            var div = this.getDiv();
            if(shadow === undefined){
                //creating shadow. Remove attributes tabindex (unnecessary) and especially focusAttr,
                //so that clicking tab key and setting the shadow focusable hides the popup. If one wants the shadow not to hide the popup. keep
                //focusAttr BUT insert shadow in the focus cycle root (see method)
                shadow = div.clone(false,false).empty().css({
                    'backgroundColor':'#000',
                    'borderColor':'#000',
                    'display':'block',
                    'zIndex':this.zIndex-1
                }).removeAttr('tabindex').removeAttr(this.getFocusAttr()).fadeTo(0,0).
                attr('id',this.getShadowDivId()).insertAfter(div);
            }
            var rect = this.getBounds.apply(this);
            shadow.css({
                'left':(rect.x + so)+'px',
                'top':(rect.y + so)+'px',
                'width':(rect.width)+'px',
                'height':(rect.height)+'px'
            });
        }
    //return shadow;
    };

    p._getShadow = function(){
        var next = this.getDiv().next('div');
        if(next && next.length && next.attr('id') === this.getShadowDivId()){
            return next;
        }
        return undefined;
    };

    p._setBoundsAsPopup = function(){
        var invoker = this.invoker;

        this.preSizeFcn();

        var div = this.getDiv();

        var shadowOffset = this.shadowOffset;
        var windowRectangle = this.getBoundsOf(wdw); //returns the window rectangle

        var invokerOffset = invoker.offset();

        var invokerOuterHeight = invoker.outerHeight();
        var spaceAbove = invokerOffset.top - windowRectangle.y;
        var spaceBelow = windowRectangle.height - invokerOuterHeight - spaceAbove;
        var placeAbove = spaceAbove > spaceBelow && div.outerHeight(false) + shadowOffset > spaceBelow;

        var invokerOuterWidth = invoker.outerWidth();
        var spaceRight = windowRectangle.x + windowRectangle.width - invokerOffset.left ;
        var spaceLeft = invokerOffset.left + invokerOuterWidth - windowRectangle.x;
        var placeLeft = spaceLeft > spaceRight && div.outerWidth(false) + shadowOffset > spaceRight;

        
        this.setMaxSize({
            height : (placeAbove ? spaceAbove : spaceBelow),
            width: (placeLeft ? spaceLeft : spaceRight)
        }); //width will be ignored (for the moment)
        //decrement of one pixel cause when the popup has to be reduced and the shadows bounds "touch" the window right or bottom sides,
        //the window scrolls (and it shouldn't)

        //setting the minimum size to the invoker width, minheight the same as maxHeight (see above)
        this.setMinSize({
            width: invoker.outerWidth()+this.shadowOffset //workaround to NOT consider the shadow, as offset below substracts the shadow
        //height : spaceAbove>spaceBelow ? spaceAbove : spaceBelow //why this? because if we click the popup a
        //computed height CH seems to be set. At subsequent popup show, CH will be the same UNLESS a new maxHeight lower than CH is set
        //however, we want CH to change even if a new maxHeight greater than CH is set
        });

        
        this.postSizeFcn();

    };
    //places and resize the popupdiv inside parent
    //padding is a dict {top:,left:,bottom:..,right:,...} measuring the distance of the popupdiv from the corners, so that
    //padding={top:0.25,left:0.25,bottom:0.25,right:0.25} will place the popupdiv at the center of parent
    //padding={top:25,left:25,bottom:25,right:25} will place the popupdiv at distances 25 px from parent sides
    //in other words, padding keys lower or euqals to 1 will be conbsidered as percentage, otherwise as absolute measures in px
    p._setBoundsInside = function(){
        var parent = this.invoker;
        var pd = this.bounds;
        var boundsExact = this.boundsExact;

        var div = this.getDiv();
        
        this.preSizeFcn();
        
        var bounds = this.getBoundsOf(parent);
       
        
        var x=bounds.x;
        var y = bounds.y;
        var w = bounds.width;
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
            if(padding.hasOwnProperty(k)){
                if(padding[k]<=0){
                    padding[k]=0;
                }else if(padding[k]<=1){
                    padding[k] = k=='top' || k =='bottom' ? h*padding[k] : w*padding[k];
                }else{
                    padding[k] = pInt(padding[k]);
                }
            }
        }

        var maxSize = {
            'width':w-padding['left']-padding['right']+this.shadowOffset,
            'height':h-padding['top']-padding['bottom']+this.shadowOffset
        };
        
        this.setMaxSize({
            width:maxSize.width,
            height:maxSize.height
        }); //a copy cause the argument will be modified

        if(boundsExact){
            this.setMinSize({
                width:maxSize.width,
                height:maxSize.height
            }); //a copy cause the argument will be modified

        }

        this.postSizeFcn();
    };
    
    p.preSizeFcn = function(){
        var div = this.getDiv();
        var subdivs = div.children();
        subdivs.css('display','none');
        var subdivsshow = subdivs.eq(1);
        if(this.showClose || this.title){
            subdivsshow = subdivsshow.add(subdivs.eq(0));
        }
        if(this.showOk){
            subdivsshow = subdivsshow.add(subdivs.eq(2));
        }

        subdivsshow = subdivsshow.add(div);
        subdivsshow.css({
            'display':'block',
            'float':'',
            'overflow' : 'visible'
        });


        //reset properties:
        subdivsshow.css({
            'maxHeight':'',
            'maxWidth':'',
            'minHeight':'',
            'minWidth':'',
            'height':'',
            'width':'',
            'overflow':'',
            'visibility' : 'visible',
            'float':''
        });
        div.css({
            'margin':'0px',
            'zIndex':this.zIndex,
            'position':'absolute'
        });


        //place the div in the upperleft corner of the window
        var bounds = this.getBoundsOf(); //returns the window rectangle
        div.css({
            'left':bounds.x+'px',
            'top':bounds.y+'px'
        });

    //            var topDiv =subdivs.eq(0);
    //            var centralDiv = subdivs.eq(1);
    //            var bottomDiv = subdivs.eq(2);
    //            console.log('presize');
    //            console.log('width: '+ topDiv.width()+' css-minWidth: ' +topDiv.css('minWidth')+' css-width: ' +topDiv.css('width')+' css-maxWidth: ' +topDiv.css('maxWidth'));
    //            console.log('width: '+centralDiv.width()+' css-minWidth: ' +centralDiv.css('minWidth')+' css-width: ' +centralDiv.css('width')+' css-maxWidth: ' +centralDiv.css('maxWidth'));
    //            console.log('width: '+bottomDiv.width()+' css-minWidth: ' +bottomDiv.css('minWidth')+' css-width: ' +bottomDiv.css('width')+' css-maxWidth: ' +bottomDiv.css('maxWidth'));
    //            console.log(' ' );
    };
    
    p.postSizeFcn = function(){
        
        //set title and close button to span whole width, if necessary
        //closeButton.outerWidth should be zero if this.showClose = false
        //titleInput.outerWidth(true) should be equal to titleInput.width(), as margins borders and padding are zero, however we want to calculate it safely
        var div = this.getDiv();
        var subdivs = div.children();
        var topDiv = subdivs.eq(0);

        var centralDiv = subdivs.eq(1);
        //
        var bottomDiv = subdivs.eq(2);
        //set central div height. We could set the central div height only if necessary, or the central div max height,
        //but this has side effect in IE
       
        var maxHeight = (div.height()-topDiv.outerHeight(true)-bottomDiv.outerHeight(true)-
            (centralDiv.outerHeight(true)-centralDiv.height()));
       
        //setting centralDiv maxHeight or height is actually the same, we use height to be sure...
        if(maxHeight>0){
            centralDiv.css('height',maxHeight+'px');
        }
       
        //to be put AT THE END otherwise bug in IE7
        centralDiv.css('overflow','auto');
        //after the command above, centralDiv.hegith is set to zero in IE7.
        //It might be a refresh problem cause if we display an alert then the size is properly set.
        //However, put it at the end
        

        //                console.log('postsize');
        //                console.log('width: '+ topDiv.width()+' css-minWidth: ' +topDiv.css('minWidth')+' css-width: ' +topDiv.css('width')+' css-maxWidth: ' +topDiv.css('maxWidth'));
        //                console.log('width: '+centralDiv.width()+' css-minWidth: ' +centralDiv.css('minWidth')+' css-width: ' +centralDiv.css('width')+' css-maxWidth: ' +centralDiv.css('maxWidth'));
        //                console.log('width: '+bottomDiv.width()+' css-minWidth: ' +bottomDiv.css('minWidth')+' css-width: ' +bottomDiv.css('width')+' css-maxWidth: ' +bottomDiv.css('maxWidth'));
        //                console.log(' ' );

        
        this.setOffset();

    };

    p._setOffsetAsPopup = function(){
        var div = this.getDiv();

        var shadowOffset = this.shadowOffset;
        var windowRectangle = this.getBoundsOf(wdw); //returns the window rectangle
        var invoker = this.invoker;
        var invokerOffset = invoker.offset();

        var invokerOuterHeight = invoker.outerHeight();
        var spaceAbove = invokerOffset.top - windowRectangle.y;
        var spaceBelow = windowRectangle.height - invokerOuterHeight - spaceAbove;
        var placeAbove = spaceAbove > spaceBelow && div.outerHeight(false) + shadowOffset > spaceBelow;

        var invokerOuterWidth = invoker.outerWidth();
        var spaceRight = windowRectangle.x + windowRectangle.width - invokerOffset.left ;
        var spaceLeft = invokerOffset.left + invokerOuterWidth - windowRectangle.x;
        var placeLeft = spaceLeft > spaceRight && div.outerWidth(false) + shadowOffset > spaceRight;



        //setting the top and left. This must be done at last because popupDiv.outerHeight(true)
        //must have been computed according to the height set above...
        var offs = {
            'left': placeLeft ? invokerOffset.left+ invokerOuterWidth - div.outerWidth(true)-shadowOffset : invokerOffset.left,
            'top': (placeAbove ? invokerOffset.top -  div.outerHeight(true) :
                invokerOffset.top + invokerOuterHeight)
        };
        div.css({
            'top':offs.top+'px',
            'left':offs.left+'px'
        });
        this.refreshShadow(); //repositioning the shadow
    };

    p._setOffsetInside = function(){
       
        var div = this.getDiv();

        
        var parent = this.invoker;
        var bounds = this.getBoundsOf(parent);
        var pd = this.bounds;

        var x=bounds.x;
        var y = bounds.y;
        var w = bounds.width;
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
            if(padding.hasOwnProperty(k)){
                if(padding[k]<=0){
                    padding[k]=0;
                }else if(padding[k]<=1){
                    padding[k] = k=='top' || k =='bottom' ? h*padding[k] : w*padding[k];
                }else{
                    padding[k] = pInt(padding[k]);
                }
            }
        }

        var maxSize = {
            'width':w-padding['left']-padding['right']+this.shadowOffset,
            'height':h-padding['top']-padding['bottom']+this.shadowOffset
        };
        //we add shadowOffset cause in convertSize below we will substract the shadow. However, in this case the shadow is NOT
        //counted in the size

        var ww = div.outerWidth(true);
        var hh = div.outerHeight(true);

        var spanLeft = 0;
        var spanTop = 0;
        if(ww<maxSize.width){
            spanLeft = (maxSize.width-ww)/2;
        }
        if(hh < maxSize.height){
            spanTop = (maxSize.height-hh)/2;
        }

        div.css({
            'left':(x+padding['left']+spanLeft)+'px',
            'top':(y+padding['top']+spanTop)+'px'
        });

        this.refreshShadow(); //repositioning the shadow
    };

    p.getBounds = function(){
        return this.getBoundsOf(this.getDiv());
    };

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
    //getDiv must be sizable (preShowFcn must have been called)
    p.setMaxSize = function(size){
        var div = this.getDiv();
        
        this._convertSize(div, size);
        var css;
        if(size.hasOwnProperty('width')){
            if(!css){
                css = {};
            }
            css.maxWidth = size.width+'px';
        }
        if(size.hasOwnProperty('height')){
            if(!css){
                css = {};
            }
            css.maxHeight = size.height+'px';
        }
        if(css){
            div.css(css);
        }
        return size;
    };
    //getDiv must be sizable (preShowFcn must have been called)
    p.setMinSize = function(size){
        var div = this.getDiv();
        
        this._convertSize(div, size);
        var css;
        if(size.hasOwnProperty('width')){
            if(!css){
                css = {};
            }
            css.minWidth = size.width+'px';
        }
        if(size.hasOwnProperty('height')){
            if(!css){
                css = {};
            }
            css.minHeight = size.height+'px';
        }
        if(css){
            div.css(css);
        }
        return size;
    };
    //div must be display!=hidden. size is a dict with at least one of the fields 'width' and 'height'
    p._convertSize = function(div, size){
        var eD = {
            'width': div.outerWidth(true)-div.width(),
            'height':div.outerHeight(true)-div.height()
        };

        if(size.hasOwnProperty('width')){
            size.width -= (eD.width + this.shadowOffset);
        }
        if(size.hasOwnProperty('height')){
            size.height -= (eD.height + this.shadowOffset);
        }
    };

    p.offset = function(offs){
        var div = this.getDiv();
        div.offset(offs);
    };

    p.close = function(){
        this.__isClosing = true;
        if(this._resizeTimeInterval!==undefined){
            clearInterval(this._resizeTimeInterval);
            this._resizeTimeInterval = undefined;
        }
        this.setFocusCycleRoot(false);
        var div = this.getDiv();
        var shadow = this._getShadow(); //$('#'+this.getShadowDivId());
        if(shadow !== undefined){
            shadow.remove();
        }
        var me = this;
        var remove = this.defaultCloseOperation == 'remove';
        div.hide(this.fadeOutTime, function(){

            if(remove){
                div.remove();
            }

            //restore event data on invoker, if any
            var id = '_tmpHandlers'+me.getId();
            if(me[id]){
                var oldHandlers = me[id];
                delete me[id];
                me.invoker.unbind('click');
                for(var k =0; k< oldHandlers.length; k++){
                    var h = oldHandlers[k];
                    me.invoker.bind(h.type+(h.namespace ? "."+h.namespace : ""),h.handler);
                }
            }

            delete me['__isClosing'];
            if(arguments && arguments.length>0 && typeof arguments[0] === 'string'){
                me.trigger('close',arguments[0]);
            }else{
                me.trigger('close');
            }
        });

    };

    //sets a t=timeout and returns t. eventName can be 'show' or 'close'
    p.setTimeout = function(eventName, millseconds){
        var me = this;
        var t=undefined;
        if(eventName === 'show'){
            t=setTimeout(function(){
                me.show();
            },millseconds);
        }else if(eventName === 'close'){
            t=setTimeout(function(){
                me.close();
            },millseconds);
        }
        return t;
    };

    p.getShadowDivId = function(){
        return this.getId()+"_shadow";
    };

    p.getFocusAttr = function(){
        return this.getId()+"_focus";
    };

    p.getFormDataAttrName = function(){
        return this.getId()+"_data";
    };

})(PopupDiv.prototype);