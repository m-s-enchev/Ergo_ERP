/** Fetches product price from either Products or Inventory models.
 * In case of Inventory ot matches both by name and lot */

// function getProductPrice(index, modelName, formsetPrefix, priceFieldNoVatSuffix, priceFieldWithVatSuffix=null) {
//     const productNameInput = document.getElementById(`${formsetPrefix}-${index}-product_name`);
//     const productLotInput = document.getElementById(`${formsetPrefix}-${index}-product_lot_number`);
//     const productPriceInput = document.getElementById(`${formsetPrefix}-${index}-${priceFieldNoVatSuffix}`);
//
//     productNameInput.addEventListener('change', function() {
//         const productName = this.value;
//         let fetchUrl = `/common/get-product-price/?product_name=${encodeURIComponent(productName)}&model_name=${modelName}`;
//         if (productLotInput) {
//             fetchUrl += `&product_lot=${encodeURIComponent(productLotInput.value)}`;
//         }
//
//         fetch(fetchUrl)
//             .then(response => {
//                 if (response.ok) {
//                     return response.json();
//                 }
//                 throw new Error('Network response was not ok.');
//             })
//             .then(data => {
//                 productPriceInput.value = data.product_price;
//                 rowTotal(index, formsetPrefix, priceFieldNoVatSuffix, 'product_total_before_tax');
//                 if (priceFieldWithVatSuffix) {
//                     const productPriceInputWithVat = document.getElementById(`${formsetPrefix}-${index}-${priceFieldWithVatSuffix}`);
//                     productPriceInputWithVat.value = (data.product_vat*0.01+1)*data.product_price
//                     rowTotal(index, formsetPrefix, priceFieldWithVatSuffix, 'product_total');
//                 }
//
//             })
//             .catch(error => console.error('There has been a problem with your fetch operation:', error));
//     });
// }


document.addEventListener('DOMContentLoaded', () => {
    profileTooltip();
})



/** Hides on or more columns in a table based on class name of cells */
function tableColumnHide (table, ...columnClassNames) {
    for (let name of columnClassNames) {
        let cells = table.querySelectorAll(`td.${name}, th.${name}`);
        cells.forEach(cell => {cell.style.display = 'none'});
    }
}

/** Shows on or more hidden columns in a table based on class name of cells */
function tableColumnShow (table, ...columnClassNames) {
    for (let name of columnClassNames) {
        let cells = table.querySelectorAll(`td.${name}, th.${name}`);
        cells.forEach(cell => {cell.style.display = 'table-cell'});
    }
}


/** Fetches the price and unit of selected product */
function getProductPrice(index, formsetPrefix, priceNoTaxSuffix, priceWithTaxSuffix, priceType) {
    const nameInput = document.getElementById(`${formsetPrefix}-${index}-product_name`);
    const priceNoTaxInput = document.getElementById(`${formsetPrefix}-${index}-${priceNoTaxSuffix}`);
    const priceWithTaxInput = document.getElementById(`${formsetPrefix}-${index}-${priceWithTaxSuffix}`);
    nameInput.addEventListener('change', function() {
        const productName = this.value;
        fetch(`/common/get-product-price/?product_name=${encodeURIComponent(productName)}&price_type=${priceType}`)
            .then(response => {
                if (response.ok) {
                    return response.json();
                }
                throw new Error('Network response was not ok.');
            })
            .then(data => {
                priceNoTaxInput.value = data.product_price;
                rowTotal(index, formsetPrefix, priceNoTaxSuffix, 'product_total_before_tax');
                priceWithTaxInput.value = ((data.product_vat*0.01+1)*data.product_price).toFixed(2)
                rowTotal(index, formsetPrefix, priceWithTaxSuffix, 'product_total');
            })
            .catch(error => console.error('There has been a problem with your fetch operation:', error));
    });
}

function get_purchase_price(index, formsetPrefix, priceSuffix){
    const nameInput = document.getElementById(`${formsetPrefix}-${index}-product_name`);
    const priceInput = document.getElementById(`${formsetPrefix}-${index}-${priceSuffix}`);
    nameInput.addEventListener('change', function() {
        const productName = this.value;
        fetch(`/common/get-purchase-price/?product_name=${encodeURIComponent(productName)}`)
            .then(response => {
                    if (response.ok) {
                        return response.json();
                    }
                    throw new Error('Network response was not ok.');
                })
            .then(data => {
                priceInput.value = data.purchase_price;
                rowTotal(index, formsetPrefix, priceSuffix, 'product_total');
            })
            .catch(error => console.error('There has been a problem with your fetch operation:', error));
    });
}


/** Calculates quantity*price*discount for every row */
function rowTotal(index, formsetPrefix, priceFieldSuffix, totalFieldSuffix) {
    const quantityField = document.getElementById(`${formsetPrefix}-${index}-product_quantity`);
    const priceField = document.getElementById(`${formsetPrefix}-${index}-${priceFieldSuffix}`);
    const discountField = document.getElementById(`${formsetPrefix}-${index}-product_discount`);
    const rowTotalField = document.getElementById(`${formsetPrefix}-${index}-${totalFieldSuffix}`);
    let quantity = parseFloat(quantityField.value);
    let price = parseFloat(priceField.value);
    if (discountField && discountField.value){
        rowTotalField.value = (quantity * price * (1 - discountField.value*0.01)).toFixed(2);
    }else {
        rowTotalField.value = (quantity * price).toFixed(2);
    }
}


/** Updates row total */
function updateRowTotal(index, formsetPrefix, priceFieldSuffix, totalFieldSuffix) {
    const rowProductForm = document.querySelector(`.product-form:nth-child(${index+1})`);
    rowProductForm.addEventListener('input', () => {
        rowTotal(index, formsetPrefix, priceFieldSuffix, totalFieldSuffix)
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
    totalSumField.value = totalSum.toFixed(2);
    return totalSum.toFixed(2)
}


function scrollToBottom(wrapperId) {
        const container = document.getElementById(wrapperId);
        container.scrollTop = container.scrollHeight;
    }


function fetchProductsByDepartment(departmentId) {
    if (departmentId) {
        let url = `/common/get-products-by-department/?department_id=${departmentId}`;
        return fetch(url)
            .then(response => response.json())
            .then(data => {
                productNamesDict = data;
                return productNamesDict;
            })
            .catch(error => console.error('Error fetching products:', error));
    } else {
        return Promise.resolve(null);
    }
}


function fetchProductsAll() {
    let url = `/common/get-products-all/`;
    return fetch(url)
        .then(response => response.json())
        .then(data => {
            productNamesDictAll = data;
            return productNamesDictAll;
        })
        .catch(error => console.error('Error fetching products:', error));
}

// function updateProductsDropdown() {
//     const departmentField = document.getElementById('id_department');
//     departmentField.addEventListener('change', function () {
//         let productForms = document.querySelectorAll(".product-form");
//         let departmentId = departmentField.value
//         let numberOfRows = productForms.length;
//         fetchProductsByDepartment(departmentId).then(() => {
//             for (let index = 0; index < numberOfRows; index++) {
//                 multicolumnDropdown(`#id_sold_products-${index}-product_name`);
//             }
//         });
//     });
// }


function updateProductsDropdown(departmentFieldId, formsetPrefix) {
    const departmentField = document.getElementById(departmentFieldId);
    departmentField.addEventListener('change', function () {
        let productForms = document.querySelectorAll(".product-form");
        let departmentId = departmentField.value
        let numberOfRows = productForms.length;
        fetchProductsByDepartment(departmentId).then(() => {
            for (let index = 0; index < numberOfRows; index++) {
                multicolumnDropdown(`#${formsetPrefix}-${index}-product_name`);
            }
        });
    });
}


function profileTooltip () {
    const target = document.querySelector('#main-navigation #user');
    const popup = document.getElementById('user-profile-tooltip');
    let isVisible = false;
    function showPopup() {
        isVisible = true;
        popup.style.display = 'flex';
    }
    function hidePopup() {
        isVisible = false;
        popup.style.display = 'none';
    }
    document.addEventListener('click', function(e) {
        if (target.contains(e.target)) {
            if (!isVisible){
                showPopup();
            }
        } else if (!popup.contains(e.target)) {
            if (isVisible) {
                hidePopup();
            }
        }
    });
}


function getElementsWidth(selectors) {
    let totalWidth = 0;
    selectors.forEach(function(selector) {
        let width = $(selector).outerWidth(true) || 0;
        totalWidth += width;
    });
    return totalWidth;
}

function deleteRow(e){
    const row = e.target.closest('tr');
    const product = row.querySelector('.name input').value;
    if (row && product) {
        row.remove();

    }
}

function resetNumerators (){
    const totalForms=document.querySelector('[id$="-TOTAL_FORMS"]');
    const productForms = document.querySelectorAll(".product-form");
    totalForms.value = productForms.length;
    const numerators = document.querySelectorAll('.numerator');
    const productRows = document.querySelectorAll('tbody tr');
    const indexRegex = /-(\d+)-/;
    for (let i= 1; i<= productForms.length; i++) {
        numerators[i].textContent = `${i}`;
        let productInputs = productRows[i-1].querySelectorAll('td input')
        for (let input of productInputs) {
            input.name = input.name.replace(indexRegex, `-${i-1}-`)
            input.id = input.id.replace(indexRegex, `-${i-1}-`)
        }
    }
}

function addDeleteRowButton(index){
const deleteButton = document.querySelector(`table tr:nth-child(${index}) .row-delete-button .fa-trash`);
    deleteButton.addEventListener('click', (e) => {
        deleteRow(e);
        resetNumerators();
    });
}