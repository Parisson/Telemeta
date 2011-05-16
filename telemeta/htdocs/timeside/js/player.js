var Player = TimesideClass.extend({
    
    //sound duration is in milliseconds because the soundmanager has that unit,
    //player (according to timeside syntax) has durations in seconds
    init: function(container, sound, soundDurationInMsec, itemId, visualizers, currentUserName) {
        this._super();
        this.ready = false;
        var player = this;

        //container is the div #player
        
        if (!container){
            this.debug('ERROR: container is null in initializing the player')
        }
        this.getItemId = function(){
            return itemId;
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
        var map = new MarkerMap(this.getItemId(), currentUserName);
        this.getMarkerMap = function(){
            return map;
        }
        var mapUI = new MarkerMapDiv(currentUserName);
        this.getMarkersUI = function(){
            return mapUI;
        }
        this.getCurrentUserName = function(){
            return currentUserName;
        }
    //TODO: define setUpInterface here????

    },

  

    setupInterface: function() {
        
        var sound = this.getSound();
        consolelog('player _setupInterface sound.readyState:'+sound.readyState); //handle also cases 0 and 2????
        
        var $J = this.$J; //defined in the super constructor
        var me=this;
        //image source (see below) is given a src with a temporary 1x1 pixels transparent image
        //see http://www.nczonline.net/blog/2009/11/30/empty-image-src-can-destroy-your-site/ and
        //http://geekswithblogs.net/bcaraway/archive/2007/08/24/114945.aspx
        //for details
        var html = ["<div class='ts-viewer'>",
        "<div class='ts-ruler'></div>",
        "<div class='ts-wave'>",
        "<div class='ts-image-canvas'></div>",
        "<div class='ts-image-container'>",
        "<img class='ts-image' src='/images/transparent.png' alt='' />",
        "</div>",
        "</div>",
        "</div>",
        "<div class='ts-control'>",
        "<div class='ts-layout'>",
        "<div class='ts-playback'>",
        "<a class='ts-play'></a>",
        "<a class='ts-pause'></a>",
        "<a class='ts-rewind'></a>",
        "<a class='ts-forward'></a>",
        "<a class='ts-set-marker'></a>",
        "<a class='ts-volume'></a>",
        "<img class='ts-wait'/>",
        "<select class='ts-visualizer'></select>",
        "</div>",
        "</div>",
        "</div>"];

        this.getContainer().html(html.join(''));
        var container = this.getContainer();
       

        var rewind = container.find('.ts-rewind');
        var forward = container.find('.ts-forward');
        var play = container.find('.ts-play');
        var pause = container.find('.ts-pause');
        var volume = container.find('.ts-volume');


        //hide the wait image and set the src
        var waitImg = container.find('.ts-wait');
        waitImg.attr('src','/images/wait_small.gif').attr('title','refreshing image').attr('alt','refreshing image').hide();

        //setting the select option for visualizers:
        var visualizers = this.getVisualizers();
        var select = container.find('.ts-visualizer');
        for(var name in visualizers){
            //$J('<option/>').val(visualizers[name]).html(name).appendTo(select);
            $J('<option/>').html(name).appendTo(select);
        }
        //assigning event on select:
        select.change(
            function (){
                me.refreshImage.apply(me);
            });

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

        //assigning title to all anchors
        container.find('a').attr('href', '#')
        .each(function(i, a){
            a = $J(a);
            a.attr('title', a.attr('class').substring(3));
        });
        
        //creating the ruler
        var viewer = container.find('.ts-viewer');
        var ruler = new Ruler(viewer, this.getSoundDuration(), (this.getCurrentUserName() || false));
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
        //NOTE: loadMarkers ASYNCHRONOUSLY CALLS THE SERVER, SO METHODS WRITTEN AFTER IT MIGHT BE EXECUTED BEFORE
        //loadMarkers has finished its job
        this.loadMarkers();

    //set the marker popup
    //functions to set the marker popup
    //        var popupMarker = $J('<div/>').addClass('component').css({
    //            'dislay':'none',
    //            'position':'absolute',
    //            'zIndex':1000,
    //            'overflow':'auto',
    //            'display':'none' //TODO: remove this
    //        //'backgroundColor':'#666'
    //        });
    //        $J('body').append(popupMarker);
    //        var w = v.width();
    //        var h = v.height();
    //        var offs = v.offset(); //relative to the document
    //        var width = parseInt(w/2);
    //        var height = parseInt(h/2);
    //        var margin = 5;
    //        popupMarker.css({
    //            'left':(margin+offs.left+width)+'px',
    //            'top': parseInt(margin+offs.top)+'px',
    //            'width':width+'px',
    //            'height':height+'px'
    //        });
    //        popupMarker.html("<table style='width:100%'><tr><td>"+gettrans('title')+"</td><td class='title'></td></tr><tr><td>"+
    //            gettrans('description')+"</td><td class='description'></td></tr></table>");
    //        this.getMarkerPopup = function(){
    //            return popupMarker;
    //        }
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
        var image = container.find('.ts-image');
        height = wave.height();
        this.debug("wave height:" + height);
        if (!height) {
            //this.debug('ERROR: image height is zero in player.,resize!!!!')
            height = image.height();
        }
        //set image, imagecontainer and canvas (container on imagecontainer for lines and pointer triangles) css
        var elements = image
        .add(container.find('.ts-image-container'))
        .add(container.find('.ts-image-canvas'));

        elements.css('width', 'auto'); // for IE6

        if (!height){
            height = 200;
        }
        var style = {
            width: wave.width(),
            height: height
        }
        elements.css(style);

        
        //refreshing images:
        this.refreshImage(image);
        this.getRuler().resize();


        //adjusting select size:
        var select = container.find('.ts-visualizer');
        var imgWait = container.find('.ts-wait');

        //NOTE: some buttons might be hidden AFTER THIS METHOD HAS BEEN INVOKED
        //Therefore, setting the width of select or imgWait is skipped for the moment.
        select.css('fontSize','90%'); //this is to increase probability that the select width will fit the available space

        var control = container.find('.ts-control');
        var maxHeight = control.height();
        select.add(imgWait).css('maxHeight',(maxHeight-2)+'px'); //at least a margin left and top of 1 px (see below)

        var span = (maxHeight-select.outerHeight())/2; //do not include margins in oputerHeight (we will set them to zero below)
        select.css({'margin':'0px', 'marginTop':span+'px','marginLeft':span+'px'});
        var span2 = (maxHeight - imgWait.outerHeight())/2; //do not include margins in oputerHeight (we will set them to zero below)
        imgWait.css({'margin':'0px', 'marginTop':span2+'px','marginLeft':span+'px'})

        
        return this;
    },

    //    getImageUrl: function(){
    //        return this.$J('#visualizer_id').get(0).value;
    //    },
    refreshImage: function(optionalImgJQueryElm){
        var image;
        var container = this.getContainer();
        if(optionalImgJQueryElm){
            image = optionalImgJQueryElm;
        }else{
            image = container.find('.ts-image');
        }
        var select = container.find('.ts-visualizer');
        var funcImg = function(player_image_url, width, height){
            var _src_ = null;
            if (player_image_url && (width || height)) {
                _src_ = player_image_url.replace('WIDTH', width + '').replace('HEIGHT', height + '');
            }
            return _src_;
        };
        var imageUrl = this.getVisualizers()[""+select.val()];
        //consolelog(this.getVisualizers());
        //alert(imageUrl);
        var imgSrc = funcImg(imageUrl, image.width(),image.height());
        if(image.attr('src')==imgSrc){
            // consolelog('setting attrt');
            return;
        }
        var w =select.width();
        var h = select.height();
        select.hide();
        var progressBar = container.find('.ts-wait').css({
            'width':w+'px',
            'height':h+'px'
        }).show();

        image.load(function(){
            progressBar.hide();
            select.show();
            image.unbind('load');
        });
        //this timeout is set in order to leave the time to hide show components above:
        //setTimeout(function(){
        image.attr('src', imgSrc);
    //},100);
       
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

        var volumeElm = this.getContainer().find('.ts-volume');
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
        
    loadMarkers: function(){
        //ruler.bind('markermoved',this.markerMoved,this);
        var $J = this.$J; //reference to jQuery
        var isInteractive_ = this.getCurrentUserName() || false;
        var itemId = this.getItemId();

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
            var setMarkerButton = player.getContainer().find('.ts-set-marker');
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

            $J('#loading_span').empty().remove();
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