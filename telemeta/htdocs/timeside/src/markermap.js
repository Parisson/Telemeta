/**
 * TimeSide - Web Audio Components
 * Copyright (c) 2011 Parisson
 * Author: Riccardo Zaccarelli
 * License: GNU General Public License version 2.0
 */
var MarkerMap = TimesideArray.extend({

    init: function() {
        this._super();
        var ui = uniqid; //defined in application.js (global vars and functions)
        this.uniqid = function(){
            return  ui();
        };
    },

    //overridden
    add: function(obj) {
        //var markers = this.toArray();
        var marker = this.createMarker(obj);
        var idx = this.insertionIndex(marker);
        if(idx>=0){ //it exists? there is a problem....
            this.debug('adding a marker already existing!!'); //should not happen. however...
            return -1;
        }
       
        idx = -idx-1;
        //we do not call the super add cause we want to insert at a specified index
        this._super(marker,idx);
        //notifies controller.onMarkerMapAdd

        this.fire('add', {
            marker: marker,
            index: idx,
            isNew: (typeof obj == 'number' || typeof obj == 'string')
        });
        //var temp = new MarkerDiv();
        // this.debug(this.createMarkerDiv());
         
            
        return idx;
    },
    //TODO: remove from here
        

    //argument is either an object loaded from server or a number specifying the marker offset
    createMarker: function(argument){
        var marker = null;
        var pFloat = parseFloat;
        if(typeof argument == 'string'){ //to be sure, it might be that we pass an offset in string format
            argument = pFloat(argument);
        }
        if(typeof argument == 'object'){
            var editable = CURRENT_USER_NAME === argument.author;
            marker = {
                id: argument.public_id,
                offset: pFloat(argument.time), //IMPORTANT: IT IS A STRING!!!!!!
                desc: argument.description,
                title: argument.title,
                author: argument.author,
                isEditable: editable,
                isSavedOnServer: true
            };
        }else if(typeof argument == 'number'){
            marker = {
                id: this.uniqid(),
                offset: pFloat(argument),
                desc: "",
                title: "",
                author: CURRENT_USER_NAME,
                isEditable: true,
                isSavedOnServer: false
            };
        }
        marker.toString = function(){
            var props = [];
            for(var prop in this){
                if(!(prop == 'toString')){
                    props.push(prop+': '+this[prop]);
                }
            }
            return props.sort().join("\n");
        }
        return marker;

    },

    //overridden
    //markerOrIndex can be an number (marker index) or a marker (the index will be aearched)
    remove: function(identifier) {
        var idx = -1;
        if(typeof index == 'number'){
            idx = identifier;
        }else{
            idx = this.insertionIndex(identifier);
        }
        if(idx<0 || idx>=this.length){
            this.each(function(i,m){
                consolelog(m);
            });
            consolelog(identifier);
            //TODO: handle error
            this.debug('remove: marker not found');
            return;
        }

        //build the function to be called if the marker is deleted
        //if the marker is NOT saved on server, call the function immediately
        var marker = this.toArray()[idx];
        var me = this;
        var superRemove = me._super;
        var functionOnSuccess = function(){
            superRemove.apply(me,[idx]);
            me.fire('remove',{
                    'index':idx
                })
        }

        if(marker.isSavedOnServer){
             //json(param,method,onSuccessFcn,onErrorFcn){
            json([marker.id], "telemeta.del_marker",functionOnSuccess);
        }else{
            functionOnSuccess();
        }
    },

    save: function(marker){
        var idx = this.insertionIndex(marker);
        if(idx<0 || idx>=this.length){
            //TODO: habdle error
            this.debug('marker not found');
        }
        
        //TODO: item public id defined elsewhere up, not here inside
        var itemid = ITEM_PUBLIC_ID;
        var isSavedOnServer = marker.isSavedOnServer;
        var method = isSavedOnServer ? "telemeta.update_marker" : "telemeta.add_marker";
        var param = {
            'item_id':itemid,
            'public_id': marker.id,
            'time':marker.offset,
            'author': marker.author,
            'title':marker.title,
            'description':marker.desc
        };

        //function on success:
        var me = this;
        var success = function(){
            if(!isSavedOnServer){
                marker.isSavedOnServer = true;
                marker.isModified = false;
            }
             me.fire('save',{
                'index':idx
            });
        };
        //json(param,method,onSuccessFcn,onErrorFcn){
        json([param], method, success);

    },

    //TODO: there is no need of a public method
//    removeHTTP: function(marker){
//        var public_id = marker.id
//        //json(param,method,onSuccessFcn,onErrorFcn){
//        json([public_id], "telemeta.del_marker");
//    },

    //overridden method
    move: function(markerIndex, newOffset){
        var newIndex = this.insertionIndex(newOffset);
        //select the case:
        if(newIndex<0){
            //we didn't move the marker on another marker (newOffset does not correspond to any marker)
            //just return the real insertionIndex
            newIndex = -newIndex-1;
        }
        //            var markers = this.getMarkers();
        //            //TODO: remove move from array prototype!!!!
        var realIndex = this._super(markerIndex,newIndex);
        //            //var realIndex = markers.move(markerIndex,newIndex);
        //            this.debug('fromindex '+markerIndex+' to: '+newIndex+' results in '+realIndex);
        var markers = this.toArray();
        var marker = markers[realIndex];
        marker.offset = newOffset;
        marker.isModified = true;
        this.fire('move', {
            fromIndex: markerIndex,
            toIndex: newIndex,
            newOffset: newOffset
        //,newIndex: realIndex
        });
    },
       
    
    //returns the insertion index of object in this sorted array by means of a binary search algorithm.
    // A) If object is a marker and:
    //   a1) Is found (ie, there is a marker in this map
    //       with same offset and same id), returns the index of the marker found, in the range [0, this.length-1]. Otherwise, if
    //   a2) Is not found, then returns -(insertionIndex-1), where insertionIndex is the
    //       index at which object would be inserted preserving the array order. Note that this assures that a
    //       number lower than zero means that object is not present in the array, and viceversa
    // B) If object is a number or a string number (eg, "12.567"), then a marker with offset = object is built and compared 
    //    against the markers in the map. Note however that in this case that equality between marker's offset is sufficient,
    //    as object is not provided with an id. THEREFORE, IF THE MAP CONTAINS SEVERAL MARKERS AT INDICES i, i+1, ... i+n
    //    WITH SAME OFFSET == object, THERE IS NO WAY TO DETERMINE WHICH INDEX IN [i, i+1, ... i+n] WILL BE RETURNED.
    //    See player.forward and player.rewind for an example of the B) case.
    //LAST NOTE: BE SURE object is either a number (float) or object.offset is a number (float).
    //In case it is not known, If it is a string number such as
    //"4.562" the comparison falis (eg, "2.567" > "10.544") but obviously, no error is thrown in javascript
    //
    insertionIndex: function(object){
        //default comparator function:
        //returns 1 as the first argument is greater than the second
        //returns -1 as the first argument is lower than the second
        //returns 0 if the arguments are equal
        var comparatorFunction = function(markerInMap,newMarker){
            var a = markerInMap.offset;
            var b = newMarker.offset;
            if(a<b){
                return -1;
            }else if(a >b){
                return 1;
            }else{
                var a1 = markerInMap.id;
                var b1 = newMarker.id;
                if(a1<b1){
                    return -1;
                }else if(a1>b1){
                    return 1;
                }
            }
            return 0;
            //var ret = a < b ? -1 : (a>b ? 1 : (markerInMap.id === newMarker.id ? 0 : -1));
            //return ret;
        };
        if(!(typeof object == 'object')){
            var offset;
            if(typeof object == 'number'){
                offset = object;
            }else{ //to be sure...
                offset = parseFloat(object);
            }
            object = {
                'offset':offset
            };
            //key will never be found, so return either 1 or -1:
            comparatorFunction = function(markerInMap,newMarker){
                var a = markerInMap.offset;
                var b = newMarker.offset;
                return a < b ? -1 : (a>b ? 1 : 0);
            };
        }
        var pInt = parseInt; //reference to parseInt outside the loop below
        //(to increase algorithm performances)

        var data = this.toArray();
        var low = 0;
        var high = data.length-1;

        while (low <= high) {
            //int mid = (low + high) >>> 1;
            var mid = pInt((low + high)/2);
            var midVal = data[mid];
            var cmp = comparatorFunction(midVal,object);
            if (cmp < 0){
                //the midvalue is lower than the searched index element
                low = mid + 1;
            }else if (cmp > 0){
                //the midvalue is greater than the searched index element
                high = mid - 1;
            }else{
                return mid; // key found
            }
        }
        return -(low + 1);  // key not found
    }
}
);