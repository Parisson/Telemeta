/**
 * TimeSide - Web Audio Components
 * Copyright (c) 2008-2009 Samalyse
 * Author: Olivier Guilyardi <olivier samalyse com>
 * License: GNU General Public License version 2.0
 */

TimeSide(function($N, $J) {

    $N.Class.create("MarkerMap", $N.Core, {
        markers: null,
        divContainer: $J("#markers_div_id"),
        initialize: function($super, markers) {
            $super();
            if (!markers){
                markers = [];
            }
            this.markers = markers;
        },

        toArray: function() {
            return [].concat(this.markers);
        },

        byIndex: function(index) {
            return this.markers[index];
        },

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


        addNew: function(offset, description){
            var id = this.uniqid();
            var marker = {
                id: id,
                offset: offset,
                desc: description,
                isNew: true
            };
            this.add(marker);
        },

        //this function adds a new marker. It is actually
        add: function(marker) {
            var idx = this.insertionIndex(marker);
            //adding the div
            marker.div = this.createDiv(marker,idx);
            this.markers.splice(idx,0,marker);
            //calls core.js $N.attachFunction
            //which calls ruler.js onMapAdd
            this.fire('add', {
                marker: marker,
                index: idx
            });
            this.fireRefreshLabels(idx+1,this.markers.length);
            //this._reorder(marker.offset);
            return marker;
        },
        
        

        remove: function(klass, marker) {
            if (marker) {
                if(!(klass)){
                    klass = this;
                }
                var i = klass.indexOf(marker);
                klass.markers.splice(i, 1);
                marker.div['div'].remove();
                klass.fire('remove', {
                    marker: marker
                });
                //                var i1= Math.min(oldIndex,newIndex);
                //                var i2= Math.max(oldIndex,newIndex);
                //var mrks = this.markers;
                klass.fireRefreshLabels(i,klass.markers.length);

                klass.removeHTTP(marker);

            }
            return marker;
        },

        compare: function(marker1, marker2) {
            if (marker1.offset > marker2.offset){
                return 1;
            }
            if (marker1.offset < marker2.offset){
                return -1;
            }
            return 0;
        },

        move: function(marker, offset) {
            var oldIndex = this.indexOf(marker);
            marker.offset = offset;
            marker.offset = offset;
            var newIndex = this.insertionIndex(marker);
            //change marker time
            //$($( marker.div.children()[0] ).children()[1]).html(this.formatMarkerOffset(offset));
            marker.div['labelOffset'].html(this.formatMarkerOffset(offset));
            if(newIndex>oldIndex){
                newIndex--;
            }
            if(newIndex==oldIndex){
                return;
            }
            var l = this.markers.length;
            this.markers.splice(oldIndex,1);
            this.markers.splice(newIndex,0,marker);
            //The .detach() method is the same as .remove(), except that .detach() keeps
            //all jQuery data associated with the removed elements.
            //This method is useful when removed elements are to be reinserted into the DOM at a later time.
            marker.div['div'].detach();
            if(newIndex==l-1){
                this.divContainer.append(marker.div['div']);
            }else{
                $( this.divContainer.children()[newIndex] ).before(marker.div['div']);
            }
            //$($( marker.div.children()[1] )).focus();
            marker.div['textarea'].focus();
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
                this.markers[i].div['labelIndex'].html(i+1)
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


        createDiv: function(marker,insertionIndex){
            var div = this.divContainer;
            var m = this.markers;
            var l = m.length;
            var ret = {};
            if(div){
                //var textWithFocus;
                //div.style.display = "block";
                //var doc = document;


                var text, timeSpan, closeAnchor, ok, header;


                //creating marker, see marker.js
                //would be better not to copy this code but to
                //reference it.
                var label = $J('<span/>')
                .css({
                    color:'#fff',
                    backgroundColor:'#009',
                    width: '2em',
                    textAlign: 'center'
                //,fontFamily: 'monospace'
                })
                .html(insertionIndex+1);
                ret['labelIndex']=label;

                timeSpan = $J('<span/>')
                .css({
                    marginLeft:'1ex'
                });
                ret['labelOffset']=timeSpan;

                closeAnchor = $J('<input/>')
                .attr("type","submit")
                .attr("value","x")
                .css({
                    //fontFamily: 'monospace',
                    fontWeight:'bold',
                    border:'1px dotted #333333',
                    float:'right',
                    color:'white'
                });
                ret['submitCancel']=closeAnchor;

                header = $J('<div/>')
                .append(label)
                .append(timeSpan)
                .append(closeAnchor);

                text = $J('<textarea/>')
                .css({
                    margin:0,
                    padding:0,
                    width:'100%'
                });
                ret['textarea']=text;

                ok = $J('<input/>')
                .attr("type","submit")
                .attr("value","OK");
                ret['submitOk']=ok;

                //create new div
                var subdiv = $J('<div/>')
                .append(header)
                .append(text)
                .append(ok)
                .css({
                    marginBottom:'1em',
                    marginTop:'1ex'
                });

                var timeStr = this.formatMarkerOffset(marker.offset);

                timeSpan.html(timeStr);

                //updating text
                text.val(marker.desc);

                var send = this.sendHTTP;
                //set the ok function
                //we clear all the click event handlers from ok and assign a new one:
                ok.unbind('click').click( function(){
                    marker.desc = text.val();
                    send(marker);
                });
                //set the remove action
                var remove = this.remove;
                var klass = this;
                closeAnchor.unbind('click').click( function(){
                    remove(klass, marker);
                });

                var divLen = div.children().length;
                div.append(subdiv);
                if(insertionIndex==divLen){
                    div.append(subdiv);
                }else{
                    $( div.children()[insertionIndex] ).before(subdiv);
                }
                //if(textWithFocus){
                text.focus();
                // }
                ret['div']=subdiv;
                return ret;
            }
        },
        createDivOld: function(marker,insertionIndex){
            var div = this.divContainer;
            var m = this.markers;
            var l = m.length;
            if(div){
                //var textWithFocus;
                //div.style.display = "block";
                //var doc = document;


                var text, timeSpan, closeAnchor, ok, header;


                //creating marker, see marker.js
                //would be better not to copy this code but to
                //reference it.
                var label = $J('<span/>')
                .css({
                    color:'#fff',
                    backgroundColor:'#009',
                    width: '2em',
                    textAlign: 'center'
                //,fontFamily: 'monospace'
                })
                .html(insertionIndex+1);

                timeSpan = $J('<span/>')
                .css({
                    marginLeft:'1ex'
                });

                closeAnchor = $J('<a/>')
                .attr("href","#")
                .html("x")
                .css({
                    //fontFamily: 'monospace',
                    fontWeight:'bold',
                    ackgroundColor:'#888877',
                    float:'right',
                    color:'white'
                //,backgroundImage:'url("img/cancel.png")'
                });
                //.append('</img>').attr("src","img/cancel.png");

                header = $J('<div/>')
                .append(label)
                .append(timeSpan)
                .append(closeAnchor);

                text = $J('<textarea/>')
                .css({
                    margin:0,
                    padding:0,
                    width:'100%'
                });

                ok = $J('<a/>')
                .attr("href","#")
                .addClass('ts-marker-button')
                .html("OK");

                //create new div
                var subdiv = $J('<div/>')
                .append(header)
                .append(text)
                .append(ok)
                .css({
                    marginBottom:'1em',
                    marginTop:'1ex'
                });

                var timeStr = this.formatMarkerOffset(marker.offset);

                timeSpan.html(timeStr);

                //updating text
                text.val(marker.desc);

                var send = this.sendHTTP;
                //set the ok function
                //we clear all the click event handlers from ok and assign a new one:
                ok.unbind('click').click( function(){
                    marker.desc = text.val();
                    send(marker);
                });
                //set the remove action
                var remove = this.remove;
                var klass = this;
                closeAnchor.unbind('click').click( function(){
                    remove(klass, marker);
                });

                var divLen = div.children().length;
                div.append(subdiv);
                if(insertionIndex==divLen){
                    div.append(subdiv);
                }else{
                    $( div.children()[insertionIndex] ).before(subdiv);
                }
                //if(textWithFocus){
                text.focus();
                // }
                return subdiv;
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
            msec;
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
