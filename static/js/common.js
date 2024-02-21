
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
                updateRowSum(index, formsetPrefix, priceFieldSuffix, 'product_total');
            })
            .catch(error => console.error('There has been a problem with your fetch operation:', error));
    });
}



function updateRowSum(index, formsetPrefix, priceFieldSuffix, sumFieldSuffix) {
    const quantityField = document.getElementById(`${formsetPrefix}-${index}-product_quantity`);
    const priceField = document.getElementById(`${formsetPrefix}-${index}-${priceFieldSuffix}`);
    const discountField = document.getElementById(`${formsetPrefix}-${index}-product_discount`);
    const rowSumField = document.getElementById(`${formsetPrefix}-${index}-${sumFieldSuffix}`);
    let quantity = parseFloat(quantityField.value);
    let price = parseFloat(priceField.value);
    let discount = parseFloat(discountField.value);

    if (discount) {
        rowSumField.value = quantity * price * (1 - discount / 100);
    } else {
        rowSumField.value = quantity * price;
    }
}



function rowTotal(index, formsetPrefix, priceFieldSuffix, sumFieldSuffix) {
    const rowProductForm = document.querySelector(`.product-form:nth-child(${index+1})`);
    rowProductForm.addEventListener('input', () =>
        updateRowSum(index, formsetPrefix, priceFieldSuffix, sumFieldSuffix))
}



function footerOkButton (formId) {
    const okButton = document.getElementById('footer-ok-button');
    const formToSubmit = document.getElementById(formId);
    okButton.addEventListener('click', () => {
        formToSubmit.submit();
    });
};