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

        _reorder: function(selectedMarkerOffset) {
            //selectedMarkerOffset is the offset of the marker whose textarea
            //must be selected. It can be undefined

            //first of all, assign to each marker its text.
            //we could assign it onchange, but that event is NOT fired when the textarea changes.
            //so we doit it here
            var div = this.divContainer;
            var m = this.markers;
            
            if(div){
                var divChildren = div.childNodes;
                if(divChildren){
                    var l = Math.min(divChildren.length, m.length);
                    for(var i=0; i<l; i++){
                        var marker = m[i];
                        var subdiv = divChildren[i];
                        var text = subdiv.childNodes[1];
                        marker.desc = text.value;
                    }
                }
            }
            //old code:
            this.markers.sort(this.compare);
            for (var i in this.markers) {
                this.fire('indexchange', {
                    marker: this.markers[i],
                    index: parseInt(i)
                });
            }
            //now update the div
            this.updateDiv(selectedMarkerOffset);
        },

        add: function(offset, desc) {
            var id = this.uniqid();
            var marker = {
                id: id,
                offset: offset,
                desc: desc
            };
            var i = this.markers.push(marker) - 1;
            this.fire('add', {
                marker: marker,
                index: i
            });
            this._reorder(offset);
            return marker;
        },

        remove: function(marker) {
            if (marker) {
                var i = this.indexOf(marker);
                this.markers.splice(i, 1);
                this.fire('remove', {
                    marker: marker
                });
                this._reorder();
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
            oldMarkers = [].concat(this.markers);
            marker.offset = offset;
            this._reorder(offset);
        },

        getPrevious: function(offset, skip) {
            var marker = null;
            if (!skip) {
                skip = 0;
            }
            markers = [].concat(this.markers).reverse();
            $J(markers).each(function(i, m) {
                if (offset > m.offset && !(skip--)) {
                    marker = m;
                    return false;
                }
            });
            return marker;
        },

        getNext: function(offset, skip) {
            var marker = null;
            if (!skip) {
                skip = 0;
            }
            $J(this.markers).each(function(i, m) {
                if (offset < m.offset && !(skip--)) {
                    marker = m;
                    return false;
                }
            });
            return marker;
        },

        each: function(callback) {
            $J(this.markers).each(callback);
        },

        updateDiv: function(selectedMarkOffset){
            var div = this.divContainer;
            var m = this.markers;
            var l = m.length;
            if(div){
                var textWithFocus;
                //div.style.display = "block";
                //var doc = document;
                var divChildren = div.children();
                //var round = Math.round;
                for(var i=0; i<l; i++){
                    var marker = m[i];

                    var subdiv, text;
                    if(divChildren.length<=i){
                       
                        //creating marker, see marker.js
                        //would be better not to copy this code but to
                        //reference it.
                        var label = $J('<span/>')
                        .css({
                            color:'#fff',
                            backgroundColor:'#009',
                            width: '2ex',
                            textAlign: 'center',
                            fontFamily: 'monospace'
                        })
                        .html(i+1);

                        var timeSpan = $J('<span/>')
                        .css({
                            marginLeft:'1ex'
                        });
                        
                        
                        var header = $J('<div/>')
                        .append(label)
                        .append(timeSpan);

                        text = $J('<textarea/>')
                        .css({
                            margin:0,
                            padding:0,
                            width:'100%'
                        });
                        
                        var ok = $J('<a/>')
                        .attr("href","#")
                        .html("OK");

                        //create new div
                        subdiv = $J('<div/>')
                        .append(header)
                        .append(text)
                        .append(ok)
                        .css({
                            marginBottom:'1em',
                            marginTop:'1ex'
                        });

                        div.append(subdiv);
                    }else{
                        subdiv = $( div.children()[i] );
                        text = $( subdiv.children()[1] );
                        header = $( subdiv.children()[0] );
                        ok = $( subdiv.children()[2] ); 
                    }
                    var timeStr = this.formatMarkerOffset(marker.offset);

                    $( header.children()[1] ).html(timeStr);
                    //updating text
                    text.val(marker.desc);

                    if(selectedMarkOffset==marker.offset){
                        textWithFocus = text;
                    }
                    var send = this.sendHTTP;
                    //set the ok function
                    ok.click( function(){
                        marker.desc = text.val();
                        send(marker);
                    });

                }
                if(textWithFocus){
                    textWithFocus.focus();
                }
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
            var data2send = '{"id":"jsonrpc", "params":[{"item_id":"'+ itemid+'", "public_id": "'+marker.id+'", "time": "'+
            marker.offset+'","description": "'+marker.desc+'"}], "method":"telemeta.add_marker","jsonrpc":"1.0"}';


            $.ajax({
                type: "POST",
                url: 'http://localhost:9000/json/',
                contentType: "application/json",
                data: data2send
            });
        }

    });

    $N.notifyScriptLoad();

});
