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
        
       
        //CODE HERE BELOW IS EXECUTED ONLY IF THE MARKER HAS CAN MOVE IMPLEMENTED.
        //Otherwise, no mouse event can call these methods
        //re-implement function move
        var position = 0;
        var relativePosition = 0; //position in percentage of container width, set it in move and use it in refreshPosition
        
        var mRound = Math.round; //instantiate the functio once

        this.move = function(pixelOffset) {
            var width =  viewer.width();
            if (position != pixelOffset) {
                if (pixelOffset < 0) {
                    pixelOffset = 0;
                } else if (pixelOffset >= width) {
                    pixelOffset = width - 1;
                }
                nodes.each(function(i, node) {
                    $J(node).css('left', mRound(node.originalPosition + pixelOffset) + 'px');
                });
                position = pixelOffset;
                this.refreshLabelPosition(width);
                //store relative position (see refreshPosition below)
                relativePosition = pixelOffset == width-1 ? 1 : pixelOffset/width;
            }
            return this;
        };

        this.refreshLabelPosition = function(optionalContainerWidth){
            if(!(optionalContainerWidth)){
                optionalContainerWidth = viewer.width();
            }
            var width = optionalContainerWidth;
            var pixelOffset = position;
            var labelWidth = label.outerWidth(); //consider margins and padding //label.width();
            var labelPixelOffset = pixelOffset - labelWidth / 2;
            if (labelPixelOffset < 0){
                labelPixelOffset = 0;
            }else if (labelPixelOffset + labelWidth > width){
                labelPixelOffset = width - labelWidth;
            }
            label.css({
                left: mRound(labelPixelOffset) + 'px'
            });

        };

        //function called on ruler.resize. Instead of recreating all markers, simply redraw them
        this.refreshPosition = function(){
            var width =  viewer.width();
            //store relativePosition:
            var rp = relativePosition;
            this.move(mRound(relativePosition*width));
            //reset relative position, which does not have to change
            //but in move might have been rounded:
            relativePosition = rp;
            //last thing: resize the vertical line.
            //Assumptions (having a look at the web page element with a debugger and the code above
            //which uses jsgraphics):
            //The line is the first item (see drawLine above)
            //not only the height, but also the height of the clip property must be set
            var h = viewer.height();
            $J(nodes[0]).css({
                'height':h+'px',
                'clip': 'rect(0px 1px '+h+'px 0px)'
            });
        }

        this.remove = function() {
            painter.clear();
            $J(painter.cnv).remove();
            label.remove();
            return this;
        };
    },

    //sets the text of the marker, if the text changes the marker width and optionalUpdateLabelPosition=true,
    //re-arranges the marker position to be center-aligned with its vertical line (the one lying on the wav image)
    setText: function(text, optionalUpdateLabelPosition) {
        var label = this.getLabel();
        if (label) {
            text += '';
            var labelWidth = this._textWidth(text, this.getFontSize()) + 10;
            var oldWidth = label.width();
            if (oldWidth != labelWidth) {
                label.css({
                    width: labelWidth+'px'
                });
            }
            label.find('span').html(text);
            if(oldWidth != labelWidth && optionalUpdateLabelPosition){
                consolelog('refreshing label position');
                this.refreshLabelPosition();
            }
        }
        return this;
    }

});
