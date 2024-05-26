let productNamesDict= {};






// /** Handles the adding of a new products row in table, which is a SoldProductsForm instance.
//  * If the product_name field of the last row is filled and focus is shifted to another field,
//  * a new row is added for the next product */
// class AddProductFormManager {
//     constructor() {
//         this.container = document.querySelector("#sold-products tbody");
//         this.totalForms = document.querySelector("#id_sold_products-TOTAL_FORMS");
//         this.productForms = document.querySelectorAll(".product-form");
//         this.formNum = this.productForms.length;
//         this.soldProductsTable = document.getElementById('sold-products');
//         this.updateTotalSum();
//     }
//
//     addRow() {
//         let newForm = this.productForms[0].cloneNode(true);
//         let formRegex = /sold_products-0-/g;
//         let numeratorRegex = /(<td class="numerator">)\d+(<\/td>)/g;
//         newForm.innerHTML = newForm.innerHTML.replace(formRegex, `sold_products-${this.formNum}-`);
//         newForm.innerHTML = newForm.innerHTML.replace(numeratorRegex, `<td class="numerator">${this.formNum + 1}</td>`);
//         // Remove error messages from copied form
//         let ulElements = newForm.querySelectorAll('ul');
//         ulElements.forEach(function(ul) {
//             ul.parentNode.removeChild(ul);
//         });
//         // Remove values from fields in copied form
//         let inputs = newForm.querySelectorAll('input');
//         inputs.forEach(input => {
//             if (input.type === 'text' || input.type === 'number') {
//                 input.value = '';
//             }
//         });
//         this.container.appendChild(newForm);
//         this.totalForms.setAttribute('value', `${this.formNum + 1}`);
//         this.formNum++;
//         this.attachBlurEventToLastField();
//         }
//
//     attachBlurEventToLastField() {
//         let lastNameField = document.getElementById(`id_sold_products-${this.formNum - 1}-product_name`);
//         let needsRowAfter = true;
//         lastNameField.addEventListener('focus',  (e) => {
//             if (e.target.value) {
//                 needsRowAfter = false;
//             }
//         });
//         lastNameField.addEventListener('blur', (e) => {
//             if (e.target.value && e.target === lastNameField && needsRowAfter === true) {
//                 this.addRow();
//                 multicolumnDropdown(`#id_sold_products-${this.formNum - 1}-product_name`, productNamesDict, 'id_sold_products');
//                 getProductPrice(this.formNum - 1, "id_sold_products", "product_price_before_tax", "product_price", "product_retail_price");
//                 updateRowTotal(this.formNum - 1,"id_sold_products", "product_price_before_tax", "product_total_before_tax");
//                 updateRowTotal(this.formNum - 1,"id_sold_products", "product_price", "product_total");
//                 scrollToBottom('sales-wrapper');
//                 addDeleteRowButton(this.formNum);
//             }
//         });
//     }
//
//    updateTotalSum() {
//         this.soldProductsTable.addEventListener('change', () => {
//         let sumNoVat = totalSum(this.formNum, "id_sale_total_before_tax", "id_sold_products", "product_total_before_tax");
//         let sumWithVat = totalSum(this.formNum, "id_sale_total_final", "id_sold_products", "product_total");
//         const totalVat = document.getElementById('id_sale_total_tax');
//         totalVat.value = (sumWithVat - sumNoVat).toFixed(2);
//         });
//     }
//
// }



class AddProductFormSale extends AddProductForm {
    constructor() {
        super("#sold-products tbody", "#id_sold_products-TOTAL_FORMS", "id_sold_products", "sold-products", "id_sale_total_final");
    }

    additionalSetup() {
        multicolumnDropdown(`#id_sold_products-${this.formNum - 1}-product_name`, productNamesDict, 'id_sold_products');
        getProductPrice(this.formNum - 1, "id_sold_products", "product_price_before_tax", "product_price", "product_retail_price");
        updateRowTotal(this.formNum - 1, "id_sold_products", "product_price_before_tax", "product_total_before_tax");
        updateRowTotal(this.formNum - 1, "id_sold_products", "product_price", "product_total");
        scrollToBottom('sales-wrapper');
        addDeleteRowButton(this.formNum);
    }
}







/** Adds or removes from the html the fields necessary for an invoice,
 * depending on whether an invoice will be issued */
function setupInvoiceToggle() {
    const invoiceCheckbox = document.getElementById('id_is_linked_to_invoice');
    const invoiceData = document.getElementById('invoice-number-and-dates');
    const buyerData = document.getElementById('buyer-data');
    const buyerDataToggleFields = document.getElementById('buyer-data-toggle-fields');
    const invoiceToggledFields = document.getElementById('invoice-toggled-fields');
    const productsTable = document.querySelector('#sold-products table');
    const totalBeforeVat = document.getElementById('total_before_tax');
    const totalVat = document.getElementById('total_tax');

    function toggleAllFields() {
        if (invoiceCheckbox.checked) {
            invoiceData.appendChild(invoiceToggledFields);
            initializeDatepicker ()
            buyerData.appendChild(buyerDataToggleFields);
            initializeDatepicker ()
            tableColumnShow(productsTable, 'price-before-tax', 'total-before-tax');
            tableColumnHide(productsTable, 'price-with-tax', 'total-with-tax');
            totalBeforeVat.style.display = 'block';
            totalVat.style.display = 'block';
        } else {
            invoiceData.removeChild(invoiceToggledFields);
            buyerData.removeChild(buyerDataToggleFields);
            tableColumnShow(productsTable,'price-with-tax', 'total-with-tax');
            tableColumnHide(productsTable, 'price-before-tax', 'total-before-tax');
            totalBeforeVat.style.display = 'none';
            totalVat.style.display = 'none';
        }
    }
    toggleAllFields();
    invoiceCheckbox.addEventListener('change', () =>{ toggleAllFields()});
}


/** Toggles the visibility of quick-product-select widget*/
function toggleQuickSelect () {
    const quickSelectSection = document.getElementById('quick-product-select');
    const salesForm = document.getElementById('sales-form');
    if (!quickSelectSection) {
        salesForm.style.width = '100vw';
    }
}

/** Goes through all the rows of the product table on initial load or reload after validation errors
 * and runs functions corresponding to fields - adding dropdown menu, getting prices, calculating sums and adding buttons */
function initialSaleProductRowFunctions () {
    let departmentId = document.getElementById('id_department').value;
    const productForms = document.querySelectorAll(".product-form");
    let numberOfRows = productForms.length;
    fetchProductsByDepartment(departmentId, productNamesDict).then(() => {
        for (let index = 0; index < numberOfRows; index++) {
            multicolumnDropdown(`#id_sold_products-${index}-product_name`, productNamesDict, 'id_sold_products');
            getProductPrice(index, "id_sold_products", "product_price_before_tax", "product_price", "product_retail_price");
            updateRowTotal(index, "id_sold_products", "product_price_before_tax", "product_total_before_tax");
            updateRowTotal(index, "id_sold_products", "product_price", "product_total");
            addDeleteRowButton(index+1);
        }
    });
}




document.addEventListener('DOMContentLoaded', function () {
    const addProductFormSale = new AddProductFormSale();
    setupInvoiceToggle();
    EnterKeyBehavior('sold-products','id_sold_products');
    disableArrowKeys("sale-document");
    initialSaleProductRowFunctions();
    getClientNames();
    toggleQuickSelect();
    updateProductsDropdown('id_department', 'id_sold_products', productNamesDict);
});




