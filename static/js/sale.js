
let productNamesDict = {};


document.addEventListener('DOMContentLoaded', function () {
    const addProductFormManager = new AddProductFormManager();
    addProductFormManager.attachBlurEventToLastField();
    setupInvoiceToggle();
    saleEnterKeyBehavior();
    disableArrowKeys("sale-document");
    initialSaleProductRowFunctions();
    getClientNames();
    toggleQuickSelect();
    updateProductsDropdown('id_department', 'id_sold_products', productNamesDict);
});


/** Handles the adding of a new products row in table, which is a SoldProductsForm instance.
 * If the product_name field of the last row is filled and focus is shifted to another field,
 * a new row is added for the next product */
class AddProductFormManager {
    constructor() {
        this.container = document.querySelector("#sold-products tbody");
        this.totalForms = document.querySelector("#id_sold_products-TOTAL_FORMS");
        this.productForms = document.querySelectorAll(".product-form");
        this.formNum = this.productForms.length;
        this.soldProductsTable = document.getElementById('sold-products');
        this.updateTotalSum();
    }

    addRow() {
        let newForm = this.productForms[0].cloneNode(true);
        let formRegex = /sold_products-0-/g;
        let numeratorRegex = /(<td class="numerator">)\d+(<\/td>)/g;
        newForm.innerHTML = newForm.innerHTML.replace(formRegex, `sold_products-${this.formNum}-`);
        newForm.innerHTML = newForm.innerHTML.replace(numeratorRegex, `<td class="numerator">${this.formNum + 1}</td>`);
        // Remove error messages from copied form
        let ulElements = newForm.querySelectorAll('ul');
        ulElements.forEach(function(ul) {
            ul.parentNode.removeChild(ul);
        });
        // Remove values from fields in copied form
        let inputs = newForm.querySelectorAll('input');
        inputs.forEach(input => {
            if (input.type === 'text' || input.type === 'number') {
                input.value = '';
            }
        });
        this.container.appendChild(newForm);
        this.totalForms.setAttribute('value', `${this.formNum + 1}`);
        this.formNum++;
        this.attachBlurEventToLastField();
        }

    attachBlurEventToLastField() {
        let lastNameField = document.getElementById(`id_sold_products-${this.formNum - 1}-product_name`);
        let needsRowAfter = true;
        lastNameField.addEventListener('focus',  (e) => {
            if (e.target.value) {
                needsRowAfter = false;
            }
        });
        lastNameField.addEventListener('blur', (e) => {
            if (e.target.value && e.target === lastNameField && needsRowAfter === true) {
                this.addRow();
                multicolumnDropdown(`#id_sold_products-${this.formNum - 1}-product_name`, productNamesDict, 'id_sold_products');
                getProductPrice(this.formNum - 1, "id_sold_products", "product_price_before_tax", "product_price", "product_retail_price");
                updateRowTotal(this.formNum - 1,"id_sold_products", "product_price_before_tax", "product_total_before_tax");
                updateRowTotal(this.formNum - 1,"id_sold_products", "product_price", "product_total");
                scrollToBottom('sales-wrapper');
                addDeleteRowButton(this.formNum);
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
function saleEnterKeyBehavior() {
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


/** Uses jquery autoselect to create a dropdown menu for 'Clients' field.
 * Populates it with instances of Clients model */
function getClientNames() {
    $(document).ready(function() {
        $("#id_buyer_name").autocomplete({
            source: function(request, response) {
                $.ajax({
                    url: "/common/get-client-names/",
                    data: { term: request.term },
                    dataType: "json",
                    success: function(data) {
                        response($.map(data, function(item) {
                            return {
                                value: item.client_names,
                                client_phone_number: item.client_phone_number,
                                client_email: item.client_email,
                                client_identification_number: item.client_identification_number,
                                client_address: item.client_address,
                                client_accountable_person: item.client_accountable_person,
                            };
                        }));
                    }
                });
            },
            minLength: 2,
            position: { my : "right top", at: "right bottom" },
            select: function(event, ui) {
                $('#id_buyer_identification_number').val(ui.item.client_identification_number);
                $('#id_buyer_address').val(ui.item.client_address);
                $('#id_client_email').val(ui.item.client_email);
                $('#id_buyer_accountable_person').val(ui.item.client_accountable_person);
            }
        })
        .autocomplete("instance")._renderItem = function(ul, item) {
            return $("<li>")
                .append(`<div class="clients-dropdown">
                            <span>${item.value}</span>
                            <span>${item.client_phone_number}</span> 
                            <span>${item.client_email}</span>
                            <span>${item.client_identification_number}</span>
                         </div>`)
                .appendTo(ul);
        };
    });
}



function toggleQuickSelect () {
    const quickSelectSection = document.getElementById('quick-product-select');
    const salesForm = document.getElementById('sales-form');
    if (!quickSelectSection) {
        salesForm.style.width = '100vw';
    }
}

/** Goes through all the rows of the product table on initial load or reload after validation errors
 * and runs functions corresponding to fields. */
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



