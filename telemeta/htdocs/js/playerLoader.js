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

//var player; //global player variable

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



function loadPlayer(analizerUrl, soundUrl, itemId, visualizers, currentUserName, isStaffOrSuperuser){
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


    //grab the case of soundManager init errors:
    soundManager.onerror = function() {
        end('SoundManager error. If your browser does not support HTML5, Flash player (version '+soundManager.flashVersion+'+) must be installed.\nIf flash is installed, try to:\n - Reload the page\n - Empty the cache (see browser preferences/options/tools) and reload the page\n - Restart the browser');
    };



    //we load the player once the window is fully loaded. Note that the function Timeside.load (called within this method)
    //is started on $J(wdw), so it will be executed immediately. The reason of a 'double' $K(wdw)
    //is that we want to display some messages on html spans (which therefore must exist) and that if the
    //div#player does not exist the Timeside.load throws an error that the
    //function end (see above) will convert in an alert dialog. The problem is that the non existence of div#player
    //is not always an error, (eg, the user not logged in and the item has only metadata public).
    //Ideally, we should not enter here in some cases. For the moment we just catch the case div#player doesnt exist and
    //we return
    
    var maxTime = 10000;
    //if the loading span is still visible in 10 seconds, throw an error:
    setTimeout(function(){
        end('SoundManager is not responding. Try to:\n - Reload the page\n - Empty the cache (see browser preferences) and reload the page\n - Restart the browser');
    },maxTime);
    
    //    var playerDiv = $J('#player');
    //    var markersUI = $J("#markers_div_id");

    
        
    
    //var msgElm = $J('#loading_span_text').html('Loading sound info...');
    //var uinqid_ = Timeside.utils.uniqid; //defined in application.js
    var pFloat = parseFloat;
    //load analyser xml and proceed on success:
    $J.ajax({
        url: analizerUrl, //'analyze/xml',
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
                
                


            //loaded analizer, loading player
            //msgElm.html('Loading markers...');
                
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
                            isEditable: argument.author === currentUserName || isStaffOrSuperuser,
                            canBeAddedToPlaylist: currentUserName ? true : false,
                            isSavedOnServer: true
                        };
                        markerMap.push(marker);
                    //mapAdd.apply(map,[result[i]]);
                    }
                //add markers to ruler and div
                //                map.each(function(i,marker){
                //                    rulerAdd.apply(ruler,[marker, i]);
                //                    mapuiAdd.apply(mapUI,[marker, i]);
                //                });

                //tabIndex = result.length>0 ? 1 : 0;
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
                            isEditable: true,
                            canBeAddedToPlaylist: true,
                            isSavedOnServer: false
                        };
                        return m;
                    };
                }
                //create visualizer select element (append it later, document here could NOT be ready)
                var visualizersSelectElement = $J('<select/>');
                for(var name in visualizers){
                    $J('<option/>').html(name).appendTo(visualizersSelectElement);
                }

                //creating the visualizer <select/> tag
                var imageSrcFcn = function(width,height){
                    var player_image_url = visualizers[""+visualizersSelectElement.val()];
                    var _src_ = null;
                    if (player_image_url && (width || height)) {
                        _src_ = player_image_url.replace('WIDTH', width + '').replace('HEIGHT', height + '');
                    }
                    return _src_;
                };

                var playerDiv = '#player';
                if(!($J(playerDiv).length)){
                    end(); //stop without raising error messages. If passed within Timeside.load, an error will be thrown
                }

                //function(container, soundUrl, durationInMsec, visualizers, markerMap, showAddMarkerButton, onError,onReady ){
                Timeside.load(playerDiv,soundUrl,timeInMSecs,imageSrcFcn,markerMap,markerMode, function(msg){
                    end(msg);
                },
                function(player){
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
                    //bind save marker -> player save
                    var map = player.getMarkerMap();
                    if(map){
                        mapUI.bind('save',function(data){
                            var marker = data.marker;
                            var idx = map.insertionIndex(marker);
                            if(idx<0 || idx>=map.length){
                                this.debug('marker not found');
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

                    //setting up the select tag
                    //assigning event on select:
                    visualizersSelectElement.change(
                        function (){
                            player.refreshImage.apply(player);
                        });
                    var control = player.getContainer().find('.ts-control');
                    var ch = control.height();
                    var margin = 3;
                    visualizersSelectElement.css({
                        'display':'inline-block',
                        'height':(ch-2*margin)+'px',
                        'position':'absolute',
                        'top':margin+'px',
                        'right':margin,
                        'margin':0
                    });
                    player.bind('waiting', function(data){
                        if(data.value){ //is waiting
                            visualizersSelectElement.hide();
                            return;
                        }
                        visualizersSelectElement.css('display','inline-block');
                    });
                    control.append(visualizersSelectElement);
                    //Eventually, do 3 last things:
                    //1) call end (without arguments simply clears the wait span and avoid subsequent calls to end(msg) to
                    //display error messages)
                    end();
                    //set a warning leaving the page with unsaved markers:
                    if(map){
                        var confirmExit = function(){
                            var markerUnsaved=0;
                            map.each(function(i,marker){
                                if(!marker.isSavedOnServer){
                                    markerUnsaved++;
                                }
                            });
                            if(markerUnsaved>0){
                                return gettrans('there is at least one unsaved marker') +' ('+ markerUnsaved+ '). '+
                                gettrans('If you exit the page you will loose your changes');
                            }

                        };
                        wdw.onbeforeunload = confirmExit;
                    }
                    if(map && wdw.PopupDiv){
                        var popupdiv = new PopupDiv({
                            focusable: false,
                            titleClass: 'markersdivTitle',
                            showClose:false,
                            bounds: {
                                top:0.4,
                                left:0.1,
                                right:0.1,
                                bottom:0
                            },
                            invoker: player.getContainer().find('.ts-wave'),
                            defaultCloseOperation: 'hide'
                        });
                        var closeTimeout = undefined;
                        var ci = clearTimeout;
                        player.bind('markerCrossed',function(data){
                            if(closeTimeout !== undefined){
                                cl(closeTimeout);
                            }
                            closeTimeout=undefined;
                            popupdiv.refresh(data.marker.desc,data.marker.title);
                            if(!popupdiv.isShowing()){
                                popupdiv.show();
                            }
                            var index = data.index;
                            if(index+1 == map.length || map.toArray()[index+1].offset-data.marker.offset>3){
                                closeTimeout = popupdiv.setTimeout('close',3000);
                            }
                            //consolelog('firing markercrossed');
                            //consolelog(data.marker.title);
                            
                        });
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
                }
                );
            }
                
            //execute all the stuff once the document is ready:
            var onSuccess = function(data){
                $J(wdw).ready(function(){
                    callbackAfterMarkersLoading(data);
                });
            }
            //and niow call json method to load markers (load player also onError, no markers will be loaded)
            json([itemId],"telemeta.get_markers", onSuccess,onSuccess);
        //function(container, soundUrl, durationInMsec, visualizers, markerMap, showAddMarkerButton, onError, onReady){
        //Timeside.load(playerDiv,soundUrl,,timeInMSecs,visualizers,markerMap,)
        //load_player(soundUrl, timeInMSecs, itemId, visualizers, currentUserName);
        }
    });
   
}

