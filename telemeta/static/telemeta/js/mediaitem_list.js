/**
 * Created by crem on 19/05/16.
 */
$(function () {
    $("#results-per-page").selectmenu({
        icons: {button: "ui-icon-carat-2-n-s"},
        change: function () {
            location.search = '?page=1&results_page=' + $(this).val();
        }
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

});