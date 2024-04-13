let productNamesDict = {};

function initialReceiveProductRowFunctions () {
    const productForms = document.querySelectorAll(".product-form");
    let numberOfRows = productForms.length;
    fetchProductsAll().then(() => {
        for (let index = 0; index < numberOfRows; index++) {
            multicolumnDropdown(`#id_transferred_products-${index}-product_name`);
            // getProductPrice(index, "id_transferred_products", "product_purchase_price", "product_price", "product_retail_price");
            updateRowTotal(index, "id_transferred_products", "product_purchase_price", "product_total_before_tax");
        }
    });
}

id_transferred_products-0-product_name