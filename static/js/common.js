/** Fetches product price from either Products or Inventory models.
 * In case of Inventory ot matches both by name and lot */
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
                rowTotal(index, formsetPrefix, priceFieldSuffix, 'product_total');
            })
            .catch(error => console.error('There has been a problem with your fetch operation:', error));
    });
}


/** Calculates quantity*price*discount for every row */
function rowTotal(index, formsetPrefix, priceFieldSuffix, sumFieldSuffix) {
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


/** Updates row total */
function updateRowSum(index, formsetPrefix, priceFieldSuffix, sumFieldSuffix) {
    const rowProductForm = document.querySelector(`.product-form:nth-child(${index+1})`);
    rowProductForm.addEventListener('input', () => {
        rowTotal(index, formsetPrefix, priceFieldSuffix, sumFieldSuffix)
    })
}

/** Sums all the values or a specified column and sets that as the value of a specified field */
function totalSum (formNum, totalSumId, formsetPrefix, sumFieldSuffix) {
    const totalSumField = document.getElementById(totalSumId);
    let totalSum = 0;
    for (let i= 0; i<formNum; i++) {
        let productSumField = document.getElementById(`${formsetPrefix}-${i}-${sumFieldSuffix}`);
        if (productSumField.value) {
            totalSum += parseFloat(productSumField.value);
        }
    }
    totalSumField.value = totalSum;
}



/** Connects the footer button to the form, so it can be used to submit it */
function footerOkButton (formId) {
    const okButton = document.getElementById('footer-ok-button');
    const formToSubmit = document.getElementById(formId);
    okButton.addEventListener('click', () => {
        formToSubmit.submit();
    });
}