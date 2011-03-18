

var playlist = {
    add : function(element){
        var $J = jQuery;

        var dText = $('<input/>')
        .attr('type','text').val("");
        var tText = $('<input/>')
        .attr('type','text').val("");

        var table = $J('<table/>')
        .append($J('<tr/>')
            .append($J('<td/>').html('title'))
            .append($J('<td/>').append(tText)))
        .append($J('<tr/>')
            .append($J('<td/>').html('description'))
            .append($J('<td/>').append(dText)));

        var onOk= function(){
            var pl = [{
                "public_id":uniqid(),
                "title":tText.val(),
                "description":dText.val(),
                user:CURRENT_USER_NAME
            }];
            json(pl,'telemeta.add_playlist',function(){
                window.location.reload();
            },true);
        };
        popupDialog(element,table,onOk);

    }
//    ,add:function(title){
//        if(title instanceof String)
//
//        var pl = [{"public_id":new Date().getTime(), "title":title, "description":"", user:"admin"}];
//    json(pl,'telemeta.add_playlist',alert('done'),true);
//}
}

//varf();
//function varf(){
//    playlist.add('myplaylist');
//}

