
let productNamesDict = {};

document.addEventListener('DOMContentLoaded', function () {
    const productFormManager = new ProductFormManager();
    productFormManager.attachBlurEventToLastField();
    setupInvoiceToggle();
    setupEnterKeyBehavior();
    disableArrowKeys();
    updateProductsDropdown();
    getProductPrice(0,"id_sold_products", "product_price_before_tax","product_price", "product_retail_price");
    updateRowTotal(0,"id_sold_products", "product_price_before_tax", "product_total_before_tax");
    updateRowTotal(0,"id_sold_products", "product_price", "product_total");
    getClientNames();
    profileTooltip();
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
            $(`#${idPrefix}product_unit`).val(details[1]);
            $(`#${idPrefix}product_lot_number`).val(details[2]);
            $(`#${idPrefix}product_exp_date`).val(details[3]);
            return false;
        },
        open: function() {
        let rowWidth = getRowWidth(".product-form");
        let dropdownWidth = rowWidth * 0.71;
        $(this).autocomplete("widget").css({
            "width": dropdownWidth + "px"
        });
        }

    }).autocomplete("instance")._renderItem = function(ul, item) {
        let details = productNamesDict[item.value];
        let label = `<div>
                                <span>${item.value}</span>
                                <span>${details[0]}</span>
                                <span>${details[1]}</span>
                                <span>${details[2]}</span>
                                <span>${details[3]}</span>
                            </div>`;
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
                getProductPrice(this.formNum - 1, "id_sold_products", "product_price_before_tax", "product_price", "product_retail_price");
                updateRowTotal(this.formNum - 1,"id_sold_products", "product_price_before_tax", "product_total_before_tax");
                updateRowTotal(this.formNum - 1,"id_sold_products", "product_price", "product_total");
                scrollToBottom('sales-wrapper');
            }
        });
    }

       updateTotalSum() {
        this.soldProductsTable.addEventListener('change', () => {
            let sumNoVat = totalSum(this.formNum, "id_sale_total_before_tax", "id_sold_products", "product_total_before_tax");
            let sumWithVat = totalSum(this.formNum, "id_sale_total_final", "id_sold_products", "product_total");
            const totalVat = document.getElementById('id_sale_total_tax');
            totalVat.value = (sumWithVat - sumNoVat).toFixed(2);
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
    const totalBeforeVat = document.getElementById('total_before_tax');
    const totalVat = document.getElementById('total_tax');

    tableColumnHide(productsTable, 'price-before-tax', 'total-before-tax');
    invoiceData.removeChild(invoiceToggledFields);
    buyerData.removeChild(buyerDataToggleFields);
    totalBeforeVat.style.display = 'none';
    totalVat.style.display = 'none';

    invoiceCheckbox.addEventListener('change', function () {
        if (invoiceCheckbox.checked) {
            invoiceMainHeading.style.fontWeight = 'bold';
            invoiceData.appendChild(invoiceToggledFields);
            initializeDatepicker ()
            buyerData.appendChild(buyerDataToggleFields);
            initializeDatepicker ()
            tableColumnShow(productsTable, 'price-before-tax', 'total-before-tax');
            tableColumnHide(productsTable, 'price-with-tax', 'total-with-tax');
            totalBeforeVat.style.display = 'block';
            totalVat.style.display = 'block';
        } else {
            invoiceMainHeading.style.fontWeight = 'normal';
            invoiceData.removeChild(invoiceToggledFields);
            buyerData.removeChild(buyerDataToggleFields);
            tableColumnShow(productsTable,'price-with-tax', 'total-with-tax');
            tableColumnHide(productsTable, 'price-before-tax', 'total-before-tax');
            totalBeforeVat.style.display = 'none';
            totalVat.style.display = 'none';
        }
    });
}

function getClientNames (){
    $(document).ready(function() {
    $("#id_buyer_name").autocomplete({
        source: "/common/get-client-names/",
        minLength: 2,
    });
});
}








