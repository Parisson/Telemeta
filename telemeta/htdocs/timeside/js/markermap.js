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
 * class fior managing markers in the player. This class extends TimesideArray (see timeside.js), and communicates with the other 
 * two TimesideArrays of the player which receive edit events (click, keys events etcetera): the ruler (ruler.js) and the markermapdiv (divmarker.js)
 * All bindings between these three classes are set in in the player (See player.js , in particular loadMarkers method)
 */
Timeside.classes.MarkerMap = Timeside.classes.TimesideArray.extend({

    init: function() { 
        this._super();
    },

    pFloat: parseFloat, //reference to function parseFloat for faster lookup
    //overridden
    add: function(obj) {
        //var markers = this.toArray();
        
        if(!('offset' in obj)){
            return -1;
        }


        if(typeof obj.offset != 'number'){ //check to be sure:
            obj.offset = this.pFloat(obj.offset);
        }
        if(!('id' in obj)){
            obj.id = Timeside.utils.uniqid();
        }
        if(!('isEditable' in obj)){
            obj.isEditable = false;
        }
        var marker = obj; //this.createMarker(obj);
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
            index: idx
            //,isNew: (typeof obj == 'number' || typeof obj == 'string')
        });
        //var temp = new MarkerDiv();
        // this.debug(this.createMarkerDiv());
         
            
        return idx;
    },

    //overridden
    //identifier can be an number (marker index) or a marker (the index will be aearched)
    remove: function(identifier) {
        var idx = -1;
        if(typeof index == 'number'){
            idx = identifier;
        }else{
            idx = this.insertionIndex(identifier);
        }
        if(idx<0 || idx>=this.length){
            this.debug('remove: marker not found');
            return -1;
        }
        var marker = this._super(idx);
        this.fire('remove',{
                'index':idx,
                'marker':marker
            });
            return idx;
    },

    //overridden method
    move: function(markerIndex, newOffset){
        var newIndex = this.insertionIndex(newOffset);
        //select the case:
        if(newIndex<0){
            //we didn't move the marker on another marker (newOffset does not correspond to any marker)
            //just return the real insertionIndex
            newIndex = -newIndex-1;
        }
        
        var realIndex = this._super(markerIndex,newIndex);
        
        var markers = this.toArray();
        var marker = markers[realIndex];
        var oldOffset = marker.offset;
        marker.offset = newOffset;
        this.fire('move', {
            marker: marker,
            fromIndex: markerIndex,
            toIndex: newIndex,
            oldOffset: oldOffset
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
        //var pInt = parseInt; //reference to parseInt outside the loop below
        //(to increase algorithm performances)

        var data = this.toArray();
        var low = 0;
        var high = data.length-1;

        while (low <= high) {
            var mid = (low + high) >>> 1;
            //biwise operation equivalent to (but faster than):
            //var mid = parseInt((low + high)/2);
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