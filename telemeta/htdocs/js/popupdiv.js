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
 * class for showing non-modal dialogs such as popups or combo lists. Requires jQuery. If you're scared about the doc, scroll below to
 * see some examples.
 * This class builds an absolutely positioned div for popup forms, message dialogs or listitem popup (emilating the
 * <select> tag element popup).
 * Usage:
 * var p = new PopupDiv(dictionary); p.show(); or simply new PopupDiv(dictionary).show();
 * dictionary is an object with the following parameters (In brackets the default value if missing). None of them is mandatory, but
 * at least content should be specified (unless showing an empty div is what you want to get)
 * content (""): the popup content. Can be:
 *      a dictionnary of (key: val) pairs for form filling popup. Each pair represents a row in the popupm built as a div with
 *          a string (key) followed by an input with value = val (the popup takes care of inputs horizontal alignement so there should be
 *          no need of extra css).
 *          The input is determined as follows:
 *          val is boolean: checkbox input
 *          val is an array of strings: select tag (non multi select)
 *          otherwise: text input (with val.toString as value)
 *          If showOk is true (see below), a click on the ok anchor will trigger the popup onOk callback (see below) with
 *          argument a dictionary of (key: val) pairs, where each val is the relative input value
 *      an array of strings for listItem popup. Each array element represents a line of the popup (internally, an anchor with
 *          inner html the array element value). A click on each anchor triggers the onOk callback (see onOk below)
 *      a jQuery object: the content will be appended to the popup
 *      otherwise: content.toString() will be set as the popup innerHTML
 * invoker (jQuery(window)): a jQuery object representing an html element. If invoker is a clickable element (anchor, input of type button or submit,
 *      button), then the PopupDiv bounds will be placed according to invoker as if it was a popup list of a select tag. Otherwise, the popupdiv will be centered inside invoker. Note that
 *      internally each popupdiv is appended to the body element, so it will be visually centered in invoker, it should not belong
 *      to invoker children
 * bounds ({'top':0.25, 'left':0.25, 'right':0.25, 'bottom':0.25}): if invoker is a clickable element, it is ignored. Otherwise, specifies the
 *      insets (margins) of the popup within invoker (internally, the popup has no margins, so bounds represents the distances from each window
 *      size). Each bounds element can be in percentage of invoker size if lower than 1 (eg, bounds first element is 0.25: popup left margin is
 *      25% of invoker height, and so on) or as pixel measure (if greater than 1)
 * boundsExact (false): if invoker is a clickable element, it is ignored. Otherwise, specifies whether bounds (see above) should be a hint
 *      (maximum allowed margins) or an exact measure. In other words, with boundsExact the popup will have the size of the rectangle R
 *      determined by invoker size and bounds. Otherwise, the maximum popup size will be R, and if the popup size is included in R, it
 *      will be centered in R.
 * focusable (false): boolean. When true, the popup gains the focus when shown, and disappears when losses the focus
 *      (popup.close() is called, see below)
 * showOk (false): determines whether or not an ok button should be shown at the bottom of the popup. The ok button is an anchor whose
 *      click will trigger the popup.onOk callback. This parameter should always be true for form filling popup (see content)
 * onOk (null): callback. callback to be executed when the ok button is pressed. The callback takes as argument a dictionary of the popup data.
 *      which is not empty only if the popup was built as form filling or listitem popup (see content above). In this last two cases,
 *      the data returned is a dictionnary of [key:value] pairs (form filling popup) or a dictionary with one key (selIndex) and the
 *      selected index that was clicked. This parameter should be specified for form filling popup (see content). popup.close() is always called
 *      after onOk callback is executed, but without triggering the onClose callback, if any (see below)
 * onShow (function): callback to be executed when the popup shows up
 * defaultCloseOperation ('hide'): specified what to do when popup.close() is called. 'remove' removes the html element from the document,
 *      'hide' or any other value simply call jQuery.hide() on the popup
 * onClose (null): callback to be executed when the popup .close() function is called. It includes the case when focusable=true and
 *      the popup looses the focus BUT NOT when the ok button (if any) is pressed (see onOk above)
 * shadowOffset (4): the shadow offset. Each popup has a 'shadow' which renders a kind of 3d raised effect. Set to 0 if no shadow must be visualized
 * popupClass ("") [see note1]: the popup class, if any, in the same form as jQuery.addClass() argument (ie, it can include multiple classes separated by space).
 *      The top and bottom divs (housing title and close anchor and ok button respectively) are not affected by this parameter
 * popupCss ({}) [see note1]: the popup css, if any, in the same form as jQuery.css() argument.
 *      The top and bottom divs (housing title and close anchor and ok button respectively) are not affected by this parameter
 * showClose (false): a parameter specifying whether a close button should appear on the top-right corner of the popup. Clicking the close button
 *      (internally, an anchor) will close the popup and trigger popup.close() (and associated callbacks bindings, if any)
 * title (""): a parameter specifying whether the popup should have a title. The title will be placed on the top of the popup.
 * okButtonClass ('') [see note1]: the ok button (anchor) class, if showOk = true, in the same form as jQuery.addClass() argument (ie, it can include multiple classes separated by space).
 * okButtonTitle ('Ok'): self-explicatory
 * p.okButtonAlign ('right'): self explicatory. Takes the same argument as css text-align property
 * closeButtonClass ('') [see note1]: the close button (anchor) class, if showClose = true, in the same form as jQuery.addClass() argument (ie, it can include multiple classes separated by space).
 * closeButtonTitle ('x'): self- explicatory
 * titleClass ('') [see note1]: the title (inpuit of type text) class, if title is not empty, in the same form as jQuery.addClass() argument (ie, it can include multiple classes separated by space).
 * fadeInTime ('fast'): the fade in time when popup.show() is called. See jQuery show for possible values (briefly, a number in milliseconds or the string 'fast' or 'slow')
 * fadeOutTime (0): the fade out time when popup.close() is called. See jQuery show for possible values (briefly, a number in milliseconds or the string 'fast' or 'slow')
 * shadowOpacity (0.25): elf-explicatory. 1 means shadow completely black, 0 completely transparent (bascially, no shadow)
 * zIndex (10000): the popup zIndex. Should be left untouched unless there are issues with other component with hight zIndex.
 * listItemClass ('') [see note1]: the list items css, valid only if the popup is a listitem popup (see content above),
 *      in the same form as jQuery.addClass() argument (that is, can take multiple classes separated by space).
 * listItemCss ('') [see note1]: the list items css, valid only if the popup is a listitem popup (see content above),
 *      in the same form as jQuery.addClass() argument (ie, a dictionary of key:value pairs).
 *
 * [note1] IMPORTANT: For every css or class parameter, some css styles might be overridden before showing the popup because they would interfere with the correct placement and
 *      appearence of the popup: surely, 'display', 'position' and 'visibility' are among them. Usually, also 'size' css properties
 *      such as width, height, left, right ectetera. Css and class parameters are useful for customizing the popup 'visually' (eg, colors, font,
 *      backgrounds etcetera)
 *
 * EXAMPLES: given an anchor <a> (jQuery element)
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
function PopupDiv(){
    var $J = jQuery;
    var me = this;
    var data = arguments.length && arguments[0] || {};

    //var wdw = $J(window);
    var div  = $J('<div/>');
    //we use an input rather than a span for two reasons:
    //1: span with overflow:hidden have problems in vertical align with the close button in FF and IE
    //2: if text title overlaps, with a span it is not selectable, with an input it is
    var header = $J('<div/>').append($J('<input/>')).append($J('<a/>').attr('href','#').click(function(){
        me.close();
        return false;
    })); //.css('float','right');
    var container = $J('<div/>').css('overflow','auto');
    var footer = $J('<div/>').append($J('<a/>').attr('href','#').click(function(){
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

    
    //setting static properties, if any.
    //The idea is that static PopupDiv properties SPP (eg, PopupDiv.shadowOffset = 5) should be added to the current PopupDiv
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
    var staticProps = undefined;
    for(k in PopupDiv){
        if(!staticProps){
            staticProps = {};
        }
        var f = PopupDiv[k];
        if(typeof f !== 'function'){ //do not assign functions (PopupDiv.function... might be used in future as
            //static functions accessible from outside
            staticProps[k] = f;
        }
    }
    if(staticProps){
        var remove = true;
        var proto = undefined;
        if ( typeof Object.getPrototypeOf !== "function" ) {
            if ( typeof this.__proto__ === "object" ) {
                proto = this.__proto__;
            } else {
                // May break if the constructor has been tampered with:
                // proto =  this.constructor.prototype;
                //so we assign tis class BUT we DO NOT remove static properties
                proto = this;
                remove = false;
            }
        }else{
            proto = Object.getPrototypeOf(this);
        }
        for(k in staticProps){
            proto[k] = staticProps[k];
            if(remove){
                delete PopupDiv[k];
            }
        }
    }

    //setting instance-specific properties:
    for(k in data){
        if(k == 'onOk' || k == 'onShow' || k == 'onClose'){
            this.bind(k.substring(2).toLowerCase(),data[k]);
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

//populating the prototype object:
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
    p.fadInTime = 'fast',
    p.fadeOutTime = 0,
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
                    me.trigger('ok',true);
                    return false;
                }).focus(function(){ //focus because we need to get the value if ok is present
                    input.val(idx);
                })
            };
            var listItems = $([]);
            for(var h=0; h<content.length; h++){
                var item = content[h];
                var a = $('<a/>').attr('href','#').html(""+item);
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
                'width':Math.round((3/5)*max(maxw[0], maxw[1]))+'em'
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
        if(this.showClose){
            elementsWithFocus =elementsWithFocus.add(topDiv.find('a'));
        }
        if(this.showOk || this.title){
            elementsWithFocus = elementsWithFocus.add(topDiv.find(':text'));
            if(this.showOk){
                elementsWithFocus = elementsWithFocus.add(bottomDiv.find('a'));
            }
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
                    //console.log(v);
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
            //this.popupClass might be in the prototype (not set by user)
            div.removeClass().addClass(this.popupClass);
            this.popupClass = ''; //override prototype property
        }
        if(this.popupCss){
            //this.popupCss might be in the prototype (not set by user)
            div.css(this.popupCss);
            this.popupCss = ''; //override prototype property
        }
        //css modified, restore properties we need not to change:
        //cssModified should be true ALL first times we call show, as this.popupCss = {} )ie, it evaluates to TRUE)
        if(cssModified){
            div.css({
                'position':'absolute',
                'zIndex':this.zIndex,
                'margin':'0px',
                'overflow':'hidden'
            });
        }

        this.setFocusCycleRoot(this.focusable);

        var subdiv = div.children();
        //configure buttons. Text and classes are added here cause might have been changed
        var topDiv = $(subdiv[0]);
        var titleInput = topDiv.find(':text').eq(0); //$(':text') is equivalent to $('[type=text]') (selects all <input type="text"> elements)
        var closeBtn = topDiv.find('a').eq(0);
        if(!this.showClose && !this.title){
            topDiv.hide();
        }else{
            topDiv.css({
                'paddingBottom':'1em',
                'whiteSpace': 'nowrap'
            }).show(); //add padding to bottom
            //warning: do NOT use real numbers such as 0.5ex cause browsers round it in a different manner
            //whiteSpace is FUNDAMENTAL in calculating the popup div in case the title is the longest (max width) element
            //in the popup div. We will set the same whitespace css also on the title (see below)

            if(this.showClose){
                closeBtn.attr('class',this.closeButtonClass); //removes all existing classes, if any (see jQuery removeClass doc)
                closeBtn.html(this.closeButtonTitle);
                closeBtn.css({
                    'display':'inline-block',
                    'visibility':'visible',
                    'marginLeft':'1em'
                //warning: do NOT use real numbers such as 0.5ex cause browsers round it in a different manner
                //inline-block in order to retrieve/set width and height on the element
                });
            }else{
                closeBtn.css({
                    'margin':'0px'
                }).hide(); //margin:0 is to be sure, as afterwards we must span the title the whole popup width
            }
            //in any case, show titleElement cause even if title="", titleElement is used to position close on the right
            titleInput.val(this.title).attr('readonly','readonly').attr('class',this.titleClass).removeClass().css({
                'display':'inline-block',
                'backgroundColor':'transparent',
                'padding': '0px',
                'margin':'0px',
                'border':'0px',
                'visibility': this.title ? 'visible' : 'hidden',
                'width':'',
                'maxWidth':'1px'	//it is too tricky to set the width of the input spanning the whole title (in case of long titles)
            //we might use a span, but we experienced problems in vertical align with the close button, as stated somewhere above.
            //Moreover, a long title messes up the calculations in popup mode:
            //a long title most likely determines the popup size, the latter the popup position, and once
            //positioned and sized the popup size determines the title width (in order to span the title or letting the close button be visible)
            //This is not robust at all and in fact it does not render the same popup position in all browsers.
            //So, finally, set the input to the minimum allowed width, This means that maxWidth and maxHeight
            //will be calculated based on the centraldiv dimensions, which is anyway the core div we want to properly visualize.
            //Moreover, this way title resizing does not interfeere with the position
            });
        }

        var bottomDiv = $(subdiv[2]);
        var okButton = bottomDiv.find('a').eq(0);
        //see note above about why we dont use okButton.is(':visible')
        if(this.showOk){
            bottomDiv.css({
                'paddingTop':'1em',
                'textAlign':this.okButtonAlign
            }).show(); //add padding to bottom
            //warning: do NOT use real numbers such as 0.5ex cause browsers round it in a different manner
            okButton.attr('class', this.okButtonClass); //removes all existing classes, if any
            okButton.html(this.okButtonTitle);
            okButton.css({
                'display':'inline-block',
                'visibility':'visible'
            }); //in order to set width and height on the element
        }else{
            bottomDiv.hide();
        }

        var centralDiv = $(subdiv[1]);
        //reset properties of the central div
        centralDiv.css({
            'overflow':'auto',
            'maxHeight':'',
            'maxWidth':'',
            'minHeight':'',
            'minWidth':'',
            'height':'',
            'width':'',
            'visibility':'visible'
        }).show();

        this.setSizable();//this means the popupdiv is display: !none and visibility:hidden, so every element
        //inside it should be visible and therefore sizable. Being visible means that jQuery.is(':visible') returns true
        //start with showing top and bottom if some elements are visible

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
            this.setBoundsInside(invoker, this.bounds, this.boundsExact, true);
        }

        //set title and close button to span whole width, if necessary
        //closeButton.outerWidth should be zero if this.showClose = false
        //titleInput.outerWidth(true) should be equal to titleInput.width(), as margins borders and padding are zero, however we want to calculate it safely
        if(this.showClose || this.title){
            var titleW = topDiv.width() - closeBtn.outerWidth(true) - (titleInput.outerWidth(true)-titleInput.width());
            titleInput.css({
                'maxWidth':'',
                'width':(titleW)+'px'
            });
        }

        //set central div max height ONLY IF NECESSARY (overflow). Until here, the main popup is sized and placed
        //but the central div might overflow
        var height = centralDiv.height();
        var maxHeight = (div.height()-topDiv.outerHeight(true)-bottomDiv.outerHeight(true)-
            (centralDiv.outerHeight(true)-centralDiv.height()));
        if(maxHeight<height){
            centralDiv.css('maxHeight',maxHeight+'px');
        }
        //same for width:
        var maxWidth = div.width();
        var width = centralDiv.outerWidth(true);
        if(maxWidth<width){
            centralDiv.css('maxWidth',maxWidth+'px');
        }

        // var height = centralDiv.height();
        // if(sizeAsPopup && maxHeight<height){
        // centralDiv.css('maxHeight',maxHeight+'px');
        // }else{
        // centralDiv.css({
        // 'maxHeight': maxHeight+'px',
        // 'minHeight': maxHeight+'px'
        // });
        // }
        // //set central div max width ONLY IF NECESSARY:
        // var maxWidth = div.width();
        // var width = $(subdiv[1]).outerWidth(true);
        // if(sizeAsPopup && maxWidth<width){
        // centralDiv.css('maxWidth',maxWidth+'px');
        // }else{
        // centralDiv.css({
        // 'maxWidth': maxWidth+'px',
        // 'minWidth':maxWidth+'px'
        // });
        // }



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
            'left': placeLeft ? invokerOffset.left+ invokerOuterWidth - div.outerWidth(true)-shadowOffset : invokerOffset.left,
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

    p.getFormDataAttrName = function(){
        return this.getId()+"_data";
    }

})(PopupDiv.prototype);
