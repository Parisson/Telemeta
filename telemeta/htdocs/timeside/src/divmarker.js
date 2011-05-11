/**
 * TimeSide - Web Audio Components
 * Copyright (c) 2011 Parisson
 * Author: Riccardo Zaccarelli
 * License: GNU General Public License version 2.0
 */

/**
 * Class for showing/editing a marker on details. 
 */
var MarkerMapDiv = TimesideArray.extend({
    init:function(currentUserName){
        this._super();
        this.div = this.$J("#markers_div_id");
        this.getCurrentUserName = function(){
            return currentUserName;
        }
    },
    //overridden
    add: function(marker, index,  isNew){
         
        var div = this.createMarkerDiv(index, marker);
        if(index==this.length){
            this.div.append(div);
        }else{
            this.$J( this.div.children()[index] ).before(div);
        }
        //this.setIndex(this.length-1,d); //length has been increased when calling super
        this._super(div,index);
        if(isNew){
            this.setEditMode(index,true);
            this.setFocus(index,true);
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
    //overridden
    move: function(from, to, newOffset){

        //call super method
        var realIndex = this._super(from,to);
        //reflect the same changes in the document:
        var me = this.toArray();
        if(realIndex!=from){
            var div = me[realIndex]; //me has already been updated
            div.detach();
            var parent = this.div;
            if(to==this.length){
                parent.append(div);
            }else{
                this.$J( parent.children()[realIndex] ).before(div);
            }
        }

        var t = this;
        var setIdx = t.setIndex;

        this.each(Math.min(from,realIndex),Math.max(from,realIndex)+1, function(i, div){
            setIdx.apply(t,[div,i]);
        });

        this.setOffset(me[realIndex],newOffset);

        //TODO: create a function?
        this.setEditMode(realIndex,true);
        this.setFocus(realIndex,true);
        return realIndex;
    },
    //overridden
    remove : function(index){
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
        if(value){
            this.debug('setting editmode');
            div.css('backgroundColor','#E65911');
            e_descriptionText.removeAttr('readonly').removeClass('markersdivUneditable');
            e_titleText.removeAttr('readonly').removeClass('markersdivUneditable');
            e_okButton.add(e_okButton.parent()).show(); //hiding also the parent div saves space (padding bottom hidden)
            e_titleText.select(); //TODO: this does NOT set the focus on the div. Why?
            editButton.hide();
        //e_titleText.focus();
        }else{
            e_descriptionText.attr('readonly','readonly').addClass('markersdivUneditable');
            e_titleText.attr('readonly','readonly').addClass('markersdivUneditable');
            consolelog(e_okButton.parent());
            e_okButton.add(e_okButton.parent()).hide(); //hiding also the parent div saves space (padding bottom hidden)
            editButton.show();
            div.css('backgroundColor','');
        }

        //var e_addplaylistButton = div.find('.markersdivAddPlaylist');

        this.setFocus(index,value);
        this.stretch(e_titleText);
    },

    

    setFocus: function(index,value){
    //        this.each(function(i,div){
    //            if(i==index && value){
    //                div.css('backgroundColor','#E65911'); //'#f5cf23'
    //            }else{
    //                div.css('backgroundColor','');
    //            }
    //        });
    },


    setIndex: function(div,index){
        //div.attr('id','_markerdiv'+index);
        div.find('.ts-marker').html(index+1);
        var me = this;
        var e_indexLabel = div.find('.ts-marker');
        var e_offsetLabel =div.find('.markersdivOffset');
        e_indexLabel.add(e_offsetLabel).unbind('click').click(function(){
            me.setFocus(index,true);
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
        //consolelog("\t"+spaceStretchable+' elm:'+$J(elm).attr('class')+" left: "+$J(elm).position().left+" outerw:" +$J(elm).outerWidth(true)+" w: "+$J(elm).width());
        });
        //consolelog('w'+ jQueryElm.parent().width()+' elm.w: '+jQueryElm.width()+' spacestretchable: '+spaceStretchable);
        var w = jQueryElm.width() + spaceStretchable;
        jQueryElm.css('width', w+'px');
    },

    setOffset: function(div,offset){
        div.find('.markersdivOffset').html(this.makeTimeLabel(offset));
    },
    createMarkerDiv : function(index, marker){
        //TODO: why class 'ts-marker' does not work?
        //for the moment we set the style manually, remove
        //TODO: table width with CSS?
        var div = this.$J('<div/>').attr('tabindex','0').addClass("markerdiv").html('<div>'+
            '<a href=# class="ts-marker"></a>'+
            '<a href=# class="markersdivOffset" type="text"></a>'+
            '<input class="markersdivTitle" type="text"/>'+
            '<a class="markersdivAddPlaylist" title="add to playlist"></a>'+
            '<a class="markersdivEdit" title="edit">EDIT</a>'+
            '<a class="markersdivDelete" title="delete"></a>'+
            '</div>'+
            '<div zero_top_padding><textarea class="markersdivDescription"></textarea></div>'+
            '<div zero_top_padding><a class="markersdivSave">OK</a></div>'+
        '<div zero_top_padding><span style="font-size:75%;color:#999">'+gettrans('author')+': '+marker.author+'</span></div>'); //TODO: avoid text nodes
        div.find('a').attr('href','#');
        //todo: remove markerlabel from css!!!!!!!
        //new RulerMarker(div.find('.markerlbl'),div.find('.markercanvas'),'marker',false);

        var e_indexLabel = div.find('.ts-marker');
        //var e_offsetLabel =div.find('.markersdivOffset');
        var e_okButton = div.find('.markersdivSave');
        var e_editButton = div.find('.markersdivEdit');
        var e_deleteButton =  div.find('.markersdivDelete');
        var e_addplaylistButton = div.find('.markersdivAddPlaylist');
        var e_descriptionText = div.find('.markersdivDescription');
        var e_titleText = div.find('.markersdivTitle');

        //set defualt element values regardeless of the marker state
        e_indexLabel.attr('title',marker.toString());
        this.setIndex(div, index);
            
        //e_offsetLabel.html(this.makeTimeLabel(marker.offset));
        this.setOffset(div,marker.offset);
        //set visibility and attach events according to the marker state:
        //first, is editing or not
        //var isEditing = marker.isEditable && marker.isModified;
        //            (!marker.isSavedOnServer || !(this.e_editButton.is(':visible')));

        //if(!isEditing){
        e_descriptionText.val(marker.desc ? marker.desc : "");
        e_titleText.val(marker.title ? marker.title : "");
        //}

        e_okButton.add(e_okButton.parent()).hide(); //hiding also the parent div saves space (padding bottom hidden)
        e_editButton.show();
        e_deleteButton.show();
        e_addplaylistButton.show();
        e_descriptionText.attr('readonly','readonly').addClass('markersdivUneditable').unbind('focus');
        e_titleText.attr('readonly','readonly').addClass('markersdivUneditable').unbind('focus');

        //add to playlist always visible, provided that it is saved on server AND current user is logged
        //(getCurrentUserName evaluates to true)
        //        if(!marker.isSavedOnServer || !this.getCurrentUserName()){
        //            e_addplaylistButton.hide();
        //        }else{
        e_addplaylistButton.unbind('click').bind('click',function(evtObj_){
            if(!marker.isSavedOnServer){
                return false;
            }
            //make a request to the server to get the pk (id)
            //note that marker.id (client side) is marker.public_id (server side)
            json([marker.id],"telemeta.get_marker_id", function(data){
                consolelog('received');
                consolelog(data);
                var id = data.result;
                playlistUtils.showAddResourceToPlaylist(e_addplaylistButton,'marker',""+id,gettrans('marker added to the selected playlist'));
            });
            return false;
        });

        if(!this.getCurrentUserName()){
            e_addplaylistButton.hide();
        }


        if(!marker.isEditable){ //marker is editable means that author == getCurrentUserName(). addToPlaylist
            //visibility is skipped because it depends on other circumstances (see above)
            e_editButton.hide();
            e_deleteButton.hide();
            //we unbind events to be sure
            //e_addplaylistButton.unbind('click').hide();
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
        })

        

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