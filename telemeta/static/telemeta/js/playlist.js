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
    'border': '1px solid #999',
    'padding': '1ex'
};
PopupDiv.okButtonTitle = 'Ok';
PopupDiv.okButtonClass = 'component_icon button icon_ok';
PopupDiv.closeButtonTitle = '';
PopupDiv.closeButtonClass = 'markersdivDelete';
PopupDiv.defaultCloseOperation = 'remove';
PopupDiv.focusable = true;
PopupDiv.listItemClass = "component_icon list_item icon_playlist";


var playlistUtils = {
    playlists : [],
    id: '', // ID var: used to edit playlist
    title: '',
    description: '',
    state: 'stop', // state var: to state play or pause glyphicon
    playing: '', // playing var: used to know if an audio is already playing or not
    audio: new Audio(),

    addPlaylist: function (name, id) {
        this.playlists.push({
            'name': name,
            'id': id
        });
    },

    addEditPlaylist: function (id, title, description) {
        this.playlists.push({
            'id': id,
            'title': title,
            'description': description,
        });
    },

    addNewPlaylist: function(){
        this.add({
            'title': $('#titleAdd').val(),
            'description': $('#descriptionAdd').val(),
        });
    },

    // function to change global var ID (used when edit button is pressed)
    editVar: function(id){
        this.id = id;
        for (var i=0; i<this.playlists.length; i++){
            if (this.playlists[i].id == id){
                $('#titleEdit').val(this.playlists[i].title);
                $('#descriptionEdit').val(this.playlists[i].description);
            }
        }
    },

    editPlaylist: function(){
        this.update({
            'public_id': this.id,
            'title': $('#titleEdit').val(),
            'description': $('#descriptionEdit').val(),
        });
        this.id = ""; // init ID
    },

    loadAudio: function(resElem){
        this.audio.src = resElem;
        this.audio.play();
    },

    stopAudio: function(){
        this.audio.pause();
    },

    changeGlyph: function(resElem){
        //wait image element
        var waitImg = "<img id='wait' src='"+static_url+"telemeta/images/wait.gif' style='width: 15px;'/>";
        //load filepath when the elment id is the public_id of resource element.
       if(resElem.indexOf("/")==-1){
           $('#'+resElem).removeClass().append(waitImg);
           json_sync([resElem, "mp3"], "telemeta.get_item_export_url", function (data) {
               $('#'+resElem).attr('id', data.result);
               resElem = data.result;
           });
       }
       if(this.playing === '' || this.playing === resElem){
           if(this.state === 'stop'){
               //if wait image is not displayed
               if($('#wait').length==0){
                   $('[id="'+resElem+'"]').append(waitImg);
               }
               this.state = 'play';
               document.getElementById(resElem).setAttribute("class", "glyphicon glyphicon-pause");
               playlistUtils.loadAudio(resElem);
               this.playing = resElem;
           }
           else if(this.state === 'play'){
               this.state = 'stop';
               document.getElementById(resElem).setAttribute("class", "glyphicon glyphicon-play");
               playlistUtils.stopAudio();
               this.playing = '';
           }
       }
       else{
           playlistUtils.stopAudio();
           this.state = 'stop';
           document.getElementById(this.playing).setAttribute("class", "glyphicon glyphicon-play");
           this.playing = '';
           playlistUtils.changeGlyph(resElem);
       }
    },

    /**
     * Returns an uniqid by creating the current local time in millisecond + a random number. Used for markers and some json calls
     * Copied from Timeside.utils.uniqid (Timeside might NOT ALWAYS be loaded, see home.html when user is authenitcated)
     *
     */
    uniqid: function () {
        var d = new Date();
        return new String(d.getTime() + '' + Math.floor(Math.random() * 1000000)).substr(0, 18);
    },

    add: function (dictionary) {

        if (dictionary.public_id === undefined) {
            dictionary.public_id = this.uniqid();
        }
        if (dictionary.user === undefined) {
            dictionary.user = CURRENT_USER_NAME;
        }

        json([dictionary], 'telemeta.add_playlist', function () {
            window.location.reload();
        });
    },

    remove: function (id) {
        json([id], 'telemeta.del_playlist', function () {
            window.location.reload();
        });
    },

    removeResource: function (id, range_playlist) {
        json([id, range_playlist], 'telemeta.del_playlist_resource', function (data) {
            var id = data.result;
            window.location.pathname = '/desk/lists/' + id;
        });
    },

    update: function (dictionary) {
        json([dictionary], 'telemeta.update_playlist', function () {
            window.location.reload();
        });
    },

    /*shows the popup for adding a resource to a playlist*/
    showAddResourceToPlaylist: function (anchorElement, resourceType, objectId, optionalOkMessage) {
        var ar = [];
        var pl = this;
        var playlists = this.playlists;

        for(var i=0; i< playlists.length; i++){
            ar.push(playlists[i].name);
        }


        if(!ar.length){
            this.showAdd(anchorElement);
        }

        //var addFcn = this.addResourceToPlaylist;
        new PopupDiv({
            invoker: anchorElement,
            content: ar,
            onOk: function (data) {
                var val = data.selIndex;
                var callbackok = undefined;

                if (optionalOkMessage) {
                    callbackok = function () {
                        localStorage['messOkPlaylist'] = optionalOkMessage;
                        localStorage['displayOkPlaylist']=true;
                        window.location.reload();
                    }
                }
                pl.addResourceToPlaylist.apply(pl, [playlists[val].id, resourceType, objectId, callbackok]);
            }
        }).show();

    },

    //resourceType can be: 'collection', 'item', 'marker'
    addResourceToPlaylist: function (playlistId, resourceType, objectId, callbackOnSuccess, callbackOnError) {
        var send = {
            'public_id': this.uniqid(),
            'resource_type': resourceType,
            'resource_id': objectId
        };
        json([playlistId, send], 'telemeta.add_playlist_resource', callbackOnSuccess, callbackOnError);
    },

    messageOk: function () {
        if (localStorage['displayOkPlaylist']) {
            var p = new PopupDiv({
                content: "<div class='component_icon icon_ok'>" + localStorage['messOkPlaylist']+ "</div>",
                focusable: false

            });
            p.bind('show', function () {
                this.setTimeout('close', 1500); //this refers to p
            });
            p.show();
            localStorage.removeItem('displayOkPlaylist');
            localStorage.removeItem('messOkPlaylist');
        }

    }
}

$(function () {
    //event in order to remove wait image when audio is playing
    playlistUtils.audio.onplay = function () {
        $('#wait').remove();
    }
})
