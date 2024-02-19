
function getProductPrice(index, modelName, formsetPrefix, priceFieldSuffix) {
    const productNameInput = document.getElementById(`${formsetPrefix}-${index}-product_name`);
    const productLotInput = document.getElementById(`${formsetPrefix}-${index}-product_lot_number`);
    const productPriceInput = document.getElementById(`${formsetPrefix}-${index}-${priceFieldSuffix}`);

    productNameInput.addEventListener('change', function() {
        const productName = this.value;
        let fetchUrl = `/common/get-product-price/?product_name=${encodeURIComponent(productName)}&model_name=${modelName}`;
        if (productLotInput) {
            fetchUrl += `&product_lot=${encodeURIComponent(productLotInput.value)}`;
        }

        fetch(fetchUrl)
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