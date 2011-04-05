

var playlistUtils = {
    playlists : {},
    
    addPlaylist: function(name, id){
        this.playlists[name]=id;
    },

    /*shows the popup for adding an item to the playlist*/
    showPopupAddToPlaylist: function(event,resourceType,objectId, optionalMessage){
        var $J = jQuery;
        var content = $J('<div/>').addClass("_popup_add_to_playlist");
        var addToPlaylist = this.addToPlaylist;
        for(var p in this.playlists){
            var id = this.playlists[p];

            var a =  $J('<a/>').
            attr('href','#').
            addClass("component_icon").
            addClass("list_item icon_playlist").
            html(p).
            //by wrapping the addToPlaylist function in order to accept the id variable as an argument 
            //we avoid calling the function with id = number_of_playlists for all anchors 
            //by returning another function (basically create another closure) we avoid executing the function
            //immediately
            click(function(id_){
                    return function(){
                        addToPlaylist(id_,resourceType,objectId,optionalMessage);
                        return false;
                    }
                }(id)
            );
            content.append(a);
        }
        return popup.show(content,event);
    },

    add : function(dictionary){

        if(dictionary.public_id===undefined){
            dictionary.public_id = uniqid();
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
    
    //resourceType can be: 'collection', 'item', 'marker'
    addToPlaylist: function(playlistId,resourceType,objectId, optionalOkMessage){
        consolelog(playlistId)
        var send = {
            'public_id':uniqid(),
            'resource_type':resourceType,
            'resource_id':objectId
        };
        json([playlistId,send],'telemeta.add_playlist_resource',function(){
            var p = popup;
            if(optionalOkMessage){
                p.show(jQuery('<div/>').addClass("icon_ok").addClass("component_icon").html(optionalOkMessage));
                setTimeout(function(){
                    p.hide();
                },1000);
            }else{
                p.hide(); //to be sure
            }
        });
    }


}

