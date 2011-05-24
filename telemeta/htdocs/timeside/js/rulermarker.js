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
 * Class representing a RulerMarker in TimesideUI
 * Requires jQuery wz_jsgraphics and all associated player classes
 */

var RulerMarker = TimesideClass.extend({

    class2CanvasColor: {
        'pointer':'#a10006',
        'marker':'#e65911'
    },

    init: function(rulerDiv, waveImgDiv, className) {
        this._super();
        var $J = this.$J;
        var fontSize = 10;
        this.getFontSize = function(){
            return fontSize;
        }

        var zIndex = 1000;
        var tooltip = '';

        var cssPref = this.cssPrefix;

        var label = $J('<a/>')
        .css({
            display: 'block',
            width: fontSize +'px',
            textAlign: 'center',
            position: 'absolute',
            fontSize: fontSize + 'px',
            fontFamily: 'monospace',
            top: 0
        })
        .attr('href', '#')
        .addClass(cssPref + className)
        .html('<span>0</span>'); //the text inside the span is FUNDAMENTAL, although it will be replaced later,
        //to calculate now the label position (see below *)
       
        
        if (tooltip){
            label.attr('title', tooltip);
        }

        if(rulerDiv.css('position')!='relative'){
            rulerDiv.css({
                'position':'relative'
            });
        }
        rulerDiv.append(label);

       
        if(className != "pointer"){
            label.css('top',rulerDiv.height()-label.outerHeight());
        }
        
        var style = {};
        if (zIndex) {
            style.zIndex = zIndex;
            label.css(style);
        }
        
        //set the index,
        var index = -1;
        this.setIndex = function(idx, optionalUpdateLabelWidth){
            index = idx;
            this.setText(idx+1, optionalUpdateLabelWidth ? true : false);
        };
        this.getIndex = function(){
            return index;
        }

        //end=======================================================
        //creating public methods:
        this.getLabel = function(){
            return label;
        }


        this.getRulerWidth = function(){
            return rulerDiv.width();
        }
        this.getWaveHeight = function(){
            return waveImgDiv.height();
        }

        this.positionInPixels = 0;
        this.positionAsViewerRatio = 0;

        var tW = 2*((fontSize - 1) >>> 1)+1; //if fontsize:10 or 9, tW:9, if fontSize:8 or 7, tW:7, and so on
        
        var fillColor = this.class2CanvasColor[className];
        var canvas = undefined;
        if(this.isSvgSupported()){
            canvas = this.createCanvasSvg(waveImgDiv, tW);
            var path = canvas.childNodes[0]; //note that $J(canvas).find('path') does not work in FF at least 3.5
            path.setAttributeNS(null,'fill',fillColor);
            path.setAttributeNS(null,'stroke-width',0);
            this.moveCanvas = function(pixelOffset){
                //consolelog(pixelOffset);
                canvas.setAttributeNS( null, "transform", "translate("+pixelOffset+",0)");
            }
            this.jQueryCanvas = $J(canvas);
        }else{
            canvas = this.createCanvasVml(waveImgDiv, tW);
            this.jQueryCanvas = $J(canvas.node);
            var attributes = {
                'stroke-width':'0',
                'fill':fillColor
            };
            canvas.attr(attributes); //Raphael method
            this.moveCanvas = function(pixelOffset){
                //for some reason, coordinates inside the VML object are stored by raphael with a zoom of 10:
                this.jQueryCanvas.css('left',(10*pixelOffset)+'px');
            }
            //apparently, when resizing the markers loose their attributes. Therefore:
            var r = this.refreshPosition; //reference to current refreshPosition
            this.refreshPosition = function(){
                r.apply(this);
                canvas.attr(attributes);
            }
        }
    },

    //sets the text of the marker, if the text changes the marker width and optionalUpdateLabelPosition=true,
    //re-arranges the marker position to be center-aligned with its vertical line (the one lying on the wav image)
    setText: function(text, optionalUpdateLabelPosition) {
        var label = this.getLabel();
        if (label) {
            text += '';
            var labelWidth = this.textWidth(text, this.getFontSize()) + 10;
            var oldWidth = label.width();
            if (oldWidth != labelWidth) {
                label.css({
                    width: labelWidth+'px'
                });
            }
            label.find('span').html(text);
            if(oldWidth != labelWidth && optionalUpdateLabelPosition){
                this.refreshLabelPosition();
            }
        }
        return this;
    },


    getNodes: function(){
        return this.$J([]);
    //return this.$J(this.getPainter().cnv).children();
    },
    //these methods are executed only if marker is movable (see Ruler.js)

    move : function(pixelOffset) {
        var width =  this.getRulerWidth();
        if (this.positionInPixels != pixelOffset) {
            if (pixelOffset < 0) {
                pixelOffset = 0;
            } else if (pixelOffset >= width) {
                pixelOffset = width - 1;
            }
           //defined in the conmstructor (it depends on wehter the current browser supports SVG or not)
            this.moveCanvas(pixelOffset);
           
            this.positionInPixels = pixelOffset;
            this.refreshLabelPosition(width);
            //store relative position (see refreshPosition below)
            this.positionAsViewerRatio = pixelOffset == width-1 ? 1 : pixelOffset/width;
        }
        return this;
    },

    refreshLabelPosition : function(optionalContainerWidth){
        if(!(optionalContainerWidth)){
            optionalContainerWidth = this.getRulerWidth();
        }
        var label = this.getLabel();
        var width = optionalContainerWidth;
        var pixelOffset = this.positionInPixels;
        var labelWidth = label.outerWidth(); //consider margins and padding //label.width();
        var labelPixelOffset = pixelOffset - labelWidth / 2;
        if (labelPixelOffset < 0){
            labelPixelOffset = 0;
        }else if (labelPixelOffset + labelWidth > width){
            labelPixelOffset = width - labelWidth;
        }
        label.css({
            left: this.mRound(labelPixelOffset) + 'px'
        });

    },

    //function called on ruler.resize. Instead of recreating all markers, simply redraw them
    refreshPosition : function(){
        var width =  this.getRulerWidth();
        //store relativePosition:
        var rp = this.positionAsViewerRatio;
        this.move(this.mRound(this.positionAsViewerRatio*width));
        //reset relative position, which does not have to change
        //but in move might have been rounded:
        this.positionAsViewerRatio = rp;
    },

    
    remove : function() {
        var label = this.getLabel();
        label.remove();
        this.jQueryCanvas.remove(); //defined in the constructor
        return this;
    },


    createCanvasSvg: function(container, arrowBaseWidth){
        //<path fill="#0000ff" stroke="#000000" d="M0,0L9,0L4.5,5Z" style="stroke-width: 0px; left: 100px; position: absolute;" stroke-width="0" x="100px"></path>
        var $J = this.$J;
        var svgNS = "http://www.w3.org/2000/svg";
        var d = document;
        var svg = undefined;
        if(container.children().length>0){
            svg = container.children().get(0);
        }else{
            svg = d.createElementNS(svgNS, "svg:svg");
            container.append($J(svg));
        }
            var group = d.createElementNS(svgNS, "svg:g");
            group.setAttributeNS( null, "transform", "translate(0,0)");

            var path = d.createElementNS(svgNS, "svg:path");
            path.setAttributeNS( null, "d", this.createCanvasPath(0,arrowBaseWidth));
            
            group.appendChild(path);
            svg.appendChild(group);
       
        return group;
    //return $J('<path/>').attr('fill',fillColor).attr('style','fill:'+fillColor+';strokeWidth:0');
    },

    createCanvasVml: function(container, arrowBaseWidth){
        //for creating a vml object, we make use of raphael to avoid a pain in the ... implementing a non standard Microsoft syntax
        //(which, after a glance, it's even syntactically a mess)
        //unfotunately (and this is a real lack not even planned to be fixed, see raphael forums),
        //raphael does not allow to wrap existing object, so we have to register in this.elementToPaperMap (see timeside.js)
        //which is a map where to each container is associated a raphael paper:
        var paper = this.elementToPaperMap && this.elementToPaperMap[container.get(0)];
        if(!paper){ 
            var obj = this.elementToPaperMap;
            if(!obj){
                this.elementToPaperMap = {};
                obj = this.elementToPaperMap;
            }
            paper = Raphael(container.get(0),container.width(),container.height());
            obj[container.get(0)] = paper;
            //paper canvas is a div with weird dimensions. You can check it by printing paper.canvas.outerHTML in IE.
            //We set them to 100% so we dont have clipping regions when resizing (maximizing)
            paper.canvas.style.width='100%';
            paper.canvas.style.height='100%';
            paper.canvas.width='100%';
            paper.canvas.height='100%';
        //apparently, there is also a clip style declaration. The following code trhows an error in IE7:
        //paper.canvas.style.clip = 'auto';
        //however, even leaving the clip style declaration as it is, it seems to work (the div spans the whole width)
        }
        
        
        var shape = paper.path(this.createCanvasPath(0, arrowBaseWidth));
        return shape;
    },

    //w must be odd. Cause le central line must be centered. Example:
    //
    //      xxxxx
    //       xxx
    //        x
    //        x
    //        x
    //
    createCanvasPath: function(x,w){
        var halfW = w >>> 1;
        var h = this.$J(window).height();
        return 'M '+(x-halfW)+' 0 L '+(x)+' '+(halfW)+' L '+x+' '+h+
        ' L '+ (x+1)+' '+h+' L '+(x+1)+ ' '+(halfW)+' L '+(x+halfW+1)+' 0 z';
    },

    //used for faster lookup
    mRound: Math.round

});
