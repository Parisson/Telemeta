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
                map: null
            });
            if (this.cfg.player && !$N.isInstanceOf(this.cfg.player, 'Player')) {
                this.cfg.player = new $N.Player(this.cfg.player);
            }
            this._setupPlayer();
            
        },

        _setupPlayer: function() {
//             if (this.cfg.player && !$N.isInstanceOf(this.cfg.player, 'Player')) {
//                this.cfg.player = new $N.Player(this.cfg.player);
//            }
            this.attach(this.updateMarkersDiv);
            this.cfg.player
            .setSoundProvider(this.cfg.soundProvider)
            .setMarkerMap(this.cfg.map)
            .observe('play', $N.attachFunction(this.cfg.soundProvider, this.cfg.soundProvider.play))
            .observe('pause', $N.attachFunction(this.cfg.soundProvider, this.cfg.soundProvider.pause))
            .observe('move', this.attach(this._onMove))
            .observe('markeradd', this.attach(this._onMarkerAdd))
            .observe('markermove', this.attach(this._onMarkerMove))
            
            .draw();
            this.loadHTTP();
            
        },


        _onMove: function(e, data) {
            this.cfg.soundProvider.seek(data.offset);
        },


        _onMarkerMove: function(e, data) {
            if (this.cfg.map) {
                this.cfg.map.move(this.cfg.map.byId(data.id), data.offset);
            }
        },

        _onMarkerAdd: function(e, data) {
            if (this.cfg.map) {
                //this.refreshMarkersText(this.cfg.map);
                this.cfg.map.addNew(data.offset, '');
            //this.updateMarkersDiv(this.cfg.map, data.offset);

            }
        },

        loadHTTP: function(){

            //itemid is the item (spund file) name
            var sPath = window.location.pathname;
            //remove last "/" or last "/#", if any...
            sPath = sPath.replace(/\/#*$/,"");
            var itemid = sPath.substring(sPath.lastIndexOf('/') + 1);

            //WARNING: use single quotes for the whole string!!
            //see http://stackoverflow.com/questions/4809157/i-need-to-pass-a-json-object-to-a-javascript-ajax-method-for-a-wcf-call-how-can
            var data2send = '{"id":"jsonrpc","params":["'+itemid+'"], "method":"telemeta.get_markers","jsonrpc":"1.0"}';
            var map = this.cfg.map;
            var me = this;
            $.ajax({
                type: "POST",
                url: '/json/',
                contentType: "application/json",
                data: data2send,
                dataType: "json",
                success: function(data) {
                    if(data){
                        if(data.result){
                            var result = data.result;
                            
                            for(var i =0; i< result.length; i++){
                                var marker = {
                                    id: result[i].public_id,
                                    offset: result[i].time,
                                    desc: result[i].description
                                };
                                map.add(marker);
                            }
                        }
                        
                    }
                    //me._setupPlayer();
                }
            });
            var g = 9;
        }

    

    });

    $N.notifyScriptLoad();

});
