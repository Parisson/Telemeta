/**
 * TimeSide - Web Audio Components
 * Copyright (c) 2008-2009 Samalyse
 * Author: Olivier Guilyardi <olivier samalyse com>
 * License: GNU General Public License version 2.0
 */

TimeSide(function($N, $J) {

    $N.Class.create("MarkerMap", $N.Core, {
        markers: null,
        divContainer: $J("#markers_div"),
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

        _reorder: function() {
            //first of all, assign to each marker its text.
            //we could assign it onchange, but that event is NOT fired when the textarea changes.
            //so we doit it here
            var div = this.divContainer;
            var m = markers;
            var l = m.length;
            if(div){
                var divChildren = div.childNodes;
                for(var i=0; i<l; i++){
                    var marker = m[i];
                    var subdiv = divChildren[i];
                    var text = subdiv.childNodes[1];
                    marker.desc = text.value;
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
            this.updateDiv();
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
            this._reorder();
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
            this._reorder();
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
            var m = markers;
            var l = m.length;
            if(div){
                var textWithFocus;
                div.style.display = "block";
                var doc = document;
                var divChildren = div.childNodes;
                //var round = Math.round;
                for(var i=0; i<l; i++){
                    var marker = m[i];
                    var subdiv, text;
                    if(divChildren.length<=i){
                        //create new div
                        subdiv = $J('div');
                        var header = doc.createElement('div');
                        //creating marker, see marker.js
                        //would be better not to copy this code but to
                        //reference it.
                        var label = doc.createElement('span');
                        label.style.cssText = "color:#fff;background-color:#009;width: '2ex';textAlign: 'center';font-family: 'monospace'";
                        label.innerHTML = (i+1);
                        header.appendChild(label);
                        var timeSpan = doc.createElement('span');
                        timeSpan.style.cssText="margin-left:1ex";
                        header.appendChild(timeSpan);
                        subdiv.appendChild(header);

                        text = doc.createElement('textarea');
                        text.style.cssText="margin:0;padding:0;width:100%";

                        var ok = doc.createElement('a');
                        ok.setAttribute("href","#");
                        ok.innerHTML = "OK";
                        subdiv.appendChild(text);
                        subdiv.appendChild(ok);
                        subdiv.style.cssText="margin-bottom:1em;margin-top:1ex";
                        div.appendChild(subdiv);
                    }else{
                        subdiv = divChildren[i];
                        text = subdiv.childNodes[1];
                        header = subdiv.childNodes[0];
                    }
                    var timeStr = this.formatMarkerOffset(marker.offset);

                    header.childNodes[1].innerHTML = timeStr;
                    //updating text
                    text.value = marker.desc;

                    if(selectedMarkOffset==marker.offset){
                        textWithFocus = text;
                    }
                    var send = this.sendHTTP;
                    //set the ok function
                    ok.onclick = function(){
                        marker.desc = text.value;
                        send(marker);
                    };

                }
                if(textWithFocus){
                    textWithFocus.focus();
                }
            }
        }

    });

    $N.notifyScriptLoad();

});
