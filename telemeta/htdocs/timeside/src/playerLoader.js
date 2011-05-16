/**
 * TimeSide - Web Audio Components
 * Copyright (c) 2011 Parisson
 * Author: Riccardo Zaccarelli <riccardo.zaccarelli gmail.com> and Olivier Guilyardi <olivier samalyse com>
 * License: GNU General Public License version 2.0
 */

/**
 * Class for loading a player. Requires a div#player, jQuery and all timeside javascript (player.js, markermap.js etcetera)
 */

var player; //global player variable

function togglePlayerMaximization() {
    consolelog('entered togglePlayerMaximization');
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



function loadPlayer(analizerUrl, soundUrl, itemId, visualizers, currentUserName){
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

   
    //consolelog('till here all ok1');
    var msgElm = $J('#loading_span_text'); //element to show messages
    //consolelog('till here all ok2');
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

        loadScripts('/timeside/src/',['rulermarker.js','markermap.js', 'player.js', 'ruler.js','divmarker.js'], function() {
            

            var p = new Player(jQuery('#player'), sound, durationInMsec, itemId, visualizers, currentUserName);
            consolelog('initialized player');
            p._setupInterface();

            player = p;

            $J('#player_maximized .toggle, #player_minimized .toggle').click(function() {
                togglePlayerMaximization();
                this.blur();
                return false;
            });
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
            consolelog('analyzer loaded, duration: '+duration);
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



//function loadPlayer(analizerUrl, soundUrl, itemId, visualizers, currentUserName){
//
//    if(!(analizerUrl) || !(soundUrl)){
//        return;
//    }
//
//    var $J = jQuery;
//    //consolelog('till here all ok1');
//    var msgElm = $J('#loading_span_text'); //element to show messages
//    //consolelog('till here all ok2');
//    if(msgElm){
//        msgElm.html('Loading analyzer...');
//    }
//    var url = urlNormalized();
//    var tableBody = $J('#analyzer_div_id').find('table').find('tbody:last');
//    var load_player = this.load_player;
//    $J.ajax({
//        url: analizerUrl, //'analyze/xml',
//        dataType: 'xml',
//        success: function(data){
//            //populatetable
//            $J.each($J(data).find('data'),function(index,element){
//                var elm = $J(element);
//                tableBody.append('<tr><td>'+elm.attr('name')+'</td><td>'+elm.attr('value')+'</td><td>'
//                    +elm.attr('unit')+'</td></tr>');
//            });
//            //loaded analizer, loading player
//            if(msgElm){
//                msgElm.html('Loading player...');
//            }
//            var duration = $J(data).find('#duration').attr('value');
//            duration = duration.split(":");
//            consolelog('analyzer loaded, duration: '+duration);
//            //format duration
//            var pin = parseInt;
//            var pfl = parseFloat;
//            var timeInMSecs=pin(duration[0])*3600+pin(duration[1])*60+pfl(duration[2]);
//            timeInMSecs = Math.round(timeInMSecs*1000);
//            load_player(soundUrl, timeInMSecs, itemId, visualizers, currentUserName);
//        },
//        error:function(){
//            playerError('Error loading analyzer');
//            //"<img src='/images/dialog-error.png' style='vertical-align:middle'/><span class='login-error'>Error loading analyzer</span>");
//        }
//    });
//}
//
//
////loads a player WAITING for the sound identified by soundUrl to be FULLY LOADED!!!!
//function load_player(soundUrl, durationInMsecs, itemId, visualizers, currentUserName) {
//    consolelog('PlayerLoader.load_player: '+soundUrl+' '+durationInMsecs);
//    var load_player2 = this.load_player2;
//
//    //this variable can be changed to load a sound immediately or not
//    var loadImmediately = true;
//    if(durationInMsecs){
//        loadImmediately = false;
//    }
//    var sound = soundManager.createSound({
//        id: 'sound',
//        autoLoad: loadImmediately,
//        url: soundUrl,
//        onload: function() { //formerly was: whileloading
//            //PROBLEM/BUG: on chrome and firefox whileloading is the same as onload,
//            //ie it is not called at regular interval but when the whole file has loaded
//            if(loadImmediately){
//                consolelog('entering while loading setting up---------------'+this.bytesLoaded+' of '+this.bytesTotal);
//                loadImmediately=false;
//                load_player2(this, this.duration, itemId, visualizers, currentUserName);
//            }
//        }
//    });
//    if(!loadImmediately){
//        //TODO: remove this code is only temporary here!!!!!!!!!!!!!!!!!!!!1
//        loadScripts('/timeside/src/',['rulermarker.js', //'markerlist.js',
//            'markermap.js', 'player.js', 'ruler.js','divmarker.js'], function(){
//                load_player2(sound,durationInMsecs,itemId, visualizers, currentUserName);
//            });
//    }
//
//}
////NOTE: the duration must be present. Loaded from xmlanalyzer (see above)
//function load_player2(sound, durationInMsec, itemId, visualizers, currentUserName) {
//
//    if (!$('#player').length){
//        return;
//    }
//    consolelog("entered load_player2");
//
//    //TODO: what are we doing here????
////    $('.ts-wave a img').insertAfter('.ts-wave a');
////    $('.ts-wave a').remove();
//
//    var p = new Player(jQuery('#player'), sound, durationInMsec, itemId, visualizers, currentUserName);
//    consolelog('initialized player');
//    p._setupInterface();
//    //p.loadMarkers();
//
//    player = p;
//
////    var change_visualizer_click = change_visualizer_clicked;
////    $('#visualizer_id').change(change_visualizer_click);
//    //$('#visualizer_id_form').submit(change_visualizer_clicked);
//
//    $('#player_maximized .toggle, #player_minimized .toggle').click(function() {
//        togglePlayerMaximization();
//        this.blur();
//        return false;
//    });
//
//
//}
