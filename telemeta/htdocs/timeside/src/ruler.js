/**
 * TimeSide - Web Audio Components
 * Copyright (c) 2008-2009 Samalyse
 * Author: Olivier Guilyardi <olivier samalyse com>
 * License: GNU General Public License version 2.0
 */

TimeSide(function($N, $J) {

    $N.Class.create("Ruler", $N.Core, {

        fullSectionDuration: 60,
        sectionSubDivision: 10,
        sectionSteps: [[5, 1], [10, 1], [20, 2], [30, 5], [60, 10], [120, 20], [300, 30],
        [600, 60], [1800, 300], [3600, 600]],
        sectionsNum: 0,
        timeLabelWidth: 0,
        pointerPos: 0,
        layout: null,
        width: null,
        mouseDown: false,
        pointer: null,
        markers: new Array(),
        duration: 0,
        container: null,
        waveContainer: null,

        initialize: function($super, cfg) {
            $super();
            this.configure(cfg, {
                viewer: [null, 'required'],
                fontSize: 10,
                //map: null,
                sound: [null, 'required'],
                soundDurationInMsec:0
            });
            this.cfg.viewer = $J(this.cfg.viewer);
            this.container = this.cfg.viewer.find('.' + $N.cssPrefix + 'ruler');
            this.waveContainer = this.cfg.viewer.find('.' + $N.cssPrefix + 'image-canvas');

            //this.duration = this.cfg.sound.duration/1000; //TODO: improve this function!!
            //note that soundmanager2 returns the duration in milliseconds, while here we compute the
            //layout according to the duration in seconds. Changing all functions it's a pain and it's useless'

            //initialize duration. If sound autoLoad=false, duration is zero and we must use durationEstimate
            //this.duration = this.cfg.sound.duration ? this.cfg.sound.duration : this.cfg.sound.durationEstimate;
            //this
            this.duration = this.cfg.soundDurationInMsec/1000;
            consolelog('duration - - '+this.cfg.sound.duration);
            consolelog('duration -E- '+this.cfg.sound.bytesTotal);
            
            var imgContainer = this.cfg.viewer.find('.' + $N.cssPrefix + 'image-container'); // for IE
            
            this._observeMouseEvents(this.waveContainer.add(imgContainer));

             //this is a workaround: when moving the marker the first time sound.setPosition seems not to work
             //after playing the first time, it works. Or after having set position explicitly, apparently
             //this.cfg.sound.setPosition(0);
        //            this.sp = this._setPosition;
            
        //            this.cfg.sound.whileplaying(function(){
        //                sp(this.position/1000);
        //            });
        //            this.cfg.sound.onfinish(function(){ //when it reaches the end (naturally) force pointer to be at the end
        //                sp(this.duration);
        //            });

        //if (this.cfg.map) {
        //    this.cfg.map
        //.observe('add', this.attach(this._onMapAdd))
        //.observe('remove', this.attach(this._onMapRemove))
        //.observe('indexchange', this.attach(this._onMapIndexChange));
        //}
            
        //this.cfg.soundProvider.observe('update', this.attach(this._onSoundProviderUpdate));
        //this.cfg.soundProvider.observe('play', this.attach(this._onSoundProviderPlaying));
        },

        free: function($super) {
            this.layout = null;
            this.container = null;
            this.waveContainer = null;
            this.cfg.viewer = null;
            $super();
        },

        _computeLayout: function() {
            this.width = this.waveContainer.width();
            this.debug('container width: ' + this.width);
            var i, ii = this.sectionSteps.length;
            this.timeLabelWidth = this._textWidth('00:00', this.cfg.fontSize);
            for (i = 0; i < ii; i++) {
                //                this.debug('step: ' +i+' duration: '+this.sectionSteps[i][0]);
                //                this.debug('step: ' +i+' subdivision: '+this.sectionSteps[i][1]);
                //                this.debug('labelsNum: ' +i+' labelsNum (this.duration/duration): '+Math.floor(this.duration / duration));

                var duration = this.sectionSteps[i][0];
                var subDivision = this.sectionSteps[i][1];
                var labelsNum = Math.floor(this.duration / duration);
                if ((i == ii - 1) || (this.width / labelsNum > this.timeLabelWidth * 2)) {
                    this.fullSectionDuration = duration;
                    this.sectionSubDivision = subDivision;
                    this.sectionsNum = Math.floor(this.duration / this.fullSectionDuration);
                    this.debug('(in _computeLayout) this.fullSectionDuration: ' + this.fullSectionDuration);
                    this.debug('(in _computeLayout) sectionsNum: ' +this.sectionsNum);
                    this.debug('(in _computeLayout) duration: ' +this.duration);
                    break;
                }
            }
        },

        getUnitDuration: function() {
            return this.sectionSubDivision;
        },

        resize: function() {
            //            var pointerVisible = this.pointer && this.pointer.isVisible();
            //            this.debug('resizing (pointer visible: :'+pointerVisible+':');
            //            alert(this.pointer.isVisible());
            this._computeLayout();
            
            this.draw();
            if(this.pointer){
                if(!this.pointer.isVisible()){
                    this.pointer.show();
                }
                //            }
                //            if (pointerVisible) {
                //                this.setPosition(this.cfg.soundProvider.getPosition());
                //                this.setBuffering(this.cfg.soundProvider.isBuffering() && this.cfg.soundProvider.isPlaying());

                this._movePointer(this.cfg.sound.position/1000);
                this.setBuffering(this.cfg.sound.isBuffering && this.cfg.sound.playState==1);
            //Note that playState =  1 may not always guarantee that sound is being heard, given buffering and autoPlay status.
            //(from soundmanager2 tutorial)
            }
        },

//        _setDuration: function(duration) {
//            this.debug('duration setting ruler: ' + duration);
//            this.duration = duration;
//            this._computeLayout();
//        },
//
//        setDuration: function(durationInMillisecs) {
//            var duration = durationInMillisecs ? durationInMillisecs/1000 : 60;
//            if (this.duration != duration) {
//                this._setDuration(duration);
//                this.draw();
//            }
//        },

        _createSection: function(timeOffset, pixelWidth) {
            var section = $J('<div/>')
            .addClass($N.cssPrefix + 'section')
            .css({
                fontSize: this.cfg.fontSize + 'px',
                fontFamily: 'monospace',
                width: pixelWidth,
                overflow: 'hidden'
            })
            .append($J('<div />').addClass($N.cssPrefix + 'canvas'));

            var topDiv = $J('<div/>')
            .addClass($N.cssPrefix + 'label')
            .appendTo(section);
            var bottomDiv = $J('<div/>')
            .addClass($N.cssPrefix + 'lines')
            .appendTo(section);
            var empty = $J('<span/>').css({
                visibility: 'hidden'
            }).text('&nbsp;');
            if (pixelWidth > this.timeLabelWidth) {
                var text = $J('<span/>')
                .text($N.Util.makeTimeLabel(timeOffset))
                .bind('mousedown selectstart', function() {
                    return false;
                });
            } else {
                var text = empty.clone();
            }
            topDiv.append(text);
            bottomDiv.append(empty);
            return section;
        },

        _drawSectionRuler: function(section, drawFirstMark) {
            var j;
            var jg = new jsGraphics(section.find('.' + $N.cssPrefix + 'canvas').get(0));
            jg.setColor(this.layout.find('.' + $N.cssPrefix + 'lines').css('color'));
            var height = section.height();
            var ypos;
            for (j = 0; j < section.duration; j += this.sectionSubDivision) {
                if (j == 0) {
                    if (drawFirstMark) {
                        ypos = 0;
                    } else {
                        continue;
                    }
                } else {
                    ypos = (j == section.duration / 2) ? 1/2 + 1/8 : 3/4;
                }
                var x = j / this.duration * this.width;
                jg.drawLine(x, height * ypos, x, height - 1);
            }
            jg.paint();
        },

        getHeight: function() {
            return this.container.find('' + $N.cssPrefix + '.section').height();
        },

        draw: function() {
            if (!this.duration) {
                this.debug("Can't draw ruler with a duration of 0");
                return;
            }
            this.debug("draw ruler, duration: " + this.duration);
            if (this.layout){
                this.layout.remove();
            }
            this.layout = $J('<div/>')
            .addClass($N.cssPrefix + 'layout')
            .css({
                position: 'relative'
            }) // bugs on IE when resizing
            .bind('dblclick', this.attachWithEvent(this._onDoubleClick))
            //.bind('resize', this.attachWithEvent(this.resize)) // Can loop ?
            .appendTo(this.container);

            //this.container.html(this.layout);

            var sections = new Array();
            var currentWidth = 0;
            var i;
            for (i = 0; i <= this.sectionsNum; i++) {
                if (i < this.sectionsNum) {
                    var duration = this.fullSectionDuration;
                    var width = Math.floor(duration / this.duration * this.width);
                } else {
                    var duration = this.duration - i * this.fullSectionDuration;
                    var width = this.width - currentWidth;

                }
                var section = this._createSection(i * this.fullSectionDuration, width);
                if (i > 0) {
                    section.css({
                        left: currentWidth,
                        top: 0,
                        position: 'absolute'
                    });
                }
                section.duration = duration;
                this.layout.append(section);
                currentWidth += section.width();
                sections[i] = section;
            }

            for (i = 0; i <= this.sectionsNum; i++) {
                this._drawSectionRuler(sections[i], (i > 0));
            }

            this._createPointer();
            //draw markers
            if (this.cfg.map) {
                $J(this.markers).each(function(i, m) {
                    m.clear();
                });
                this.markers = new Array();
                this.cfg.map.each(this.attach(function(i, m) {
                    this.markers.push(this._drawMarker(m, i));
                }));
            }
        //this._drawMarkers();
        },

        //        _drawMarkers: function() {
        //            if (this.cfg.map) {
        //                $J(this.markers).each(function(i, m) {
        //                    m.clear();
        //                });
        //                this.markers = new Array();
        //                this.cfg.map.each(this.attach(function(i, m) {
        //                    this.markers.push(this._drawMarker(m, i));
        //                }));
        //            }
        //        },

        _createPointer: function() {
            if (this.pointer) {
                this.pointer.clear();
            }
            this.pointer = new $N.RulerMarker({
                rulerLayout: this.layout.get(0),
                viewer: this.waveContainer,
                fontSize: this.cfg.fontSize,
                zIndex: 1000,
                top:0,
                className: 'pointer',
                tooltip: 'Move head',
                canMove: true
            });
            //            //create the label
            //            var tsMainLabel = $.find('.' + $N.cssPrefix + 'label');
            //            if(tsMainLabel){
            //                var label = tsMainLabel.find('#' + $N.cssPrefix + 'pointerOffset');
            //                if(!label){
            //                    label = $("<span/>").id('#' + $N.cssPrefix + 'pointerOffset').css('zIndex','10').appendTo(tsMainLabel);
            //                    this.pointer.label = label;
            //                }
            //            }

            this.pointer
            //.setText("+")
            .setText($N.Util.makeTimeLabel(0))
            .observe('move', this.attach(this._onPointerMove));
        },

        //        _setPosition: function(offset) {
        //            this._movePointer(offset);
        ////            if (this.pointer) {
        ////                this.pointer.show();
        ////            }
        //        },
        
    

        

        //        setPosition: function(offset) {
        //            if (!this.mouseDown) {
        //                this._setPosition(offset);
        //            }
        //        },

        //        shiftPosition: function(delta) {
        //            this.setPosition(this.pointerPos + delta);
        //        },

        hidePointer: function() {
            if (this.pointer)
                this.pointer.hide();
        },

        setBuffering: function(state) {
            if (this.pointer) {
                this.pointer.blink(state);
            }
        },
        /*
    _onClick: function(evt) {
        var offset = (evt.pageX - this.container.offset().left) 
            / this.width * this.duration;
        this._setPosition(offset);
        this.fire('move', {offset: offset});
    },
*/
        _onMouseDown: function(evt) {
            this.mouseDown = true;
            this._onMouseMove(evt);
            evt.preventDefault(); //If this method is called, the default action of the event will not be triggered.
        },

       
        _onMouseMove: function(evt) {
            if (this.mouseDown) {
                var pixelOffset = evt.pageX - this.container.offset().left;
                this._movePointerAndUpdateSoundPosition(pixelOffset / this.width * this.duration);
                //moves the pointer and fires onPointerMove
                return false;
            }
        },

        _onMouseUp: function(evt) {
            if (this.mouseDown) {
                this.mouseDown = false;
                this.debug('_onMouseUp:'+this.pointerPos+' '+this.cfg.sound.position);
                //this.debug("mousedup"+this.cfg.sound.position)
            }
            return false;
        },
        //called while playing, does not update sound position
        _movePointer: function(offset) {
            
            if (offset < 0){
                offset = 0;
            }else if (offset > this.duration){
                offset = this.duration;
            }
            var pixelOffset = offset / this.duration * this.width;
            if (this.pointer) {
                this.pointer.move(pixelOffset); //does NOT fire any move method
                this.pointer.setText($N.Util.makeTimeLabel(offset));
            }
            this.pointerPos = offset;
            this.debug('_movePointer: position set to'+offset);
        },
        //called by everything else than playing, same as _movePointer but updates also the sound position accordingly
        _movePointerAndUpdateSoundPosition: function(offset) {
            this._movePointer(offset);
            this.cfg.sound.setPosition(parseInt(1000*this.pointerPos));
        },

         _onPointerMove: function(evt, data) {
            //this.debug('_onPointerMove:'+ this.pointerPos+' '+this.cfg.sound.position);

            this.mouseDown = true;
            this._movePointerAndUpdateSoundPosition(data.offset / this.width * this.duration);
            if(data.finish) {
                //                this.fire('move', {
                //                    offset: this.pointerPos
                //                });
                this.mouseDown = false;
            }
            return false;
        },

        
        _observeMouseEvents: function(element) {
            if(!(CURRENT_USER_NAME)){
                return;
            }
            element
            .bind('click dragstart', function() {
                return false;
            })
            .bind('mousedown', this.attachWithEvent(this._onMouseDown))
            .bind('mousemove', this.attachWithEvent(this._onMouseMove))
            .bind('mouseup', this.attachWithEvent(this._onMouseUp));
            $J(document)
            .bind('mousemove', this.attachWithEvent(this._onMouseMove));
        },

        _drawMarker: function(marker, index) {
            if (marker.offset < 0){
                marker.offset = 0;
            }else if (marker.offset > this.duration){
                marker.offset = this.duration;
            }
            
            pixelOffset = marker.offset / this.duration * this.width;
            
            m = new $N.RulerMarker({
                rulerLayout: this.layout.get(0),
                viewer: this.waveContainer,
                fontSize: this.cfg.fontSize,
                className: 'marker',
                index: index,
                tooltip: 'Move marker',
                canMove: marker.isEditable
            });
            
            if(marker.isEditable){
                m.observe('move', this.attach(this._onMarkerMove))
            }
            //m.observe('move', this.attach(this._onMarkerMove))
            m
            //.setText(index + 1)
            .move(pixelOffset)
            .show();
            return m;
        },

        _onMarkerMove: function(e, data) {
            if (data.finish) {
                var offset = data.offset / this.width * this.duration;
                this.fire('markermove', {
                    index: data.index,
                    offset: offset
                });
            }
        },
        
        //called from markermap after we retrieved the marker index:
        onMapAdd: function(marker, index){
            this.markers.splice(index, 0, this._drawMarker(marker, index));
        },

        //        _onMapAdd2: function(e, data) {
        //            this.markers.push(this._drawMarker(data.marker, data.index));
        //        },

        remove: function(index){
            var rulermarker = this.markers[index];
            rulermarker.clear();
            this.markers.splice(index, 1);
        },
        
        //it is assured that fromIndex!=toIndex and fromIndex!=toIndex+1 (see markermap.move)
        //        move: function(fromIndex, toIndex){
        //            var m = this.markers.splice(fromIndex,1)[0]; //remove
        //            this.markers.splice(toIndex,0,m); //add
        //        },

        updateMarkerIndices:function(fromIndex, toIndex){
            for(var i=fromIndex; i<=toIndex; i++){
                this.markers[i].setIndex(i);
            }
        },

        _onDoubleClick: function(evt) {
            if (CURRENT_USER_NAME) {
                var offset = (evt.pageX - this.container.offset().left)
                / this.width * this.duration;
                this.fire('markeradd', {
                    offset: offset
                });
            }
        }

    //        , _onSoundProviderUpdate: function(e) {
    //            this.debug("spupdate");
    //
    //            //this.setDuration(this.cfg.soundProvider.getDuration());
    //            this.setPosition(this.cfg.soundProvider.getPosition());
    //            this.setBuffering(this.cfg.soundProvider.isBuffering() && this.cfg.soundProvider.isPlaying());
    //        }
    });

    $N.notifyScriptLoad();

});


