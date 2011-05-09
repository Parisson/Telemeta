
var playlistUtils = {
    playlists : [],
    
    addPlaylist: function(name, id){
        //this.playlists[name]=id;
        this.playlists.push({
            'name':name,
            'id':id
        });
    },

    /*shows the popup for adding an item to the playlist*/
    showAddToPlaylist: function(anchorElement,resourceType,objectId, optionalOkMessage){
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
        var addFcn = this.addToPlaylist;
        new PopupDiv({
            defaultCloseOperation: 'remove',
            focusable:true,
            invoker:anchorElement,
            content: ar,
            ok:function(data){
                var val = data.selIndex;
                consolelog(data);
                var callbackok = undefined;
                if(optionalOkMessage){
                    callbackok = function(){
                        var p =new PopupDiv({
                            content : "<div class='component_icon icon_ok'>"+optionalOkMessage+"</div>",
                            defaultCloseOperation: 'remove'

                        });
                        p.bind('show', function(){
                            this.closeLater(2500)
                        });
                        p.show();
                    }
                }
                addFcn(playlists[val].id,resourceType,objectId,callbackok);
                
                
            }
        }).show();

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
            focusable:true,
            invoker:anchorElement,
            defaultCloseOperation:'remove',
            showclose:true,
            showok:true,
            ok:function(data){
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
    addToPlaylist: function(playlistId,resourceType,objectId, callbackOnSuccess,callbackOnError){
        consolelog(playlistId)
        var send = {
            'public_id':uniqid(),
            'resource_type':resourceType,
            'resource_id':objectId
        };
        json([playlistId,send],'telemeta.add_playlist_resource',callbackOnSuccess,callbackOnError);
    }


}

