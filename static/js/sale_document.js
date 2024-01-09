let productForm = document.querySelectorAll(".product-form");
let container = document.querySelector("#sold-products tbody");
let addButton = document.querySelector("#add-row");
let totalForms = document.querySelector("#id_sold_products-TOTAL_FORMS");

let formNum = productForm.length;

addButton.addEventListener('click', addForm);

function addForm(e) {
    e.preventDefault()

    let newForm = productForm[0].cloneNode(true);
    let formRegex = /sold_products-0-/g;
    let numeratorRegex = /(<td class="numerator">)\d+(<\/td>)/g;


    newForm.innerHTML = newForm.innerHTML.replace(formRegex, `sold_products-${formNum}-`);
    formNum++
    newForm.innerHTML = newForm.innerHTML.replace(numeratorRegex, `<td class="numerator">${formNum}</td>`);
    container.appendChild(newForm)
    totalForms.setAttribute('value', `${formNum}`);
}


// Hide and show different columns depending on weather it's an invoice or not

let invoiceCheckbox = document.getElementById('invoice-checkbox');
let invoiceMainHeading = document.querySelector('label[for="invoice-checkbox"]');
let invoiceData = document.getElementById('invoice-data');
let buyerData = document.getElementById('buyer-data');
let productsTable = document.querySelector('#sold-products table');


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
    tableColumnHide(productsTable, 5, 8);
    invoiceData.removeChild(buyerData);
});

invoiceCheckbox.addEventListener('change', displayHandler);

function displayHandler () {
    if (invoiceCheckbox.checked) {
        invoiceMainHeading.style.fontWeight = 'bold';
        buyerData.style.display = 'flex';
        invoiceData.appendChild(buyerData);
        tableColumnShow(productsTable,5,8)
        tableColumnHide(productsTable,6,9)

    } else {
        invoiceMainHeading.style.fontWeight = 'normal';
        invoiceData.removeChild(buyerData);
        tableColumnShow(productsTable,6,9)
        tableColumnHide(productsTable,5,8)
    }
}











