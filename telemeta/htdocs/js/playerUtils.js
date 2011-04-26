var player; //public player variable

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
        if (player){
            player.refreshImage();
        }
        //img.remove();
        setTimeout(function(){
            if(src){
                img.attr('src',src);
            }
            visId.removeAttr("disabled");
        },300);
    },600);
}

function loadPlayer(analizerUrl, soundUrl){
    if(!(analizerUrl) || !(soundUrl)){
        return;
    }
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
        //TODO: remove this code is only temporary here!!!!!!!!!!!!!!!!!!!!1
        loadScripts('/timeside/src/',['rulermarker.js', //'markerlist.js',
            'markermap.js', 'player.js', 'ruler.js','divmarker.js'], function(){
                load_player2(sound,durationInMsecs);
            });
    }

}
//NOTE: the duration must be present. Loaded from xmlanalyzer (see above)
function load_player2(sound, durationInMsec) {
    if (!$('#player').length){
        return;
    }
    consolelog("entered load_player2");

    //TODO: what are we doing here????
    $('.ts-wave a img').insertAfter('.ts-wave a');
    $('.ts-wave a').remove();

    var p = new Player(jQuery('#player'), sound, durationInMsec);
    consolelog('initialized player');
    p._setupInterface(CURRENT_USER_NAME ? true : false);
    //p.loadMarkers();

    player = p;

    var change_visualizer_click = change_visualizer_clicked;
    $('#visualizer_id').change(change_visualizer_click);
    //$('#visualizer_id_form').submit(change_visualizer_clicked);

    $('#player_maximized .toggle, #player_minimized .toggle').click(function() {
        togglePlayerMaximization();
        this.blur();
        return false;
    });


}
