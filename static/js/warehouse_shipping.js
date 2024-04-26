let productNamesDictShip= {};


function fetchProductsByDepartmentShip(departmentId) {
    if (departmentId) {
        let url = `/common/get-products-by-department/?department_id=${departmentId}`;
        return fetch(url)
            .then(response => response.json())
            .then(data => {
                productNamesDictShip = data;
                return productNamesDictShip;
            })
            .catch(error => console.error('Error fetching products:', error));
    } else {
        return Promise.resolve(null);
    }
}


function multicolumnDropdownShip(selector) {
    let productNames = Object.keys(productNamesDictShip);
    $(selector).autocomplete({
        source: productNames,
        select: function(event, ui) {
            let idPrefix = this.id.substring(0, this.id.lastIndexOf("-") + 1);
            let details = productNamesDictShip[ui.item.value];
            $(`#${idPrefix}product_unit`).val(details[1]);
            $(`#${idPrefix}product_lot_number`).val(details[2]);
            $(`#${idPrefix}product_exp_date`).val(details[3]);
            return false;
        },
        open: function() {
        let dropdownWidth = 1.02*getElementsWidth([
            '#id_transferred_products-0-product_name',
            '#id_transferred_products-0-product_quantity',
            '#id_transferred_products-0-product_unit',
            '#id_transferred_products-0-product_lot_number',
            '#id_transferred_products-0-product_exp_date'
        ]);
        $(this).autocomplete("widget").css({
            "width": dropdownWidth + "px"
        });
        }

    }).autocomplete("instance")._renderItem = function(ul, item) {
        let details = productNamesDictShip[item.value];
        let label;
        const lotColumn = document.querySelector('th.lot')
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


function saleEnterKeyBehavior() {
    const tableBodyContainer = document.querySelector("#shipped-products tbody");
    tableBodyContainer.addEventListener('keydown', function (e) {
        if (e.target.tagName === 'INPUT' && e.key === 'Enter') {
            e.preventDefault();
            const currentId = e.target.id;
            const integerInId = currentId.match(/\d+/);
            const currentRowIndex = parseInt(integerInId[0], 10);
            if (currentId.includes('-product_name')) {
                const nextInput = document.querySelector(`#id_transferred_products-${currentRowIndex}-product_quantity`);
                if (nextInput) nextInput.focus();
            } else {
                const productForms = document.querySelectorAll(".product-form");
                const productFormsLength = productForms.length;
                const nextInput = document.querySelector(`#id_transferred_products-${productFormsLength-1}-product_name`);
                if (nextInput) nextInput.focus();
            }
        }
    });
}



function initialShippedProductRowFunctions () {
    let departmentId = document.getElementById('id_shipping_department').value;
    const productForms = document.querySelectorAll(".product-form");
    let numberOfRows = productForms.length;
    fetchProductsByDepartmentShip(departmentId).then(() => {
        for (let index = 0; index < numberOfRows; index++) {
            multicolumnDropdownShip(`#id_transferred_products-${index}-product_name`);
            get_purchase_price(index, "id_transferred_products", "product_purchase_price");
            updateRowTotal(index, "id_transferred_products", "product_purchase_price", "product_value");
        }
    });
}


class ShippedProductsFormManager {
    constructor() {
        this.container = document.querySelector("#shipped-products tbody");
        this.totalForms = document.querySelector("#id_transferred_products-TOTAL_FORMS");
        this.productForms = document.querySelectorAll(".product-form");
        this.formNum = this.productForms.length;
        this.receivedProductsTable = document.getElementById('shipped-products');
        this.updateTotalSum();
    }

    addForm() {
            let newForm = this.productForms[0].cloneNode(true);
            let formRegex = /transferred_products-0-/g;
            let numeratorRegex = /(<td class="numerator">)\d+(<\/td>)/g;
            newForm.innerHTML = newForm.innerHTML.replace(formRegex, `transferred_products-${this.formNum}-`);
            newForm.innerHTML = newForm.innerHTML.replace(numeratorRegex, `<td class="numerator">${this.formNum + 1}</td>`);
            // Remove error messages from copied form
            let ulElements = newForm.querySelectorAll('ul');
            ulElements.forEach(function(ul) {
                ul.parentNode.removeChild(ul);
            });
            // Remove values from fields in copied form
            let inputs = newForm.querySelectorAll('input');
            inputs.forEach(input => {
                if (input.type === 'text' || input.type === 'number') {
                    input.value = '';
                }
            });
            this.container.appendChild(newForm);
            this.totalForms.setAttribute('value', `${this.formNum + 1}`);
            this.formNum++;
            this.attachBlurEventToLastField();
        }

    attachBlurEventToLastField() {
        let lastNameField = document.getElementById(`id_transferred_products-${this.formNum - 1}-product_name`);
        let needsRowAfter = true;
        lastNameField.addEventListener('focus',  (e) => {
            if (e.target.value) {
                needsRowAfter = false;
            }
        });
        lastNameField.addEventListener('blur', (e) => {
            if (e.target.value && e.target === lastNameField && needsRowAfter === true) {
                this.addForm();
                multicolumnDropdownShip(`#id_transferred_products-${this.formNum - 1}-product_name`);
                updateRowTotal(this.formNum - 1,"id_transferred_products", "product_purchase_price", "product_value");
                scrollToBottom('ship-wrapper');
            }
        });
    }

       updateTotalSum() {
        this.receivedProductsTable.addEventListener('change', () => {
            let documentTotalSum = totalSum(this.formNum, "id_total_sum", "id_transferred_products", "product_value");
        });
    }

}






document.addEventListener('DOMContentLoaded', function () {
    const shippedProductsFormManager = new ShippedProductsFormManager();
    shippedProductsFormManager.attachBlurEventToLastField();
    initialShippedProductRowFunctions();
    saleEnterKeyBehavior();
});