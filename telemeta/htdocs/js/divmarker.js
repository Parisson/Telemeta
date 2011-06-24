/*
 * Copyright (C) 2007-2011 Parisson
 * Copyright (c) 2011 Riccardo Zaccarelli <riccardo.zaccarelli@gmail.com>
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
 * Author: Riccardo Zaccarelli <riccardo.zaccarelli@gmail.com>
 */

/**
 * Class representing a marker div html element for showing/editing a marker on details.
 */
Timeside.classes.MarkerMapDiv = Timeside.classes.TimesideArray.extend({
    init:function(containerDiv){
        this._super();
        var $J = this.$J;

        var div = containerDiv instanceof $J ? containerDiv : $J(containerDiv);
        div = div.length ? div.eq(0) : $J([]); //empty jQuery object
        this.div = div
    },
    //overridden
    add: function(marker, index,  isNew){
       
        var div = this.createMarkerDiv(index, marker);
        if(index==this.length){
            this.div.append(div);
        }else{
            this.$J( this.div.children()[index] ).before(div);
        }
        
        this._super(div,index);
        if(isNew){
            this.setEditMode(index,true);
        }
        if(index<this.length){
            //update indices. Note that this is NOT done at startup as index == this.length ALWAYS
            var t = this;
            var setIdx = t.setIndex;
            this.each(index, function(i, div){
                setIdx.apply(t,[div,i]);
            });
        }
        this.stretch(div.find('.markersdivTitle'));
        this.stretch(div.find('.markersdivDescription'));
        return div;
    },
    //overridden. Do not call explicitly, use marker map.move
    move: function(from, to, newOffset){
        
        //call super method
        to = this._super(from,to);
        if(to<0){
            return -1;
        }

        //reflect the same changes in the document:
        var me = this.toArray();
        if(to!=from){
            var div = me[to]; //me has already been updated
            div.detach();
            var parent = this.div;
            if(to==this.length-1){
                parent.append(div);
            }else{
                this.$J( parent.children()[to] ).before(div);
            }
        }

        var t = this;
        var setIdx = t.setIndex;

        this.each(Math.min(from,to),Math.max(from,to)+1, function(i, div){
            setIdx.apply(t,[div,i]);
        });
        this.setOffset(me[to],newOffset);

        this.setEditMode(to,true);
        return to;
    },
    //overridden
    remove : function(index){
        if(index<0 || index>=this.length){
            return;
        }
        var div = this._super(index);
        div.remove();
        var me = this;
        this.each(index,function(i, div){
            me.setIndex.apply(me,[div,i]);
        });
    },
    //overridden
    makeTimeLabel: function(time){
        return this._super(time,['hh','mm','ss','C']);
    },
    //overridden
    clear: function(){
        var divs = this._super();
        for(var i=0; i< divs.length; i++){
            divs[i].empty().remove();
        }
        return divs;
    },
    //if value is missing, toggles edit mode
    //if editbutton is not present (marker not editable), this method does nothing
    setEditMode: function(index, value){
        
        var div = this.toArray()[index];
        var editButton = div.find('.markersdivEdit');
        if(!((editButton) && (editButton.length))){
            return;
        }
        var visible = editButton.is(':visible');

        if(arguments.length==1){ //toggle
            value = visible; //if edit visible, editmode = true, otherwise false
        }else if(value!=visible){ 
            //value is defined. if true and edit mode is NOT visible, we return cause we are already in edit mode
            //same if false (dont edit) and edit mode is visible (not edit mode)
            return;
        }
        var e_okButton = div.find('.markersdivSave');
        var e_descriptionText = div.find('.markersdivDescription');
        var e_titleText = div.find('.markersdivTitle');
        var mas = div.find(".marker_author_span");
        if(value){
            div.css('backgroundColor','#E65911');
            mas.css('color','#6a0307');
            e_descriptionText.removeAttr('readonly').removeClass('markersdivUneditable');
            e_titleText.removeAttr('readonly').removeClass('markersdivUneditable');
            e_okButton.add(e_okButton.parent()).show(); //hiding also the parent div saves space (padding bottom hidden)
            e_titleText.select(); 
            editButton.hide();
        }else{
            e_descriptionText.attr('readonly','readonly').addClass('markersdivUneditable');
            e_titleText.attr('readonly','readonly').addClass('markersdivUneditable');
            e_okButton.add(e_okButton.parent()).hide(); //hiding also the parent div saves space (padding bottom hidden)
            editButton.show();
            div.css('backgroundColor','');
            mas.css('color','#999'); //TODO: should be set in one declaration only. Change here and also in marker div creation
        }

        this.fire('edit',{'value':value, 'index':index});

        this.stretch(e_titleText);
    },


    setIndex: function(div,index){
        div.find('.ts-marker').html(index+1);
        var me = this;
        var e_indexLabel = div.find('.ts-marker');
        var e_offsetLabel =div.find('.markersdivOffset');
        e_indexLabel.add(e_offsetLabel).unbind('click').click(function(){
            me.fire('focus', {
                'index': index
            });
            return false;
        });
        div.find('.markersdivEdit').unbind('click').click( function(){
            me.setEditMode(index);
            return false; //avoid scrolling of the page on anchor click
        });
    },
    /**
 * stretches jQueryElm the whole possible width. Note that text nodes are not considered!!!!
 */
    stretch: function(jQueryElm){
        var siblings = jQueryElm.siblings(":visible");
        siblings = siblings.add(jQueryElm);
        var spaceStretchable = jQueryElm.parent().width();
        var $J = this.$J;
        siblings.each(function(i,elm){
            spaceStretchable -= $J(elm).outerWidth(true);
        });
        var w = jQueryElm.width() + spaceStretchable;
        jQueryElm.css('width', w+'px');
    },

    setOffset: function(div,offset){
        div.find('.markersdivOffset').html(this.makeTimeLabel(offset));
    },
    createMarkerDiv : function(index, marker){
        //create html content. Use array.join cause it is usually faster than string concatenation:
        var html_ = ['<div style="white-space:nowrap">', //whitespace no wrap is really important to keep all content of first div on one line (without it, IE displays it on 2 lines)
        '<a href=# class="ts-marker"></a>',
        '<a href=# class="markersdivOffset" type="text"></a>',
        '<input class="markersdivTitle" type="text"/>',
        '<a class="markersdivAddPlaylist" title="add to playlist"></a>',
        '<a class="markersdivEdit" title="edit">EDIT</a>',
        '<a class="markersdivDelete" title="delete"></a>',
        '</div>',
        '<div zero_top_padding><textarea class="markersdivDescription"></textarea></div>',
        '<div zero_top_padding><a class="markersdivSave">OK</a></div>',
        '<div zero_top_padding><span class="marker_author_span" style="font-size:75%;color:#999">'+gettrans('author')+': '+marker.author+'</span></div>'].join("");
        var div = this.$J('<div/>').addClass("markerdiv").html(html_); //.attr('tabindex','0')
        div.find('a').attr('href','#');
        
        var e_okButton = div.find('.markersdivSave');
        var e_editButton = div.find('.markersdivEdit');
        var e_deleteButton =  div.find('.markersdivDelete');
        var e_addplaylistButton = div.find('.markersdivAddPlaylist');
        var e_descriptionText = div.find('.markersdivDescription');
        var e_titleText = div.find('.markersdivTitle');

        //set defualt element values regardeless of the marker state (for debugging, comment it if not needed)
        //e_indexLabel.attr('title',marker.toString());
        this.setIndex(div, index);

        this.setOffset(div,marker.offset);
        
        e_descriptionText.val(marker.desc ? marker.desc : "");
        e_titleText.val(marker.title ? marker.title : "");
        
        e_okButton.add(e_okButton.parent()).hide(); //hiding also the parent div saves space (padding bottom hidden)
        e_editButton.show();
        e_deleteButton.show();
        e_addplaylistButton.show();
        e_descriptionText.attr('readonly','readonly').addClass('markersdivUneditable').unbind('focus');
        e_titleText.attr('readonly','readonly').addClass('markersdivUneditable').unbind('focus');

        
        e_addplaylistButton.unbind('click').bind('click',function(evtObj_){
            if(!marker.isSavedOnServer){
                return false;
            }
            //make a request to the server to get the pk (id)
            //note that marker.id (client side) is marker.public_id (server side)
            json([marker.id],"telemeta.get_marker_id", function(data){
                var id = data.result;
                //TODO: we should not call global objects, rather pass them in the construcotr:
                playlistUtils.showAddResourceToPlaylist(e_addplaylistButton,'marker',""+id,gettrans('marker added to the selected playlist'));
            });
            return false;
        });

        if(!marker.canBeAddedToPlaylist){
            e_addplaylistButton.hide();
        }

        if(!marker.canBeSetEditable){ //marker is editable means that author is superuser or author == getCurrentUserName().
            e_editButton.hide();
            e_deleteButton.hide();
            e_okButton.unbind('click')
            e_deleteButton.unbind('click').hide();
            e_editButton.remove(); //so that if edit button is not present, we do not edit (safety reasons) see this.setEditMode
            return div;
        }
        
        var me = this;

        e_deleteButton.unbind('click').click( function(){
            if(!(marker.isSavedOnServer) || confirm(gettrans('delete the marker permanently?'))){
                me.fire('remove',{
                    'marker':marker
                });
            }
            return false; //avoid scrolling of the page on anchor click
        });
        
        //action for ok button
        e_okButton.unbind('click').click( function(){
            //if(marker.desc !== descriptionText.val()){ //strict equality needed. See note below
            marker.desc = e_descriptionText.val();
            marker.title = e_titleText.val();
            me.fire('save',{
                'marker':marker
            });
            return false; //avoid scrolling of the page on anchor click
        });


        e_titleText.keydown(function(event){
            if(e_okButton.is(':visible')){
                if (event.keyCode == '13') {
                    event.preventDefault();
                    e_okButton.trigger('click');
                }
            }
        });

        return div;
    }

});