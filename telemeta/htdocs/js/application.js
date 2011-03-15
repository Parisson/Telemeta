//adds a move function to the array object.
//moves the element at position from into to position
//returns from if no move was accomplished, ie when either:
//1) from or to are not integers
//2) from==to or from==to-1 (also in this latter case there is no need to move)
//3) from or to are lower than zero or greater than the array length
//in any other case, returns to
Array.prototype.move = function(from, to){
    var pInt = parseInt;
    if(pInt(from)!==from || pInt(to)!==to){
        return from;
    }
    var len = this.length;
    if((from<0 || from>len)||(to<0 || to>len)){
        return from;
    }
    //if we moved left to right, the insertion index is actually
    //newIndex-1, as we must also consider to remove the current index markerIndex, so:
    if(to>from){
        to--;
    }
    if(from != to){
        var elm = this.splice(from,1)[0];
        this.markers.splice(to,0,elm);
        return to;
    }
    return from;
}

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
        var elm = jQuery(this); //does not work with $.. conflicts?
        if(pageOrigin===pageHref){
            if(pageHref == linkHref){
                elm.addClass('active');
            }else{
                elm.removeClass('active');
            }
        }else{
            //here, on the other hand, we select if a link points to a page or super page
            //of the current paqge
            if(linkHref!=pageOrigin && pageHref.match("^"+linkHref+".*")){
                elm.addClass('active');
            }else{
                elm.removeClass('active');
            }
        }
        
    })
}

$(document).ready(function() {
    foldInfoBlocks();
    setSelectedMenu();
});

