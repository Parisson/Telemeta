/**
 * TimeSide - Web Audio Components
 * Copyright (c) 2008-2009 Samalyse
 * Author: Riccardo Zaccarelli
 * License: GNU General Public License version 2.0
 */

TimeSide(function($N, $J) {

    $N.Class.create("DivMarker", $N.Core, {
        //static constant variables to retireve the Marker Html Elements (MHE)
        //to be used with the function below getHtmElm, eg:
        //getHtmElm(marker, this.MHE_OFFSET_LABEL)
        e_indexLabel:null,
        e_descriptionText:null,
        e_offsetLabel:null,
        e_deleteButton:null,
        e_okButton:null,
        e_header:null,
        e_editButton:null,
        e_titleText:null,
        me:null,
        markerMap:null,

        initialize: function($super, markermap) {
            $super();
            //sets the fields required???? see ruler.js createPointer
            this.configure({
                //why instantiating a variable to null?
                parent: [null, 'required']
            });
            this.cfg.parent = $J("#markers_div_id");
            this.markerMap = markermap;
            this.me = this.createDiv();
            this.cfg.parent.append(this.me);
        },


        //creates a new div. By default, text is hidden and edit button is visible
        createDiv: function(){
            
            var div = this.cfg.parent;
            var markerDiv;
            if(div){
                
                //index label
                this.e_indexLabel = $J('<span/>')
                .addClass('markersdivIndexLabel')
                .addClass('markersdivTopElement');

                //offset label
                this.e_offsetLabel = $J('<span/>')
                .addClass('markersdivTopElement')
                .addClass('markersdivOffset')
                

                //title text
                this.e_titleText = $J('<input/>')
                .attr('type','text')
                .addClass('markersdivTitle')
                .addClass('markersdivTopElement')
                

                //close button
                this.e_deleteButton = $J('<a/>')
                .addClass('markersdivDelete')
                .addClass('markersdivTopElement')
                .attr('title','delete marker')
                .attr("href","#")
               
                //edit button
                this.e_editButton = $J('<a/>')
                .addClass('roundBorder4')
                .addClass('markersdivEdit')
                .addClass('markersdivTopElement')
                .attr('title','edit marker description')
                .attr("href","#")
                .html('<span>EDIT</span>')
                                

                //add all elements to header:
                this.e_header = $J('<div/>').css('margin','1ex 0ex 0.5ex 0ex')
                .append(this.e_indexLabel)
                .append(this.e_offsetLabel)
                .append(this.e_titleText)
                .append(this.e_deleteButton)
                .append(this.e_editButton);
                
                //description text
                this.e_descriptionText = $J('<textarea/>')
                .addClass('markersdivDescription')

                //ok button
                this.e_okButton = $J('<a/>')
                .attr('title','save marker description and offset')
                .addClass('markersdivSave')
                .attr("href","#")
                .html("OK");
                

                //create marker div and append all elements
                markerDiv = $J('<div/>')
                .append(this.e_header)
                .append(this.e_descriptionText)
                //.append(this.e_okButton)
                .append($J('<div/>').css('margin','1ex 0ex 1ex 0ex').append(this.e_okButton))
                .addClass('roundBorder8')
                .addClass('markerdiv');

            //set default visibility

            }
            return markerDiv;
        },

        updateMarkerIndex: function(index){
            var map = this.markerMap;
            var marker = map.get(index);

            //set defualt element values regardeless of the marker state
            this.e_indexLabel.attr('title',marker.toString());
            this.e_indexLabel.html("<span>"+(index+1)+"</span>");
            this.e_offsetLabel.html(this.formatMarkerOffset(marker.offset));
            //move the div to the correct index
            var divIndex = this.me.prevAll().length;
            //move the div if necessary:
            //note that moving left to right the actual insertionIndex is index-1
            //because we will first remove the current index
            var insertionIndex = index>divIndex ? index-1 : index;
            if(insertionIndex!=divIndex){
                this.me.detach();//The .detach() method is the same as .remove(), except that .detach() keeps
                //all jQuery data associated with the removed elements
                $( this.cfg.parent.children()[insertionIndex] ).before(this.me); //add
            }
            
            //set visibility and attach events according to the marker state:
            //first, is editing or not
            var isEditing = marker.isEditable && marker.isModified;
            //            (!marker.isSavedOnServer || !(this.e_editButton.is(':visible')));

            if(!isEditing){
                this.e_descriptionText.val(marker.desc ? marker.desc : "");
                this.e_titleText.val(marker.title ? marker.title : "");
            }

            this.e_okButton.hide();
            this.e_editButton.show();
            this.e_deleteButton.show();
            this.e_descriptionText.attr('readonly','readonly').addClass('markersdivUneditable');
            this.e_titleText.attr('readonly','readonly').addClass('markersdivUneditable');
            

            if(!marker.isEditable){
                this.e_editButton.hide();
                this.e_deleteButton.hide();
                //we unbind events to be sure
                this.e_okButton.unbind('click')
                this.e_deleteButton.unbind('click').hide();
                this.e_editButton.unbind('click').hide();
                return;
            }
            
            var remove = map.remove;
            this.e_deleteButton.unbind('click').click( function(){
                if(!(marker.isSavedOnServer) || confirm('delete the marker permanently?')){
                    remove.apply(map,[index]);
                }
                return false; //avoid scrolling of the page on anchor click
            })


            //notifies controller.js
            //                this.fire('remove', {
            //                    index: index
            //                });

            var dText = this.e_descriptionText;
            var tText  = this.e_titleText;
            var okB = this.e_okButton;
            var utw = this.updateTitleWidth;
            var divmarker = this;
            var eB = this.e_editButton;
            var startEdit = function(){
                marker.isModified = true;
                dText.removeAttr('readonly').removeClass('markersdivUneditable').show();
                tText.removeAttr('readonly').removeClass('markersdivUneditable').show();
                okB.show();
                eB.hide();
                utw.apply(divmarker,[tText]);
            };
            
            this.e_editButton.unbind('click').click( function(){
                startEdit();
                divmarker.focusOn();
                return false; //avoid scrolling of the page on anchor click
            });
            
            //action for ok button
            this.e_okButton.unbind('click').click( function(){
                //if(marker.desc !== descriptionText.val()){ //strict equality needed. See note below
                marker.desc = dText.val();
                marker.title = tText.val();
                map.sendHTTP(marker,
                    
                    function(){
                        dText.attr('readonly','readonly').addClass('markersdivUneditable');
                        tText.attr('readonly','readonly').addClass('markersdivUneditable');
                        eB.show();
                        okB.hide();
                        utw.apply(divmarker,[tText]);
                    },
                    true
                    );
                return false; //avoid scrolling of the page on anchor click
            });
            
            if(isEditing){
                startEdit();
            }else{
                this.updateTitleWidth();
            }
            
        },

        focusOn: function(){
            this.me.css('backgroundColor','#f5f5c2');
            this.e_titleText.select();
        },

        focusOff: function(){
            this.me.css('backgroundColor','');
        },

        updateTitleWidth: function(tText){
            if(!(tText)){
                tText = this.e_titleText;
            }
            if(tText){
                var w = tText.parent().width();
                w-=tText.outerWidth(true)-tText.width(); //so we consider also tText margin border and padding
                var space = w
                - (this.e_indexLabel.is(':visible') ? this.e_indexLabel.outerWidth(true) : 0)
                - (this.e_offsetLabel.is(':visible') ? this.e_offsetLabel.outerWidth(true) : 0)
                - (this.e_editButton.is(':visible') ? this.e_editButton.outerWidth(true) : 0)
                - (this.e_deleteButton.is(':visible') ? this.e_deleteButton.outerWidth(true) : 0);
                tText.css('width',space+'px');
            }
        },

        remove: function(){
            this.me.remove();
            this.e_indexLabel = null;
            this.e_descriptionText=null;
            this.e_offsetLabel=null;
            this.e_deleteButton=null;
            this.e_okButton=null;
            this.e_header=null;
            this.e_editButton=null;
            this.e_titleText=null;
            this.me=null;
        },

        formatMarkerOffset: function(markerOffset){
            //marker offset is in float format second.decimalPart
            var hours = parseInt(markerOffset/(60*24));
            markerOffset-=hours*(60*24);
            var minutes = parseInt(markerOffset/(60));
            markerOffset-=minutes*(60);
            var seconds = parseInt(markerOffset);
            markerOffset-=seconds;
            var msec = Math.round(markerOffset*100); //show only centiseconds
            //(use 1000* to show milliseconds)
            var format = (hours<10 ? "0"+hours : hours )+":"+
            (minutes<10 ? "0"+minutes : minutes )+":"+
            (seconds<10 ? "0"+seconds : seconds )+"."+
            (msec<10 ? "0"+msec : msec );
            return format;
        }
   


    });

    $N.notifyScriptLoad();

});


Object.prototype.toString = function(){
    var s="";
    for(var k in this){
        s+=k+": "+this[k]+"\n";
    }
    return s;
}