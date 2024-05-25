let productNamesDictShip= {};


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
    fetchProductsByDepartment(departmentId, productNamesDictShip ).then(() => {
        for (let index = 0; index < numberOfRows; index++) {
            multicolumnDropdownShip(`#id_transferred_products-${index}-product_name`);
            get_purchase_price(index, "id_transferred_products", "product_purchase_price");
            updateRowTotal(index, "id_transferred_products", "product_purchase_price", "product_total");
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

    addRow() {
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
                this.addRow();
                multicolumnDropdownShip(`#id_transferred_products-${this.formNum - 1}-product_name`);
                updateRowTotal(this.formNum - 1,"id_transferred_products", "product_purchase_price", "product_total");
                scrollToBottom('ship-wrapper');
            }
        });
    }

       updateTotalSum() {
        this.receivedProductsTable.addEventListener('change', () => {
            let documentTotalSum = totalSum(this.formNum, "id_total_sum", "id_transferred_products", "product_total");
        });
    }

}






document.addEventListener('DOMContentLoaded', function () {
    const shippedProductsFormManager = new ShippedProductsFormManager();
    shippedProductsFormManager.attachBlurEventToLastField();
    initialShippedProductRowFunctions();
    saleEnterKeyBehavior();
    updateProductsDropdown(
        'id_shipping_department',
        'id_transferred_products',
        productNamesDictShip
    );
});