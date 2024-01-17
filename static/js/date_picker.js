function initializeDatepicker (){
    $(".datepicker").datepicker({
        dateFormat: "dd.mm.yy"
    });
}

$(document).ready(function() {
    initializeDatepicker();
});