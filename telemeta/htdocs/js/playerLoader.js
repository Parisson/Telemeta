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
    var p = Timeside.player;
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



function loadPlayer(analizerUrl, soundUrl, soundImgSize, itemId, visualizers, currentUserName, isStaffOrSuperuser){
    var $J = jQuery;
    var wdw = window;


    //end(''): clears loading span, if any
    //end('msg') if loading span is there, clear loading span. If loading span is there, display alert msg

    function end(optionalErrorMsg){
        //var $J = jQuery;
        $J(wdw).ready(function(){
            var elm = $J('#loading_span');
            if(elm.length<1){
                return;
            }
            elm.empty().remove();
            if(optionalErrorMsg){
                $J('#rightcol').hide();
                alert(optionalErrorMsg);
            }
        });
    }

    //we load the player once the window is fully loaded. Note that the function Timeside.load (called within this method)
    //is started on $J(wdw), so it will be executed immediately. The reason of a 'double' $K(wdw)
    //is that we want to display some messages on html spans (which therefore must exist) and that if the
    //div#player does not exist the Timeside.load throws an error that the
    //function end (see above) will convert in an alert dialog. The problem is that the non existence of div#player
    //is not always an error, (eg, the user not logged in and the item has only metadata public).
    //Ideally, we should not enter here in some cases. For the moment we just catch the case div#player doesnt exist and
    //we return
    
//    var maxTime = 10000;
//    //if the loading span is still visible in 10 seconds, throw an error:
//    setTimeout(function(){
//        end('SoundManager is not responding. Try to:\n - Reload the page\n - Empty the cache (see browser preferences) and reload the page\n - Restart the browser');
//    },maxTime);
     
    
    var pFloat = parseFloat;
    //load analyser xml and proceed on success:
    $J.ajax({
        url: analizerUrl, 
        dataType: 'xml',
        error:function(){
            end('Error loading analyzer');
        },
        success: function(data){
            //populatetable
            var analyzerContentArray = []; //content is an array which we will transform in table innerHTML via the method join
            //which is faster in some browsers than string concatenation
            $J.each($J(data).find('data'),function(index,element){
                var elm = $J(element);
                analyzerContentArray.push('<tr><td>');
                analyzerContentArray.push(elm.attr('name'));
                analyzerContentArray.push('</td><td>');
                analyzerContentArray.push(elm.attr('value'));
                analyzerContentArray.push('</td><td>');
                analyzerContentArray.push(elm.attr('unit'));
                analyzerContentArray.push('</td></tr>');
            });
               
            var duration = $J(data).find('#duration').attr('value');
            duration = duration.split(":");
            //format duration
            var pin = parseInt;
                
            var radix = 10; //REALLY IMPORTANT. IF ANY ELEMENT OF DURATION STARTS WITH '0', THEN THE RADIX IS CONSIDERED EITHER OCTAL OR HEXADECIMAL
            //WE WANT TO PREVENT NON 10-BASED RADIX PARSING
            var timeInMSecs=pin(duration[0],radix)*3600+pin(duration[1],radix)*60+pFloat(duration[2],radix);
            timeInMSecs = Math.round(timeInMSecs*1000);
            //callback to be executed after json gets the markers (see last line below)
            var callbackAfterMarkersLoading = function(data) {
                var markerMap = [];
            
                if(data && data.result && data.result.length>0){
                    var result = data.result;
                
                    //add markers to the map. No listeners associated to it (for the moment)
                    //var mapAdd = map.add;
                    for(var i =0; i< result.length; i++){

                        var argument = result[i];
                        var marker = {
                            id: argument.public_id,
                            offset: pFloat(argument.time), //IMPORTANT: IT IS A STRING!!!!!!
                            desc: argument.description,
                            title: argument.title,
                            author: argument.author,
                            isEditable: false,
                            canBeSetEditable: isStaffOrSuperuser || (argument.author === currentUserName) ,
                            canBeAddedToPlaylist: currentUserName ? true : false,
                            isSavedOnServer: true
                        };
                        markerMap.push(marker);
                    }
                }

                //defining the marker callback:
                
                var markerMode = currentUserName || false;
                if(markerMode){
                    //markerMode becomes a function:
                    markerMode = function(offset){
                        var m = {
                            //id: uinqid_(), //will be set in markermap
                            offset: pFloat(offset),
                            desc: "",
                            title: "",
                            author: currentUserName,
                            isEditable: false,
                            canBeSetEditable: true,
                            canBeAddedToPlaylist: true,
                            isSavedOnServer: false
                        };
                        return m;
                    };
                }
               

                //creating the visualizer <select/> tag
                
//                var playerDiv = '#player';
//                if(!($J(playerDiv).length)){
//                    end(); //stop without raising error messages. If passed within Timeside.load, an error will be thrown
//                }

                var timesideConfig = {
                    container: '#player',
                    sound : soundUrl,
                    soundDuration: timeInMSecs,
                    onError: end, //globally defined (see above)
                    markersArray: markerMap,
                    newMarker: markerMode
                };
                timesideConfig.soundImage = function(width,height){
                    var player_image_url = visualizers[""+visualizersSelectElement.val()];
                    var _src_ = null;
                    if (player_image_url && (width || height)) {
                        _src_ = player_image_url.replace('WIDTH', width + '').replace('HEIGHT', height + '');
                    }
                    return _src_;
                };
                if(typeof soundImgSize === 'object' && (soundImgSize.hasOwnProperty('width') || soundImgSize.hasOwnProperty('height'))){
                    timesideConfig.imageSize = soundImgSize;
                }
                //onReadyWithImage: set select visualizers:
                 //create visualizer select element (append it later, document here could NOT be ready)
                var visualizersSelectElement = $J('<select/>');
                for(var name in visualizers){
                    $J('<option/>').html(name).appendTo(visualizersSelectElement);
                }
               timesideConfig.onReadyWithImage = function(player){
                   //setting up the select tag

                    player.bind('waitShown', function(data){
                        visualizersSelectElement.hide();
                    });
                    player.bind('waitHidden', function(data){
                        visualizersSelectElement.css('display','inline-block');
                    });

                    //assigning event on select:
                    visualizersSelectElement.change(
                        function (){
                            player.refreshImage.apply(player);
                        });
                    var control = player.getContainer().find('.ts-control');
                    var ch = control.height();
                    var margin = 3;
                    visualizersSelectElement.css({
                        'display': 'inline-block',
                        'height':(ch-2*margin)+'px',
                        'position':'absolute',
                        'top':margin+'px',
                        'right':margin,
                        'margin':0
                    });
                    control.append(visualizersSelectElement);
               };
                timesideConfig.onReady = function(player){
                    //document here is READY
                    var markersUI = "#markers_div_id";
                    var mapUI = new Timeside.classes.MarkerMapDiv(markersUI);
                    player.getMarkerMap().each(function(i,marker){
                        mapUI.add(marker,i,false);
                    });
                    Timeside.markerMapDiv = mapUI;
                    //bind add marker -> markerdiv add:
                    player.bind('markerAdded', function(data){
                        //select the marker tab:
                        var tab = $J('#tab_markers');
                        if(tab && tab.length){
                            tab.trigger('click');
                        }
                        mapUI.add.apply(mapUI,[data.marker, data.index, true]);
                    });
                    //bind move marker -> markerdiv move:
                    player.bind('markerMoved', function(data){
                        mapUI.move.apply(mapUI,[data.fromIndex,data.toIndex,data.marker.offset]);
                    });
                    //bind move marker -> markerdiv move:
                    player.bind('markerRemoved', function(data){
                        mapUI.remove.apply(mapUI,[data.index]);
                    });

                    //bind remove marker -> player remove -> remove marker
                    //(wait for json success)
                    mapUI.bind('remove',function(data){
                        var marker = data.marker;
                            
                        var functionOnSuccess = function(){
                            player.removeMarker.apply(player,[data.marker]);//map.remove + fires markerMoved on player
                        };
                        if(marker.isSavedOnServer){
                            //json(param,method,onSuccessFcn,onErrorFcn){
                            json([marker.id], "telemeta.del_marker",functionOnSuccess);
                        }else{
                            functionOnSuccess();
                        }

                    });

                    mapUI.bind('edit',function(data){
                        var map = player.getMarkerMap();
                        var len = map.length;
                        var idx = data.index;
                        if(map && idx>=0 && idx<len){
                            map.setEditable(idx,data.value);
//                            map.toArray()[idx].isEditable = data.value;
//                            player.getRuler().setEditable(idx,data.value, false);
                        }
                    }); 

                    //bind save marker -> player save
                    var map = player.getMarkerMap();
                    if(map){
                        mapUI.bind('save',function(data){
                            var marker = data.marker;
                            var idx = map.insertionIndex(marker);
                            if(idx<0 || idx>=map.length){
                                this.debug('mapUI.save: marker not found');
                                return;
                            }

                            //var itemid = this.getItemId(); //TODO2: NOt anymore used
                            var isSavedOnServer = marker.isSavedOnServer;
                            var method = isSavedOnServer ? "telemeta.update_marker" : "telemeta.add_marker";
                            var param = {
                                'item_id':itemId,
                                'public_id': marker.id,
                                'time':marker.offset,
                                'author': marker.author,
                                'title':marker.title,
                                'description':marker.desc
                            };

                            //function on success:
                            //go back to the marker div to notify tha tis saved
                            var success = function(){
                                if(!isSavedOnServer){
                                    marker.isSavedOnServer = true;
                                }
                                mapUI.setEditMode.apply(mapUI,[idx,false]);
                            };
                            //json(param,method,onSuccessFcn,onErrorFcn){
                            json([param], method, success);
                        });
                    }
                    //bind focus marker - > player focus
                    mapUI.bind('focus', function(data){
                        if(data && 'index' in data){
                            if(data.index>=0 && data.index<map.length){
                                var offset = map.toArray()[data.index].offset;
                                player.setSoundPosition(offset);
                            }
                        }
                    });
                    //last things:
                    //populate the analyzers table
                    $J('#analyzer_div_id').find('table').find('tbody:last').append(analyzerContentArray.join(""));

                    
                    //Eventually, do 3 last things:
                    //1) call end (without arguments simply clears the wait span and avoid subsequent calls to end(msg) to
                    //display error messages)
                    end();
                    //set a warning leaving the page with unsaved markers:
                    if(map){
                        var confirmExit = function(){
                            var markerUnsaved=0;
                            map.each(function(i,marker){
                                if(!marker.isSavedOnServer || marker.isEditable){
                                    markerUnsaved++;
                                }
                            });
                            if(markerUnsaved>0){
                                return gettrans('there are unsaved or modified markers') +' ('+ markerUnsaved+ '). '+
                                gettrans('If you exit the page you will loose your changes');
                            }

                        };
                        wdw.onbeforeunload = confirmExit;
                    }

                   
                    if(map && wdw.PopupDiv){
                        var POPUP_TIMEOUT=3; //in seconds. Zero means: no popup, negative numbers:
                        //popup stays infinitely on the player (until next marker cross)
                        //a number N means: popup stays maximum N seconds on the screen
                        if(POPUP_TIMEOUT){
                            var popupdiv = new PopupDiv({
                                //focusable: false,
                                titleClass: 'markersdivTitle',
                                //showClose:true,

                                //boundsExact:true,
                                bounds: {
                                    top:0.4,
                                    left:0.1,
                                    right:0.1,
                                    bottom:0
                                },
                                invoker: player.getContainer().find('.ts-wave'),
                                defaultCloseOperation: 'hide'
                            });
                            var popupShowFunction = function(data){
                                popupdiv.refresh(data.marker.desc,data.marker.title);
                                if(!popupdiv.isShowing()){
                                    popupdiv.show();
                                }
                            };
                            if(POPUP_TIMEOUT<0){
                                player.bind('markerCrossed',popupShowFunction);
                            }else{
                                var popupTimeoutId = undefined;
                                var clearHidePopupTimeout = clearTimeout;
                                player.bind('markerCrossed',function(data){
                                    if(popupTimeoutId !== undefined){
                                        clearHidePopupTimeout(popupTimeoutId);
                                    }
                                      popupTimeoutId=undefined;
                                    popupShowFunction(data);
                                    if(POPUP_TIMEOUT<0){
                                        return;
                                    }
                                    var next = data.nextMarkerTimeInterval ? data.nextMarkerTimeInterval[0] :undefined;
                                    if(next === undefined || next-data.currentSoundPosition > POPUP_TIMEOUT){
                                        popupTimeoutId = popupdiv.setTimeout('close',POPUP_TIMEOUT*1000);
                                    }
                            
                                });
                                

                            }
                            var draggingSomeMarker = false;
                            //now bind mouse events
                            player.bind('markerMouseEvent', function(data){
                                if(data.eventName === 'click' && data.index>-1){
                                    player.setSoundPosition(data.marker.offset);
                                    draggingSomeMarker = false; //to be sure
                                    return;
                                }
                                if(data.eventName === 'mouseenter'){
                                    if(!draggingSomeMarker && data.index>=0 && player.playState===0){
                                        popupShowFunction(data);
                                        return;
                                    }
                                }else if(data.eventName === 'dragstart'){
                                    draggingSomeMarker = true;
                                }else if(data.eventName === 'dragend'){
                                    draggingSomeMarker = false;
                                }
                                if(popupdiv.isShowing()){
                                    popupdiv.close();
                                }
                            });
                        }
                    }

                    //set up the marker tab
                    var tabIndex = map.length ? 1 : 0;
                    setUpPlayerTabs($J('#tab_analysis').add($J('#tab_markers')),
                        [$J('#analyzer_div_id'), $J('#markers_div_id')], tabIndex,
                        'tab_selected','tab_unselected');
                    //2)  and selects the current marker if it is present on the url
                    var url = wdw.location.href+"";
                    var lastPart = url.replace(/\/+$/,"").replace(/^.*\/([^\/]*)$/,"$1");
                    var selOffs = -1;
                    map.each(function(i,marker){
                        if(marker.id == lastPart){
                            selOffs = marker.offset;
                        }
                    });
                    if(selOffs >= 0){
                        player.setSoundPosition(selOffs);
                    }
                    //3) assing a binding to the player maximization button:
                    $J('#player_maximized .toggle, #player_minimized .toggle').click(function() {
                        togglePlayerMaximization();
                        return false;
                    });
                    //and assing the function to the form_link element
                    $J('#player_maximized .embed_player_frame, #player_minimized .embed_player_frame').click(function() {
                        var player_url = urlNormalized(); //defined in application.js
                        var size= player.getImageSize();
                        player_url += "/player/"+size.width+"x"+size.height;
                        var iframeSpanW = 15;
                        var iframeSpanH = 85;
                        var input_text = "<iframe width='"+(size.width+iframeSpanW)+"' height='"+(size.height+iframeSpanH)+
                            "' frameborder='0' scrolling='no' marginheight='0' marginwidth='0' src='"+
                            player_url+"'></iframe>";
                        var ipt = $J('<input/>').attr('type','text');
                        ipt.val(input_text);
                        ipt.focus(function(){
                            $J(this).select();
                        });
                        var p = new PopupDiv({
                            invoker: $J(this),
                            title: gettrans('Paste HTML to embed player in website'),
                            content: ipt,
                            defaultCloseOperation:'remove',
                            focusable: 'true',
                            onShow : function(){
                                if(ipt.outerWidth(true)<ipt.parent().width()){
                                    ipt.css('width',(ipt.parent().width()-(ipt.outerWidth(true)-ipt.width()))+'px');
                                }
                            }
                        });
                        p.show();
                        return false;
                    });
                };
                //and finally, load the player:
                Timeside.load(timesideConfig);

            };
                
            //execute all the stuff once the document is ready:
//            var onSuccess = function(data){
//                $J(wdw).ready(function(){
//                    callbackAfterMarkersLoading(data);
//                });
//            }
            //and niow call json method to load markers (load player also onError, no markers will be loaded)
            json([itemId],"telemeta.get_markers", callbackAfterMarkersLoading,callbackAfterMarkersLoading);
        }
    });
   
}


/*
* Sets a "tab look" on some elements of the page. Takes at least 3 arguments, at most 5:
* 1st argument: an array (or a jquery object) of html elements, ususally anchors, representing the tabs
* 2nd argument: an array (or a jquery object) of html elements, ususally divs, representing the containers to be shown/hidden when
*   clicking the tabs. The n-th tab will set the n-th container to visible, hiding the others. So order is important. Note that if tabs
*   or container are jQuery objects, the html elements inside them are sorted according to the document order. That's why tabs and
*   container can be passed also as javascript arrays, so that the binding n-th tab -> n-th container can be decided by the user
*   regardeless on how elements are written on the page, if already present
* 3rd argument: the selected index. If missing it defaults to zero.
* 4th argument: selectedtab class. Applies to the selected tab after click of one tab. If missing, nothing is done
* 5th argument the unselectedtab class. Applies to all tabs not selected after click of one tab. If missing, nothing is done
*
* NOTE: The last 2 arguments are mostly for customizing the tab "visual look", as some css elements (eg, (position, top, zIndex)
* are set inside the code and cannot be changed, as they are mandatory to let tab anchor behave like desktop application tabs. Note also
* that every tab container is set to 'visible' by means of jQuery.show()
*
* Examples:
* setUpPlayerTabs([jQuery('#tab1),jQuery('#tab1)], [jQuery('#div1),jQuery('#div2)], 1);
* sets the elements with id '#tab1' and '#tab2' as tab and assign the click events to them so that clicking tab_1 will show '#div_1'
* (and hide '#div2') and viceversa for '#tab2'. The selected index will be 1 (second tab '#tab2')
*/
function setUpPlayerTabs() {//called from within controller.js once all markers have been loaded.
    //this is because we need all divs to be visible to calculate size. selIndex is optional, it defaults to 0
    
    var $J = jQuery;
    var tabs_ = arguments[0];
    var divs_ = arguments[1]; //they might be ctually any content, div is a shoertand

    //converting arguments to array: tabs
    var tabs=[];
    if(tabs_ instanceof $J){
        tabs_.each(function(i,elm){
            tabs.push(elm);
        });
    }else{
        tabs = tabs_;
    }
    //set the overflow property of the parent tab to visible, otherwise scrollbars are displayed
    //and the trick of setting position:relative+top:1px+zIndices (see css) doesnt work)
    $J(tabs).each(function(i,tab){
        var t = $J(tab).attr('href','#');
        t.show(); //might be hidden
        //set necessary style for the tab appearence:
        var overflow = t.parent().css('overflow');
        if(overflow && overflow != 'visible'){
            t.parent().css('overflow','visible');
        }
    });
    //converting arguments to array: divs
    var divs=[];
    if(divs_ instanceof $J){
        divs_.each(function(i,elm){
            divs.push(elm);
        });
    }else{
        divs = divs_;
    }

    //reading remaing arguments (if any)
    var selIndex = arguments.length>2 ? arguments[2] : 0;
    var selectedTabClass = arguments.length>3 ? arguments[3] : undefined;
    var unselectedTabClass = arguments.length>4 ? arguments[4] : undefined;

    //function to be associate to every click on the tab (see below)
    var tabClicked = function(index) {
        for(var i=0; i<tabs.length; i++){
            var t = $J(tabs[i]);

            var div = $J(divs[i]);
            var addClass = i==index ? selectedTabClass : unselectedTabClass;
            var removeClass = i==index ? unselectedTabClass : selectedTabClass;
            if(removeClass){
                t.removeClass(removeClass);
            }
            if(addClass){
                t.addClass(addClass);
            }

            //relevant css. Will override any css set in stylesheets
            t.css({
                'position':'relative',
                'top':'1px',
                'zIndex': (i==index ? '10' : '0')
            });

            if(i===index){
                div.fadeIn('slow');
            }else{
                div.hide();
            }
        }
    };

    //bind clicks on tabs to the function just created
    for (var i=0;i<tabs.length;i++){
        // introduce a new scope (round brackets)
        //otherwise i is retrieved from the current scope and will be always equal to tabs.length
        //due to this loop
        (function(tabIndex){
            $J(tabs[i]).click(function(){
                tabClicked(tabIndex);
                return false;//returning false avoids scroll of the anchor to the top of the page
            });
        })(i);
    }

    //select the tab
    $(tabs[selIndex]).trigger("click");
}
