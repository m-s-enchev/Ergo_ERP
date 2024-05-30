function initializeDatepicker (){
    $(".datepicker").datepicker({
        dateFormat: "dd.mm.yy"
    });
}

function clearDateInput() {
    const dateInputFieldInForm = document.getElementById('date');
    const resetButton = document.getElementById('reset-button');
    resetButton.addEventListener('click',()=>{
        dateInputFieldInForm.removeAttribute("value");
    });
}

$(document).ready(function() {
    initializeDatepicker();
    // clearDateInput()
});

