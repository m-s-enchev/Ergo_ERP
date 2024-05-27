let productNamesDictShip= {};


class AddProductsFormShip extends AddProductForm {
    constructor() {
        super(
            "#shipped-products tbody",
            "#id_transferred_products-TOTAL_FORMS",
            "id_transferred_products",
            "shipped-products",
            "id_total_sum"
        );
    }
    additionalSetup() {
        multicolumnDropdown(
            `#id_transferred_products-${this.formNum - 1}-product_name`,
            productNamesDictShip,
            'id_transferred_products'
        );
        getPurchasePrice(
            this.formNum - 1,
            "id_transferred_products",
            "product_purchase_price"
        );
        updateRowTotal(
            this.formNum - 1,
            "id_transferred_products",
            "product_purchase_price",
            "product_total"
        );
        scrollToBottom('ship-wrapper');
    }
}



/** Goes through all the rows of the product table on initial load or reload after validation errors
 * and runs functions corresponding to fields - adding dropdown menu, getting prices, calculating sums and adding buttons */
function initialShippedProductRowFunctions () {
    let departmentId = document.getElementById('id_shipping_department').value;
    const productForms = document.querySelectorAll(".product-form");
    let numberOfRows = productForms.length;
    fetchProductsByDepartment(departmentId, productNamesDictShip ).then(() => {
        for (let index = 0; index < numberOfRows; index++) {
            multicolumnDropdown(
                `#id_transferred_products-${index}-product_name`,
                productNamesDictShip,
                'id_transferred_products'
            );
            getPurchasePrice(
                index,
                "id_transferred_products",
                "product_purchase_price"
            );
            updateRowTotal(
                index,
                "id_transferred_products",
                "product_purchase_price",
                "product_total"
            );
        }
    });
}

document.addEventListener('DOMContentLoaded', function () {
    const addProductFormShip = new AddProductsFormShip();
    disableArrowKeys("ship-document");
    initialShippedProductRowFunctions();
    EnterKeyBehavior('shipped-products','id_transferred_products');
    updateProductsDropdown(
        'id_shipping_department',
        'id_transferred_products',
        productNamesDictShip
    );
});