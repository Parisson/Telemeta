var Player = TimesideClass.extend({
    
    //sound duration is in milliseconds because the soundmanager has that unit,
    //player (according to timeside syntax) has durations in seconds
    init: function(container, sound, soundDurationInMsec,visualizers) {
        this._super();
        var player = this;
        
        if (!container){
            this.debug('ERROR: container is null in initializing the player')
        }
        this.getContainer = function(){
            return container;
        }
        this.getSound = function(){
            return sound;
        }
        
        this.getVisualizers = function(){
            return visualizers;
        }


        //rpivate functions for converting
        //soundmanager has milliseconds, we use here seconds
        var pInt = Math.round; //instantiate once for faster lookup
        var pFloat = parseFloat; //instantiate once for faster lookup
        function toMsec(seconds){
            return pInt(seconds*1000);
        }
        function toSec(msec){
            return pFloat(msec)/1000;
        }


        var sd = toSec(soundDurationInMsec);
        this.getSoundDuration = function(){
            return sd;
        }
       
        this.isPlaying = function(){
            /*Numeric value indicating the current playing state of the sound.
             * 0 = stopped/uninitialised
             * 1 = playing or buffering sound (play has been called, waiting for data etc.)
             *Note that a 1 may not always guarantee that sound is being heard, given buffering and autoPlay status.*/
            return sound && sound.playState==1;
        };

        var currentMarkerIndex=0;
        this.getCurrentMarkerIndex = function(){
            return currentMarkerIndex;
        };

        //setting the position===============================================
        //if sound is not loaded, position is buggy. Moreover, we have to handle the conversions between units: 
        //seconds (here) and milliseconds (swmanager sound). So we store a private variable
        //private variable and function
        var soundPos = sound.position ? toSec(sound.position) : 0.0;
        //private method: updates just the internal variable (called in whilePlaying below)
        function setPos(value){
            soundPos = value;
            var map = player.getMarkerMap();
            if(map){
                currentMarkerIndex = map.insertionIndex(value);
                if(currentMarkerIndex<0){ //see markermap.insertionindex
                    currentMarkerIndex = -currentMarkerIndex-1;
                }
            }
        }
        //public methods: calls setPos above AND updates sounbd position
        this.setSoundPosition = function(newPositionInSeconds){
            //for some odd reason, if we set sound.setPosition here soundPos
            //is rounded till the 3rd decimal integer AND WILL BE ROUNDED THIS WAY IN THE FUTURE
            //don't know why, however we set the sound position before playing (see below)
            //however, now it works. Even odder....
            setPos(newPositionInSeconds);
            if(sound){
                var s = toMsec(this.getSoundPosition());
                sound.setPosition(s);
            }
        }
        //public methods: returns the sound position
        this.getSoundPosition = function(){
            return soundPos;
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
        
        //implement play here: while playing we do not have to update the sound position, so
        //we call the private variable soundPos
        this.play = function(){
            if(!player || player.isPlaying()){ //TODO: remove?, multishot is set to false
                return false;
            }
            var sound = player.getSound();
            if(!sound){
                return false;
            }

            var ruler = player.getRuler();
            
            var playOptions = {
                whileplaying: function(){
                    var sPos = toSec(this.position); //this will refer to the sound object (see below)
                    setPos(sPos);
                    if(ruler && !ruler.isPointerMovingFromMouse()){
                        ruler.movePointer(sPos);
                    }
                    
                    player.showMarkerPopup(currentMarkerIndex);
                },
                onfinish: function() {
                    setPos(0); //reset position, not cursor, so that clicking play restarts from zero
                }
            };
            //internal play function. Set all properties and play:
            var play_ = function(sound, positionInSec){
                //consolelog('position is '+positionInSec+' sec');
                sound.setPosition(toMsec(positionInSec)); //TODO: remove???
                //consolelog('sound position is '+sound.position+' msec');
                sound.setVolume(sound.volume); //workaround. Just to be sure. Sometimes it fails when we re-play
                playOptions.position = toMsec(positionInSec); //apparently THIS IS WORKING
                sound.play(playOptions);
            };
           
            play_(sound, player.getSoundPosition());
            
            return false;
        };
        //now implement also pause here: note that pause has some odd behaviour.
        //Try this sequence: play stop moveforward moveback play pause
        //When we press the last pause the sound restarts (??!!!!)
        this.pause = function(){
            var sound = this.getSound();
            //we don't check if it's playing, as the stop must really stop anyway
            //if(sound && this.isPlaying()){
            sound.stop();
            //}
            return false;
        };

        //initializing markermap and markerui
        var map = new MarkerMap();
        this.getMarkerMap = function(){
            return map;
        }
        var mapUI = new MarkerMapDiv();
        this.getMarkersUI = function(){
            return mapUI;
        }
    //TODO: define setUpInterface here????

    },

  

    _setupInterface: function(isInteractive) {
        
        this.isInteractive = function(){
            return isInteractive;
        }

        var sound = this.getSound();
        consolelog('player _setupInterface sound.readyState:'+sound.readyState); //handle also cases 0 and 2????
        
        var $J = this.$J; //defined in the super constructor
        var me=this;
        //TODO: use cssPrefix or delete cssPrefix!!!!!
        //TODO: note that ts-viewer is already in the html page. Better avoid this (horrible) method and use the html
        var skeleton =  {
            'div.ts-viewer': {
                'div.ts-ruler': {},
                'div.ts-wave': {
                    'div.ts-image-canvas': {},
                    'div.ts-image-container': ['img.ts-image']
                }
            },
            'div.ts-control': {
                'div.ts-layout': {
                    'div.ts-playback': ['a.ts-play', 'a.ts-pause', 'a.ts-rewind', 'a.ts-forward', 'a.ts-set-marker' //]
                    ,'a.ts-volume','select.visualizer']
                }
            }/*,
        'div.marker-control': ['a.set-marker']*/
        };
        var jQueryObjs = this.loadUI(this.getContainer(), skeleton);

            

        this.getElements = function(){
            return jQueryObjs;
        }



        var rewind = jQueryObjs.find('.ts-rewind');
        var forward = jQueryObjs.find('.ts-forward');
        var play = jQueryObjs.find('.ts-play');
        var pause = jQueryObjs.find('.ts-pause');
        var volume = jQueryObjs.find('.ts-volume');


        //setting the select option for visualizers:
        var visualizers = this.getVisualizers();
        var select = jQueryObjs.find('.visualizer');
        for(var name in visualizers){
            $J('<option/>').val(visualizers[name]).html(name).appendTo(select);
        }
        select.css('margin',0).css('marginLeft','5px');
        //TODO: why the line below does not work?!!!!!
        //jQueryObjs.find('.ts-control')
        var control = $J('#player').find('.ts-control');
        var span = control.height() - select.outerHeight(true);
        consolelog()
        if(span>1){
            select.css('marginTop',(span/2)+'px');
        }
        select.change(
            function (){
                
                var img = $J('<img/>').attr("src","/images/wait_small.gif").css(
                {
                    'marginLeft':select.css('marginLeft'),
                    'marginTop':select.css('marginTop'),
                    'height' :select.height()+'px',
                    'width':select.width()+'px'
                });
                select.hide();
                img.insertBefore(select);
                setTimeout(function(){
                    if (me){
                        me.refreshImage();
                    }
                    //img.remove();
                    setTimeout(function(){
                        img.remove();
                        select.show();
                    },150);
                },300);
            });


        //setting events to buttons (code left untouched from olivier):
        //rewind
        //
        //(olivier comment) IE apparently doesn't send the second mousedown on double click:
        //        var jump = $J.browser.msie ? 'mousedown dblclick' : 'mousedown';
        //        rewind.attr('href', '#').bind(jump, this.attach(this._onRewind))
        //        .click(function() {
        //            return false;
        //        });
        //        //forward:
        //        forward.attr('href', '#').bind(jump, this.attach(this._onForward))
        //        .click(function() {
        //            return false;
        //        });
        
        //attaching event to the image. Note that attaching an event to a transparent div is buggy in IE
        //        if($J.browser.msie){
        //
        //        }
       

        var rewind_ = this.rewind;
        var forward_ = this.forward;
        rewind.attr('href', '#').click(function(e){
            rewind_.apply(me);
            return false;
        });
        forward.attr('href', '#').click(function(e){
            forward_.apply(me);
            return false;
        });

        //volume:
        function setVolume(event){
            var ticks = [18,26,33,40,47];
            var vol = event.layerX;
            for(var i=0; i<ticks.length; i++){
                if(vol<=ticks[i]){
                    var volume = i*20;
                    me.setSoundVolume(volume);
                    me.debug('setting volume'+volume);
                    return false;
                }
            }
            me.setSoundVolume(100);
            return false;
        }
        volume.attr('href', '#').click(function(event){
            return setVolume(event);
        });
        //        volume.attr('href', '#').click(function(){
        //            return false;
        //        }).bind('mousedown', this.attach(
        //            function(e){
        //                if(e.which===1){ //left button
        //                    this.setVolume(e);
        //                }
        //                return false;
        //            }
        //            ));

        //assigning title to all anchors
        jQueryObjs.attr('href', '#')
        .each(function(i, a){
            a = $J(a);
            a.attr('title', a.attr('class').substring(3));
        });
        
        //creating the ruler

        //TODO: why the line below does not work?!!!!!
        //var viewer = jQueryObjs.find('.ts-viewer');
        var viewer = this.getContainer().find('.ts-viewer');
        var ruler = new Ruler(viewer, this.getSoundDuration(), isInteractive);
        this.getRuler = function(){
            return ruler;
        }
        
        this.resize(); //which calls also ruler.resize() (see below)

        //TODO: here? maybe in the constructor
        this.setSoundVolume(this.getSoundVolume());


        //bind events to play and pause.
        //pause:
        var pause_ = me.pause;
        pause.attr('href', '#').bind('click', function(){
            pause_.apply(me);
            return false;
        });
        //play:
        var play_ = me.play;
        play.attr('href', '#').bind('click', function(){
            play_.apply(me);
            return false;
        });

        //binds click for the pointer: TODO: change this way of getting the tsviweer!!!!
        var v = $J('#player').find('.ts-viewer');
        v.unbind('click').click(function(evt){
            var w = v.width();
            var x = evt.pageX - v.offset().left; //using absolute coordinates allows us to
            //avoid checking whether or not we are clicking on a vertical marker line, on a subdiv etcetera
            var sd = me.getSoundDuration();
            me.setSoundPosition(sd*x/w);
            ruler.movePointer(ruler.toSoundPosition(x));
        });
       

        //finally, load markers and bind events for markers (see method below):
        this.loadMarkers(isInteractive);

        //set the marker popup
        //functions to set the marker popup
        var popupMarker = $J('<div/>').addClass('component').css({
            'dislay':'none',
            'position':'absolute',
            'zIndex':1000,
            'overflow':'auto',
            'display':'none' //TODO: remove this
        //'backgroundColor':'#666'
        });
        $J('body').append(popupMarker);
        var w = v.width();
        var h = v.height();
        var offs = v.offset(); //relative to the document
        var width = parseInt(w/2);
        var height = parseInt(h/2);
        var margin = 5;
        popupMarker.css({
            'left':(margin+offs.left+width)+'px',
            'top': parseInt(margin+offs.top)+'px',
            'width':width+'px',
            'height':height+'px'
        });
        popupMarker.html("<table style='width:100%'><tr><td>"+gettrans('title')+"</td><td class='title'></td></tr><tr><td>"+
            gettrans('description')+"</td><td class='description'></td></tr></table>");
        this.getMarkerPopup = function(){
            return popupMarker;
        }
    },

    showMarkerPopup: function(markerIndex){
    //        var popup = this.getMarkerPopup();
    //
    //        if(popup.attr('id') != 'markerpopup'+markerIndex){
    //
    //            var marker = this.getMarkerMap().toArray()[markerIndex];
    //            var pos = this.getSoundPosition();
    //            var mPos = marker.offset;
    //            var span = 0.3;
    //
    //            if(pos>=mPos-span && pos<=mPos+span){
    //                consolelog('songpos: '+pos+' nextmarkerpos:'+mPos);
    //                popup.attr('id','markerpopup'+markerIndex);
    //                popup.find('.title').html(marker.title);
    //                popup.find('.description').html(marker.desc);
    //                if(!popup.is(':visible')){
    //                    popup.show('fast');
    //                }
    //            }
    //        }
    },


    setDynamicResize: function(value){
        var key = '_dynamicResize';
        if(!value && key in this){
            clearInterval(this[key]);
            delete this[key];
            return;
        }
        var wdw = this.$J(window);
        var w = wdw.width();
        var h = wdw.height();
        var me = this;
        this.dynamicResize = setInterval(function(){
            var newW = wdw.width();
            if(w!=newW){
                w = newW;
                //still wait a second: are we still adjusting the window? (call resize just once):
                setTimeout(function(){
                    if(wdw.width()==newW){
                        me.resize.apply(me);
                    }else{
                        consolelog('resizing in act');
                    }
                },150);
            }
        },250);
    },

    resize: function() {
        this.debug("resizing");
        var height;
        var playerelements = this.getElements();
        var wave = playerelements.find('.ts-wave');
        var image = playerelements.find('.ts-image');
        height = wave.height();
        this.debug("wave height:" + height);
        if (!height) {
            this.debug('ERROR: image height is zero in player.,resize!!!!')
            height = image.height();
        }
        //set image, imagecontainer and canvas (container on imagecontainer for lines and pointer triangles) css
        var elements = image
        .add(playerelements.find('.ts-image-container'))
        .add(playerelements.find('.ts-image-canvas'));

        elements.css('width', 'auto'); // for IE6

        if (!height){
            height = 200;
        }
        var style = {
            width: wave.width(),
            height: height
        }
        elements.css(style);
        //this.imageWidth = style.width;
        //this.imageHeight = style.height;
        //refreshing images
        //        var funcImg = function(player_image_url, width, height){
        //            var _src_ = null;
        //            if (player_image_url && (width || height)) {
        //                _src_ = player_image_url.replace('WIDTH', width + '').replace('HEIGHT', height + '');
        //            }
        //            return _src_;
        //        };
        //        var imgSrc = funcImg(this.getImageUrl(), style.width,style.height);
        //        if(image.attr('src')!=imgSrc){
        //            image.attr('src', imgSrc);
        //        }
        this.refreshImage(image);
        this.getRuler().resize();
        return this;
    },

    //    getImageUrl: function(){
    //        return this.$J('#visualizer_id').get(0).value;
    //    },
    refreshImage: function(optionalImgJQueryElm){
        var image;
        if(optionalImgJQueryElm){
            image = optionalImgJQueryElm;
        }else{
            image = this.getElements().find('.ts-image');
        }
        var funcImg = function(player_image_url, width, height){
            var _src_ = null;
            if (player_image_url && (width || height)) {
                _src_ = player_image_url.replace('WIDTH', width + '').replace('HEIGHT', height + '');
            }
            return _src_;
        };
        var imageUrl = this.getElements().find('.visualizer').val();
        //alert(imageUrl);
        var imgSrc = funcImg(imageUrl, image.width(),image.height());
        if(image.attr('src')!=imgSrc){
            // consolelog('setting attrt');
            image.attr('src', imgSrc);
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
        //consolelog('current pointer position: '+position+' '+(typeof position));
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
        this.getRuler().movePointer(offset);
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
        this.getRuler().movePointer(offset)
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
        var sound = this.getSound();
        //        if(sound.volume == volume){
        //            return;
        //        }
        sound.setVolume(volume);
        //update the anchor image:
        var indices = [20,40,60,80,100,100000];

        var volumeElm = this.getElements().find('.ts-volume');
        for(var i=0; i <indices.length; i++){
            if(volume<indices[i]){
                var pos = -28*i;
                pos = '0px '+ pos+ 'px'; //DO NOT SET !important as in FF3 DOES NOT WORK!!!!!
                volumeElm.css('backgroundPosition',pos);
                return;
            }
        }
    // this.elements.volume.css('backgroundPosition','0px 0px !important')

    },
        
    loadMarkers: function(isInteractive_){
        //ruler.bind('markermoved',this.markerMoved,this);
        var $J = this.$J; //reference to jQuery

        var itemId = ITEM_PUBLIC_ID;

        var player = this;
        //initialize the map.
        var map = this.getMarkerMap();
        var mapUI = this.getMarkersUI();
        var ruler = this.getRuler();
        map.clear();
        mapUI.clear();
        ruler.clear();
        
        //building the onSuccess function
        var onSuccess = function(data) {
            var tabIndex = 0;
            var mapuiAdd = mapUI.add;
            var rulerAdd = ruler.add;

            if(data && data.result && data.result.length>0){
                var result = data.result;
                //add markers to the map. No listeners associated to it (for the moment)
                var mapAdd = map.add;
                for(var i =0; i< result.length; i++){
                    mapAdd.apply(map,[result[i]]);
                }
                //add markers to ruler and div
                map.each(function(i,marker){
                    rulerAdd.apply(ruler,[marker, i]);
                    mapuiAdd.apply(mapUI,[marker, i]);
                });

                tabIndex = result.length>0 ? 1 : 0;
            }
            //BINDINGS:
            //
            //1) ADD
            //
            //add binding to the setMarker button (html anchor):
            var setMarkerButton = player.getElements().find('.ts-set-marker');
            var tab = $J('#tab_markers');
            if(setMarkerButton){
                if(isInteractive_){
                    setMarkerButton.show().attr('href','#').unbind('click').bind('click', function(){
                        if(tab && tab.length){
                            tab.trigger('click');
                        }
                        map.add(player.getSoundPosition());
                        return false;
                    });
                }else{
                    setMarkerButton.hide().unbind('click');
                }
            }

                    
            //the function above calls map.add:
            //add bindings when adding a marker:
            map.bind('add',function(data){
                mapuiAdd.apply(mapUI,[data.marker, data.index,data.isNew]);
                rulerAdd.apply(ruler,[data.marker, data.index]);
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
            var rulerMove = ruler.move;
            var mapuiMove = mapUI.move;
                   
            map.bind('move', function(data){
                var from = data.fromIndex;
                var to = data.toIndex;
                rulerMove.apply(ruler,[from,to]);
                mapuiMove.apply(mapUI,[from,to,data.newOffset]);
            });
                    
            //3) EVENTS ON MARKERDIV: SAVE AND REMOVE
            //save - UI delegates the map:
            var mapSave = map.save;
            mapUI.bind('save',function(data){
                mapSave.apply(map,[data.marker]);
            });
            //and map delegates back to the UI:
            var mapuiSetEditMode = mapUI.setEditMode;
            map.bind('save',function(data){
                mapuiSetEditMode.apply(mapUI,[data.index,false]);
            });

            //remove - UI delegates the map:
            var mapRemove = map.remove;
            mapUI.bind('remove',function(data){
                mapRemove.apply(map,[data.marker]);
            });
            //and, again, map delegates back to the UIs:
            var mapuiRemove = mapUI.remove;
            var rulerRemove = ruler.remove;
            map.bind('remove',function(data){
                mapuiRemove.apply(mapUI, [data.index]);
                rulerRemove.apply(ruler, [data.index]);
            });

            //finally, focus events (WHEN the user CLICKS on a textinput or a textarea on a markerdiv)
            mapUI.bind('focus', function(data){
                if(data && 'index' in data){
                    if(data.index>=0 && data.index<map.length){
                        var offset = map.toArray()[data.index].offset;
                        player.setSoundPosition(offset);
                        player.getRuler().movePointer(offset);
                    }
                }
            });

            jQuery('#loading_span').empty().remove();
            //TODO: move this in load_player?
            //                    setUpPlayerTabs([jQuery('#tab_analysis'), jQuery('#tab_markers')],
            //                    [jQuery('#analyzer_div_id'), jQuery('#markers_div_id')], tabIndex,
            //                    'tab_selected','tab_unselected');
            setUpPlayerTabs($J('#tab_analysis').add($J('#tab_markers')),
                [$J('#analyzer_div_id'), $J('#markers_div_id')], tabIndex,
                'tab_selected','tab_unselected');
        };
        json([itemId],"telemeta.get_markers", onSuccess);
    }
});