

var playlistUtils = {
    
    //    add : function(event){
    //
    //        var $J = jQuery;
    //
    //        var dText = $('<input/>')
    //        .attr('type','text').val("");
    //        var tText = $('<input/>')
    //        .attr('type','text').val("");
    //
    //        var table = $J('<table/>')
    //        .append($J('<tr/>')
    //            .append($J('<td/>').html('title'))
    //            .append($J('<td/>').append(tText)))
    //        .append($J('<tr/>')
    //            .append($J('<td/>').html('description'))
    //            .append($J('<td/>').append(dText)));
    //
    //        var onOk= function(){
    //            var pl = [{
    //                "public_id":uniqid(),
    //                "title":tText.val(),
    //                "description":dText.val(),
    //                user:CURRENT_USER_NAME
    //            }];
    //            json(pl,'telemeta.add_playlist',function(){
    //                window.location.reload();
    //            },true);
    //        };
    //        var onCancel= function(){
    //            popup.hide();
    //            return false;
    //        };
    //        var subdiv = $J('<div/>').append(
    //            $J('<a/>').
    //            html('Cancel').
    //            css('float','right').
    //            addClass('mediaitem_button').
    //            addClass('mediaitem_button_cancel').
    //            attr('href','#').
    //            click(function(){
    //                return onCancel();
    //            })
    //            ).append(
    //            $J('<a/>').
    //            html('Ok').
    //            css('float','right').
    //            addClass('mediaitem_button').
    //            addClass('mediaitem_button_ok').
    //            attr('href','#').
    //            click(function(){
    //                return onOk();
    //            })
    //            );
    //        //popupDialog(element,table,onOk);
    //        popup.show($J('<div/>').append(table).append(subdiv), event);
    //    },

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
    addToPlaylist: function(playlistId,resourceType,objectId){
        var send = {
            'public_id':uniqid(),
            'resource_type':resourceType,
            'resource_id':objectId
        };
        json([playlistId,send],'telemeta.add_playlist_resource',function(){
            var p = popup;
            p.show(jQuery('<div/>').html('<a style="border:0" class="mediaitem_button mediaitem_button_ok">Ok</span>'));
            setTimeout(function(){p.hide()},600);
        });
    }


}

