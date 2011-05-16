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

    init: function(rulerLayout, viewer, className) {
        this._super();
        var $J = this.$J;
        var fontSize = 10;
        this.getFontSize = function(){
            return fontSize;
        }
        var zIndex = 1000;
        var tooltip = '';
        //TODO: why viewer get(0) ? more than one? check and maybe simplify
        var painter = new jsGraphics(viewer.get(0));
        //from create (oldCode)
        var cssPref = this.cssPrefix;
        var y = rulerLayout.find('.' + cssPref + 'label').outerHeight();
        //added by me:================
        if(className == "pointer"){
            y = 0;
        }
        //==========================
        var label = $J('<a/>')
        .css({
            display: 'block',
            width: '10px',
            textAlign: 'center',
            position: 'absolute',
            fontSize: fontSize + 'px',
            fontFamily: 'monospace',
            top: y + 'px'
        })
        .attr('href', '#')
        .addClass(cssPref + className)
        .append('<span />')
        //.hide();

        if (tooltip){
            label.attr('title', tooltip);
        }

        rulerLayout.append(label);
        
        var height = viewer.height();
        var x = 0;
        painter.drawLine(x, 0, x, height);
        
        x     = [-4, 4, 0];
        y = [0, 0, 4];

        painter.fillPolygon(x, y);
        painter.paint();
        var nodes = $J(painter.cnv).children();

        var style = {};
        if (zIndex) {
            style.zIndex = zIndex;
            label.css(style);
        }
        style.backgroundColor = '';
        //nodes.hide();
        nodes.css(style).addClass(cssPref + className)
        .each(function(i, node) {
            node.originalPosition = parseInt($J(node).css('left'));
        });

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
        
        this.getViewer = function(){
            return viewer;
        }
        this.getPainter = function(){
            return painter;
        }

        this.positionInPixels = 0;
        this.positionAsViewerRatio = 0;

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
        return this.$J(this.getPainter().cnv).children();
    },
    //these methods are executed only if marker is movable (see Ruler.js)

    move : function(pixelOffset) {
        var width =  this.getViewer().width();
        if (this.positionInPixels != pixelOffset) {
            if (pixelOffset < 0) {
                pixelOffset = 0;
            } else if (pixelOffset >= width) {
                pixelOffset = width - 1;
            }
            var nodes = this.getNodes();
            var $J = this.$J;
            var mRound = this.mRound;
            nodes.each(function(i, node) {
                $J(node).css('left', mRound(node.originalPosition + pixelOffset) + 'px');
            });
            this.positionInPixels = pixelOffset;
            this.refreshLabelPosition(width);
            //store relative position (see refreshPosition below)
            this.positionAsViewerRatio = pixelOffset == width-1 ? 1 : pixelOffset/width;
        }
        return this;
    },

    refreshLabelPosition : function(optionalContainerWidth){
        if(!(optionalContainerWidth)){
            optionalContainerWidth = this.getViewer().width();
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
        var width =  this.getViewer().width();
        //store relativePosition:
        var rp = this.positionAsViewerRatio;
        this.move(this.mRound(this.positionAsViewerRatio*width));
        //reset relative position, which does not have to change
        //but in move might have been rounded:
        this.positionAsViewerRatio = rp;
        //last thing: resize the vertical line.
        //Assumptions (having a look at the web page element with a debugger and the code above
        //which uses jsgraphics):
        //The line is the first item (see drawLine above)
        //not only the height, but also the height of the clip property must be set
        var h = this.getViewer().height();
        var nodes = this.getNodes();
        var $J = this.$J;
        $J(nodes[0]).css({
            'height':h+'px',
            'clip': 'rect(0px 1px '+h+'px 0px)'
        });
    },

    remove : function() {
        var $J = this.$J;
        var painter = this.getPainter();
        var label = this.getLabel();
        painter.clear();
        $J(painter.cnv).remove();
        label.remove();
        return this;
    },

    mRound: Math.round

});
