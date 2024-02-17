
function getProductPrice(index, modelType) {
    const productNameInput = document.getElementById(`id_sold_products-${index}-product_name`);
    const productPriceInput = document.getElementById(`id_sold_products-${index}-product_price`);

    productNameInput.addEventListener('change', function() {
        const productName = this.value;

        fetch(`/common/get-product-price/?product_name=${encodeURIComponent(productName)}&model_type=${modelType}`)
            .then(response => {
                if (response.ok) {
                    return response.json();
                }
                throw new Error('Network response was not ok.');
            })
            .then(data => {
                productPriceInput.value = data.product_price;
            })
            .catch(error => console.error('There has been a problem with your fetch operation:', error));
    });
}
