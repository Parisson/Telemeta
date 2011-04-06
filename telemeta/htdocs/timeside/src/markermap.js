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
   
        get: function(index){
            return this.markers[index];

        },


        add: function(obj) {
            var marker = this.createMarker(obj);
            var idx = this.insertionIndex(marker);

            //if exists (ix>0) add it AFTER the existing item
            idx = idx<0 ? -idx-1 : idx+1;

            this.markers.splice(idx,0,marker);
            //notifies controller.onMarkerMapAdd
            this.fire('add', {
                marker: marker,
                index: idx
            });
            return idx;
        },

        //argument is either an object loaded from server or a number specifying the marker offset
        createMarker: function(argument){
            var marker = null;
            if(typeof argument == 'string'){ //to be sure, it might be that we pass an offset in string format
                argument = parseFloat(argument);
            }
            if(typeof argument == 'object'){
                var editable = CURRENT_USER_NAME === argument.author;
                marker = {
                    id: argument.public_id,
                    offset: argument.time,
                    desc: argument.description,
                    title: argument.title,
                    author: argument.author,
                    isEditable: editable,
                    isSavedOnServer: true,
                    isModified:false
                };
            }else if(typeof argument == 'number'){
                marker = {
                    id: this.uniqid(),
                    offset: parseFloat(argument),
                    desc: "",
                    title: "",
                    author: CURRENT_USER_NAME,
                    isEditable: true,
                    isSavedOnServer: false,
                    isModified: true
                };
            }
            return marker;

        },

        remove: function(index) {
            var marker = this.get(index);
            if (marker) {
                if(marker.isSavedOnServer){
                    this.removeHTTP(marker);
                }
                this.markers.splice(index, 1);
                //notifies controller.js
                this.fire('remove', {
                    index: index
                });
            }
            return marker;
        },

        move: function(markerIndex, newOffset){
            var newIndex = this.indexOf(newOffset);
            var realIndex = this.markers.move(markerIndex,newIndex);

            var marker = this.markers[realIndex];
            marker.offset = newOffset;
            marker.isModified = true;
            
            this.fire('moved', {
                fromIndex: markerIndex,
                toIndex: newIndex,
                newIndex: realIndex
            });


        },
        //
        //The core search index function: returns insertionIndex if object is found according to comparatorFunction,
        //(-insertionIndex-1) if object is not found. This assures that if the returned
        //number is >=0, the array contains the element, otherwise not and the element can be inserted at
        //-insertionIndex-1
        insertionIndex: function(object){
            var offset;
            if(typeof object == 'object'){
                offset = object.offset;
            }else if(typeof object == 'number'){
                offset = object;
            }else{ //to be sure...
                offset = parseFloat(object);
            }
            var pInt = parseInt; //reference to parseInt (to increase algorithm performances)
            var comparatorFunction = function(a,b){
                return (a<b ? -1 : (a>b ? 1 : 0));
            };
            var data = this.markers;
            var low = 0;
            var high = data.length-1;

            while (low <= high) {
                //int mid = (low + high) >>> 1;
                var mid = pInt((low + high)/2);
                var midVal = data[mid];
                var cmp = comparatorFunction(midVal.offset,offset);
                if (cmp < 0){
                    low = mid + 1;
                }else if (cmp > 0){
                    high = mid - 1;
                }else{
                    return mid; // key found
                }
            }
            return -(low + 1);  // key not found
        },
        //indexOf is the same as insertionIndex, but returns a positive number.
        //in other words, it is useful when we do not want to know if obj is already present
        //in the map, but only WHERE WOULD be inserted obj in the map. obj can be a marker
        //or an offset (time). In the latter case a dummy marker with that offset will be considered
        indexOf: function(obj){
            var idx = this.insertionIndex(obj);
            return idx<0 ? -idx-1 : idx;
        },
        each: function(callback) {
            $J(this.markers).each(callback);
        },
        //        length: function(){
        //            return this.markers ? this.markers.length : 0;
        //        },
       

        sendHTTP: function(marker, functionOnSuccess, showAlertOnError){
            var itemid = ITEM_PUBLIC_ID;
             var isSaved = marker.isSavedOnServer;
            var method = isSaved ? "telemeta.update_marker" : "telemeta.add_marker";
            var param = {
                'item_id':itemid,
                'public_id': marker.id,
                'time':marker.offset,
                'author': marker.author,
                'title':marker.title,
                'description':marker.desc
            };
            var success = function(){
                    if(!isSaved){
                        marker.isSavedOnServer = true;
                        marker.isModified = false;
                    }
                    if(functionOnSuccess){
                        functionOnSuccess();
                    }
                };
            //json(param,method,onSuccessFcn,onErrorFcn){
            json([param], method, success);
            
        },

        removeHTTP: function(marker){
             var public_id = marker.id
            //json(param,method,onSuccessFcn,onErrorFcn){
            json([public_id], "telemeta.del_marker");
        }

    });

    $N.notifyScriptLoad();

});
