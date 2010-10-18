/*
 * eZTelemeta web audio player
 *
 * Copyright (c) 2009 Samalyse
 * Author: Olivier Guilyardi <olivier samalyse com>
 * License: CeCILL Free Software License Agreement
 */

function TelemetaPlayer(cfg)
{
    var that            = this;
    var soundManager    = null;
    var sound           = null;
    var currentLink     = null;
   
    this.init = function() {
        var sounds = this.byClass(document, 'dd', 'telemeta-sound');
        var i;
        for (i in sounds) {
            if (typeof(sounds[i].getElementsByTagName) != 'undefined') {
                link = sounds[i].getElementsByTagName('a')[0];
                link.onclick = this.togglePlayback;
            }
        }
    }

    this.findContainer = function(link) {
        var e = link;
        while (e) {
            e = e.parentNode;
            if (this.hasClass(e, 'telemeta-item'))
                break;
            if (e == document)
                e = null;
        }
        return e;
    }

    this.setStateStyle = function(link, state) {
        var container = this.findContainer(link);
        if (state == 'stopped') {
            if (this.hasClass(container, 'telemeta-playing'))
                container.className = container.className.replace('telemeta-playing', '');
        }

        if (state == 'stopped' || state == 'playing') {
            if (this.hasClass(container, 'telemeta-loading'))
                container.className = container.className.replace('telemeta-loading', '');
        }

        if (state == 'playing' || state == 'loading') {
            if (!this.hasClass(container, 'telemeta-playing'))
                container.className += ' telemeta-playing';
            if (state == 'loading') {
                if (!this.hasClass(container, 'telemeta-loading'))
                    container.className += ' telemeta-loading';
            }
        } 
    }

    this.togglePlayback = function() {
        var link = this;
        if (that.soundManager) {
            if (that.sound)
                that.sound.stop();
            if (that.currentLink) {
                that.setStateStyle(that.currentLink, 'stopped');
                that.updatePosition(0);
            }
            if (!that.currentLink || that.currentLink != link) {
                that.sound = that.soundManager.createSound({
                    id: 'telemeta_sound', 
                    url: link.href,
                    whileplaying: function() { that.update(); },
                    onbufferchange: function() { that.update(); }
                });
                that.currentLink = link;
                that.sound.play();
                that.setStateStyle(link, 'loading');
                that.updatePosition(0);
            } else {
                that.currentLink = null;
            }
        }
        return false;
    }

    this.updatePosition = function(position)
    {
        var container = that.findContainer(that.currentLink)
        var positionContainer = that.byClass(container, 'span', 'telemeta-position')[0];

        function format(i) { i = '' + parseInt(i); return i.length < 2 ? '0' + i : i; }

        var hours = format(position / 3600);
        var mins  = format(position % 3600 / 60);
        var secs  = format(position % 3600 % 60);
        positionContainer.firstChild.nodeValue = hours + ':' + mins + ':' + secs;
    }

    this.update = function()
    {
        that.updatePosition(that.sound.position / 1000);
        if (that.sound.isBuffering) {
            that.setStateStyle(that.currentLink, 'loading');
        } else {
            that.setStateStyle(that.currentLink, 'playing');
        }
    }

    this.hasClass = function(element, className) {
        if (typeof(element.className) != 'undefined') 
            return new RegExp('(^|\\s)' + className + '(\\s|$)').test(element.className);

        return false;
    }

    this.byClass = function(root, tag, className) {
        var result = [];
        var nodes = root.getElementsByTagName(tag);
        var i;
        for (i = 0; i < nodes.length; i++) {
            if (this.hasClass(nodes[i], className)) 
                result.push(nodes[i]);
        }
        return result;
    }

    this.setSoundManager = function(soundManager) {
        this.soundManager = soundManager;
    }

    TelemetaDom.ready(function() { that.init(cfg); });
}

(function(){

    var DomReady = window.TelemetaDom = {};

	// Everything that has to do with properly supporting our document ready event. Brought over from the most awesome jQuery. 

    var userAgent = navigator.userAgent.toLowerCase();

    // Figure out what browser is being used
    var browser = {
    	version: (userAgent.match( /.+(?:rv|it|ra|ie)[\/: ]([\d.]+)/ ) || [])[1],
    	safari: /webkit/.test(userAgent),
    	opera: /opera/.test(userAgent),
    	msie: (/msie/.test(userAgent)) && (!/opera/.test( userAgent )),
    	mozilla: (/mozilla/.test(userAgent)) && (!/(compatible|webkit)/.test(userAgent))
    };    

	var readyBound = false;	
	var isReady = false;
	var readyList = [];

	// Handle when the DOM is ready
	function domReady() {
		// Make sure that the DOM is not already loaded
		if(!isReady) {
			// Remember that the DOM is ready
			isReady = true;
        
	        if(readyList) {
	            for(var fn = 0; fn < readyList.length; fn++) {
	                readyList[fn].call(window, []);
	            }
            
	            readyList = [];
	        }
		}
	};

	// From Simon Willison. A safe way to fire onload w/o screwing up everyone else.
	function addLoadEvent(func) {
	  var oldonload = window.onload;
	  if (typeof window.onload != 'function') {
	    window.onload = func;
	  } else {
	    window.onload = function() {
	      if (oldonload) {
	        oldonload();
	      }
	      func();
	    }
	  }
	};

	// does the heavy work of working through the browsers idiosyncracies (let's call them that) to hook onload.
	function bindReady() {
		if(readyBound) {
		    return;
	    }
	
		readyBound = true;

		// Mozilla, Opera (see further below for it) and webkit nightlies currently support this event
		if (document.addEventListener && !browser.opera) {
			// Use the handy event callback
			document.addEventListener("DOMContentLoaded", domReady, false);
		}

		// If IE is used and is not in a frame
		// Continually check to see if the document is ready
		if (browser.msie && window == top) (function(){
			if (isReady) return;
			try {
				// If IE is used, use the trick by Diego Perini
				// http://javascript.nwbox.com/IEContentLoaded/
				document.documentElement.doScroll("left");
			} catch(error) {
				setTimeout(arguments.callee, 0);
				return;
			}
			// and execute any waiting functions
		    domReady();
		})();

		if(browser.opera) {
			document.addEventListener( "DOMContentLoaded", function () {
				if (isReady) return;
				for (var i = 0; i < document.styleSheets.length; i++)
					if (document.styleSheets[i].disabled) {
						setTimeout( arguments.callee, 0 );
						return;
					}
				// and execute any waiting functions
	            domReady();
			}, false);
		}

		if(browser.safari) {
		    var numStyles;
			(function(){
				if (isReady) return;
				if (document.readyState != "loaded" && document.readyState != "complete") {
					setTimeout( arguments.callee, 0 );
					return;
				}
				if (numStyles === undefined) {
	                var links = document.getElementsByTagName("link");
	                for (var i=0; i < links.length; i++) {
	                	if(links[i].getAttribute('rel') == 'stylesheet') {
	                	    numStyles++;
	                	}
	                }
	                var styles = document.getElementsByTagName("style");
	                numStyles += styles.length;
				}
				if (document.styleSheets.length != numStyles) {
					setTimeout( arguments.callee, 0 );
					return;
				}
			
				// and execute any waiting functions
				domReady();
			})();
		}

		// A fallback to window.onload, that will always work
	    addLoadEvent(domReady);
	};

	// This is the public function that people can use to hook up ready.
	DomReady.ready = function(fn, args) {
		// Attach the listeners
		bindReady();
    
		// If the DOM is already ready
		if (isReady) {
			// Execute the function immediately
			fn.call(window, []);
	    } else {
			// Add the function to the wait list
	        readyList.push( function() { return fn.call(window, []); } );
	    }
	};
    
	bindReady();
	
})();
