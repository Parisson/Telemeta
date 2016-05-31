$(document).ready(function () {
    var nouvellesIcones = {
        header: 'ui-icon-carat-1-e',
        activeHeader: 'ui-icon-carat-1-s',


    };

    function getPrevUrlParameter(sParam) {
        var sPageURL = document.referrer.substring(1);
        var sURLVariables = sPageURL.split('&');
        for (var i = 0; i < sURLVariables.length; i++) {
            var sParameterName = sURLVariables[i].split('=');
            if (sParameterName[0] == sParam) {
                return sParameterName[1];
            }
        }
    };

    function getCurrUrlParameter(sParam) {
        var sPageURL = window.location.search.substring(1);
        var sURLVariables = sPageURL.split('&');
        for (var i = 0; i < sURLVariables.length; i++) {
            var sParameterName = sURLVariables[i].split('=');
            if (sParameterName[0] == sParam) {
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
    if (prev < curr) {
        $(".fullpage").show("slide", {direction: "right"});
        if ($("#anchor")) {
            scrollToElement($("#anchor"));
        }

    }
    else if (!curr || (prespage != crespage)) {
        $(".fullpage").fadeIn(500);
        if ($("#anchor")) {
            scrollToElement($("#anchor"));
        }
    }
    else if (!prev) {
        $(".fullpage").show("slide", {direction: "right"});
        if ($("#anchor")) {
            scrollToElement($("#anchor"));
        }
    }
    else {
        $(".fullpage").show("slide", {direction: "left"});
        if ($("#anchor")) {
            scrollToElement($("#anchor"));
        }
    }
    ;

    $("#id_media_type").buttonset();
    $("#id_viewable").buttonset();
    $("#id_item_status").buttonset();
    $("#id_ethnic_group").selectmenu({
        icons: {button: "ui-icon-carat-2-n-s"}
    }).selectmenu("menuWidget").addClass("overflow");
    $("#id_year_published_from").selectmenu({
        icons: {button: "ui-icon-carat-2-n-s"}
    }).selectmenu("menuWidget").addClass("overflow");
    $("#id_year_published_to").selectmenu({
        icons: {button: "ui-icon-carat-2-n-s"}
    }).selectmenu("menuWidget").addClass("overflow");
    $("#id_recorded_from_date").selectmenu({
        icons: {button: "ui-icon-carat-2-n-s"}
    }).selectmenu("menuWidget").addClass("overflow");
    $("#id_recorded_to_date").selectmenu({
        icons: {button: "ui-icon-carat-2-n-s"}
    }).selectmenu("menuWidget").addClass("overflow");
    $("#id_recording_context").selectmenu({
        icons: {button: "ui-icon-carat-2-n-s"}
    }).selectmenu("menuWidget").addClass("overflow");
    $("#id_physical_format").selectmenu({
        icons: {button: "ui-icon-carat-2-n-s"}
    }).selectmenu("menuWidget").addClass("overflow");
    $("#selectAll").click(function () {
        if (this.checked) {
            $(".check1").each(function () {
                this.checked = true;
            });
        }
        else {
            $(".check1").each(function () {
                this.checked = false;
            });
        }
    });

    function activate_autocomplete(selector, attribute) {

        selector.each(function () {
            var self = this;
            $(this).autocomplete({
                minLength: 3,
                source: function (request, response) {
                    $.ajax({
                        url: '/search/autocomplete/',
                        dataType: 'json',
                        data: {
                            q: $(self).val(),
                            attr: ((attribute) ? attribute : $(self).attr('name'))
                        },
                        success: function (data) {
                            response(data.results);
                        }
                    });
                }
            });
        });

    }

    activate_autocomplete($('#id_code, #id_instruments, #id_collectors, #id_location'));

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


    $('#dialog').dialog({
        autoOpen: false,
        width: '40%',
        height: 600,
    });

    $('.fieldWrapper a').click(function () {
        $('#dialog').dialog("open");
    });

    var deleteButton = '<a class="btn btn-default" id="del" href="#">' + gettrans('delete field') + '</a><br/>';

    var tag = $('#copy').clone();
    $(tag).children().each(function () {
        $(this).val('').prop('checked', false).prop('selected', false);
    });

    function deleteField(e) {
        e.preventDefault();
        var number = $('input[name*="text_field"]').length;
        if (number == 3) {
            $('#del').remove();
        }
        $('#bloc-' + (number - 1)).remove();
        $('#id_form-TOTAL_FORMS').attr('value', number - 1);

    }

    function addField(e) {
        e.preventDefault();
        var number = $('input[name*="text_field"]').length;
        var tag_field = $(tag).clone().attr('id', 'bloc-' + number);
        if (number == 2) {
            $('#add').after(deleteButton);
            $('#del').click(deleteField);
        }
        $('#add').before(tag_field);
        $('#bloc-' + number).html($('#bloc-' + number).html().replace(/1/g, number));
        activate_autocomplete($('#id_form-' + number + '-text_field'), 'instruments');
        $('#id_form-TOTAL_FORMS').attr('value', number + 1);
    }

    $('#add').click(addField);

    activate_autocomplete($('#id_form-0-text_field, #id_form-1-text_field'), 'instruments');

    var interval = null;
    var textInput = "";

    $('#dialog form').on('submit change', function (e) {
        if (e.type != 'keypress') e.preventDefault();
        $.ajax({
            url: '/search/booleaninstru/',
            dataType: 'json',
            data: $(this).serialize(),
            success: function (donnees) {
                if (e.type == 'submit' && !donnees.result.match(/\[ERROR\]/g)) {
                    $("#dialog").dialog("close");
                    $('#id_instruments').val(donnees.result);
                }
                $('#res').html(gettrans('final query') + " :<br/><strong>" + gettrans(donnees.result) + '</strong>');
            },
        });
    });

    $('#dialog input[type="text"]').on('focus', function () {
        textInput = $(this).val();
        var self = this;
        interval = setInterval(function () {
            if ($(self).val() != textInput) {
                textInput = $(self).val();
                $('#dialog form').trigger('change');
            }
        }, 500);
    });

    $('#dialog input[type="text"]').on('blur', function () {
        clearInterval(interval);
        textInput = ""
    });


});
