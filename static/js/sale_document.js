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


// Hide and show different columns depending on weather it's an invoice or not

let invoiceCheckbox = document.getElementById('invoice-checkbox');
let invoiceMainHeading = document.querySelector('label[for="invoice-checkbox"]');
let sellerAndBuyer = document.getElementById('seller-and-buyer');
let productsTable = document.querySelector('#sold-products table');

invoiceCheckbox.addEventListener('change', displayHandler);

function tableColumnHide(table, priceColumnIndex, amountColumnIndex) {
    let rows = table.rows
    for (let i = 0; i < rows.length; i++) {
      let cells = rows[i].cells;
      cells[priceColumnIndex].style.display = 'none';
      cells[amountColumnIndex].style.display = 'none';
    }
}

function tableColumnShow(table, priceColumnIndex, amountColumnIndex) {
    let rows = table.rows
    for (let i = 0; i < rows.length; i++) {
      let cells = rows[i].cells;
      cells[priceColumnIndex].style.display = 'table-cell';
      cells[amountColumnIndex].style.display = 'table-cell';
    }
}

document.addEventListener('DOMContentLoaded', function () {
    tableColumnHide(productsTable, 5, 8)})

function displayHandler () {
    if (invoiceCheckbox.checked) {
        invoiceMainHeading.style.fontWeight = 'bold';
        sellerAndBuyer.style.display = 'flex';
        tableColumnShow(productsTable,5,8)
        tableColumnHide(productsTable,6,9)
    } else {
        invoiceMainHeading.style.fontWeight = 'normal';
        sellerAndBuyer.style.display = 'none';
        tableColumnShow(productsTable,6,9)
        tableColumnHide(productsTable,5,8)
    }
}











