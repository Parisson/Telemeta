var sound = null;
var soundUrl = null;
var soundEngineReady = false;
var map;
var provider;
var player;

function togglePlayerMaximization() {
    var view = $('#player');
    $('#player_maximized, #player_minimized').css('display', 'none');
    var ctr;
    if (view.parents('#player_maximized').length) {
        ctr = $('#player_minimized').append(view);
    } else {
        ctr = $('#player_maximized').append(view);
    }
    ctr.css({opacity: 0, display: 'block'});
    player.resize();
    ctr.animate({opacity: 1}, 100, null);
}

function load_sound() {
    if (!sound && soundUrl && soundEngineReady) {
        sound = soundManager.createSound({
            id: 'sound',
            url: soundUrl
        });
        
        TimeSide.load(function() {
            provider.setSource(sound);
        });
        // sound.load(); // Auto-loading overloads the Django test server
    }
}

function load_player(duration) {
    $(document).ready(function () {
        soundUrl = $('.ts-wave a').attr('href');

        $('.ts-wave a img').insertAfter('.ts-wave a');
        $('.ts-wave a').remove();

        TimeSide.load(function() {
            map = new TimeSide.MarkerMap();
            provider = new TimeSide.SoundProvider({duration: duration});
            player = new TimeSide.Player('#player');
            controller = new TimeSide.Controller({
                player: player,
                soundProvider: provider, 
                map: map
            });
        });

        $('#player_maximized .toggle, #player_minimized .toggle').click(function() {
            togglePlayerMaximization();
            this.blur();
            return false;
        });

        load_sound();
    });    

    soundManager.onload = function() {
        soundEngineReady = true;
        load_sound();
    }

}




