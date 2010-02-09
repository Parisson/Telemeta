
function foldInfoBlocks() {
    var extra = $('.extraInfos');
    extra.find('.folded dl, .folded table').css('display', 'none');
    extra.find('a').click(function() { 
        $(this).parents('.extraInfos').children().toggleClass('folded').find('dl, table').toggle(100); 
        return false; 
    });
}

$(document).ready(function() {
    foldInfoBlocks();
});

