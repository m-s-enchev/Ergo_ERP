document.addEventListener('DOMContentLoaded', () => {
    profileTooltip();
})


/** Prevents the ArrowUp and ArrowDown keys from incrementing and decrementing number fields.
 * A users intuitive expectation in a table would be from those key to navigate,
 * so when pressed, the change of value in a field may not be noticed.*/
function disableArrowKeys (documentId) {
    const documentSection = document.getElementById(documentId);
    documentSection.addEventListener('keydown', (e) => {
        if (e.key === 'ArrowUp' || e.key === 'ArrowDown') {
            e.preventDefault();
        }
        });
}


/** Prevents the default behavior of "Enter" key and instead uses it to switch from product_name
 * to product_quantity and from there to the next row. The purpose is to make its use intuitive
 * for the user and speed up product entry.*/
function EnterKeyBehavior(tableId, formsetPrefix) {
    const tableBodyContainer = document.querySelector(`#${tableId} tbody`);
    tableBodyContainer.addEventListener('keydown', function (e) {
        if (e.target.tagName === 'INPUT' && e.key === 'Enter') {
            e.preventDefault();
            const currentId = e.target.id;
            const integerInId = currentId.match(/\d+/);
            const currentRowIndex = parseInt(integerInId[0], 10);
            if (currentId.includes('-product_name')) {
                const nextInput = document.querySelector(`#${formsetPrefix}-${currentRowIndex}-product_quantity`);
                if (nextInput) nextInput.focus();
            } else {
                const productForms = document.querySelectorAll(".product-form");
                const productFormsLength = productForms.length;
                const nextInput = document.querySelector(`#${formsetPrefix}-${productFormsLength-1}-product_name`);
                if (nextInput) nextInput.focus();
            }
        }
    });
}


function scrollToBottom(wrapperId) {
        const container = document.getElementById(wrapperId);
        container.scrollTop = container.scrollHeight;
    }


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


/** Fetches one of the prices of selected product */
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


/** Fetches the purchase_price and unit of selected product */
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


/** A multicolumn dropdown menu that displays choice of products, their unit, lot and exp. date
 * and available quantity in inventory. After selection name, lot and exp. date fields get filled */
function multicolumnDropdown(selector, productNamesDict, formsetPrefix) {
    let productNames = Object.keys(productNamesDict);
    $(selector).autocomplete({
        source: productNames,
        select: function(event, ui) {
            let idPrefix = this.id.substring(0, this.id.lastIndexOf("-") + 1);
            let details = productNamesDict[ui.item.value];
            $(`#${idPrefix}product_unit`).val(details[1]);
            $(`#${idPrefix}product_lot_number`).val(details[2]);
            $(`#${idPrefix}product_exp_date`).val(details[3]);
            return false;
        },
        open: function() {
            let dropdownWidth = 1.02 * getElementsWidth([
                `#${formsetPrefix}-0-product_name`,
                `#${formsetPrefix}-0-product_quantity`,
                `#${formsetPrefix}-0-product_unit`,
                `#${formsetPrefix}-0-product_lot_number`,
                `#${formsetPrefix}-0-product_exp_date`
            ]);
            $(this).autocomplete("widget").css({
                "width": dropdownWidth + "px"
            });
        }
    }).autocomplete("instance")._renderItem = function(ul, item) {
        let details = productNamesDict[item.value];
        let label;
        const lotColumn = document.querySelector('th.lot');
        if (lotColumn.style.display !== 'none') {
            label = `<div class="products-dropdown">
                        <span>${item.value}</span>
                        <span>${details[0]}</span>
                        <span>${details[1]}</span>
                        <span>${details[2]}</span>
                        <span>${details[3]}</span>
                    </div>`;
        } else {
            label = `<div class="products-dropdown">
                        <span>${item.value}</span>
                        <span>${details[0]}</span>
                        <span>${details[1]}</span>
                    </div>`;
        }
        return $("<li>")
            .append(`${label}`)
            .appendTo(ul);
    };
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


function fetchProductsByDepartment(departmentId, outputDict) {
    if (departmentId) {
        let url = `/common/get-products-by-department/?department_id=${departmentId}`;
        return fetch(url)
            .then(response => response.json())
            .then(data => {
                for (let key in outputDict) {
                    if (outputDict.hasOwnProperty(key)) {
                        delete outputDict[key];
                    }
                }
                for (let key in data) {
                    if (data.hasOwnProperty(key)) {
                        outputDict[key] = data[key];
                    }
                }
            })
            .catch(error => console.error('Error fetching products:', error));
    } else {
        return Promise.resolve(null);
    }
}



function updateProductsDropdown(departmentFieldId, formsetPrefix, outputDict) {
    const departmentField = document.getElementById(departmentFieldId);
    departmentField.addEventListener('change', function () {
        let productForms = document.querySelectorAll(".product-form");
        let departmentId = departmentField.value;
        let numberOfRows = productForms.length;
        fetchProductsByDepartment(departmentId, outputDict ).then(() => {
            for (let index = 0; index < numberOfRows; index++) {
                multicolumnDropdown(`#${formsetPrefix}-${index}-product_name`,outputDict,formsetPrefix);
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

