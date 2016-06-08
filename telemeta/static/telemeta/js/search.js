$(function() {

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

            var prev = getPrevUrlParameter("page");
            var curr = getCurrUrlParameter("page");
            if(prev<curr){
                $(".fullpage").show( "slide", {direction:"right"} );
            }
            else if(!curr){
                $(".fullpage").fadeIn(500);
            }
            else if(!prev){
                $(".fullpage").show( "slide", {direction:"right"} );
            }
            else{
                $(".fullpage").show( "slide", {direction:"left"} );
            };

            //alert("prev = "+ prev +" curr = "+ curr);

            var nouvellesIcones = {
                header : 'ui-icon-carat-1-e',
                activeHeader : 'ui-icon-carat-1-s',


            };

            $("#accordeon").accordion({
                collapsible : true,
                icons : nouvellesIcones,
            });
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

                var colSort = [];

    if (sessionStorage['sort'] && sessionStorage['order']) {
        $.tablesorter.defaults.sortList = [[sessionStorage['sort'], sessionStorage['order']]];
    }
    else {
        $.tablesorter.defaults.sortList = [[1, 0]];
    }

    $('#searchtable th').each(function (index) {
        colSort[index] = $(this).text();
    });


    $('#searchtable th').on('click', function () {
        var index = colSort.indexOf($(this).text());
        var order = $.tablesorter.defaults.headerList[index]['order'];
        if (index != sessionStorage['sort']) {
            sessionStorage['order'] = 0;
        }
        else {
            sessionStorage['order'] = (sessionStorage['order'] == 0) ? 1 : 0;
        }
        sessionStorage['sort'] = index;
    });

    $("#searchtable").tablesorter({
        headers: {

            0: {sorter: false},
        }

    });

	});
