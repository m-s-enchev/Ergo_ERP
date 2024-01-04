let productForm = document.querySelectorAll(".product-form");
let container = document.querySelector("#sold-products tbody");
let addButton = document.querySelector("#add-row");
let totalForms = document.querySelector("#id_sold_products-TOTAL_FORMS");

let formNum = productForm.length-1;

addButton.addEventListener('click', addForm);

function addForm(e) {
    e.preventDefault()

    let newForm = productForm[0].cloneNode(true);
    let formRegex = /sold_products-0-/g;
    let numeratorRegex = /(<td class="numerator">)\d+(<\/td>)/g;


    formNum++
    newForm.innerHTML = newForm.innerHTML.replace(formRegex, `sold_products-${formNum}-`);
    newForm.innerHTML = newForm.innerHTML.replace(numeratorRegex, `<td class="numerator">${formNum+1}</td>`);
    container.appendChild(newForm)

    totalForms.setAttribute('value', `${formNum+1}`);
}



let invoiceCheckbox = document.getElementById('invoice-checkbox');
let invoiceMainHeading = document.querySelector('label[for="invoice-checkbox"]');

invoiceCheckbox.addEventListener('change', displayHandler);

function displayHandler () {
    if (invoiceCheckbox.checked) {
        invoiceMainHeading.style.fontSize = '2vw';
    }
}











