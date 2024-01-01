let productForm = document.querySelectorAll(".product-form");
let container = document.querySelector("#sold-products");
let addButton = document.querySelector("#add-row");
let totalForms = document.querySelector("#id_sold_products-TOTAL_FORMS");

let formNum = productForm.length-1;

addButton.addEventListener('click', addForm);

function addForm(e) {
    e.preventDefault()

    let newForm = productForm[0].cloneNode(true);
    let formRegex = /sold_products-0-/g;

    formNum++
    newForm.innerHTML = newForm.innerHTML.replace(formRegex, `sold_products-${formNum}-`);
    container.insertBefore(newForm, addButton);

    totalForms.setAttribute('value', `${formNum+1}`);
}















