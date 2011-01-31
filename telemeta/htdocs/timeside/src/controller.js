/**
 * TimeSide - Web Audio Components
 * Copyright (c) 2008-2009 Samalyse
 * Author: Olivier Guilyardi <olivier samalyse com>
 * License: GNU General Public License version 2.0
 */

TimeSide(function($N) {

    $N.Class.create("Controller", $N.Core, {

        initialize: function($super, cfg) {
            $super();
            this.configure(cfg, {
                player: null,
                soundProvider: null,
                map: null,
                markersDiv: document.getElementById("markers_div_id")
            });
            if (this.cfg.player && !$N.isInstanceOf(this.cfg.player, 'Player')) {
                this.cfg.player = new $N.Player(this.cfg.player);
            }
            this._setupPlayer();
        },

        _setupPlayer: function() {
            this.attach(this.updateMarkersDiv);
            this.cfg.player
            .setSoundProvider(this.cfg.soundProvider)
            .setMarkerMap(this.cfg.map)
            .observe('play', $N.attachFunction(this.cfg.soundProvider, this.cfg.soundProvider.play))
            .observe('pause', $N.attachFunction(this.cfg.soundProvider, this.cfg.soundProvider.pause))
            .observe('move', this.attach(this._onMove))
            .observe('markeradd', this.attach(this._onMarkerAdd))
            .observe('markermove', this.attach(this._onMarkerMove))
            .observe('markeradd2',this.attach(this._onMarkerAdd2))
            .draw();
            
        },

        _onMarkerAdd2: function(e,data){
            if (this.cfg.map) {
                alert(this.cfg.map._toString());
            }
        },

        _onMove: function(e, data) {
            this.cfg.soundProvider.seek(data.offset);
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
        _onMarkerMove: function(e, data) {
            if (this.cfg.map) {
                this.refreshMarkersText(this.cfg.map);
                this.cfg.map.move(this.cfg.map.byId(data.id), data.offset);
                this.updateMarkersDiv(this.cfg.map, data.offset);
            }
        },

        _onMarkerAdd: function(e, data) {
            if (this.cfg.map) {
                this.refreshMarkersText(this.cfg.map);
                this.cfg.map.add(data.offset, '');
                this.updateMarkersDiv(this.cfg.map, data.offset);
            }
        },
        
        refreshMarkersText: function(nonNullMarkersMap){
            var div = this.cfg.markersDiv;
            var m = nonNullMarkersMap.markers;
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

        },
        updateMarkersDiv: function(nonNullMarkersMap, selectedMarkOffset){
            var div = this.cfg.markersDiv;
            var m = nonNullMarkersMap.markers;
            var l = m.length;
            if(div){
                var d = new Date();
                var textWithFocus;
                div.style.display = "block";
                var doc = document;
                var divChildren = div.childNodes;
                var round = Math.round;
                for(var i=0; i<l; i++){
                    var marker = m[i];
                    var subdiv, text;
                    if(divChildren.length<=i){
                        //create new div
                        subdiv = doc.createElement('div');
                        var header = doc.createElement('div');
                        //creating marker, see marker.js
                        //would be better not to copy this code but to
                        //reference it.
                        var label = doc.createElement('span');
                        label.style.cssText = "color:#fff;background-color:#009;width: '2ex';textAlign: 'center';font-family: 'monospace'";
                        //label.setAttribute("class", $N.cssPrefix + this.cfg.className);
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
                }
                if(textWithFocus){
                    textWithFocus.focus();
                }
            }
        }

    });

    $N.notifyScriptLoad();

});
