/*
 * Copyright (C) 2007-2011 Parisson
 * Copyright (c) 2011 Riccardo Zaccarelli <riccardo.zaccarelli@gmail.com>
 * Copyright (c) 2010 Olivier Guilyardi <olivier@samalyse.com>
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
 * Authors: Riccardo Zaccarelli <riccardo.zaccarelli@gmail.com>
 *          Olivier Guilyardi <olivier@samalyse.com>
 */

/**
 * Class for loading a player. Requires a div#player, jQuery and all timeside javascript (player.js, markermap.js etcetera)
 */

var player; //global player variable

function togglePlayerMaximization() {
    var $ = jQuery;
    var view = $('#player');
    $('#player_maximized, #player_minimized').css('display', 'none');
    var ctr;
    var dynamicResize = false;
    if (view.parents('#player_maximized').length) {
        ctr = $('#player_minimized').append(view);
    } else {
        ctr = $('#player_maximized').append(view);
        dynamicResize = true;
    }
    ctr.css({
        opacity: 0,
        display: 'block'
    });
    var p = player;
    if (p){
        p.resize();
    }
    ctr.animate({
        opacity: 1
    }, 100);
    if (p){
        p.setDynamicResize(dynamicResize);
    }
}

//function loadPlayer_(htmlContainer, w, h, durationInMsec, soundUrl, callback){
//    var $ = jQuery;
//    if(w<=0){
//        w = 360;
//    }
//    if(h<=0){
//        h= 130;
//    }
//    if(!callback || (typeof callback !== 'function')){
//        callback = function(){};
//    }
//    if(!(htmlContainer instanceof $)){
//        htmlContainer = $(htmlContainer);
//    }
//    if(htmlContainer.length!=1){
//        throw 'invalid htmlContainer';
//    }
//    var errMsg = '';
//    if(typeof durationInMsecOrAnalyzerUrl == 'number'){
//        load_player(soundUrl, durationInMsecOrAnalyzerUrl, itemId, visualizers, currentUserName);
//    }else{
//
//        $.ajax({
//            url: durationInMsecOrAnalyzerUrl, //'analyze/xml',
//            dataType: 'xml',
//            success: function(data){
//                //populatetable
//                $J.each($J(data).find('data'),function(index,element){
//                    var elm = $J(element);
//                    tableBody.append('<tr><td>'+elm.attr('name')+'</td><td>'+elm.attr('value')+'</td><td>'
//                        +elm.attr('unit')+'</td></tr>');
//                });
//                //loaded analizer, loading player
//                if(msgElm){
//                    msgElm.html('Loading player...');
//                }
//                var duration = $J(data).find('#duration').attr('value');
//                duration = duration.split(":");
//                //format duration
//                var pin = parseInt;
//                var pfl = parseFloat;
//                var timeInMSecs=pin(duration[0])*3600+pin(duration[1])*60+pfl(duration[2]);
//                timeInMSecs = Math.round(timeInMSecs*1000);
//                load_player(soundUrl, timeInMSecs, itemId, visualizers, currentUserName);
//            },
//            error:function(){
//                errMsg = 'Error loading analyzer';
//            }
//        });
//    }
//}


function loadPlayer(analizerUrl, soundUrl, itemId, visualizers, currentUserName, isStaffOrSuperuser){
    var $J = jQuery;
    var playerDiv = $J('#player');
    if (!playerDiv.length){
        //playerError('div #player does not exists');
        //DO NOT RAISE ANY ERROR, JUST RETURN
        return;
    }

    if(!(analizerUrl)){
        playerError('invalid analyzer url');
        return;
    }

    if(!(soundUrl)){
        playerError('invalid sound url');
        return;
    }

   
    var msgElm = $J('#loading_span_text'); //element to show messages
    if(msgElm){
        msgElm.html('Loading analyzer...');
    }
    
    var tableBody = $J('#analyzer_div_id').find('table').find('tbody:last');

    //function to be executed when the analyzer has fully loaded (ie, a duration is provided)
    function load_player(soundUrl, durationInMsec, itemId, visualizers, currentUserName) {
        var sound = soundManager.createSound({
            id: 'sound',
            autoLoad: false,
            url: soundUrl
        });

        loadScripts('/timeside/js/',['rulermarker.js','markermap.js', 'player.js', 'ruler.js','divmarker.js'], function() {
            

            var p = new Player(jQuery('#player'), sound, durationInMsec, itemId, visualizers, currentUserName, isStaffOrSuperuser);

            var cbckAtEnd = function(){
                //this callback is executed at the end and does 3 things:
                //1)sets up the marker tab
                $J('#loading_span').empty().remove();
                //                    setUpPlayerTabs([jQuery('#tab_analysis'), jQuery('#tab_markers')],
                //                    [jQuery('#analyzer_div_id'), jQuery('#markers_div_id')], tabIndex,
                //                    'tab_selected','tab_unselected');
                var map = p.getMarkerMap();
                var tabIndex = map.length ? 1 : 0;
                setUpPlayerTabs($J('#tab_analysis').add($J('#tab_markers')),
                    [$J('#analyzer_div_id'), $J('#markers_div_id')], tabIndex,
                    'tab_selected','tab_unselected');
                //2)  and selects the current marker if it is present on the url
                var url = window.location.href+"";
                var lastPart = url.replace(/\/+$/,"").replace(/^.*\/([^\/]*)$/,"$1");
                var selOffs = -1;
                map.each(function(i,marker){
                    if(marker.id == lastPart){
                        selOffs = marker.offset;
                    }
                });
                if(selOffs >= 0){
                    p.setSoundPosition(selOffs);
                }
                //3) assing a binding to the player maximization button:
                $J('#player_maximized .toggle, #player_minimized .toggle').click(function() {
                    togglePlayerMaximization();
                    return false;
                });
            }
            p.setupInterface(cbckAtEnd);
            player = p;
        });
    };

    $J.ajax({
        url: analizerUrl, //'analyze/xml',
        dataType: 'xml',
        success: function(data){
            //populatetable
            $J.each($J(data).find('data'),function(index,element){
                var elm = $J(element);
                tableBody.append('<tr><td>'+elm.attr('name')+'</td><td>'+elm.attr('value')+'</td><td>'
                    +elm.attr('unit')+'</td></tr>');
            });
            //loaded analizer, loading player
            if(msgElm){
                msgElm.html('Loading player...');
            }
            var duration = $J(data).find('#duration').attr('value');
            duration = duration.split(":");
            //format duration
            var pin = parseInt;
            var pfl = parseFloat;
            var timeInMSecs=pin(duration[0])*3600+pin(duration[1])*60+pfl(duration[2]);
            timeInMSecs = Math.round(timeInMSecs*1000);
            load_player(soundUrl, timeInMSecs, itemId, visualizers, currentUserName);
        },
        error:function(){
            playerError('Error loading analyzer');
        //"<img src='/images/dialog-error.png' style='vertical-align:middle'/><span class='login-error'>Error loading analyzer</span>");
        }
    });
}