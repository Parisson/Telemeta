/**
 * TimeSide - Web Audio Components
 * Copyright (c) 2008-2009 Samalyse
 * Author: Olivier Guilyardi <olivier samalyse com> and Riccardo Zaccarelli
 * License: GNU General Public License version 2.0
 */

TimeSide(function($N, $J) {

    $N.Class.create("MarkerMap", $N.Core, {
        markers: null,
        //the main div container:
        divContainer: $J("#markers_div_id"),
        initialize: function($super, markers) {
            $super();
            if (!markers){
                markers = [];
            }
            this.markers = markers;
        },
        //static constant variables to retireve the Marker Html Elements (MHE)
        //to be used with the function below getHtmElm, eg:
        //getHtmElm(marker, this.MHE_OFFSET_LABEL)
        MHE_INDEX_LABEL:'indexLabel',
        MHE_OFFSET_LABEL:'offsetLabel',
        MHE_DESCRIPTION_TEXT:'descriptionText',
        MHE_DESCRIPTION_LABEL:'descriptionLabel',
        MHE_EDIT_BUTTON:'editButton',
        MHE_OK_BUTTON:'okButton',
        MHE_DELETE_BUTTON:'deleteButton',
        //static constant variables for edit mode:
        EDIT_MODE_SAVED:0,
        EDIT_MODE_EDIT_TEXT:1,
        EDIT_MODE_MARKER_MOVED:2,

        //function to retreve html elements in the edit div associated with marker:
        getHtmElm: function(marker, elementName){
            //return marker.div.children('[name="'+elementName+'"]');
            //children returns only the first level children, we must use:
            return marker.div.find('*[name="'+elementName+'"]');
        },

        //        toArray: function() {
        //            return [].concat(this.markers);
        //        },
        //
        //        byIndex: function(index) {
        //            return this.markers[index];
        //        },
        //

        //used by controller._onMarkerMove
        byId: function(id) {
            var marker = null;
            for (var i in this.markers) {
                if (this.markers[i].id == id) {
                    marker = this.markers[i];
                    break;
                }
            }
            return marker;
        },

        indexOf: function(marker) {
            var index = null;
            for (var i in this.markers) {
                if (this.markers[i].id == marker.id) {
                    index = parseInt(i);
                    break;
                }
            }
            return index;
        },


        addNew: function(offset){
            var id = this.uniqid();
            var marker = {
                id: id,
                offset: offset,
                desc: undefined,
                isNew: true
            };
            this.add(marker, this.EDIT_MODE_EDIT_TEXT);
        },

        //editMode is optional, in case it defaults to
        //EDIT_MODE_SAVED:0
        add: function(marker, editMode) {
            var idx = this.insertionIndex(marker);
            //adding the div
            marker.div = this.createDiv(marker,idx);
            //setting focus and label description
            //set label description
            this.setLabelDescription(marker);
            //finally, set the focus to the text
            //this.getHtmElm(marker,this.MHE_DESCRIPTION_TEXT).focus();


            this.markers.splice(idx,0,marker);
            //calls core.js $N.attachFunction
            //which calls ruler.js onMapAdd
            this.fire('add', {
                marker: marker,
                index: idx
            });
            this.fireRefreshLabels(idx+1,this.markers.length);
            //this._reorder(marker.offset);
            this.fireEditMode(marker,editMode);
            return marker;
        },

        remove: function(marker) {
            if (marker) {
                var i = this.indexOf(marker);
                this.markers.splice(i, 1);
                marker.div.remove();
                this.fire('remove', {
                    marker: marker
                });

                this.fireRefreshLabels(i,this.markers.length);
                this.removeHTTP(marker);

            }
            return marker;
        },
        //        compare: function(marker1, marker2) {
        //            if (marker1.offset > marker2.offset){
        //                return 1;
        //            }
        //            if (marker1.offset < marker2.offset){
        //                return -1;
        //            }
        //            return 0;
        //        },

        move: function(marker, offset) {
            if(offset===marker.offset){
                return;
            }
            var oldIndex = this.indexOf(marker);
            marker.offset = offset;
            //marker.offset = offset;
            var newIndex = this.insertionIndex(marker);
            //change marker time
            //$($( marker.div.children()[0] ).children()[1]).html(this.formatMarkerOffset(offset));
            this.getHtmElm(marker,this.MHE_OFFSET_LABEL).html(this.formatMarkerOffset(offset));
            //            marker.div[this.MHE_OFFSET_LABEL].html(this.formatMarkerOffset(offset));
            if(newIndex>oldIndex){
                newIndex--;
            }
            //fire edit mode
            this.fireEditMode(marker, this.EDIT_MODE_MARKER_MOVED);

            if(newIndex==oldIndex){
                return;
            }
            var l = this.markers.length;
            this.markers.splice(oldIndex,1);
            this.markers.splice(newIndex,0,marker);
            //The .detach() method is the same as .remove(), except that .detach() keeps
            //all jQuery data associated with the removed elements.
            //This method is useful when removed elements are to be reinserted into the DOM at a later time.
            marker.div.detach();
            if(newIndex==l-1){
                this.divContainer.append(marker.div);
            }else{
                $( this.divContainer.children()[newIndex] ).before(marker.div);
            }
            //$($( marker.div.children()[1] )).focus();

            //this.getHtmElm(marker,this.MHE_DESCRIPTION_TEXT).focus();
            //this.getHtmElm(marker,this.MHE_DESCRIPTION_TEXT).select();
            var i1= Math.min(oldIndex,newIndex);
            var i2= Math.max(oldIndex,newIndex);
            //var mrks = this.markers;

            this.fireRefreshLabels(i1,i2+1);
            

           
            
        //this._reorder(offset);
        },

        fireRefreshLabels: function(firstIndex,lastIndex){
            if(lastIndex<=firstIndex){
                return;
            }
            for (var i=firstIndex; i <lastIndex;i++) {
                //calls ruler _onMapIndexChange
                this.fire('indexchange', {
                    marker: this.markers[i],
                    index: i
                });
                //update label element
                this.getHtmElm(this.markers[i], this.MHE_INDEX_LABEL).html(i+1);
            //                this.markers[i].div['labelIndex'].html(i+1)
            // $($( this.markers[i].div.children()[0] ).children()[0]).html(i+1);

            }
        },

        insertionIndex: function(marker){
            var index = 0;
            var l = this.markers.length;
            while (index<l && this.markers[index].offset <= marker.offset) {
                index ++;
            }
            //markers.splice(index,0,marker);
            return index;
        },

        

        each: function(callback) {
            $J(this.markers).each(callback);
        },

        //creates a new div. By default, text is hidden and edit button is visible
        createDiv: function(marker,insertionIndex){
            var div = this.divContainer;
            var markerDiv;
            if(div){
                var indexLabel, descriptionText, offsetLabel, closeButton, okButton, header, editButton, descriptionLabel;
                var margin = '1ex';

                //index label
                indexLabel = $J('<span/>')
                .attr('name', this.MHE_INDEX_LABEL)
                .css({
                    color:'#fff',
                    backgroundImage:'url("/images/marker_tiny.png")',
                    backgroundRepeat:'no-repeat',
                    backgroundPosition:'center center',
                    fontSize: '90%',
                    fontWeight:'bold',
                    display:'inline-block',
                    width:'3ex',
                    textAlign: 'center'
                    ,
                    fontFamily: 'monospace'
                })
                .html(insertionIndex+1);

                //offset label
                offsetLabel = $J('<span/>')
                .attr('name', this.MHE_OFFSET_LABEL)
                .css({
                    marginLeft:margin,
                    marginRight:margin
                })
                .html(this.formatMarkerOffset(marker.offset));
                
                //description label
                descriptionLabel = $J('<span/>')
                .attr("name",this.MHE_DESCRIPTION_LABEL)
                .attr('title',marker.desc ? marker.desc : "")
                .css({
                    fontWeight:'bold',
                    marginRight:margin
                })

                //close button
                closeButton = $J('<a/>')
                .attr('title','delete marker')
                .attr('name', this.MHE_DELETE_BUTTON)
                .attr("href","#")
                .append($J('<img/>').attr("src","/images/del_marker.png").css({
                    width:'1em'
                }))
                .css({
                    fontWeight:'bold',
                    //border:'1px dotted #333333',
                    float:'right',
                    color:'white'
                });

                //edit button
                editButton = $J('<a/>')
                .attr('title','edit marker description')
                .attr('name', this.MHE_EDIT_BUTTON)
                .attr("href","#")
                .append($J('<img/>').attr("src","/images/edit_marker.png").css({
                    width:'6.5ex'
                }))
                .css({
                    float:'right',
                    marginRight:margin
                });
            
                //add all elements to header:
                header = $J('<div/>')
                .append(indexLabel)
                .append(offsetLabel)
                .append(descriptionLabel)
                .append(closeButton)
                .append(editButton);

                //description text
                descriptionText = $J('<textarea/>')
                .attr("name", this.MHE_DESCRIPTION_TEXT)
                .val(marker.desc ? marker.desc : "")
                .css({
                    margin:0,
                    padding:0,
                    width:'100%'
                });
            
                //ok button
                okButton = $J('<a/>')
                .attr("name", this.MHE_OK_BUTTON)
                .attr('title','save marker description and offset')
                .css({
                    display:'none',
                    marginTop:'0.5ex'
                })
                .attr("href","#")
                .append($J('<img/>').attr("src","/images/marker_ok_green.png").css({
                    width:'3em'
                }))
            
                //create marker div and append all elements
                markerDiv = $J('<div/>')
                .append(header)
                .append(descriptionText)
                .append(okButton)
                .css({
                    paddingBottom:'1em',
                    paddingTop:'1ex',
                    paddingLeft:'1ex',
                    paddingRight:'1ex',
                    //borderTop: '1px solid #666666',
                    borderBottom: '1px solid #999999'
                });

                //ACTIONS TO BUTTONS:
                ////first define this keyword inside functions
                var klass = this;
                //reference to fireEditMode
                var func_fem = this.fireEditMode;
                var editModeEditText = this.EDIT_MODE_EDIT_TEXT;
                //action for edit
                editButton.unbind('click').click( function(){
                    func_fem.apply(klass,[marker,editModeEditText,editButton, descriptionText,
                        descriptionLabel, okButton]);
                    return false; //avoid scrolling of the page on anchor click
                });

                //action for ok button
                var editModeSaved = this.EDIT_MODE_SAVED;
                var func_send = this.sendHTTP;
                okButton.unbind('click').click( function(){
                    if(marker.desc !== descriptionText.val()){ //strict equality needed. See note below
                        marker.desc = descriptionText.val();
                        func_send(marker);
                    }
                    func_fem.apply(klass,[marker,editModeSaved,editButton, descriptionText,
                        descriptionLabel, okButton]);
                    return false; //avoid scrolling of the page on anchor click
                });

                //action for removing
                var remove = this.remove;
                //reference the class (this) as within the function below this will refer to the document
                
                closeButton.unbind('click').click( function(){
                    remove.apply(klass,[marker]);
                    return false; //avoid scrolling of the page on anchor click
                });

                //insert the new div created
                var divLen = div.children().length;
                div.append(markerDiv);
                if(insertionIndex==divLen){
                    div.append(markerDiv);
                }else{
                    $( div.children()[insertionIndex] ).before(markerDiv);
                }

            }
            return markerDiv;
        },

        //sets the edit mode in the div associated to marker. Last 4 arguments are optional
        fireEditMode: function(marker, editMode, editButton, descriptionText,
            descriptionLabel, okButton){
            var e = this.getHtmElm;
            if(editButton == undefined){
                editButton = e(marker,this.MHE_EDIT_BUTTON);
            }
            if(descriptionLabel == undefined){
                descriptionLabel = e(marker,this.MHE_DESCRIPTION_LABEL);
            }
            if(descriptionText == undefined){
                descriptionText = e(marker,this.MHE_DESCRIPTION_TEXT);
            }
            if(okButton == undefined){
                okButton = e(marker,this.MHE_OK_BUTTON);
            }
            var speed = 400; //fast is 200 slow is 600 (see jQuery help)
            var klass = this;
            //var editModeSaved = this.EDIT_MODE_SAVED;
            if(editMode == this.EDIT_MODE_EDIT_TEXT){ //edit text
                descriptionLabel.hide(); //without arguments, otherwise alignement problems arise (in chrome)
                editButton.hide(speed);
                descriptionText.show(speed, function(){
                    this.select();
                });
                okButton.show(speed);

            }else if(editMode == this.EDIT_MODE_MARKER_MOVED){
                if(!descriptionText.is(':visible')){
                    editButton.show(speed, function(){
                        descriptionLabel.show();
                    });
                }
                //if then a user types the edit button, this function is called with
                //editMode=1 (this.EDIT_MODE_EDIT_TEXT). Which means (see okbutton click binding above) marker will be saved
                //ONLY if text is different from marker.desc. However, as the offset has changed we want to
                //save IN ANY CASE, so we set marker.desc undefined. This way, text will be always different and
                //we will save the marker in any case
                marker.desc = undefined;
                //descriptionText.hide(speed);
                okButton.show(speed);
            }else{
                var function_sld = klass.setLabelDescription;
                editButton.show(speed, function(){
                    function_sld.apply(klass,[marker]);
                    descriptionLabel.show();
                });
                descriptionText.hide(speed);
                okButton.hide(speed);
            }
        },


        //sets the length of the label description. Note that all elements must be visible.
        //Therefore, we call nediaitem_detail.setUpTabs from controller once all markers have been loaded
        setLabelDescription: function(marker){
            var mDiv = marker.div;
            var e = this.getHtmElm;
            var space = mDiv.width()-e(marker, this.MHE_INDEX_LABEL).outerWidth(true)-e(marker, this.MHE_OFFSET_LABEL).outerWidth(true)-
            e(marker, this.MHE_EDIT_BUTTON).outerWidth(true)-e(marker, this.MHE_DELETE_BUTTON).outerWidth(true);
            var labelDesc = e(marker, this.MHE_DESCRIPTION_LABEL);
            var str='';
            labelDesc.html(str);
            if(space>0 && marker.desc && marker.desc.length>0){
                var string = marker.desc;
                labelDesc.html(string);
                var id=string.length-1;
                while(id>=0 && labelDesc.outerWidth(true)>=space){
                    str = id==0 ? "" : string.substring(0,id);
                    labelDesc.html(str);
                    id--;
                }
            }
            //we did not reach the end? in case, add dots
            if(str.length>3 && str.length<marker.desc.length){
                //workaround: add dots at the beginning, calculate the space, then move them at end
                str = "..." + str;
                labelDesc.html(str);
                //so dots are at the beginning and we can remove safely the last character
                id = str.length-1;
                while(id>=0 && labelDesc.outerWidth(true)>=space){
                    //var chr = string.substring(0,id);
                    //str += chr==' ' ? '&nbsp;' : chr;
                    str = id==0 ? "" : str.substring(0,id);
                    labelDesc.html(str);
                    id--;
                }
                //move dots at the end, if we didnt erase dots as well (space too short)
                if(str.length>3){
                    str = str.substring(3,str.length)+"...";
                }else if(str.length<3){ //zero, one or two dots might be confusing, remove them
                    str = '';
                }
                labelDesc.html(str);
            }

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
        },

        sendHTTP: function(marker){

            //itemid is the item (spund file) name
            var sPath = window.location.pathname;
            //remove last "/" or last "/#", if any...
            sPath = sPath.replace(/\/#*$/,"");
            var itemid = sPath.substring(sPath.lastIndexOf('/') + 1);

            //WARNING: use single quotes for the whole string!!
            //see http://stackoverflow.com/questions/4809157/i-need-to-pass-a-json-object-to-a-javascript-ajax-method-for-a-wcf-call-how-can
            //            var data2send = '{"id":"jsonrpc", "params":[{"item_id":"'+ itemid+'", "public_id": "'+marker.id+'", "time": "'+
            //            marker.offset+'","description": "'+marker.desc+'"}], "method":"telemeta.add_marker","jsonrpc":"1.0"}';
            var isNew = marker.isNew;
            var method = isNew ? "telemeta.add_marker" : "telemeta.update_marker";
            var data2send = '{"id":"jsonrpc", "params":[{"item_id":"'+ itemid+'", "public_id": "'+marker.id+'", "time": "'+
            marker.offset+'","description": "'+marker.desc+'"}], "method":"'+method+'","jsonrpc":"1.0"}';


            $.ajax({
                type: "POST",
                url: '/json/',
                contentType: "application/json",
                data: data2send,
                success: function(){
                    if(isNew){
                        marker.isNew = false;
                    }
                }
            });
        },

        removeHTTP: function(marker){

            //  //itemid is the item (spund file) name
            //  var sPath = window.location.pathname;
            //  //remove last "/" or last "/#", if any...
            //  sPath = sPath.replace(/\/#*$/,"");
            //  var itemid = sPath.substring(sPath.lastIndexOf('/') + 1);
            var public_id = marker.id;
            //WARNING: use single quotes for the whole string!!
            //see http://stackoverflow.com/questions/4809157/i-need-to-pass-a-json-object-to-a-javascript-ajax-method-for-a-wcf-call-how-can
            var data2send = '{"id":"jsonrpc","params":["'+public_id+'"], "method":"telemeta.del_marker","jsonrpc":"1.0"}';
            //            var map = this.cfg.map;
            //            var me = this;
            $.ajax({
                type: "POST",
                url: '/json/',
                contentType: "application/json",
                data: data2send,
                dataType: "json"
            
            });
            var g = 9;
        }

    });

    $N.notifyScriptLoad();

});
