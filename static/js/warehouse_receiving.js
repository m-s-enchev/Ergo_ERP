let productNamesDictAll= {};


/** A two column dropdown menu that displays choice of products and their unit */
function twoColumnDropdown(selector) {
    let productNames = Object.keys(productNamesDictAll);
    $(selector).autocomplete({
        source: productNames,
        select: function(event, ui) {
            let idPrefix = this.id.substring(0, this.id.lastIndexOf("-") + 1);
            let details = productNamesDictAll[ui.item.value];
            $(`#${idPrefix}product_unit`).val(details);
            return false;
        },
        open: function() {
        let dropdownWidth = 1.02*getElementsWidth([
            '#id_transferred_products-0-product_name',
            '#id_transferred_products-0-product_quantity',
            '#id_transferred_products-0-product_unit',
        ]);
        $(this).autocomplete("widget").css({
            "width": dropdownWidth + "px"
        });
        }

    }).autocomplete("instance")._renderItem = function(ul, item) {
        let details = productNamesDictAll[item.value];
        let label = `<div class="products-dropdown">
                                <span>${item.value}</span>
                                <span>${details}</span>
                            </div>`;
        return $("<li>")
            .append(`${label}`)
            .appendTo(ul);
    };
}


function receiveEnterKeyBehavior() {
    const tableBodyContainer = document.querySelector("#received-products tbody");
    tableBodyContainer.addEventListener('keydown', function (e) {
        if (e.target.tagName === 'INPUT' && e.key === 'Enter') {
            e.preventDefault();

            const inputs = Array.from(tableBodyContainer.querySelectorAll('input'));
            const currentIndex = inputs.indexOf(e.target);
            const nextIndex = currentIndex + 1;
            if (nextIndex < inputs.length) {
                inputs[nextIndex].focus();
            } else {
                inputs[0].focus();
            }
        }
    });
}


class AddProductsFormReceive extends AddProductForm {
    constructor() {
        super(
            "#received-products tbody",
            "#id_transferred_products-TOTAL_FORMS",
            "id_transferred_products",
            "received-products",
            "id_total_sum"
        );
    }
    additionalSetup() {
        twoColumnDropdown(`#id_transferred_products-${this.formNum - 1}-product_name`);
        updateRowTotal(
            this.formNum - 1,
            "id_transferred_products",
            "product_purchase_price",
            "product_total"
        );
        scrollToBottom('receive-wrapper');
        initializeDatepicker();
    }
}



/** Goes through all the rows of the product table on initial load or reload after validation errors
 * and runs functions corresponding to fields - adding dropdown menu and calculating sums and adding buttons */
function initialReceiveProductRowFunctions () {
    const productForms = document.querySelectorAll(".product-form");
    let numberOfRows = productForms.length;
    fetchProductsAll().then(() => {
        for (let index = 0; index < numberOfRows; index++) {
            twoColumnDropdown(`#id_transferred_products-${index}-product_name`);
            updateRowTotal(index, "id_transferred_products", "product_purchase_price", "product_total");
        }
    });
}


document.addEventListener('DOMContentLoaded', function () {
    const addProductFormReceive = new AddProductsFormReceive();
    // receivedProductsFormManager.attachBlurEventToLastField();
    disableArrowKeys("receive-document");
    initialReceiveProductRowFunctions();
    receiveEnterKeyBehavior();
});


