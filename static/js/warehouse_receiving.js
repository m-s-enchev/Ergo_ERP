

let productNamesDictAll= {};


function twoColumnDropdown(selector, productsDict) {
    let productNames = Object.keys(productsDict);
    $(selector).autocomplete({
        source: productNames,
        select: function(event, ui) {
            let idPrefix = this.id.substring(0, this.id.lastIndexOf("-") + 1);
            let details = productsDict[ui.item.value];
            $(`#${idPrefix}product_unit`).val(details[1]);
            return false;
        },
        open: function() {
        let dropdownWidth = 1.02*getElementsWidth([
            '#id_sold_products-0-product_name',
            '#id_sold_products-0-product_unit',
        ]);
        $(this).autocomplete("widget").css({
            "width": dropdownWidth + "px"
        });
        }

    }).autocomplete("instance")._renderItem = function(ul, item) {
        let details = productsDict[item.value];
        let label;
        const lotColumn = document.querySelector('th.lot')

            label = `<div class="products-dropdown">
                        <span>${item.value}</span>
                        <span>${details[0]}</span>
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
            multicolumnDropdown(`#id_transferred_products-${index}-product_name`);
            get_purchase_price(index, "id_transferred_products", "product_purchase_price");
            updateRowTotal(index, "id_transferred_products", "product_purchase_price", "product_total_before_tax");
        }
    });
}
document.addEventListener('DOMContentLoaded', function () {
    initialReceiveProductRowFunctions();
});