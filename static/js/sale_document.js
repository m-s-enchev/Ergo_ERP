document.addEventListener("DOMContentLoaded", addNewRowOnInput)
function addNewRowOnInput (){
    function addNewForm(formCount) {
        const lastForm = document.querySelector(`[name="sold_products-${formCount - 1}-product_name"]`);
        const newForm= lastForm.closest("form").insertAdjacentHTML('beforeend', lastForm.dataset.emptyForm.replace(new RegExp(`sold_products-${formCount - 1}`, 'g'), `sold_products-${formCount}`));
    }

    document.addEventListener("blur", function(event) {
        const target = event.target;
        if (target.name && target.name.includes("product_name") && target.value) {
            const formCount = parseInt(target.name.split('-')[1]) + 1;
            addNewForm(formCount);
        }
    }, true);  // Use capturing phase to catch the event before it reaches the target
};
