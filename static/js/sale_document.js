const priceBeforeTax = 5
const productTotalBeforeTax = 8
const price = 6
const productTotal = 9

document.addEventListener('DOMContentLoaded', function () {
    const productFormManager = new ProductFormManager();
    productFormManager.attachBlurEventToLastField();
    setupInvoiceToggle();
    setupEnterKeyBehavior();
});



class ProductFormManager {
    constructor() {
        this.container = document.querySelector("#sold-products tbody");
        this.totalForms = document.querySelector("#id_sold_products-TOTAL_FORMS");
        this.productForms = document.querySelectorAll(".product-form");
        this.formNum = this.productForms.length;
    }

    addForm() {
            let newForm = this.productForms[0].cloneNode(true);
            let formRegex = new RegExp(`sold_products-${this.formNum - 1}-`, 'g');
            let numeratorRegex = /(<td class="numerator">)\d+(<\/td>)/g;
            newForm.innerHTML = newForm.innerHTML.replace(formRegex, `sold_products-${this.formNum}-`);
            newForm.innerHTML = newForm.innerHTML.replace(numeratorRegex, `<td class="numerator">${this.formNum + 1}</td>`);
            this.container.appendChild(newForm);
            this.totalForms.setAttribute('value', `${this.formNum + 1}`);
            this.formNum++;
            this.attachBlurEventToLastField();
        }

    attachBlurEventToLastField() {
        let lastFirstField = document.getElementById(`id_sold_products-${this.formNum - 1}-product_name`);
        let needsRowAfter = true;
        lastFirstField.addEventListener('focus', function (e) {
            if (e.target.value) {
                needsRowAfter = false;
            }
        });
        lastFirstField.addEventListener('blur', (e) => {
            if (e.target.value && e.target === lastFirstField && needsRowAfter === true) {
                this.addForm();
            }
        });
    }
}


function setupEnterKeyBehavior() {
    const tableContainer = document.querySelector("#sold-products tbody");
    tableContainer.addEventListener('keydown', function (e) {
        if (e.target.tagName === 'INPUT' && e.key === 'Enter') {
            e.preventDefault();
            const currentId = e.target.id;
            const match = currentId.match(/\d+/);
            if (match) {
                const currentRowIndex = parseInt(match[0], 10);
                if (currentId.includes('-product_name')) {
                    const nextInput = document.querySelector(`#id_sold_products-${currentRowIndex}-product_quantity`);
                    if (nextInput) nextInput.focus();
                } else {
                    const nextInput = document.querySelector(`#id_sold_products-${currentRowIndex + 1}-product_name`);
                    if (nextInput) nextInput.focus();
                }
            }
        }
    });
}

function setupInvoiceToggle() {
    const invoiceCheckbox = document.getElementById('id_is_linked_to_invoice');
    const invoiceMainHeading = document.querySelector('label[for="id_is_linked_to_invoice"]');
    const invoiceData = document.getElementById('invoice-number-and-dates');
    const buyerData = document.getElementById('buyer-data');
    const buyerDataToggleFields = document.getElementById('buyer-data-toggle-fields');
    const invoiceToggledFields = document.getElementById('invoice-toggled-fields');
    const productsTable = document.querySelector('#sold-products table');

    const tableColumnHide = (table, ...columnIndices) => {
        let rows = table.rows;
        for (let i = 0; i < rows.length; i++) {
            let cells = rows[i].cells;
            columnIndices.forEach(index => cells[index].style.display = 'none');
        }
    };

    const tableColumnShow = (table, ...columnIndices) => {
        let rows = table.rows;
        for (let i = 0; i < rows.length; i++) {
            let cells = rows[i].cells;
            columnIndices.forEach(index => cells[index].style.display = 'table-cell');
        }
    };

    tableColumnHide(productsTable, priceBeforeTax, productTotalBeforeTax);
    invoiceData.removeChild(invoiceToggledFields);
    buyerData.removeChild(buyerDataToggleFields);

    invoiceCheckbox.addEventListener('change', function () {
        if (invoiceCheckbox.checked) {
            invoiceMainHeading.style.fontWeight = 'bold';
            invoiceData.appendChild(invoiceToggledFields);
            buyerData.appendChild(buyerDataToggleFields);
            tableColumnShow(productsTable, priceBeforeTax, productTotalBeforeTax);
            tableColumnHide(productsTable, price, productTotal);
        } else {
            invoiceMainHeading.style.fontWeight = 'normal';
            invoiceData.removeChild(invoiceToggledFields);
            buyerData.removeChild(buyerDataToggleFields);
            tableColumnShow(productsTable, price, productTotal);
            tableColumnHide(productsTable, priceBeforeTax, productTotalBeforeTax);
        }
    });
}




//
// // Add row (products form) at end of products table
// let productForm = document.querySelectorAll(".product-form");
// let container = document.querySelector("#sold-products tbody");
// let totalForms = document.querySelector("#id_sold_products-TOTAL_FORMS");
// let formNum = productForm.length;
// function addForm() {
//     let newForm = productForm[0].cloneNode(true);
//     let formRegex = /sold_products-0-/g;
//     let numeratorRegex = /(<td class="numerator">)\d+(<\/td>)/g;
//     newForm.innerHTML = newForm.innerHTML.replace(formRegex, `sold_products-${formNum}-`);
//     formNum++
//     newForm.innerHTML = newForm.innerHTML.replace(numeratorRegex, `<td class="numerator">${formNum}</td>`);
//     container.appendChild(newForm)
//     totalForms.setAttribute('value', `${formNum}`);
//     attachBlurEventToLastField();
// }
//
// function attachBlurEventToLastField() {
//     let lastFirstField = document.getElementById(`id_sold_products-${formNum - 1}-product_name`);
//     let needsRowAfter = true;
//     lastFirstField.addEventListener('focus', function(e) {
//         if (e.target.value) {
//             needsRowAfter = false;
//         }
//     });
//     lastFirstField.addEventListener('blur', function(e) {
//         if (e.target.value && e.target === lastFirstField && needsRowAfter === true) {
//             addForm();
//         }
//     });
// }
//
// attachBlurEventToLastField();
//
//
//
//
// //Enter KEy - behavior - should be linked to add form - this event listener should be attached the every new form
// document.addEventListener('DOMContentLoaded', enterKeyBehavior);
//
// function enterKeyBehavior() {
//     container.addEventListener('keydown', enterKeyHandler);
//     function enterKeyHandler(e) {
//         if (e.key === 'Enter' && e.target.tagName === 'INPUT') {
//             e.preventDefault();
//             if (e.target.id.includes('-product_name')) {
//                 let indexRegex = /\d+/;
//                 let currentRowIndex = parseInt(e.target.id.match(indexRegex),10);
//                 let nextInput= document.getElementById(`id_sold_products-${currentRowIndex}-product_quantity`);
//                 nextInput.focus();
//             } else {
//                 let nextInput = document.getElementById(`id_sold_products-${formNum - 1}-product_name`);
//                 if (nextInput) {
//                     nextInput.focus();
//                 }
//             }
//         }
//     }
//
// }
//
//
//
//
//
//
// // Toggle columns and fields depending on whether an invoice is needed
// let invoiceCheckbox = document.getElementById('id_is_linked_to_invoice');
// let invoiceMainHeading = document.querySelector('label[for="id_is_linked_to_invoice"]');
// let invoiceData = document.getElementById('invoice-number-and-dates');
// let buyerData = document.getElementById('buyer-data');
// let buyerDataToggleFields = document.getElementById('buyer-data-toggle-fields');
// let invoiceToggledFields = document.getElementById('invoice-toggled-fields');
// let productsTable = document.querySelector('#sold-products table');
//
// function tableColumnHide(table, priceColumnIndex, amountColumnIndex) {
//     let rows = table.rows
//     for (let i = 0; i < rows.length; i++) {
//       let cells = rows[i].cells;
//       cells[priceColumnIndex].style.display = 'none';
//       cells[amountColumnIndex].style.display = 'none';
//     }
// }
//
// function tableColumnShow(table, priceColumnIndex, amountColumnIndex) {
//     let rows = table.rows
//     for (let i = 0; i < rows.length; i++) {
//       let cells = rows[i].cells;
//       cells[priceColumnIndex].style.display = 'table-cell';
//       cells[amountColumnIndex].style.display = 'table-cell';
//     }
// }
//
// document.addEventListener('DOMContentLoaded', function () {
//     tableColumnHide(productsTable, 5, 8);
//     invoiceData.removeChild(invoiceToggledFields);
//     buyerData.removeChild(buyerDataToggleFields);
// });
//
// invoiceCheckbox.addEventListener('change', displayHandler);
//
// function displayHandler () {
//     if (invoiceCheckbox.checked) {
//         invoiceMainHeading.style.fontWeight = 'bold';
//         invoiceData.appendChild(invoiceToggledFields);
//         initializeDatepicker()
//         buyerData.appendChild(buyerDataToggleFields);
//         initializeDatepicker()
//         tableColumnShow(productsTable,5,8)
//         tableColumnHide(productsTable,6,9)
//     } else {
//         invoiceMainHeading.style.fontWeight = 'normal';
//         invoiceData.removeChild(invoiceToggledFields);
//         buyerData.removeChild(buyerDataToggleFields);
//         tableColumnShow(productsTable,6,9)
//         tableColumnHide(productsTable,5,8)
//     }
// }
















