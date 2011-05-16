
var Ruler = TimesideArray.extend({
    //init constructor: soundDuration is IN SECONDS!!! (float)
    init: function(viewer, soundDuration, isInteractive){
        this._super();
        var cssPref = this.cssPrefix;
        
        this.isInteractive = function(){
            return isInteractive;
        };
        
        this.getSoundDuration= function(){
            return soundDuration;
        };
        
        var waveContainer = viewer.find('.' + cssPref + 'image-canvas');
        this.debug( 'WAVECONTAINER?? LENGTH='+ waveContainer.length);
        this.getWaveContainer =function(){
            return waveContainer;
        };
        //ts-image-canvas has width=0. Why was not the case in old code?
        //BECAUSE IN OLD CODE ts-image-canvas has style="width..height" defined, and not HERE!!!!
        this.getContainerWidth =function(){
            return waveContainer.width();
        };
        
        
        this.debug( 'init ruler: container width '+this.getContainerWidth());
        
        
        //private function used in resize() defined below
        

        var container = viewer.find('.' + cssPref + 'ruler');
        
        this.getRulerContainer = function(){
            return container;
        }


        if(!isInteractive){ //is not interactive, skip all methods assignmenets below
            return;
        }
    },

    resize : function(){
        //code copied from old implementation, still to get completely what is going on here...
        var sectionSteps = [[5, 1], [10, 1], [20, 2], [30, 5], [60, 10], [120, 20], [300, 30],
        [600, 60], [1800, 300], [3600, 600]];
        //old computeLayout code
        var fullSectionDuration,sectionSubDivision, sectionsNum;
        var width = this.getContainerWidth();
        var duration = this.getSoundDuration();
        var cssPref = this.cssPrefix;//defined in superclass
        var fontSize = 10;
        var mfloor = Math.floor; //instanciating once increases performances
        var $J = this.$J; //reference to jQuery
        //this.debug('container width: ' +" "+width);


        var i, ii = sectionSteps.length;
        var timeLabelWidth = this._textWidth('00:00', fontSize);
        for (i = 0; i < ii; i++) {
            var tempDuration = sectionSteps[i][0];
            var subDivision = sectionSteps[i][1];
            var labelsNum = mfloor(duration / tempDuration);
            if ((i == ii - 1) || (width / labelsNum > timeLabelWidth * 2)) {
                fullSectionDuration = tempDuration;
                sectionSubDivision = subDivision;
                sectionsNum = mfloor(duration / fullSectionDuration);
                //this.debug('(in _computeLayout) this.fullSectionDuration: ' + fullSectionDuration);
                //this.debug('(in _computeLayout) sectionsNum: ' +sectionsNum);
                //this.debug('(in _computeLayout) sectionSubDivision: ' +sectionSubDivision);
                break;
            }
        }
        //old draw() code:
        if (!duration) {
            this.debug("Can't draw ruler with a duration of 0");
            return;
        }
        //this.debug("draw ruler, duration: " + duration);

        var container = this.getRulerContainer();
        var layout = container.find("."+cssPref + 'layout');
        //REDONE: if does not exists, create it
        if(!layout || !(layout.length)){
            layout = $J('<div/>')
            .addClass(cssPref + 'layout')
            .css({
                position: 'relative'
            }) // bugs on IE when resizing
            //TODO: bind doubleclick events!!!!!!
            //.bind('dblclick', this.attachWithEvent(this._onDoubleClick))
            //.bind('resize', this.attachWithEvent(this.resize)) // Can loop ?
            .appendTo(container);
        }else{
            //remove all elements neither pointer nor marker
            layout.find(':not(a.ts-pointer,a.ts-marker,a.ts-pointer>*,a.ts-marker>*)').remove();
        }

        //        if (layout && layout.length){
        //            layout.remove();
        //        }
        //        layout = $J('<div/>')
        //        .addClass(cssPref + 'layout')
        //        .css({
        //            position: 'relative'
        //        }) // bugs on IE when resizing
        //        //TODO: bind doubleclick events!!!!!!
        //        //.bind('dblclick', this.attachWithEvent(this._onDoubleClick))
        //        //.bind('resize', this.attachWithEvent(this.resize)) // Can loop ?
        //        .appendTo(container);

        

        //creating sections
        //defining function maketimelabel
        var makeTimeLabel = this.makeTimeLabel;
            
        //defining the function createSection
        var _createSection = function(timeOffset, pixelWidth,timeLabelWidth) {
            var section = $J('<div/>')
            .addClass(cssPref + 'section')
            .css({
                fontSize: fontSize + 'px',
                fontFamily: 'monospace',
                width: pixelWidth,
                overflow: 'hidden'
            })
            .append($J('<div />').addClass(cssPref + 'canvas'));

            var topDiv = $J('<div/>')
            .addClass(cssPref + 'label')
            .appendTo(section);
            var bottomDiv = $J('<div/>')
            .addClass(cssPref + 'lines')
                
            .appendTo(section);
            var empty = $J('<span/>').css({
                visibility: 'hidden'
            }).text('&nbsp;');
            var text;

            if (pixelWidth > timeLabelWidth) {
                text = $J('<span/>')
                .text(makeTimeLabel(timeOffset))
                .bind('mousedown selectstart', function() { //WHY THIS?
                    return false;
                });
            } else {
                text = empty.clone();
            }
            topDiv.append(text);
            bottomDiv.append(empty);
            return section;
        };
        //function defined, creating sections:
        var sections = new Array();
        var currentWidth = 0;
        var sectionDuration, sectionWidth;
        for (i = 0; i <= sectionsNum; i++) {
            if (i < sectionsNum) {
                sectionDuration = fullSectionDuration;
                sectionWidth = mfloor(sectionDuration / duration * width);
            } else {
                sectionDuration = duration - i * fullSectionDuration;
                sectionWidth = width - currentWidth;

            }
            var section = _createSection(i * fullSectionDuration, sectionWidth, timeLabelWidth);
            if (i > 0) {
                section.css({
                    left: currentWidth,
                    top: 0,
                    position: 'absolute'
                });
            }
            section.duration = sectionDuration;
            layout.append(section);
            currentWidth += section.width();
            sections[i] = section;
        }

        //function to draw section rulers:
        var _drawSectionRuler= function(section, drawFirstMark) {
            var j;
               
            var jg = new jsGraphics(section.find('.' + cssPref + 'canvas').get(0));
            jg.setColor(layout.find('.' + cssPref + 'lines').css('color'));
            var height = section.height();
            var ypos;
            for (j = 0; j < section.duration; j += sectionSubDivision) {
                if (j == 0) {
                    if (drawFirstMark) {
                        ypos = 0;
                    } else {
                        continue;
                    }
                } else {
                    ypos = (j == section.duration / 2) ? 1/2 + 1/8 : 3/4;
                }
                //var x = j / this.duration * this.width;
                var x = j / duration * width;
                jg.drawLine(x, height * ypos, x, height - 1);
            }
            jg.paint();
        };
        //draw section rulers
        for (i = 0; i <= sectionsNum; i++) {
            _drawSectionRuler(sections[i], (i > 0));
        }

       
        var pointer = undefined;
        if('getPointer' in this){
            pointer = this.getPointer();
        }
        if(!pointer){
            //consolelog('QUALE CHAZZO E IL CONTAINER??????                  ' + $J(layout.get(0)).attr('class'));
            //            pointer = new RulerMarker($J(layout.get(0)),this.getWaveContainer(),'pointer', true);
            //            pointer.setText(this.makeTimeLabel(0));
            //
            //            this.debug('WELL, ');
            //            consolelog(pointer);
            //            var me = this;
            //            pointer.getLabel().mousedown(function(evt) {
            //                var lbl = $J(evt.target);
            //                me.markerBeingClicked = {
            //                    'marker':pointer,
            //                    'offset':evt.pageX-(lbl.offset().left+lbl.outerWidth(true)/2)
            //                };
            //                consolelog(evt.pageX-(lbl.offset().left+lbl.outerWidth(true)/2));
            //                evt.stopPropagation(); //dont notify the ruler;
            //                return false;
            //            });
            pointer = this.add(0);
            this.getPointer = function(){
                return pointer;
            };
        }else{
            pointer.refreshPosition();
            
        }
        this.each(function(i,rulermarker){
            rulermarker.refreshPosition();
        });

    //            if(!pointer){
    //                this.debug("Creating pointer:"+layout);
    //                //this.createMarkerForRuler = function(rulerLayout,viewer,className, fontSize, optionalToolTip)
    //                pointer = this.createMarkerForRuler($J(layout.get(0)),waveContainer,'pointer',fontSize,'move pointer');
    //                this.debug('pointerdisplay'+pointer.css('display'));
    //            }

    //TODO: move pointer??????
    //this._movePointer(sound.position/1000);


    //TODO: draw markers?
    //            if (this.cfg.map) {
    //                $J(this.markers).each(function(i, m) {
    //                    m.clear();
    //                });
    //                this.markers = new Array();
    //                this.cfg.map.each(this.attach(function(i, m) {
    //                    this.markers.push(this._drawMarker(m, i));
    //                }));
    //            }
    },

    //overridden: Note that the pointer is NOT cleared!!!!!
    clear: function(){
        var markers = this._super();
        //        if('getPointer' in this){
        //            markers.push(this.getPointer());
        //        }
        for( var i=0; i<markers.length; i++){
            markers[i].remove();
        }
        return markers;
    },
    //overridden TimesideArray methods (add, move, remove):
    remove: function(index){
        var rulermarker = this._super(index);
        rulermarker.remove();
        this.each(index, function(i,rulermarker){
            consolelog(i);
            rulermarker.setIndex(i, true);
        });
    },
    //overridden
    move: function(from, to){
        var newIndex = this._super(from,to);
        //this.debug('ruler.move: [from:'+from+', to:'+to+', real:'+newIndex+']');
        if(newIndex!=from){
            var i1 = Math.min(from,newIndex);
            var i2 = Math.max(from,newIndex)+1;
            //this.debug('updating ['+i1+','+i2+']');
            this.each(i1,i2, function(index,rulermarker){
                rulermarker.setIndex(index, true);
            });
        }
    },
    //overridden
    //markerObjOrOffset can be a marker object (see in markermap) or any object with the fields isEditable and offset
    add: function(markerObjOrOffset, indexIfMarker){
        var soundPosition;
        var isMovable;
        var markerClass;

        if(typeof markerObjOrOffset == 'number'){
            soundPosition = markerObjOrOffset;
            isMovable = true; //this.isInteractive();
            markerClass='pointer';
        }else{
            soundPosition = markerObjOrOffset.offset;
            isMovable = markerObjOrOffset.isEditable && this.isInteractive();
            markerClass='marker';
        }
        
        var container = this.getRulerContainer();
        var layout = container.find("."+this.cssPrefix + 'layout');
        var $J = this.$J;
        var pointer = new RulerMarker($J(layout.get(0)),this.getWaveContainer(),markerClass);
        //call super constructor
        //if it is a pointer, dont add it
        if(markerClass != 'pointer'){
            this._super(pointer,indexIfMarker); //add at the end
            //note that setText is called BEFORE move as move must have the proper label width
            this.each(indexIfMarker, function(i,rulermarker){
                rulermarker.setIndex(i,i!=indexIfMarker);
            //rulermarker.setIndex.apply(rulermarker, [i,i!=indexIfMarker]); //update label width only if it is not this marker added
            //as for this marker we update the position below (move)
            });
            this.debug('added marker at index '+indexIfMarker+' offset: '+markerObjOrOffset.offset);
        }else{
            //note that setText is called BEFORE move as move must have the proper label width
            pointer.setText(this.makeTimeLabel(0));
        }
        //proceed with events and other stuff: move (called AFTER setText or setText)
        pointer.move(this.toPixelOffset(soundPosition));
       
        //pointer.setText(markerClass== 'pointer' ? this.makeTimeLabel(0) : this.length);

        //click on labels stop propagating. Always:
        var lbl = pointer.getLabel();
        lbl.bind('click', function(evt){
            evt.stopPropagation();
            return false;
        });

        //if there are no events to associate, return it.
        if(!isMovable){
            return pointer;
        }

        //namespace for jquery event:
        var eventId = 'markerclicked';
        var doc = $J(document);
        
        var me = this;

        var ismovingpointer = false;
        var setmovingpointer = function(value){
            ismovingpointer = value;
        }
        //TODO: this method below private, but how to let him see in the bind below???
        this.setPointerMovingFromMouse = function(value){
            setmovingpointer(value);
        }
        this.isPointerMovingFromMouse = function(){
            return ismovingpointer;
        };
        //functions to set if we are moving the pointer (for player when playing)

        lbl.bind('mousedown.'+eventId,function(evt) {
            
            if(markerClass=='pointer'){
                me.setPointerMovingFromMouse(true);
            }

            var startX = evt.pageX; //lbl.position().left-container.position().left;
            var startPos = lbl.position().left+lbl.width()/2;
            
            evt.stopPropagation(); //dont notify the ruler or other elements;
            var newPos = startPos;
            doc.bind('mousemove.'+eventId, function(evt){
                var x = evt.pageX; 
                newPos = startPos+(x-startX);
                pointer.move(newPos);
                //update the text if pointer
                if(markerClass=='pointer'){
                    pointer.setText(me.makeTimeLabel(me.toSoundPosition(newPos)));
                }
                return false;
                
            });
            //to avoid scrolling
            //TODO: what happens if the user releases the mouse OUTSIDE the browser????
            var mouseup = function(evt_){
                doc.unbind('mousemove.'+eventId);
                doc.unbind('mouseup.'+eventId);
                evt_.stopPropagation();
                if(markerClass=='pointer'){
                    me.setPointerMovingFromMouse(false);
                }
                if(newPos == startPos){
                    consolelog('NOT MOVED!!!!');
                    return false;
                }
                var data = {
                    'markerElement':pointer,
                    'soundPosition': me.toSoundPosition.apply(me,[newPos]),
                    'markerClass':markerClass
                };
                me.fire('markermoved',data);
                return false;
            };
            doc.bind('mouseup.'+eventId, mouseup);
            //lbl.bind('mouseup.'+eventId, mouseup);
            //            doc.bind('mouseup.'+eventId, function(evt){
            //                consolelog(newPos);
            //                doc.unbind('mousemove.'+eventId);
            //                doc.unbind('mouseup.'+eventId);
            //
            //                //TODO: fire event marker moved (with the class name)
            //                var data = {
            //                    'markerElement':pointer,
            //                    'soundPosition': me.toSoundPosition.apply(me,[newPos]),
            //                    'markerClass':markerClass
            //                };
            //                me.fire('markermoved',data);
            //                return false;
            //            });
            return false;
        });
        
        return pointer;


    },

    //moves the pointer, does not notify any listener.
    //soundPosition is in seconds (float)
    movePointer : function(soundPosition) {
        var pointer = this.getPointer();
        if (pointer) {
            var pixelOffset = this.toPixelOffset(soundPosition);
            //first set text, so the label width is set, then call move:
            pointer.setText(this.makeTimeLabel(soundPosition));
            pointer.move(pixelOffset); //does NOT fire any move method
        }
        //this.debug('moving pointer: position set to '+offset);
        return soundPosition;
    },

    //soundPosition is in seconds (float)
    toPixelOffset: function(soundPosition) {
        //this.debug('sPos:' + soundPosition+ 'sDur: '+this.getSoundDuration());
        var duration = this.getSoundDuration();
        if (soundPosition < 0){
            soundPosition = 0;
        }else if (soundPosition > duration){
            soundPosition = duration;
        }
        var width = this.getContainerWidth();
        var pixelOffset = (soundPosition / duration) * width;
        return pixelOffset;
    },

    //returns the soundPosition is in seconds (float)
    toSoundPosition: function(pixelOffset) {
        var width = this.getContainerWidth();

        if (pixelOffset < 0){
            pixelOffset = 0;
        }else if (pixelOffset > width){
            pixelOffset = width;
        }
        var duration = this.getSoundDuration();
        var soundPosition = (pixelOffset / width) *duration;
        return soundPosition;
    }
});


    // TODO: check here
    // http://stackoverflow.com/questions/3299926/ie-mousemove-bug
    // div in IE to receive mouse events must have a background
    // so for the moment



    //        var mouseDown = false;
    //        var _onMouseDown = function(evt) {
    //            mouseDown = true;
    //            this._onMouseMove(evt);
    //            evt.preventDefault(); //If this method is called, the default action of the event will not be triggered.
    //        };
    //        var _onMouseMove = function(evt) {
    //            if (mouseDown) {
    //                var pixelOffset = evt.pageX - container.offset().left;
    //                this._movePointerAndUpdateSoundPosition(pixelOffset / this.width * this.duration);
    //            //moves the pointer and fires onPointerMove
    //            }
    //            return false;
    //        };
    //
    //        var _onMouseUp= function(evt) {
    //            if (mouseDown) {
    //                mouseDown = false;
    //                this.debug('_onMouseUp:'+this.pointerPos+' '+this.cfg.sound.position);
    //            }
    //            return false;
    //        };
    //        var imgContainer = viewer.find('.' + cssPref + 'image-container'); // for IE
    //        var element = waveContainer.add(imgContainer); //constructs a new jQuery object which is the union of the jquery objects
    //
    //        element
    //        .bind('click dragstart', function() {
    //            return false;
    //        })
    //        .bind('mousedown', function(evt){
    //            return _onMouseDown(evt);
    //        })
    //        .bind('mousemove', function(evt){
    //            return _onMouseMove(evt);
    //        })
    //        .bind('mouseup', function(evt){
    //            return _onMouseUp(evt);
    //        });
    //        this.$J(document)
    //        .bind('mousemove', function(evt){
    //            return _onMouseMove(evt);
    //        });