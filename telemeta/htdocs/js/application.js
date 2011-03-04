
function foldInfoBlocks() {
    var extra = $('.extraInfos');
    extra.find('.folded dl, .folded table').css('display', 'none');
    extra.find('a').click(function() { 
        $(this).parents('.extraInfos').children().toggleClass('folded').find('dl, table').toggle(100); 
        return false; 
    });
}


function setSelectedMenu(){
    var menus = $('#menu a');
    //build collections/items from http:/site/collections/items,
    //being http:/site/ = window.location.origin
    
    //function for normalizing paths (removes last n occurrences of the slash)
    var normalize = function(str){
        return str.replace(/\/+$/,"");
    }
    var pageOrigin = normalize(window.location.origin);
    var pageHref = normalize(window.location.href);
    menus.each(function(){
        ///if we are at home, the window location href corresponds to window location origin,
        //so we select only links whose link points EXACTLY to the origin (home link)
        var linkHref = normalize(this.href);
        if(pageOrigin===pageHref){
            if(pageHref == linkHref){
                jQuery(this).addClass('active');
            }else{
                jQuery(this).removeClass('active');
            }
        }else{
            //here, on the other hand, we select if a link points to a page or super page
            //of the current paqge
            if(linkHref!=pageOrigin && pageHref.match("^"+linkHref+".*")){
                jQuery(this).addClass('active');
            }else{
                jQuery(this).removeClass('active');
            }
        }
        
    })
}

$(document).ready(function() {
    foldInfoBlocks();
    setSelectedMenu();
});

