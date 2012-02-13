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
 * Class for managing playlists in telemeta.
 * Requires jQuery and PopupDiv
 */

//default PopupDiv properties for playlists (mainly for css appearence)
PopupDiv.popupClass = 'control component';
PopupDiv.popupCss = {
    'border':'1px solid #999',
    'padding':'1ex'
};
PopupDiv.okButtonTitle =  'Ok';
PopupDiv.okButtonClass =  'component_icon button icon_ok';
PopupDiv.closeButtonTitle =  '';
PopupDiv.closeButtonClass =  'markersdivDelete';
PopupDiv.defaultCloseOperation = 'remove';
PopupDiv.focusable = true;
PopupDiv.listItemClass = "component_icon list_item icon_playlist";


var playlistUtils = {
    playlists : [],

    addPlaylist: function(name, id){
        this.playlists.push({
            'name':name,
            'id':id
        });
    },

    addEditPlaylist: function(id, title, description){
        this.playlists.push({
            'id': id,
            'title': title,
            'description': description,
        });
    },

    showAdd: function(anchorElement){

        var t = gettrans('title');
        var d = gettrans('description');
        var dd = {};
        dd[t]='';
        dd[d]='';
        var playlist = this;
        new PopupDiv({
            'content':dd,
            invoker:anchorElement,
            showOk:true,
            onOk:function(data){
                if(!data[t] && !data[d]){
                    return;
                }
                //convert language
                playlist.add({
                    'title':data[t],
                    'description':data[d]
                });
            }
        }).show();

    },
    /**
     * Returns an uniqid by creating the current local time in millisecond + a random number. Used for markers and some json calls
     * Copied from Timeside.utils.uniqid (Timeside might NOT ALWAYS be loaded, see home.html when user is authenitcated)
     *
     */
    uniqid : function() {
        var d = new Date();
        return new String(d.getTime() + '' + Math.floor(Math.random() * 1000000)).substr(0, 18);
    },
    add : function(dictionary){

        if(dictionary.public_id===undefined){
            dictionary.public_id = this.uniqid(); //defined in application.js
        }
        if(dictionary.user===undefined){
            dictionary.user = CURRENT_USER_NAME;
        }

        json([dictionary],'telemeta.add_playlist',function(){
            window.location.reload();
        });
    },
    
    remove: function(id){
        json([id],'telemeta.del_playlist',function(){
            window.location.reload();
        });
    },

    removeResource: function(id){
        json([id],'telemeta.del_playlist_resource',function(){
            window.location.reload();
        });
    },

    update : function(dictionary){
        json([dictionary],'telemeta.update_playlist',function(){
        window.location.reload();
        });
    },

    showEdit: function(anchorElement, id){

        var t = gettrans('title');
        var d = gettrans('description');
        var dd = {};
        var playlist = this;
        
        var playlists = this.playlists;
        for (var i=0; i< playlists.length; i++){
            if (playlists[i].id == id){
                dd[t] = playlists[i].title;
                dd[d] = playlists[i].description;
            }
        }
        
        new PopupDiv({
            'content':dd,
                    invoker:anchorElement,
                    showOk:true,
                    onOk:function(data){
                        if(!data[t] && !data[d]){
                            return;
                        }
                        //convert language
                        playlist.update({
                            'public_id': id,
                            'title': data[t],
                            'description': data[d],
                        });
                    }
        }).show();
    },
    
    /*shows the popup for adding a resource to a playlist*/
    showAddResourceToPlaylist: function(anchorElement, resourceType, objectId, optionalOkMessage){
        var ar = [];
        var playlists = this.playlists;
        for(var i=0; i< playlists.length; i++){
            ar.push(playlists[i].name);
        }
        var pl = this;
        
        if(!ar.length){
            pl.showAdd(anchorElement);
        }
        
        //var addFcn = this.addResourceToPlaylist;
        new PopupDiv({
            invoker:anchorElement,
            content: ar,
            onOk:function(data){
                var val = data.selIndex;
                var callbackok = undefined;
                    
                if(optionalOkMessage){
                    callbackok = function(){
                        var p =new PopupDiv({
                            content : "<div class='component_icon icon_ok'>"+optionalOkMessage+"</div>",
                            focusable: false

                        });
                        p.bind('show', function(){
                            this.setTimeout('close',1500); //this refers to p
                        });
                        p.show();
                    }
                }
                pl.addResourceToPlaylist.apply(pl,[playlists[val].id,resourceType,objectId,callbackok]);
            }
        }).show();

    },

    //resourceType can be: 'collection', 'item', 'marker'
    addResourceToPlaylist: function(playlistId,resourceType,objectId, callbackOnSuccess,callbackOnError){
        var send = {
            'public_id':this.uniqid(),
            'resource_type':resourceType,
            'resource_id':objectId
        };
        json([playlistId,send],'telemeta.add_playlist_resource',callbackOnSuccess,callbackOnError);
    }


}

