/**
 * TimeSide - Web Audio Components
 * Copyright (c) 2008-2009 Samalyse
 * Author: Olivier Guilyardi <olivier samalyse com>
 * License: GNU General Public License version 2.0
 */

TimeSide(function($N, $J) {

    $N.Class.create("Player", $N.Core, {
        skeleton: {
            'div.viewer': {
                'div.ruler': {},
                'div.wave': {
                    'div.image-canvas': {},
                    'div.image-container': ['img.image']
                }
            },
            'div.control': {
                'div.layout': {
                    'div.playback': ['a.play', 'a.pause', 'a.rewind', 'a.forward', 'a.set-marker' //]
                    ,'a.volume']
                }
            }/*,
        'div.marker-control': ['a.set-marker']*/
        },
        defaultContents: {
            play: 'Play',
            pause: 'Pause',
            rewind: 'Rewind',
            forward: 'Forward',
            'set-marker': 'Set marker'
        //,'text-marker' : 'textmarker'
        },
        elements: {},
        ruler: null,
        map: null,
        container: null,
        imageWidth: null,
        imageHeight: null,
        soundPosition: 0,

        initialize: function($super, container, cfg) {
            $super();
            if (!container){
                throw new $N.RequiredArgumentError(this, 'container');
            }
            this.container = $J(container);
            
            this.configure(cfg, {
                image: null,
                sound:null,
                soundDurationInMsec:0
            });
        //if(this.cfg.sound && this.cfg.sound.)
        },

        free: function($super) {
            this.elements = null;
            this.container = null;
            //this.sound.destruct(); //should be called here?
            $super();
        },


        setMarkerMap: function(map) {
            this.map = map;
            return this;
        },

        setImage: function(expr) {
            this.cfg.image = expr;
            this.refreshImage();
        },

        refreshImage: function() {
            var src = null;
            if (typeof this.cfg.image == 'function') {
                src = this.cfg.image(this.imageWidth, this.imageHeight);
            } else if (typeof this.cfg.image == 'string') {
                src = this.cfg.image;
            }

            if (src) {
                this.elements.image.attr('src', src);
            }
        },

        //        draw: function() {
        //            this.debug('drawing');
        //            $N.domReady(this.attach(this._setupInterface));
        //            return this;
        //        },

        _setupInterface: function() {
            consolelog('player _setupInterface sound.readyState:'+this.cfg.sound.readyState); //handle also cases 0 and 2????
            //0 = uninitialised
            //1 = loading
            //2 = failed/error
            //3 = loaded/success
            if(this.cfg.sound.readyState==1){
                var rsz = this.resize;
                //attach an event when fully loaded and repaint all.
                //For the moment we will display the ruler and other stuff
                //based on durationEstimate property
                this.cfg.sound.options.onload = function() {
                    rsz();
                }
            }
            this.elements = $N.Util.loadUI(this.container, this.skeleton, this.defaultContents);

            // IE apparently doesn't send the second mousedown on double click:
            var jump = $J.browser.msie ? 'mousedown dblclick' : 'mousedown';
            this.elements.rewind.attr('href', '#').bind(jump, this.attach(this._onRewind))
            .click(function() {
                return false;
            });
            this.elements.forward.attr('href', '#').bind(jump, this.attach(this._onForward))
            .click(function() {
                return false;
            });
            
            //
            this.elements.volume.attr('href', '#').click(function(){
                return false;
            }).bind('mousedown', this.attach(
                function(e){
                    if(e.which===1){ //left button
                        this.setVolume(e);
                    }
                    return false;
                }
                ));


            //assigning title string to all anchors???????
            this.elements.control.find('a').add(this.elements.setMarker)
            .attr('href', '#')
            .each(function(i, a){
                a = $J(a);
                if (!a.attr('title')){
                    a.attr('title', a.text());
                }
            });
            
            //this.elements.markerControl.find('a').attr('href', '#');
            if (this.map && CURRENT_USER_NAME) {
                //configureMarkersDiv();
                this.elements.setMarker.bind('click', this.attach(this._onSetMarker));
            //this.elements.setMarker2.bind('click', this.attach(this._onSetMarker2));
            //this.elements.textMarker.attr('type', 'text');
            //this.elements.textMarker.bind('click', this.attach(this._onSetMarker2));
          
            } else {
                this.elements.setMarker.remove();
            }
            //creating the ruler
            var ruler = new $N.Ruler({
                viewer: this.elements.viewer,
                //map: this.map,
                sound: this.cfg.sound,
                soundDurationInMsec: this.cfg.soundDurationInMsec
            });
            this.ruler = ruler;
            //bind events to the ruler (see function observe in core.js, I guess,
            //which overrides jQuery bind function):
            //the first arg is basically the event name, the second
            //arg is a function to execute each time the event is triggered
            this.ruler
            .observe('markermove', this.forwardEvent)
            .observe('markeradd', this.forwardEvent)
            //.observe('move', this.forwardEvent)
            .draw();
            this.refreshImage();
            this.resize(); 

//            var resizeTimer = null;
//            $J(window).resize(this.attach(function() {
//                if (resizeTimer){
//                    clearTimeout(resizeTimer);
//                }
//                resizeTimer = setTimeout(this.attach(this.resize), 100);
//            }));

            this.setSoundVolume(this.getSoundVolume());
            //finally, binds events to play and pause. At the end cause this.ruler has to be fully initialized
            var sound = this.cfg.sound;
            this.elements.pause.attr('href', '#').bind('click', function(){
                sound.pause();
                return false;
            });
            //var r = this.ruler;
            this.elements.play.attr('href', '#').bind('click', function(){
                consolelog('playstate'+sound.playState);
                if(sound.playState!=1 || sound.paused){
                    sound.play({
                        whileplaying: function(){
                            ruler._movePointer(this.position/1000);
                        //consolelog(this.ruler);
                        }
                    });
                }
                return false;
            });
        },

        resize: function(overrideHeight) {
            this.debug("resizing");
            var height;
            if (overrideHeight === true) {
                this.debug("override height");
                height = this.elements.image.css('height', 'auto').height();
            } else {
                height = this.elements.wave.height();
                this.debug("wave height:" + height);
                if (!height) {
                    this.elements.image.one('load', this.attach(function() {
                        this.resize(true);
                        this.debug("image loaded");
                    }));
                    height = this.elements.image.height();
                }
            }

            var elements = this.elements.image
            .add(this.elements.imageContainer)
            .add(this.elements.imageCanvas);

            elements.css('width', 'auto'); // for IE6

            if (!height){
                height = 200;
            }
            var style = {
                width: this.elements.wave.width(),
                height: height
            }
            elements.css(style);
            this.imageWidth = style.width;
            this.imageHeight = style.height;
            this.refreshImage();
            this.ruler.resize();
            return this;
        },
        //sound object methods

        getSoundPosition :function(){
            //note that this.cfg.sound.position is buggy. If we did not play, calling this.cfg.sound.setPosition(p)
            //stores the position, but this.cfg.position returns zero.
            //otherwise (we did play at least once) this.cfg.sound.position returns the good value
            //to overcome this problem, we return the ruler position, NOTE that it is in seconds
            return this.ruler.pointerPos;
        //            var s = this.cfg.sound;
        //            return s ? s.position/1000 : 0;
        },

        getSoundVolume :function(){
            var s = this.cfg.sound;
            return s ? s.volume : 0;
        },

        getSoundDuration :function(){
            var s = this.cfg.sound;
            return s ? s.duration/1000 : 0;
        },

        _onRewind: function() {
            var offset = 0;
            if (this.map) {
                var position = parseFloat(this.getSoundPosition());
                var idx = this.map.indexOf(position)-1;
                if(idx>=0){
                    var marker = this.map.get(idx);
                    if(marker){
                        offset = marker.offset;
                    }
                }
            }
            this.ruler._movePointerAndUpdateSoundPosition(offset);
            return false;
        },

        _onForward: function() {
            var offset = this.getSoundDuration();
            if (this.map) {
                var position = parseFloat(this.getSoundPosition());
                var idx = this.map.insertionIndex(position);
                if(idx>=0){ //the pointer is exactly on a marker, the index is the marker itself
                    //so increase by one otherwise  and we wouldn't move ahead
                    //more specifically, increase as long as we have markers with this offset (there could be more than
                    //one marker at offset
                    var m = this.map.get(idx);
                    while(m && m.offset == position){
                        idx++;
                        m = this.map.get(idx);
                        if(!m){
                            idx=-1;
                        }
                    }
                }else{
                    //we are not on a pointer, get the index of the marker
                    //(see markermap insertionindex)
                    idx = -idx-1;
                }
                if(idx>=0){
                    var marker = this.map.get(idx);
                    if(marker){
                        offset = marker.offset;
                    }
                }
            }
            this.ruler._movePointerAndUpdateSoundPosition(offset);
            
            return false;
        },

        //notified from a click event on the anchor
        setVolume: function(event){
            
            var ticks = [18,26,33,40,47];
            var vol = event.layerX;
            for(var i=0; i<ticks.length; i++){
                if(vol<=ticks[i]){
                    //var index = i;
                    var volume = i*20;
                    this.setSoundVolume(volume);
                    this.debug('setting volume'+volume);
                    return false;
                }
            }
            this.setSoundVolume(100);
            //            var g = 9;
            //            console.log(event.layerX);
            return false;
        },

        //TODO: remove unused
        //        onVolumeChanged: function(e, data){
        //           this.updateVolumeAnchor(data.volume);
        //        },

        setSoundVolume: function(volume){
            
            if(typeof volume != 'number'){ //note: typeof for primitive values, instanceof for the rest
                //see topic http://stackoverflow.com/questions/472418/why-is-4-not-an-instance-of-number
                volume = 100;
            }
            if(volume<0){
                volume = 0;
            }
            if(volume>100){
                volume = 100;
            }
            this.cfg.sound.setVolume(volume);
            //update the anchor image:
            var indices = [20,40,60,80,100,100000];
            
            for(var i=0; i <indices.length; i++){
                if(volume<indices[i]){
                    var pos = -28*i;
                    pos = '0px '+ pos+ 'px'; //DO NOT SET !important as in FF3 DOES NOT WORK!!!!!
                    this.elements.volume.css('backgroundPosition',pos);
                    return;
                }
            }
        // this.elements.volume.css('backgroundPosition','0px 0px !important')

        },

        _onPlay: function() {
            this.fire('play');
            return false;
        },

        _onPause: function() {
            this.fire('pause');
            return false;
        },

        _onSetMarker: function() {
            if (this.map) {
                this.fire('markeradd', {
                    offset: this.getSoundPosition()
                });
            }
            return false;
        }
    });

    $N.notifyScriptLoad();

});
