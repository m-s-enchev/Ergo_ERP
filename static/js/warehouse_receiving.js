

let productNamesDictAll= {};


function twoColumnDropdown(selector) {
    let productNames = Object.keys(productNamesDictAll);
    $(selector).autocomplete({
        source: productNames,
        select: function(event, ui) {
            let idPrefix = this.id.substring(0, this.id.lastIndexOf("-") + 1);
            let details = productNamesDictAll[ui.item.value];
            $(`#${idPrefix}product_unit`).val(details[1]);
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
                                <span>${details[1]}</span>
                            </div>`;
        return $("<li>")
            .append(`${label}`)
            .appendTo(ul);
    };
}






function initialReceiveProductRowFunctions () {
    const productForms = document.querySelectorAll(".product-form");
    let numberOfRows = productForms.length;
    fetchProductsAll().then(() => {
        for (let index = 0; index < numberOfRows; index++) {
            twoColumnDropdown(`#id_transferred_products-${index}-product_name`);
            get_purchase_price(index, "id_transferred_products", "product_purchase_price");
            updateRowTotal(index, "id_transferred_products", "product_purchase_price", "product_value");
        }
    });
}


function receiveEnterKeyBehavior() {
    const tableBodyContainer = document.querySelector("#transferred_products tbody");
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




document.addEventListener('DOMContentLoaded', function () {
    initialReceiveProductRowFunctions();
});