const priceBeforeTax = 5
const productTotalBeforeTax = 8
const price = 6
const productTotal = 9

document.addEventListener('DOMContentLoaded', function () {
    const productFormManager = new ProductFormManager();
    productFormManager.attachBlurEventToLastField();
    setupInvoiceToggle();
    setupEnterKeyBehavior();
    disableArrowKeys();
    multicolumnDropdown("#id_sold_products-0-product_name");
    getProductPrice(0, "product", "id_sold_products", "product_price_before_tax");
    updateRowSum(0,"id_sold_products", "product_price", "product_total");
    footerOkButton('sales-form');

});


function getRowWidth(selector) {
    return $(selector).outerWidth(true);
}


/** A multicolumn dropdown menu that displays choice of products, their lot and exp. date
 * and available quantity in inventory. After selection name, lot and exp. date fields get filled */
function multicolumnDropdown(selector) {
    let productNames = Object.keys(productNamesDict);
    $(selector).autocomplete({
        source: productNames,
        select: function(event, ui) {
            let idPrefix = this.id.substring(0, this.id.lastIndexOf("-") + 1);
            let details = productNamesDict[ui.item.value];
            $(`#${idPrefix}product_lot_number`).val(details[1]);
            $(`#${idPrefix}product_exp_date`).val(details[2]);
            return false;
        },
        open: function() {
        let rowWidth = getRowWidth(".product-form");
        let dropdownWidth = rowWidth * 0.66;
        $(this).autocomplete("widget").css({
            "width": dropdownWidth + "px"
        });
        }

    }).autocomplete("instance")._renderItem = function(ul, item) {
        // Retrieve the additional details
        let details = productNamesDict[item.value];
        let label = `<div><span>${item.value}</span><span>${details[0]}</span><span>${details[1]}</span><span>${details[2]}</span></div>`;
        return $("<li>")
            .append(`${label}`)
            .appendTo(ul);
    };
}

/** Handles the adding of a new products row in table, which is a SoldProductsForm instance.
 * If the product_name field of the last row is filled and focus is shifted to another field,
 * a new row is added for the next product */
class ProductFormManager {
    constructor() {
        this.container = document.querySelector("#sold-products tbody");
        this.totalForms = document.querySelector("#id_sold_products-TOTAL_FORMS");
        this.productForms = document.querySelectorAll(".product-form");
        this.formNum = this.productForms.length;
        this.soldProductsTable = document.getElementById('sold-products');
        this.updateTotalSum();
    }

    addForm() {
            let newForm = this.productForms[0].cloneNode(true);
            let formRegex = /sold_products-0-/g;
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
        lastFirstField.addEventListener('focus',  (e) => {
            if (e.target.value) {
                needsRowAfter = false;
            }
        });
        lastFirstField.addEventListener('blur', (e) => {
            if (e.target.value && e.target === lastFirstField && needsRowAfter === true) {
                this.addForm();
                multicolumnDropdown(`#id_sold_products-${this.formNum - 1}-product_name`);
                getProductPrice(this.formNum - 1, "product", "id_sold_products", "product_price_before_tax");
                updateRowSum(this.formNum - 1,"id_sold_products", "product_price", "product_total");
            }
        });
    }

       updateTotalSum() {
        this.soldProductsTable.addEventListener('change', (event) => {
            totalSum(this.formNum, "total-sum", "id_sold_products", "product_total");

        });
    }

}



/** Prevents the default behavior of "Enter" key and instead uses it to switch from product_name
 * to product_quantity and from there to the next row. The purpose is to make its use intuitive
 * for the user and speed up product entry.*/
function setupEnterKeyBehavior() {
    const tableBodyContainer = document.querySelector("#sold-products tbody");
    tableBodyContainer.addEventListener('keydown', function (e) {
        if (e.target.tagName === 'INPUT' && e.key === 'Enter') {
            e.preventDefault();
            const currentId = e.target.id;
            const integerInId = currentId.match(/\d+/);
            const currentRowIndex = parseInt(integerInId[0], 10);
            if (currentId.includes('-product_name')) {
                const nextInput = document.querySelector(`#id_sold_products-${currentRowIndex}-product_quantity`);
                if (nextInput) nextInput.focus();
            } else {
                const productForms = document.querySelectorAll(".product-form");
                const productFormsLength = productForms.length;
                const nextInput = document.querySelector(`#id_sold_products-${productFormsLength-1}-product_name`);
                if (nextInput) nextInput.focus();
            }
        }
    });
}


/** Prevents the ArrowUp and ArrowDown keys from incrementing and decrementing number fields.
 * A users intuitive expectation in a table would be from those key to navigate,
 * so when pressed, the change of value in a field may not be noticed.*/
function disableArrowKeys () {
    const saleDocument = document.getElementById('sale-document');
    saleDocument.addEventListener('keydown', (e) => {
        if (e.key === 'ArrowUp' || e.key === 'ArrowDown') {
            e.preventDefault();
        }
        });
}

/** Adds or removes from the html the fields necessary for an invoice,
 * depending on whether an invoice will be issued */
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
            initializeDatepicker ()
            buyerData.appendChild(buyerDataToggleFields);
            initializeDatepicker ()
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












