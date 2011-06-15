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
 * The player class to instantiate a new player. Requires all necessary js (timeside, ruler, markermap etcetera...) and
 * jQuery
 */

//playerDiv, sound, durationInMsec, visualizers, markerMap);
Timeside.classes.Player = Timeside.classes.TimesideClass.extend({
    
    //sound duration is in milliseconds because the soundmanager has that unit,
    //player (according to timeside syntax) has durations in seconds
    // newMarkerCallback must be either a string or a function, the necessary checks is done in Timeside.load
    // (which calls this method)
    //if markersArray is not an array, it defaults to []
    init: function(container, sound, soundDurationInMsec, soundImgFcn, soundImgSize, markersArray, newMarkerCallback) {
        this._super();

        this.playState = 0; //0: not playing, 1: loading, 2:buffering, 3 playing (sound heard)
        //container is the div #player
       
        if (!container){
            this.debug('ERROR: container is null in initializing the player');
        }

        this.getContainer = function(){
            return container;
        };
        this.getSound = function(){
            return sound;
        };
        if(typeof soundImgFcn == 'string'){
            var url = soundImgFcn;
            this.imageCallback =  new function(w,h){
                return url;
            };
        }else if(typeof soundImgFcn === 'function'){
            this.imageCallback = soundImgFcn;
        }

        var sd = this.toSec(soundDurationInMsec);
        this.getSoundDuration = function(){
            return sd;
        };
        
        this.soundPosition =  sound.position ? this.toSec(sound.position) : 0;
        //public methods: returns the sound position
        this.getSoundPosition = function(){
            return this.soundPosition;
        };


        //       if(sound.readyState != 3){
        //                /*sound.readyState
        //                 * Numeric value indicating a sound's current load status
        //                 * 0 = uninitialised
        //                 * 1 = loading
        //                 * 2 = failed/error
        //                 * 3 = loaded/success
        //                 */
        //                sound.options.whileloading=function(){
        //
        //                }
        //        };
        
        //        var currentMarkerIndex=0;
        //        this.getCurrentMarkerIndex = function(){
        //            return currentMarkerIndex;
        //        };


        //initializing markermap and markerui
        var map = new Timeside.classes.MarkerMap();
        this.getMarkerMap = function(){
            return map;
        }

        var canAddMarkers = false;
        if(newMarkerCallback){
            //            this.canAddMarker = function(){
            //                return true;
            //            }
            canAddMarkers = true;
            if(typeof newMarkerCallback === 'function'){
                this.newMarker = newMarkerCallback;
            }
        }
        //        else{
        //            this.canAddMarker = function(){
        //                return false;
        //            }
        //        }


        // },

        //sets up the player interface and loads the markers. There is theoretically no need for this method, as it might be included in
        //the init constructor, it is separated for "historical" reasons: this method stems from the old _setupInterface,
        //which was a separate method in the old player code. Future releases might include it in the init constructor
        //  setupInterface: function(markersArray) {

        //removed"
        //      var sound = this.getSound();
        //removed"
        this.debug('player _setupInterface sound.readyState:'+sound.readyState); //handle also cases 0 and 2????

        var $J = this.$J; //defined in the super constructor
        var me=this;
        //build the innerHTML as array, then join it. This is usually faster than string concatenation in some browsers.
        //Note that the player image (see below) is given a src with a temporary 1x1 pixels transparent image
        //Basically, NOT specifying any src for image tags can be harmful,
        //see http://www.nczonline.net/blog/2009/11/30/empty-image-src-can-destroy-your-site/ and
        //http://geekswithblogs.net/bcaraway/archive/2007/08/24/114945.aspx for details
        var html = [//"<div class='ts-viewer'>",
        "<div class='ts-ruler'></div>",
        "<div class='ts-wave'>",
        "<div class='ts-image-canvas'></div>",
        "<div class='ts-image-container'>",
        // "<img class='ts-image' src='/images/transparent.png' alt='' />",
        "</div>",
        "</div>",
        //"</div>",
        "<div class='ts-control'>",
        //"<div class='ts-layout'>",
        //"<div class='ts-playback'>",
        "<a class='ts-play ts-button'></a>",
        "<a class='ts-pause ts-button'></a>",
        "<a class='ts-rewind ts-button'></a>",
        "<a class='ts-forward ts-button'></a>",
        "<a class='ts-set-marker ts-button'></a>",
        //        "<a class='ts-volume'></a>",

        //"<div class='ts-volume'>",
        "<a class='ts-volume-speaker ts-button'></a>",
        "<div class='ts-volume-wrapper-div'>",
        "<a class='ts-volume-bar-container'>",
        "<span class='ts-volume-bar'></span>",
        "</a>",
        "</div>",

        "<div class='ts-wait'></div>",
        //"<img class='ts-wait'/>",
        //"<select class='ts-visualizer'></select>",
        //"</div>",
        //"</div>",
        "</div>"];

        //removed"
        //this.getContainer().html(html.join(''));
        //var container = this.getContainer();
        //removed"
        //added"
        container.html(html.join(''));
        //added"

        var control = container.find('.ts-control');

        //bind events to buttons:
        var rewind = control.find('.ts-rewind');
        rewind.attr('href', '#').click(function(e){
            me.rewind.apply(me);
            return false;
        });

        var forward = control.find('.ts-forward');
        forward.attr('href', '#').click(function(e){
            me.forward.apply(me);
            return false;
        });

        var pause = control.find('.ts-pause');
        pause.attr('href', '#').bind('click', function(){
            me.pause.apply(me);
            return false;
        });

        var play = control.find('.ts-play');
        play.attr('href', '#').bind('click', function(){
            me.play.apply(me);
            return false;
        });

        var setMarkerButton = control.find('.ts-set-marker');

        //removed"
        //var canAddMarkers = this.canAddMarker();
        //removed"

        if(canAddMarkers){
            setMarkerButton.show().attr('href','#').unbind('click').bind('click', function(){
                me.addMarker(me.getSoundPosition());
                return false;
            });
        }else{
            setMarkerButton.hide().unbind('click');
        }


        //volume:
        var volumeSpeaker = control.find('.ts-volume-speaker');
        var volumeBarContainer = control.find('.ts-volume-bar-container');
        var volumeBar = volumeBarContainer.find('.ts-volume-bar');

        var getVol = function(x){
            var vol = 100*x/volumeBarContainer.width();
            //allow click to easily set to zero or 100, ie set a margin to 5%:
            var margin = 5;
            if (vol < margin){
                vol=0;
            }else if(vol >100-margin){
                vol = 100;
            }
            return vol;
        };
        function setVolume(event,volumeElement){
            //var ticks = [18,26,33,40,47];
            var x = event.pageX - volumeElement.offset().left; //using absolute coordinates allows us to
            //avoid using layerX (not supported in all browsers) and clientX (which needs the window scrollLeft variable)
            me.setSoundVolume(getVol(x));
            return false;
        }
        volumeBarContainer.attr('href', '#').click(function(event){
            return setVolume(event,volumeBar);
        });
        volumeSpeaker.attr('href', '#').click(function(){
            me.setSoundVolume(me.getSoundVolume()>0 ? 0 : getVol(volumeBar.outerWidth()));
            return false;
        });
        this.setSoundVolume(this.getSoundVolume());

        control.find('a').attr('href', '#') ;

        //SET NECESSARY CSS (THIS WILL OVERRIDE CSS SET IN STYLESHEETS):
        //var viewer = container.find('.ts-viewer');
        var wave = container.find('.ts-wave');
        var ruler_ = container.find('.ts-ruler');
        wave.add(control).add(ruler_).css({
            'position':'relative',
            'overflow':'hidden'
        });
        //assigning display and title to all anchors
        control.find('*').css({
            'display':'inline-block',
            'overflow':'hidden'
        });
        //        if(!canAddMarkers){
        //            setMarkerButton.hide().unbind('click');
        //        }

        var waitImg = control.find('.ts-wait');
        waitImg.html('wait').css({
            'position':'absolute'
        });


        var div = control.find('.ts-volume-wrapper-div');
        div.css({
            'position':'absolute',
            'left':(volumeSpeaker.position().left+volumeSpeaker.outerWidth())+'px',
            'top':0,
            'width':'auto',
            'height':'100%'
        });
        //END NECESSARY CSS

        
        //creating the ruler
        var waveImage =  container.find('.ts-image-canvas');
        var ruler = new Timeside.classes.Ruler(ruler_, waveImage, this.getSoundDuration());
        //var ruler = new Timeside.classes.Ruler(viewer, this.getSoundDuration());
        this.getRuler = function(){
            return ruler;
        }

        //setting image size (if provided) and resize player. Note that _setImageSize (with underscore) is intended to be
        //a private method (faster). setImageSize (without underscore) is the public method to use outside of player object
        if(soundImgSize){
            this._setImageSize(soundImgSize.width,soundImgSize.height,container, wave,true); //calls this.resize which calls ruler.resize
        }else{
            this._setImageSize('','',container, wave,true); //calls this.resize which calls ruler.resize
        }

        //this.resize(); //which calls also ruler.resize() (see below)


        //binds click for the pointer:
        var v = wave; //.add(ruler);
        v.unbind('click').click(function(evt){
            var w = v.width();
            var x = evt.pageX - v.offset().left; //using absolute coordinates allows us to
            //avoid checking whether or not we are clicking on a vertical marker line, on a subdiv etcetera
            var sd = me.getSoundDuration();
            me.setSoundPosition(sd*x/w);
        });



        //finally, load markers and bind events for markers (see method below):
        //NOTE: loadMarkers ASYNCHRONOUSLY CALLS THE SERVER, SO METHODS WRITTEN AFTER IT MIGHT BE EXECUTED BEFORE
        //loadMarkers has finished its job
        //this.loadMarkers(callback);
        if(!(markersArray) || !(markersArray.length)){
            markersArray = [];
        }
        this.loadMarkers(markersArray);


        //IE7 BUG: the divs wave and control do not shift downwards after canvas is drawn and covers part of the rulrer.
        //Weird enough (with IE it isn't actually), we have just to set the property we already set in the css:
        //ie, top: auto. This is however useful even if somebody specified a top property on the divs
        ruler_.add(wave).add(control).css('top','auto');
//        if(h > $J('.ts-wave').position().top){
//            $J('.ts-wave').css('top',0+'px');
//        }

    },



    //functions for converting seconds (player unit) to milliseconds (sound manager unit) and viceversa:
    toSec: function(milliseconds){
        return milliseconds/1000;
    },
    toMsec : function(seconds){ //this function has less performances than toSec, as it calls Math.round
        return Math.round(1000*seconds); //however, it is assumed that it is NOT called in loops
    },
    isPlaying : function(){
        var sound = this.getSound();
        if(!sound){
            return false;
        }
        return this.playState;
    /*Numeric value indicating the current playing state of the sound.
             * 0 = stopped/uninitialised
             * 1 = playing or buffering sound (play has been called, waiting for data etc.)
             *Note that a 1 may not always guarantee that sound is being heard, given buffering and autoPlay status.*/
    //return sound && sound.playState==1;
    },
    setSoundPosition: function(newPositionInSeconds){
        //if the player is playing and NOT yet fully loaded, simply calling:
        //this.getSound().setPosition(this.toMsec(newPositionInSeconds));
        //resets the position to zero. So we use this workaround:
        //    this.getSound().stop(); //calling this.pause() hides the waiting bar, which is not the case here
        //    this.soundPosition = newPositionInSeconds;
        //    this.play();

        //however, if this.isPlaying() we first call stop otherwise some fast pointer move effect is undesiderable

        //So:
        var wasPlaying = this.isPlaying();
        if(wasPlaying){
            this.getSound().stop(); //dont call this.pause cause it hides the waitbar, if visible and resets the playState
        }
        //update pointer position. If this call is due to a pointer move (mouse release),
        //ruler.isPointerMovingFromMouse=true and the following code has no effect (the pointer is already at the good position)
        var ruler = this.getRuler();
        if(ruler){
            ruler.movePointer(newPositionInSeconds);
        }
        //set sound position:
        this.soundPosition = newPositionInSeconds;
        //resume playing if it was playing:
        if(wasPlaying){
            var player = this;
            
            //delay a little bit the play resume, this might avoid fast pointer repositioning
            //(it should not be the case, but it happens. why??)
            setTimeout(function(){
                //player.playState = 1; //set to loading, so we do not display waitbar 'loading' again
                player.play.apply(player);
            },100);
        }
    },
    //given a marker at index I, specifies that a marker corss event is fired whenever the sound position (pointer)
    //is in the interval ]markerCrossedOffsetMargin-I,I+markerCrossedOffsetMargin[
    //the value is in seconds
    //markerCrossedOffsetMargin : 0.5,
    play : function(){
        var player = this;
        var sound = player.getSound();
        //var imgWaitDisplaying = this.isWaitVisible();
        //soundManager multishot set false should prevent the play when already playing. We leave this check for safety
       
        if(!player || !sound){
            return false;
        }
        
        //setting markercorss callback
        //for these varirables, see explanation below:
        //var numberOfSubsequentPlayCall=0;
        //var minimumNumberOfSubsequentPlayCall=3;
        //var isPlayingId=2;
        //var isBufferingId=1;
        //var uninitializedId=0;
        //var currentState=uninitializedId;

        var fireOnMarkerPosition = function(seconds){}; //does nothing by default
        var map = player.getMarkerMap();
        var markerCrossListeners = player.listenersMap['markerCrossed'];
        //optimizing: if no listeners associated to markerCrossListeners, avoid creating a function
        if(map && map.length && markerCrossListeners){
            var idx = 0;
            if(player.soundPosition>0){
                idx = map.insertionIndex(player.soundPosition);
                if(idx<0){
                    idx=-idx-1;
                }
            }
            var len = map.length;
            if(idx>-1 && idx < len){
                var markers = map.toArray();
                var marker = markers[idx];
                var margin = 0.5; //1 second (0.5*2) of margin (before+after)
                var offs = marker.offset;
                var intervalUpperBound =  offs+margin;
                var intervalLowerBound =  offs-margin;
                var data = { //if you change data, change it also below
                    index:idx,
                    marker:marker,
                    timeMarginInSec: margin
                };
                fireOnMarkerPosition = function(seconds){
                    if(marker){
                        if(seconds>intervalLowerBound && seconds < intervalUpperBound){
                            player.fire('markerCrossed',data);
                            idx++;
                            if(idx<len){
                                marker = markers[idx];
                                offs = marker.offset;
                                intervalUpperBound =  offs+margin;
                                intervalLowerBound =  offs-margin;
                                data = { //if you change data, change it also above
                                    index:idx,
                                    marker:marker,
                                    timeMarginInSec: margin
                                };
                            }else{
                                marker = undefined;
                            }
                        }
                    }
                };
            }
        }

        var toSec = player.toSec;
        var ruler = player.getRuler();
        var sPosInMsec = player.toMsec(player.soundPosition);
        var bufferingString = this.msgs.buffering;
        var loadingString = this.msgs.loading;
        
        var updateWaitBar = this.setWait;

        if(loadingString && !this.playState){ //
            updateWaitBar.apply(this,[loadingString]); //calling setWait of an empty string hides the wait, we dont want it here
            //ps: without apply this in updateWait is the dom window
            this.playState = 1;
        }
        var playState = this.playState;
        var playOptions = {
            position: sPosInMsec,
            whileplaying: function(){

                var sPos = this.position;
                var buffering = this.isBuffering || typeof sPos != 'number' || sPos < sPosInMsec;
                //var buffering = this.isBuffering; //this refers to the soundmanager sound obj
                //Now, what are we doing here below? we could simply check whether is buffering or not..
                //Unfortunately, when buffering some playState (isBuffering = false) are also fired, randomly
                //ONCE in a while
                //the result is a blinking 'isBuffering' 'isPlaying' state in the wait element displaying the state (not so nice),
                //which is also costly in terms of computation. So, we wait for at least N playstate fired SUBSEQUENTLY, without
                //NO bufferingState fired between them. N is set to minimumNumberOfSubsequentPlayCall. When this happens, we can start moving the
                //pointer as a result of a real play state, and we avoid blinking of the wait element
                switch(buffering){
                    case true:
                        switch(playState){
                            case 2: //do nothing (wait element already displaying)
                                break;
                            default: //update the wait element showing it:
                                playState = 2;
                                player.playState = 2;
                                if(bufferingString){
                                    updateWaitBar.apply(player,[bufferingString]);
                                }
                        }
                        break;
                    default:
                        switch(playState){
                            case 0:
                            case 1:
                            case 2: //update waitbar
                                updateWaitBar.apply(player,[player.isImgRefreshing ? player.msgs.imgRefreshing : '']);
                                //currentState = isPlayingId; //set state for future subsequent calls of this case
                                playState = 3;
                                player.playState = 3;
                            default: //move pointer
                                var sPosInSec = toSec(sPos);
                                player.soundPosition = sPosInSec;
                                ruler.movePointer(sPosInSec);
                        }
                        fireOnMarkerPosition(sPosInSec);
                }

            },
            onfinish: function() {
                //whileplaying is NOT called onsinfish. We must update the pointer:
                //note that for small length sounds (wg, 5 secs) the pointer shifts abruptly from the last
                //whileplaying position to the end. We tried with a setTimeout function but the visual effect is not
                //removed. So we leave this small 'bug'
                ruler.movePointer(player.getSoundDuration());
                updateWaitBar.apply(player,[player.isImgRefreshing ? player.msgs.imgRefreshing : '']);
                player.playState = 0;
                player.fire('playbackEndReached');

            //player.fire('endReached');
            }
        };

        //        var playOptions = {
        //            position: sPosInMsec,
        //            whileplaying: function(){
        //                var sPos = this.position;
        //                var buffering = this.isBuffering; //this refers to the soundmanager sound obj
        //                //Now, what are we doing here below? we could simply check whether is buffering or not..
        //                //Unfortunately, when buffering some playState (isBuffering = false) are also fired, randomly
        //                //ONCE in a while
        //                //the result is a blinking 'isBuffering' 'isPlaying' state in the wait element displaying the state (not so nice),
        //                //which is also costly in terms of computation. So, we wait for at least N playstate fired SUBSEQUENTLY, without
        //                //NO bufferingState fired between them. N is set to minimumNumberOfSubsequentPlayCall. When this happens, we can start moving the
        //                //pointer as a result of a real play state, and we avoid blinking of the wait element
        //                switch(buffering){
        //                    case true:
        //                        numberOfSubsequentPlayCall = 0; //reset the count
        //                        switch(currentState){
        //                            case isBufferingId: //do nothing (wait element already displaying)
        //                                break;
        //                            default: //update the wait element showing it:
        //                                currentState = isBufferingId;
        //                                player.playState = 2;
        //                                if(bufferingString){
        //                                    player.setWait(bufferingString);
        //                                }
        //                        }
        //                        break;
        //                    default:
        //                        switch(currentState){
        //                            case uninitializedId:
        //                            case isBufferingId: //in these 2 cases, increment numberOfSubsequentPlayCall
        //                                numberOfSubsequentPlayCall++;
        //                                if(numberOfSubsequentPlayCall == minimumNumberOfSubsequentPlayCall){
        //                                    //if is not buffering, we could skip this. However, there could be the waitbar displaying for some other reason:
        //                                    player.setWait(player.isImgRefreshing ? player.msgs.imgRefreshing : '');
        //                                    currentState = isPlayingId; //set state for future subsequent calls of this case
        //                                    player.playState = 3;
        //                                }else{
        //                                    break; //do not move pointer (default condition below)
        //                                }
        //                            default: //move pointer
        //                                var sPosInSec = toSec(sPos);
        //                                player.soundPosition = sPosInSec;
        //                                ruler.movePointer(sPosInSec);
        //                        }
        //                        fireOnMarkerPosition(sPosInSec);
        //                }
        //
        //            },
        //            onfinish: function() {
        //                //whileplaying is NOT called onsinfish. We must update the pointer:
        //                //note that for small length sounds (wg, 5 secs) the pointer shifts abruptly from the last
        //                //whileplaying position to the end. We tried with a setTimeout function but the visual effect is not
        //                //removed. So we leave this small 'bug'
        //                ruler.movePointer(player.getSoundDuration());
        //                player.setWait(player.isImgRefreshing ? player.msgs.imgRefreshing : '');
        //                player.playState = 0;
        //                pauseFunction('endReached');
        //
        //            //player.fire('endReached');
        //            }
        //        };

        sound.setVolume(sound.volume); //workaround. Just to be sure. Sometimes it fails when we re-play
        sound.play(playOptions);


        return false;
    },

    msgs : {
        loading : 'loading',
        buffering: 'buffering',
        imgRefreshing : 'refreshing img'
    },
    pause: function(){
        var sound = this.getSound();
        //we don't check if it's playing, as the stop must really stop anyway
        //if(sound && this.isPlaying()){
        if(sound){
            var v = this.isPlaying();
            sound.stop();
            this.playState = 0;
            this.fire('paused',{
                'wasPlaying':v
            });
            this.setWait(this.isImgRefreshing ? this.msgs.imgRefreshing : '');
        }
        return false;
    },
    isWaitVisible: function(){
        return this.getContainer().find('.ts-control').find('.ts-wait').is(':visible');
    },
    getWaitString: function(){
        return this.getContainer().find('.ts-control').find('.ts-wait').html();
    },

    setWaitElement: function(element){

    },

    getWaitElement: function(){
        return this.getContainer().find('.ts-control').find('.ts-wait');
    },

    //msg string: undefined: do nothing, empty: hide, otherwise show wait with html = msg
    setWait: function(msg){
        var wait = undefined;
        //        if(typeof msg == 'function'){
        //            wait = msg();
        //            if(wait){
        //                msg = wait.html();
        //            }else{
        //                return;
        //            }
        //        }else{
        wait = this.getWaitElement();
        if(!wait || msg === undefined){
            return;
        }
        if(wait.html()!=msg){
            wait.html(msg);
        }
        //       }

        var visible = wait.css('display') != 'none';
        
        if(msg && !visible){
            wait.show();
            this.fire('waitShown');
        }else if(!msg && visible){
            wait.hide();
            this.fire('waitHidden');
        }
    },

    /**
      * sets whether or not window resize resizes also this player. When true, a variable _dynamicResize =setInterval(...) is attached to
      * this class. When false, if _dynamicResize is in this class, clearInterval(_dynamicResize) is called and then the key is deleted
      */
    setDynamicResize: function(value){
        var key = '_dynamicResize';
        if(!value && key in this){
            clearInterval(this[key]);
            delete this[key];
            return;
        }
        var wdw = this.$J(window);
        var w = wdw.width();
        //var h = wdw.height();
        var me = this;
        this.dynamicResize = setInterval(function(){
            var newW = wdw.width();
            if(w!=newW){
                w = newW;
                //still wait a second: are we still adjusting the window? (call resize just once):
                setTimeout(function(){
                    if(wdw.width()==newW){
                        me.resize.apply(me);
                    }
                },200);
            }
        },100);
    },
    resize: function() {
        this.debug("resizing");
        var height;
        var container = this.getContainer();
        
        var wave = container.find('.ts-wave');

        
        height = wave.height();
        this.debug("wave height:" + height);

        if (height) {

            //set image, imagecontainer and canvas (container on imagecontainer for lines and pointer triangles) css
            var elements = wave.find('.ts-image-container').css('zIndex','0')
            .add(wave.find('.ts-image-canvas').css('zIndex','1')); //the two children of ts-wave. Set also the zIndex
            //in order to visualize the canvas OVER the wav image

            //elements.css('width', 'auto'); // for IE6. We leave it although IE6 is not anymore supported
            var style = {
                width: wave.width(),
                height: height
            }
            elements.css(style);
            elements.css('position','absolute');

        }

        //refreshing images:

        this.refreshImage();
        this.getRuler().resize();
    },
    getImageUrl : function(){
        var image = this.getContainer().find('.ts-image');
        if(image && image.length){
            return image.attr('src');
        }
        return '';
    },
    refreshImage: function(){
        var container = this.getContainer();
        var imageC = container.find('.ts-image-container');
        var image = imageC.find('.ts-image');
        

        var size = this.getImageSize();

        if(!size.width || !size.height){
            return;
        }
        var imgSrc = this.imageCallback(size.width,size.height);
        var imageNotYetCreated = image.length == 0;
        if(!imageNotYetCreated && image.attr('src')==imgSrc){
            return;
        }
        
        var player= this;
        //var waitString = 'refreshing img';
        
        if(imageNotYetCreated){
            image = this.$J('<img/>');
        }

        //image inside ts-image-container:
        image.css({
            'width':'100%',
            'height':'100%'
        }); // for IE7. Does not seem to hurt IE8, FF, Chrome

        var updateWait = function(){};
        var ir = player.msgs.imgRefreshing;
        var we = player.getWaitElement();
        if(ir && we){
            updateWait = function(){
                if(!player.playState || player.playState==3){
                    player.setWait('');
                }
            }
        }
        image.load(function(){
            image.unbind('load');
            if(imageNotYetCreated){
                imageC.append(image.addClass('ts-image'));
            }
            updateWait();
            player.isImgRefreshing = false;
            player.fire('ImgRefreshed');
        });
        if(ir && we && (!this.playState || this.playState===3)){ //if loading (1) or buffering (2) do not update wait.
            //If not playing (undefined or 0) playing (3) update wait
            this.setWait(ir);
        }
        this.isImgRefreshing = true;
        this.fire('ImgRefreshing');
        image.attr('src', imgSrc);
       
    },
    getImageSize: function(){
        var wave = this.getContainer().find('.ts-wave');
        return {
            width: wave.width(),
            height:wave.height()
        }
    },

    setImageSize: function(width,height){
        var container = this.getContainer();
        var wave = container.find('.ts-wave');
        this._setImageSize(width,height,container, wave,true);
    },
    //this is intended to be a private method, use setImageSize from outside the player object)
    _setImageSize: function(width,height,jQueryContainerElement, jQueryWaveElement, resize){
        if(width || height){
            var re = /(?:px|ex|em|%)$/;
            if(width){
                width+='';
                width = re.exec(width) ? width : width+'px';
                jQueryContainerElement.css('width',width);
            }
            if(height){
                height+='';
                height = re.exec(height) ? height : height+'px';
                jQueryWaveElement.css('height',height);
            }
        }
        if(resize){
            this.resize();
        }
    },

    getSoundVolume :function(){
        var s = this.getSound();
        return s ? s.volume : 0;
    },
    //moves the pointer (and sound position) forward till the next marker or the end of sound
    forward: function() {
        var map = this.getMarkerMap();
        var markers = map.toArray();
        var len = markers.length;
        var offset =  this.getSoundDuration();
        var position = this.getSoundPosition(); //parseFloat(this.getSoundPosition());
        var idx = map.insertionIndex(position);
        if(idx<0){
            idx = -idx-1; //cursor is not on a a marker, get the insertion index
        }else{
            //cursor is on a marker. As there might be several markers with the same offset
            //(see MarkerMap.insertionIndex), move to the outmost right
            while(idx<len  && markers[idx].offset == position){
                idx++;
            }
        }
        
        if(idx< len){
            offset = markers[idx].offset;
        }
        this.setSoundPosition(offset);
        return false;
    },
    //moves the pointer (and sound position) backward till the previous marker or the start of sound
    rewind: function() {
        var map = this.getMarkerMap();
        var markers = map.toArray();
        var offset =  0;
        var position = this.getSoundPosition(); //parseFloat(this.getSoundPosition());
        var idx = map.insertionIndex(position);
        if(idx<0){
            idx = -idx-1; //cursor is not on a a marker, get the insertion index
        }else{
            //cursor is on a marker. As there might be several markers with the same offset
            //(see MarkerMap.insertionIndex), move to the outmost left
            while(idx>0  && markers[idx-1].offset == position){
                idx--;
            }
        }
        idx--; //move backward (rewind)
        if(idx>=0){
            offset = markers[idx].offset;
        }
        this.setSoundPosition(offset);
        return false;
    },

    setSoundVolume: function(volume){
        if(typeof volume != 'number'){ //note: typeof for primitive values, instanceof for the rest
            //see topic http://stackoverflow.com/questions/472418/why-is-4-not-an-instance-of-number
            volume = 100;
        }
        if(volume<0){
            volume = 0;
        }else if(volume>100){
            volume = 100;
        }
        volume = Math.round(volume);
        var sound = this.getSound();
        if(sound){
            sound.setVolume(volume);
        }
        var control = this.getContainer().find('.ts-control');
        var volumeSpeaker = control.find('.ts-volume-speaker');
        var volumeBarContainer = control.find('.ts-volume-bar-container');
        var volumeBar = volumeBarContainer.find('.ts-volume-bar');
        if(volume==0){
            volumeSpeaker.removeClass('ts-volume-speaker-on').addClass('ts-volume-speaker-off');
            volumeBar.css('visibility','hidden');
        }else{
            volumeSpeaker.removeClass('ts-volume-speaker-off').addClass('ts-volume-speaker-on');
            volumeBar.css('visibility','visible');
            volumeBar.css({
                'height':'100%',
                'width':volume+'%'
            });
        }
    },

    newMarker: function(offset){
        return {
            offset:offset
        };
    },
    addMarker: function(offset){
        var map = this.getMarkerMap();
        if(map){
            map.add(this.newMarker(offset));
        }
    },

    removeMarker: function(identifier){ //identifier can be an number (marker index) or a marker (the index will be aearched)
        //see marlermap.remove
        var map = this.getMarkerMap();
        if(map){
            map.remove(identifier);
        }
    },

    moveMarker: function(identifier, newOffset){ //identifier can be an number (marker index) or a marker (the index will be aearched)
        var map = this.getMarkerMap();
        if(map){
            //note that map.move does everything BUT moving visually a marker on the ruler
//            var r = this.getRuler();
//            var m = r.toArray()[identifier];
//            m.move(r.toPixelOffset(newOffset)); //TODO: check what happens here inside, no 'fire' hopefully...
            map.move(identifier,newOffset);
        }
    },

    getMarker: function(index){
        var map = this.getMarkerMap();
        if(map){
            return map.toArray()[index];
        }
        return undefined;
    },
    //markers is an array of objects with at least the field offset:sconds.milliseconds
    loadMarkers: function(markers){
        //ruler.bind('markermoved',this.markerMoved,this);
        //var $J = this.$J; //reference to jQuery

        var player = this;
        //initialize the map.
        var map = this.getMarkerMap();
        //var mapUI = this.getMarkersUI();
        var ruler = this.getRuler();
        map.clear();
        ruler.clear();
       
  
        var rulerAdd = ruler.add;
        var debug_ = player.debug; //TODO: remove
            
        if(markers){
            //add markers to the map. No listeners associated to it (for the moment)
            for(var i =0; i< markers.length; i++){
                map.add.apply(map,[markers[i]]);
            }
            //add markers to ruler and div
            map.each(function(i,marker){
                //isEditable and id are added if not present
                rulerAdd.apply(ruler,[marker.offset, i, marker.isEditable]);
            });
        }
        


        //the function above calls map.add:
        //add bindings when adding a marker:
        map.bind('add',function(data){
            //mapuiAdd.apply(mapUI,[data.marker, data.index,data.isNew]);
            rulerAdd.apply(ruler,[data.marker.offset, data.index,data.marker.isEditable]);
            player.fire('markerAdded',data);
            debug_('add');
            debug_(data);
        });

        //2) MOVE

        //add the binding when we move a marker on the ruler:
        ruler.bind('markermoved',function(data){
            var soundPos = data.soundPosition;
            var markerClass = data.markerClass;
            if(markerClass=='pointer'){
                player.setSoundPosition(soundPos);
            }else{
                map.move(data.markerElement.getIndex(), soundPos);
            }
        });

        //and now add a binding to the map when we move a marker:
          
        map.bind('move', function(data){
            consolelog(data);
            var from = data.fromIndex;
            var to = data.toIndex;
            ruler.move.apply(ruler,[from,to,data.marker.offset]);
            player.fire('markerMoved',data);
            debug_('moved');
            debug_(data);
        });

            
        //remove
        map.bind('remove',function(data){
            ruler.remove.apply(ruler, [data.index]);
            player.fire('markerRemoved',data);
            debug_('removed');
            debug_(data);
        });

    }

});