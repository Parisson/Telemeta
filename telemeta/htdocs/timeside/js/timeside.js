/*
 * Copyright (C) 2007-2011 Parisson
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
 * Base class defining classes for TimesideUI
 */

/* Simple JavaScript Inheritance
 * By John Resig http://ejohn.org/
 * MIT Licensed.
 * (Inspired by base2 and Prototype)
 */
 
/*
 * In few words: the lightest and most-comprehensive way to implement inhertance and OOP in javascript. Usages can be found below.
 * Basically,
 * 1) a new Class is instantiated with Class.extend(). This function takes a dictionary
 * of properties/methods which will be put IN THE PROTOTYPE of the class, so that each instance will share the same properties/methods
 * and the latter don't have to be created for each instance separately.
 * 2) If var A = Class.extend({...}) and var B = A.extend({..}), then methods which are found in B will override the same methods in A.
 * In this case, the variable this._super inside the overridden methods will refers to the super-method and can thus be called safely.
 * Consequently, if a _super property/method is implemented in the extend dictionary, it WILL NOT be accessible
 * to the overriding methods of B. Basically, don't use _super as a key of the argument of extend.
 * 3) AFTER the prototype has been populated, the init function, if exists, is called. The latter can be seen as a class constructor in java,
 * with a substantial difference: when executing the init() method the class prototype has already been populated with all inherited methods.
 * Private variable can be declared in the init function, as well as
 * relative getters and setters, if needed. Downside is that the privileged getters and setters can’t be put in the prototype,
 * i.e. they are created for each instance separately, and the _super keyword does not apply to them. Another issue is the overhead of closures in general (basically, write as less as possible
 * in the init function, in particular if the class has to be declared several times)
 * Of course, the this._super keyword of methods implemented in the init constructor does not work
 *
 * EXAMPLE:
 * var MyClass = Class.extend({
 *   init: function(optionalArray){ //constructor
 *       this._super();             //!!!ERROR: Class is the base class and does not have a super construcor
 *       var me = [];               //private variable
 *       this.count = 6;            //set the value of the public property defined below
 *       this.getMe = function(){   //public method
 *           this._super();         //!!!ERROR: methods defined in the init function don't have acces to _super
 *       }
 *       this.alert = function(){   //another public method, !!!WARNING: this will be put in the MyClass scope (NOT in the prototype)
 *           alert('ok');           
 *       }
 *   },
 *   count:0,                       //public property
 *   alert: function(){             //public method. !!!WARNING: this method will be put in the prototype BEFORE the init is called,
 *      alert('no');                //  so the alert defined above will be actually called
 *   }
 * });
 * var MyClass2 = MyClass.extend({
 *  init: function(){
 *      this._super();                  //call the super constructor
 *  }
 *  alert: function(){                  //override a method
 *      this._super();                  //call the super method, ie alerts 'no'. WARNING: However, as long as there is an alert written 
 *                                      //in the init method of the superclass (see above), THAT method will be called
 *  }
 * });
 *
 */
// 
(function(){

    var initializing = false, fnTest = /xyz/.test(function(){
        xyz;
    }) ? /\b_super\b/ : /.*/;

    /*The xyz test above determines whether the browser can inspect the textual body of a function.
     *If it can, you can perform an optimization by only wrapping an overridden method if it
     *actually calls this._super() somewhere in its body.
     *Since it requires an additional closure and function call overhead to support _super,
     *it’s nice to skip that step if it isn’t needed.
     */

    // The base Class implementation (does nothing)
    this.Class = function(){};

    // Create a new Class that inherits from this class
    Class.extend = function(prop) {
        var _super = this.prototype;

        // Instantiate a base class (but only create the instance,
        // don't run the init constructor)
        initializing = true;
        var prototype = new this();
        initializing = false;

        // Copy the properties over onto the new prototype
        for (var name in prop) {
            // Check if we're overwriting an existing function
            prototype[name] = typeof prop[name] == "function" &&
            typeof _super[name] == "function" && fnTest.test(prop[name]) ?
            (function(name, fn){
                return function() {
                    var tmp = this._super;

                    // Add a new ._super() method that is the same method
                    // but on the super-class
                    this._super = _super[name];

                    // The method only need to be bound temporarily, so we
                    // remove it when we're done executing
                    var ret = fn.apply(this, arguments);
                    this._super = tmp;

                    return ret;
                };
            })(name, prop[name]) :
            prop[name];
        }

        // The dummy class constructor
        function Class() {
            // All construction is actually done in the init method
            if ( !initializing && this.init ){
                this.init.apply(this, arguments);
            }
        }

        // Populate our constructed prototype object
        Class.prototype = prototype;
        
        // Enforce the constructor to be what we expect
        Class.constructor = Class;

        // And make this class extendable
        Class.extend = arguments.callee;

        return Class;
    };
})();

//Defining the base TimeClass class. Player, Ruler, MarkerMap are typical implementations (see js files)
//Basically we store here static methods which must be accessible in several timside sub-classes
var TimesideClass = Class.extend({
    //init constructor. Define the 'bind' and 'fire' (TODO: rename as 'trigger'?) methods
    //we do it in the init function so that we can set a private variable storing all
    //listeners. This means we have to re-write all methods
    init: function(){
        //the map for listeners. Must be declared in the init as it's private and NOT shared by all instances
        //(ie, every instance has its own copy)
        this.listenersMap={};
    },

    /**
     * 3 methods defining listeners, events fire and bind (aloing the lines of jQuery.bind, unbind and trigger):
     */
    bind : function(key, callback, optionalThisArgInCallback){
        if(!(callback && callback instanceof Function)){
            this.debug('cannot bind '+key+' to callback: the latter is null or not a function');
            return;
        }
        var listenersMap = this.listenersMap;
        var keyAlreadyRegistered = (key in listenersMap);
        if(!keyAlreadyRegistered){
            listenersMap[key] = [];
        }
        listenersMap[key].push({
            callback:callback,
            optionalThisArgInCallback:optionalThisArgInCallback
        });
    },
    unbind : function(){
        var listenersMap = this.listenersMap;
        if(arguments.length>0){
            var key = arguments[0];
            if(key in listenersMap){
                delete listenersMap[key];
            }
        }else{
            for(key in listenersMap){
                delete listenersMap[key];
            }
        }
    },
    fire : function(key, dataArgument){
        var listenersMap = this.listenersMap;
        if(!(key in listenersMap)){
            this.debug('"'+key+'" fired but no binding associated to it');
            return;
        }
        var callbacks = listenersMap[key];
        var len = callbacks && callbacks.length ? callbacks.length : 0;
        for(var i=0; i<len; i++){
            var obj = callbacks[i];
            if('optionalThisArgInCallback' in obj){
                obj.callback.apply(obj.optionalThisArgInCallback, [dataArgument]);
            }else{
                obj.callback(dataArgument);
            }
        }
    },
    /**
     * function to calculate the text width according to a text and a given fontsize
     */
    textWidth : function(text, fontSize) {
        var ratio = 3/5;
        return text.length * ratio * fontSize;
    },
    
    /*
     *formats (ie returns a string representation of) a time which is in the form seconds,milliseconds (eg 07.6750067)
     * formatArray is an array of strings which can be:
     * 'h' hours. Use 'hh' for a zero-padding to 10 (so that 6 hours is rendered as '06')
     * 'm' hours. Use 'mm' for a zero-padding to 10 (so that 6 minutes is rendered as '06')
     * 's' hours. Use 'ss' foar a zero-padding to 10 (so that 6 seconds is rendered as '06')
     * 'D' deciseconds
     * 'C' centiseconds (it will be padded to 10, so that 5 centiseconds will be rendered as '05')
     * 'S' milliseconds (it will be padded to 100, so that 5 milliseconds will be rendered as '005')
     * If formatArray is null or undefined or zero-length, it defaults to ['mm','ss']
     * 'h','m' and 's' will be prepended the separator ':'. For the others, the prepended separator is '.'
     * Examples:
     * makeTimeLabel(607,087)               returns '10:07' (formatArray defaults to ['mm','ss'])
     * makeTimeLabel(607,087,['m':'s'])     returns '10:7'
     * makeTimeLabel(607,087,['m':'s','C']) returns '10:7.09'
     */
    makeTimeLabel: function(time, formatArray){
        if(!(formatArray)){
            formatArray = ['mm','ss'];
        }
        //marker offset is in float format second.decimalPart
        var pInt = parseInt;
        var round = Math.round;
        var factor = 3600;
        var hours = pInt(time/factor);
        time-=hours*factor;
        factor = 60;
        var minutes = pInt(time/factor);
        time-=minutes*factor;
        var seconds = pInt(time);
        time-=seconds;
        
        //here below the function to format a number
        //ceilAsPowerOfTen is the ceil specifiedas integer indicating the relative power of ten
        //(0: return the number as it is, 1: format as "0#" and so on)
        //Examples: format(6) = "6", format(6,1)= "06", format(23,1)= "23"

        //first of all, instantiate the power function once (and not inside the function or function's loop):
        //note that minimumNumberOfDigits lower to 2 returns integer as it is
        var mpow = Math.pow; //instantiate mpow once
        var format = function(integer,minimumNumberOfDigits){
            var n = ""+integer;
            var zero = "0"; //instantiating once increases performances???
            for(var i=1; i< minimumNumberOfDigits; i++){
                if(integer<mpow(10,i)){
                    n = zero+n;
                }
            }
            return n;
        }
        var ret = [];
        for(var i =0; i<formatArray.length; i++){
            var f = formatArray[i];
            var separator = ":";
            if(f=='h'){
                ret[i]=hours;
            }else if(f=='hh'){
                ret[i]=format(hours,2);
            }else if(f=='m'){
                ret[i]=minutes;
            }else if(f=='mm'){
                ret[i]=format(minutes,2);
            }else if(f=='s'){
                ret[i]=seconds;
            }else if(f=='ss'){
                ret[i]=format(seconds,2);
            }else if(f=='S'){
                separator = ".";
                ret[i]=format(round(time*1000),3);
            }else if(f=='C'){
                separator = ".";
                ret[i]=format(round(time*100),2);
            }else if(f=='D'){
                separator = ".";
                ret[i]= round(time*10);
            }
            if(i>0){
                ret[i] = separator+ret[i];
            }
        }
        return ret.join("");
    },

    cssPrefix : 'ts-', //actually almost uneuseful, backward compatibility with old code (TODO: remove?)
    $J : jQuery,
    debugging : false,
    debug : function(message) {
        if (this.debugging && typeof console != 'undefined' && console.log) {
            console.log(message);
        }
    },

    //vml (+css specific functions): Used in ruler.js and RulerMarker.js:

    /**
     * Returns whether SVG is supported. If it is the case, this property can simply return true.
     * For a more clean code, one should remove this property, elementToPaperMap (see below),
     * check where we call isSvgSupported (ruler.js and rulermarker.js) and eventually
     * remove the vml methods in ruler.js and rulermarker.js
     */
    isSvgSupported : function(){return Raphael.svg},
    /**
     * Raphael unfortunately does not allow to wrap existing elements, which is a big lack not even planned to be implemented in
     * future releases (see raphael forum). Therefore, we store here a map which binds html elements -> Raphael paper object
     * This property can be deleted if svg is supported
     */
    elementToPaperMap: {},

    //use this function only IF isVmlSupported = true. Converts a class name declared in a stylesheet to
    //the equivalent Raphael attr argument. This function has been tested only under IE
    getVmlAttr: function(className){
        var d = document;
        className = className.replace(/^\.*/,'.'); //add a dot if not present
        var ssheets = d.styleSheets;
        var len = ssheets.length-1;
        //available attributes which can be converted from css svg to Raphael attributes (see Raphael.js):
        var availableAttrs = ["clip-rect", "cursor",'fill', "fill-opacity",'opacity', 'stroke', "stroke-dasharray", "stroke-linecap", "stroke-linejoin","stroke-miterlimit","stroke-opacity","stroke-width", "text-anchor"];

        //var availableAttrs = ['fill','stroke','stroke-width','fill-opacity','stroke-opacity'];
        var attr = {};
        for(var i=0; i<len; i++){
            var rules = ssheets[i].rules;
            var l = rules.length;
            for(var j=0; j <l; j++){
                var rule = rules[j];
                if(rule.selectorText == className){
                    var style = rule.style;
                    for(var k =0; k<availableAttrs.length; k++){
                        var val = style[availableAttrs[k]];
                        if(val){
                            attr[availableAttrs[k]] = val;
                            //console.log(val); //REMOVE THIS
                        }
                    }
                }
            }
        }
        return attr;
    },
    //map to store each class name to the relative sictionary for raphael attr function (VML only)
    classToRaphaelAttr : {},

    //css specific functions:
    //get computed style first (cross browser solution, from http://blog.stchur.com/2006/06/21/css-computed-style/
    getComputedStyle : function(_elem, _style){
        var computedStyle;
        var $J = this.$J;
        if(_elem instanceof $J){ //note: '_elem instanceof this.$J' doesnt work. why??
            _elem = _elem.get(0);
        }
        if (typeof _elem.currentStyle != 'undefined'){
            computedStyle = _elem.currentStyle;
        }else{
            computedStyle = document.defaultView.getComputedStyle(_elem, null);
        }
        return computedStyle[_style];
    },
    //returns a hex color from strColor. strColor can be one of the predefined css colors (eg, 'aliceBlue', case insensitive)
    //or rgb (eg: rgb(12,0,45)) or an hex color (eg, '#ff98a3' or '#f8g')
    color : function(strColor){
    if(!strColor){
        return '';
    }
    strColor = strColor.replace(/(^\s+|\s+$)/g,'').toLowerCase();
    var predefined_colors = {aliceblue:"#f0f8ff",antiquewhite:"#faebd7",aqua:"#00ffff",aquamarine:"#7fffd4",azure:"#f0ffff",beige:"#f5f5dc",bisque:"#ffe4c4",black:"#000000",blanchedalmond:"#ffebcd",blue:"#0000ff",blueviolet:"#8a2be2",brown:"#a52a2a",burlywood:"#deb887",cadetblue:"#5f9ea0",chartreuse:"#7fff00",chocolate:"#d2691e",coral:"#ff7f50",cornflowerblue:"#6495ed",cornsilk:"#fff8dc",crimson:"#dc143c",cyan:"#00ffff",darkblue:"#00008b",darkcyan:"#008b8b",darkgoldenrod:"#b8860b",darkgray:"#a9a9a9",darkgrey:"#a9a9a9",darkgreen:"#006400",darkkhaki:"#bdb76b",darkmagenta:"#8b008b",darkolivegreen:"#556b2f",darkorange:"#ff8c00",darkorchid:"#9932cc",darkred:"#8b0000",darksalmon:"#e9967a",darkseagreen:"#8fbc8f",darkslateblue:"#483d8b",darkslategray:"#2f4f4f",darkslategrey:"#2f4f4f",darkturquoise:"#00ced1",darkviolet:"#9400d3",deeppink:"#ff1493",deepskyblue:"#00bfff",dimgray:"#696969",dimgrey:"#696969",dodgerblue:"#1e90ff",firebrick:"#b22222",floralwhite:"#fffaf0",forestgreen:"#228b22",fuchsia:"#ff00ff",gainsboro:"#dcdcdc",ghostwhite:"#f8f8ff",gold:"#ffd700",goldenrod:"#daa520",gray:"#808080",grey:"#808080",green:"#008000",greenyellow:"#adff2f",honeydew:"#f0fff0",hotpink:"#ff69b4",indianred:"#cd5c5c",indigo:"#4b0082",ivory:"#fffff0",khaki:"#f0e68c",lavender:"#e6e6fa",lavenderblush:"#fff0f5",lawngreen:"#7cfc00",lemonchiffon:"#fffacd",lightblue:"#add8e6",lightcoral:"#f08080",lightcyan:"#e0ffff",lightgoldenrodyellow:"#fafad2",lightgray:"#d3d3d3",lightgrey:"#d3d3d3",lightgreen:"#90ee90",lightpink:"#ffb6c1",lightsalmon:"#ffa07a",lightseagreen:"#20b2aa",lightskyblue:"#87cefa",lightslategray:"#778899",lightslategrey:"#778899",lightsteelblue:"#b0c4de",lightyellow:"#ffffe0",lime:"#00ff00",limegreen:"#32cd32",linen:"#faf0e6",magenta:"#ff00ff",maroon:"#800000",mediumaquamarine:"#66cdaa",mediumblue:"#0000cd",mediumorchid:"#ba55d3",mediumpurple:"#9370d8",mediumseagreen:"#3cb371",mediumslateblue:"#7b68ee",mediumspringgreen:"#00fa9a",mediumturquoise:"#48d1cc",mediumvioletred:"#c71585",midnightblue:"#191970",mintcream:"#f5fffa",mistyrose:"#ffe4e1",moccasin:"#ffe4b5",navajowhite:"#ffdead",navy:"#000080",oldlace:"#fdf5e6",olive:"#808000",olivedrab:"#6b8e23",orange:"#ffa500",orangered:"#ff4500",orchid:"#da70d6",palegoldenrod:"#eee8aa",palegreen:"#98fb98",paleturquoise:"#afeeee",palevioletred:"#d87093",papayawhip:"#ffefd5",peachpuff:"#ffdab9",peru:"#cd853f",pink:"#ffc0cb",plum:"#dda0dd",powderblue:"#b0e0e6",purple:"#800080",red:"#ff0000",rosybrown:"#bc8f8f",royalblue:"#4169e1",saddlebrown:"#8b4513",salmon:"#fa8072",sandybrown:"#f4a460",seagreen:"#2e8b57",seashell:"#fff5ee",sienna:"#a0522d",silver:"#c0c0c0",skyblue:"#87ceeb",slateblue:"#6a5acd",slategray:"#708090",slategrey:"#708090",snow:"#fffafa",springgreen:"#00ff7f",steelblue:"#4682b4",tan:"#d2b48c",teal:"#008080",thistle:"#d8bfd8",tomato:"#ff6347",turquoise:"#40e0d0",violet:"#ee82ee",wheat:"#f5deb3",white:"#ffffff",whitesmoke:"#f5f5f5",yellow:"#ffff00",yellowgreen:"#9acd32"};
    var cl = predefined_colors[strColor];
    if(cl){
        return cl;
    }
    var pint = parseInt;
    var color_defs = [
        {re: /^rgb\((\d{1,3}),\s*(\d{1,3}),\s*(\d{1,3})\)$/, //example: ['rgb(123, 234, 45)', 'rgb(255,234,245)'],
            process: function (bits){
                return [pint(bits[1]), pint(bits[2]),pint(bits[3])];
            }},
        {re: /^#*(\w{2})(\w{2})(\w{2})$/, //example: ['#00ff00', '336699'],
            process: function (bits){
                return [pint(bits[1], 16),pint(bits[2], 16),pint(bits[3], 16)];
            }},
        {re: /^#*(\w{1})(\w{1})(\w{1})$/, //example: ['#fb0', 'f0f'],
            process: function (bits){
                return [pint(bits[1] + bits[1], 16),pint(bits[2] + bits[2], 16),pint(bits[3] + bits[3], 16)];
            }}
    ];

    // search through the definitions to find a match
    var nan = isNaN;
    for (var i = 0; i < color_defs.length; i++) {
        var re = color_defs[i].re;
        var processor = color_defs[i].process;
        var bits = re.exec(strColor);
        if (bits) {
            var channels = processor(bits);
            if(channels.length ==3){
                for(var j=0; j<3; j++){
                    var c = channels[j];
                    c = (nan(c) || c< 0 ? 0 : (c>255 ? 255 :c));
                    c = c.toString(16);
                    var len = c.length;
                    switch(len){
                        case 1:
                            c = '0'+c;
                            break;
                        case 2:
                            break;
                        default:
                            return '';
                    }
                    channels[j] = c;
                }
                return '#'+channels.join('');
            }
        }
    }
    return '';
}

});

/**
 * An Array-like implementation that suits the need of Marker mnanagement
 * Ruler, MarkerMap and MarkerMapDiv implement this class
 */
var TimesideArray = TimesideClass.extend({
    init: function(optionalArray){
        this._super();
        //here methods that CANNOT be overridden
        var me= optionalArray ? optionalArray : [];
        //note that this method written here OVERRIDES the same method written outside init in the children!!!!
        this.toArray = function(returnACopy){
            if(returnACopy){
                var ret = [];
                for(var i=0; i<me.length; i++){
                    ret.push(me[i]);
                }
                return ret;
            }
            return me;
        }
        this.length = me.length; //in order to match the javascript array property
    },
    length:0, //implement it as public property to be consistent with Array length property. Be careful however to NOT TO modify directly this property!!!
    //adds at the end of the array. If index is missing the object is appended at the end
    add : function(object, index){
        var array = this.toArray();
        if(arguments.length<2){
            index = array.length;
        }
        array.splice(index,0,object);
        this.length = array.length; //note that length is a property and must be updated!!!
        return object;
    },
    //removes item at index, returns the removed element
    remove : function(index){
        var array = this.toArray();
        var ret =  array.splice(index,1)[0];
        this.length = array.length; //note that length is a property and must be updated!!!
        return ret;
    },
    //Iterate over the array, with the same syntax of jQuery.each, ie, executes a function(index,element)
    //for each element from startIndexInclusive to
    //endIndexExclusive.
    //The only required argument is callback:
    //1) each(callback) iterates over all elements executing callback
    //2) each(m, callback) iterates over the elements from m executing callback
    //3) each(m,n,callback) iterates over the elements from m (inclusive) to n-1 (inclusive) executing callback

    //NOTE: writing   each : function(startInclusive, endExclusive, callback) throws an error in chrome, as the last 
    //argument (even if it is a function) is a number. Why?????
    //Anyway, we write the function arguments as empty
    each : function(){
        var startInclusive, endExclusive, callback;

        var arg = arguments;
        var len = arg.length;
        var l = this.length;
        switch(len){
            case 0:
                this.debug('each called without arguments!!!');
                return;
            case 1:
                //callback = arg[0];
                startInclusive = 0;
                endExclusive = l;
                break;
            case 2:
                if(arg[0] >= l){
                    return;
                }
                startInclusive = arg[0]=== undefined ? 0 : arg[0];
                endExclusive = l;
                //callback = arg[len-1];
                break;
            default:
                startInclusive = arg[0]=== undefined ? 0 : arg[0];
                endExclusive = arg[1]=== undefined ? l : arg[1];
        //callback = arg[len-1];
        }
        callback = arg[len-1];
        if(!(callback instanceof Function)){
            this.debug('callback NOT a function!!!');
            return;
        }
        var me =this.toArray();
        for(var i = startInclusive; i<endExclusive; i++){
            callback(i,me[i]);
        }
    
    },

    //clears the array and the events associated to it, ie removes all its elements and calls unbind(). Returns the array of the removed elements
    clear: function(){
        this.unbind();
        var me = this.toArray();
        var l = me.length;
        this.length = 0;
        if(l==0){
            return [];
        }
        return me.splice(0,l);
    },
    //moves the element from position [from] to position [to]. Shifts all elements
    //from position [to] (inclusive) of one position. Note that the elemnt at position from is first removed
    //and then inserted at position to. Therefore,
    //if to==from+1 the element is not moved. Returns from if the element
    //is not moved, i.e. either in the case above, or when:
    //1) from or to are not integers or from or to are lower than zero or greater than the array length.
    //in any other case, returns the index of the element moved, which is not necessarily to:
    //It is, if to<from, otherwise (to>from+1) is to-1
    move : function(from, to){
        var pInt = parseInt;
        if(pInt(from)!==from || pInt(to)!==to){
            return from;
        }
        var me =this.toArray();
        var len = me.length;
        if((from<0 || from>len)||(to<0 || to>len)){
            return from;
        }
        //if we moved left to right, the insertion index is actually
        //newIndex-1, as we must also consider the removal of the object at index from
        if(to>from){
            to--;
        }
        if(from != to){
            var elm = me.splice(from,1)[0];
            me.splice(to,0,elm);
        }
        return to;
    }
});


/*
 * Sets a "tab look" on some elements of the page. Takes at least 3 arguments, at most 5:
 * 1st argument: an array (or a jquery object) of html elements, ususally anchors, representing the tabs
 * 2nd argument: an array (or a jquery object) of html elements, ususally divs, representing the containers to be shown/hidden when 
 *   clicking the tabs. The n-th tab will set the n-th container to visible, hiding the others. So order is important. Note that if tabs
 *   or container are jQuery objects, the html elements inside them are sorted according to the document order. That's why tabs and
 *   container can be passed also as javascript arrays, so that the binding n-th tab -> n-th container can be decided by the user
 *   regardeless on how elements are written on the page, if already present
 * 3rd argument: the selected index. If missing it defaults to zero.
 * 4th argument: selectedtab class. Applies to the selected tab after click of one tab. If missing, nothing is done
 * 5th argument the unselectedtab class. Applies to all tabs not selected after click of one tab. If missing, nothing is done
 *
 * NOTE: The last 2 arguments are mostly for customizing the tab "visual look", as some css elements (eg, (position, top, zIndex)
 * are set inside the code and cannot be changed, as they are mandatory to let tab anchor behave like desktop application tabs. Note also
 * that every tab container is set to 'visible' by means of jQuery.show()
 *
 * Examples:
 * setUpPlayerTabs([jQuery('#tab1),jQuery('#tab1)], [jQuery('#div1),jQuery('#div2)], 1);
 * sets the elements with id '#tab1' and '#tab2' as tab and assign the click events to them so that clicking tab_1 will show '#div_1'
 * (and hide '#div2') and viceversa for '#tab2'. The selected index will be 1 (second tab '#tab2')
 */
function setUpPlayerTabs() {//called from within controller.js once all markers have been loaded.
    //this is because we need all divs to be visible to calculate size. selIndex is optional, it defaults to 0
    //
    
    var $J = jQuery;
    var tabs_ = arguments[0];
    var divs_ = arguments[1]; //they might be ctually any content, div is a shoertand

    //converting arguments to array: tabs
    var tabs=[];
    if(tabs_ instanceof $J){
        tabs_.each(function(i,elm){
            tabs.push(elm);
        });
    }else{
        tabs = tabs_;
    }
    //set the overflow property of the parent tab to visible, otherwise scrollbars are displayed
    //and the trick of setting position:relative+top:1px+zIndices (see css) doesnt work)
    $J(tabs).each(function(i,tab){
        var t = $J(tab).attr('href','#');
        t.show(); //might be hidden
        //set necessary style for the tab appearence:
        var overflow = t.parent().css('overflow');
        if(overflow && overflow != 'visible'){
            t.parent().css('overflow','visible');
        }
    });
    //converting arguments to array: divs
    var divs=[];
    if(divs_ instanceof $J){
        divs_.each(function(i,elm){
            divs.push(elm);
        });
    }else{
        divs = divs_;
    }
    
    //reading remaing arguments (if any)
    var selIndex = arguments.length>2 ? arguments[2] : 0;
    var selectedTabClass = arguments.length>3 ? arguments[3] : undefined;
    var unselectedTabClass = arguments.length>4 ? arguments[4] : undefined;

    //function to be associate to every click on the tab (see below)
    var tabClicked = function(index) {
        for(var i=0; i<tabs.length; i++){
            var t = $J(tabs[i]);
            
            var div = $J(divs[i]);
            var addClass = i==index ? selectedTabClass : unselectedTabClass;
            var removeClass = i==index ? unselectedTabClass : selectedTabClass;
            if(removeClass){
                t.removeClass(removeClass);
            }
            if(addClass){
                t.addClass(addClass);
            }
            
            //relevant css. Will override any css set in stylesheets
            t.css({
                'position':'relative',
                'top':'1px',
                'zIndex': (i==index ? '10' : '0')
            });
            
            if(i===index){
                div.fadeIn('slow');
            }else{
                div.hide();
            }
        }
    };
    
    //bind clicks on tabs to the function just created
    for (var i=0;i<tabs.length;i++){
        // introduce a new scope (round brackets)
        //otherwise i is retrieved from the current scope and will be always equal to tabs.length
        //due to this loop
        (function(tabIndex){
            $J(tabs[i]).click(function(){
                tabClicked(tabIndex);
                return false;//returning false avoids scroll of the anchor to the top of the page
            });
        })(i);
    }
    
    //select the tab
    $(tabs[selIndex]).trigger("click");
}

