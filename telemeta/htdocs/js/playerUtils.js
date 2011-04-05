//var sound = null;
//var soundUrl = null;
//var soundEngineReady = false;
var map;
//var provider;
var player;
var player_image_url = null;
var controller;

function togglePlayerMaximization() {
    consolelog('entered togglePlayerMaximization');
    var view = $('#player');
    $('#player_maximized, #player_minimized').css('display', 'none');
    var ctr;
    if (view.parents('#player_maximized').length) {
        ctr = $('#player_minimized').append(view);
    } else {
        ctr = $('#player_maximized').append(view);
    }
    ctr.css({
        opacity: 0,
        display: 'block'
    });
    if (player){
        player.resize();
    }
    ctr.animate({
        opacity: 1
    }, 100);
}

function change_visualizer_clicked(){
    var $J = jQuery;
    var form = $J("#visualizer_id_form");
    //var img = jQuery("<img/>").attr("src","/images/wait.gif").css('verticalAlign','middle');

    var visId = $J("#visualizer_id");
    visId.attr("disabled","disabled");
    var img = $J(form.children()[0]);
    var src = undefined;
    if(img.attr('src')){
        src = img.attr('src');
        img.attr("src","/images/wait_small.gif");
    }

    //form.append(img);
    setTimeout(function(){
        change_visualizer();
        //img.remove();
        setTimeout(function(){
            if(src){
                img.attr('src',src);
            }
            visId.removeAttr("disabled");
        },300);
    },600);
}

function change_visualizer() {
    consolelog('playerUtils.changeVisualizer');
    set_player_image_url($('#visualizer_id').get(0).value);
    if (player){
        player.refreshImage();
    }
    return false;
}




function loadPlayer(analizerUrl, soundUrl){
    var $J = jQuery;
    var msgElm = $J('#loading_span_text'); //element to show messages
    if(msgElm){
        msgElm.html('Loading analyzer...');
    }
    var url = urlNormalized();
    var tableBody = $J('#analyzer_div_id').find('table').find('tbody:last');
    var load_player = this.load_player;
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
                load_player(soundUrl, timeInMSecs);
        },
        error:function(){
            msgElm.parent().html("<img src='/images/dialog-error.png' style='vertical-align:middle'/><span class='login-error'>Error loading analyzer</span>");
        }
    });
}


//loads a player WAITING for the sound identified by soundUrl to be FULLY LOADED!!!!
function load_player(soundUrl, durationInMsecs) {
//    if (!$('#player').length){
//        return;
//    }
    consolelog('PlayerUtils.load_player: '+soundUrl+' '+durationInMsecs);
    var load_player2 = this.load_player2;

    //this variable can be changed to load a sound immediately or not
    var loadImmediately = true;
    if(durationInMsecs){
        loadImmediately = false;
    }
    var sound = soundManager.createSound({
        id: 'sound',
        autoLoad: loadImmediately,
        url: soundUrl,
        onload: function() { //formerly was: whileloading
            //PROBLEM/BUG: on chrome and firefox whileloading is the same as onload,
            //ie it is not called at regular interval but when the whole file has loaded
            if(loadImmediately){
                consolelog('entering while loading setting up---------------'+this.bytesLoaded+' of '+this.bytesTotal);
                loadImmediately=false;
                load_player2(this, this.duration);
            }
        }
    });
    if(!loadImmediately){
        load_player2(sound,durationInMsecs);
    }
}
//NOTE: the sound MUST be FULLY LOADED!!!!!! otherwise the duration is null. This method is called from load_player
function load_player2(sound, durationInMsec) {
    if (!$('#player').length){
        return;
    }
    consolelog("entered load_player2");

    $('.ts-wave a img').insertAfter('.ts-wave a');
    $('.ts-wave a').remove();

    TimeSide.load(function() {
        map = new TimeSide.MarkerMap();

        player = new TimeSide.Player('#player', {
            image: get_player_image_src,
            'sound': sound,
            'soundDurationInMsec': durationInMsec
        });
        change_visualizer();
        controller = new TimeSide.Controller({
            player: player,
            map: map
        });
    });

    var change_visualizer_click = change_visualizer_clicked;
    $('#visualizer_id').change(change_visualizer_click);
    //$('#visualizer_id_form').submit(change_visualizer_clicked);

    $('#player_maximized .toggle, #player_minimized .toggle').click(function() {
        togglePlayerMaximization();
        this.blur();
        return false;
    });


}
function set_player_image_url(str) {
    player_image_url = str;
}

function get_player_image_src(width, height) {
    var src = null;
    if (player_image_url && (width || height)) {
        src = player_image_url.replace('WIDTH', width + '').replace('HEIGHT', height + '');
    }
    return src;
}

//======================================================================
//OLD STUFF
//======================================================================


//TODO REMOVE NOTE: the sound MUST be FULLY LOADED!!!!!! otherwise the duration is null. This method is called from load_player
function load_player2Old(sound) {
    if (!$('#player').length){
        return;
    }
    consolelog("entered load_player2");
    //        sound = soundManager.createSound({
    //            id: 'sound',
    //            url: soundUrl
    //        });
    //soundUrl = $('.ts-wave a').attr('href');

    $('.ts-wave a img').insertAfter('.ts-wave a');
    $('.ts-wave a').remove();
   
    TimeSide.load(function() {
        map = new TimeSide.MarkerMap();
        //        provider = new TimeSide.SoundProvider({
        //            duration: sound.duration
        //        });
        //        provider.setSource(sound);
        player = new TimeSide.Player('#player', {
            image: get_player_image_src,
            'sound': sound
        });
        change_visualizer();
        controller = new TimeSide.Controller({
            player: player,
            //soundProvider: provider,
            map: map
        });
    //change_visualizer();
    //player.resize();
    //player.updateVolumeAnchor(provider.getVolume());
    });

    //    $('#visualizer_id').change(change_visualizer);
    //    $('#visualizer_id_form').submit(change_visualizer);
    $('#visualizer_id').change(change_visualizer_clicked);
    $('#visualizer_id_form').submit(change_visualizer_clicked);

    $('#player_maximized .toggle, #player_minimized .toggle').click(function() {
        togglePlayerMaximization();
        this.blur();
        return false;
    });


}

//TODO: REMOVE loads a player WAITING for the sound identified by soundUrl to be FULLY LOADED!!!!
function load_playerOld(soundUrl) {
    if (!$('#player').length){
        return;
    }
    consolelog('PlayerUtils.load_player: '+soundUrl);
    var callback = this.load_player2;

    //this variable can be changed to load a sound immediately or not
    var loadImmediately = true;
    var sound = soundManager.createSound({
        id: 'sound',
        autoLoad: loadImmediately,
        url: soundUrl,
        whileloading: function() {
            //PROBLEM/BUG: on chrome and firefox whileloading is the same as onload,
            //ie it is not called at regular interval but when the whole file has loaded
            if(loadImmediately){
                consolelog('entering while loading setting up---------------'+this.bytesLoaded+' of '+this.bytesTotal);
                loadImmediately=false;
                callback(this);
            }
        }
    });
    if(!loadImmediately){
        callback(sound);
    }
}
