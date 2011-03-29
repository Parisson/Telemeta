var sound = null;
var soundUrl = null;
var soundEngineReady = false;
var map;
var provider;
var player;
var player_image_url = null;

function togglePlayerMaximization() {
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

function load_sound() {
    if (!sound && soundUrl && soundEngineReady) {
        sound = soundManager.createSound({
            id: 'sound',
            url: soundUrl
        });
        
        TimeSide.load(function() {
            provider.setSource(sound);
            player.updateVolumeAnchor(provider.getVolume());
        });

    // sound.load(); // Auto-loading overloads the Django test server
    }
}

function change_visualizer() {
    set_player_image_url($('#visualizer_id').get(0).value);
    if (player){
        player.refreshImage();
    }
    return false;
}

function load_player(duration) {
    $(document).ready(function () {
        if (!$('#player').length){
            return;
        }
        soundUrl = $('.ts-wave a').attr('href');

        $('.ts-wave a img').insertAfter('.ts-wave a');
        $('.ts-wave a').remove();

        TimeSide.load(function() {
            map = new TimeSide.MarkerMap();
            provider = new TimeSide.SoundProvider({
                duration: duration
            });
            player = new TimeSide.Player('#player', {
                image: get_player_image_src
            });
            controller = new TimeSide.Controller({
                player: player,
                soundProvider: provider,
                map: map
            });
            change_visualizer();
            player.resize();
        });

        $('#visualizer_id').change(change_visualizer);
        $('#visualizer_id_form').submit(change_visualizer);

        $('#player_maximized .toggle, #player_minimized .toggle').click(function() {
            togglePlayerMaximization();
            this.blur();
            return false;
        });

        load_sound();
    });    

    //old code valid for old version:
    //    soundManager.onload = function() {
    //        soundEngineReady = true;
    //        load_sound();
    //    }
    //replaced by:
    soundManager.onready(function() {
        // SM2 is ready to go!
        //alert('okkkk');
        soundEngineReady = true;
        load_sound(); // soundManager.createSound(), etc.
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



