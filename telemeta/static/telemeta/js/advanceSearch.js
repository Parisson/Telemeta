$(document).ready(function() {
            var nouvellesIcones = {
                header : 'ui-icon-carat-1-e',
                activeHeader : 'ui-icon-carat-1-s',


            };

            function getPrevUrlParameter(sParam){
                var sPageURL = document.referrer.substring(1);
                var sURLVariables = sPageURL.split('&');
                for (var i = 0; i < sURLVariables.length; i++)
                {
                    var sParameterName = sURLVariables[i].split('=');
                    if (sParameterName[0] == sParam)
                    {
                        return sParameterName[1];
                    }
                }
            };

            function getCurrUrlParameter(sParam){
                var sPageURL = window.location.search.substring(1);
                var sURLVariables = sPageURL.split('&');
                for (var i = 0; i < sURLVariables.length; i++)
                {
                    var sParameterName = sURLVariables[i].split('=');
                    if (sParameterName[0] == sParam)
                    {
                        return sParameterName[1];
                    }
                }
            };

            function scrollToElement(ele) {
                $(document).scrollTop(ele.offset().top).scrollLeft(ele.offset().left);
            };


            var prev = getPrevUrlParameter("page");
            var curr = getCurrUrlParameter("page");
            var prespage = getPrevUrlParameter("results_page");
            var crespage = getCurrUrlParameter("results_page");
            if(prev<curr){
                $(".fullpage").show( "slide", {direction:"right"} );
                if($("#anchor")){
                    scrollToElement($("#anchor"));
                }

            }
            else if(!curr || (prespage!=crespage)){
                $(".fullpage").fadeIn(500);
                if($("#anchor")){
                    scrollToElement($("#anchor"));
                }
            }
            else if(!prev){
                $(".fullpage").show( "slide", {direction:"right"} );
                if($("#anchor")){
                    scrollToElement($("#anchor"));
                }
            }
            else{
                $(".fullpage").show( "slide", {direction:"left"} );
                if($("#anchor")){
                    scrollToElement($("#anchor"));
                }
            };

            $("#id_media_type").buttonset();
            $("#id_viewable").buttonset();
            $("#id_item_status").buttonset();
            $("#id_ethnic_group").selectmenu({
                icons : {button: "ui-icon-carat-2-n-s"}
            }).selectmenu("menuWidget").addClass("overflow");
            $("#id_year_published_from").selectmenu({
                icons : {button: "ui-icon-carat-2-n-s"}
            }).selectmenu("menuWidget").addClass("overflow");
            $("#id_year_published_to").selectmenu({
                icons : {button: "ui-icon-carat-2-n-s"}
            }).selectmenu("menuWidget").addClass("overflow");
            $("#id_recorded_from_date").selectmenu({
                icons : {button: "ui-icon-carat-2-n-s"}
            }).selectmenu("menuWidget").addClass("overflow");
            $("#id_recorded_to_date").selectmenu({
                icons : {button: "ui-icon-carat-2-n-s"}
            }).selectmenu("menuWidget").addClass("overflow");
            $("#id_recording_context").selectmenu({
                icons : {button: "ui-icon-carat-2-n-s"}
            }).selectmenu("menuWidget").addClass("overflow");
            $("#id_physical_format").selectmenu({
                icons : {button: "ui-icon-carat-2-n-s"}
            }).selectmenu("menuWidget").addClass("overflow");
            $("#selectAll").click(function(){
                if(this.checked){
                    $(".check1").each(function(){
                        this.checked=true;
                    });
                }
                else{
                    $(".check1").each(function(){
                        this.checked=false;
                    });
                }
            });
	});
