/**
 * TimeSide - Web Audio Components
 * Copyright (c) 2011 Parisson
 * Author: Riccardo Zaccarelli <riccardo.zaccarelli gmail.com>
 * License: GNU General Public License version 2.0
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

var playlistUtils = {
    playlists : [],
    
    addPlaylist: function(name, id){
        //this.playlists[name]=id;
        this.playlists.push({
            'name':name,
            'id':id
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
            showok:true,
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
    

    add : function(dictionary){

        if(dictionary.public_id===undefined){
            dictionary.public_id = uniqid(); //defined in application.js
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


    /*shows the popup for adding a resource to a playlist*/
    showAddResourceToPlaylist: function(anchorElement,resourceType,objectId, optionalOkMessage){
        var ar = [];
        var playlists = this.playlists;
        for(var i=0; i< playlists.length; i++){
            ar.push({
                'html':playlists[i].name,
                'class':"component_icon list_item icon_playlist"
            });
        }
        if(!ar.length){
            return;
        }
        var addFcn = this.addResourceToPlaylist;
        new PopupDiv({
            invoker:anchorElement,
            content: ar,
            onOk:function(data){
                var val = data.selIndex;
                consolelog(data);
                var callbackok = undefined;
                if(optionalOkMessage){
                    callbackok = function(){
                        var p =new PopupDiv({
                            content : "<div class='component_icon icon_ok'>"+optionalOkMessage+"</div>",
                            focusable: false

                        });
                        p.bind('show', function(){
                            this.closeLater(1500); //this refers to p
                        });
                        p.show();
                    }
                }
                addFcn(playlists[val].id,resourceType,objectId,callbackok);


            }
        }).show();

    },

    //resourceType can be: 'collection', 'item', 'marker'
    //addResource RENAME TODO!!!!
    addResourceToPlaylist: function(playlistId,resourceType,objectId, callbackOnSuccess,callbackOnError){
        consolelog(playlistId)
        var send = {
            'public_id':uniqid(),
            'resource_type':resourceType,
            'resource_id':objectId
        };
        json([playlistId,send],'telemeta.add_playlist_resource',callbackOnSuccess,callbackOnError);
    }


}

