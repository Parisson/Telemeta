/**
 * Created by crem on 19/05/16.
 */
$(function () {
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
