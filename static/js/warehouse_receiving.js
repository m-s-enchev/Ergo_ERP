

let productNamesDictAll= {};


function twoColumnDropdown(selector) {
    let productNames = Object.keys(productNamesDictAll);
    $(selector).autocomplete({
        source: productNames,
        select: function(event, ui) {
            let idPrefix = this.id.substring(0, this.id.lastIndexOf("-") + 1);
            let details = productNamesDictAll[ui.item.value];
            $(`#${idPrefix}product_unit`).val(details[1]);
            return false;
        },
        open: function() {
        let dropdownWidth = 1.02*getElementsWidth([
            '#id_transferred_products-0-product_name',
            '#id_transferred_products-0-product_quantity',
            '#id_transferred_products-0-product_unit',
        ]);
        $(this).autocomplete("widget").css({
            "width": dropdownWidth + "px"
        });
        }

    }).autocomplete("instance")._renderItem = function(ul, item) {
        let details = productNamesDictAll[item.value];
        let label = `<div class="products-dropdown">
                                <span>${item.value}</span>
                                <span>${details[1]}</span>
                            </div>`;
        return $("<li>")
            .append(`${label}`)
            .appendTo(ul);
    };
}






function initialReceiveProductRowFunctions () {
    const productForms = document.querySelectorAll(".product-form");
    let numberOfRows = productForms.length;
    fetchProductsAll().then(() => {
        for (let index = 0; index < numberOfRows; index++) {
            twoColumnDropdown(`#id_transferred_products-${index}-product_name`);
            get_purchase_price(index, "id_transferred_products", "product_purchase_price");
            updateRowTotal(index, "id_transferred_products", "product_purchase_price", "product_value");
        }
    });
}


function receiveEnterKeyBehavior() {
    const tableBodyContainer = document.querySelector("#received-products tbody");
    tableBodyContainer.addEventListener('keydown', function (e) {
        if (e.target.tagName === 'INPUT' && e.key === 'Enter') {
            e.preventDefault();

            const inputs = Array.from(tableBodyContainer.querySelectorAll('input'));
            const currentIndex = inputs.indexOf(e.target);
            const nextIndex = currentIndex + 1;
            if (nextIndex < inputs.length) {
                inputs[nextIndex].focus();
            } else {
                inputs[0].focus();
            }
        }
    });
}


class ReceivedProductsFormManager {
    constructor() {
        this.container = document.querySelector("#received-products tbody");
        this.totalForms = document.querySelector("#id_transferred_products-TOTAL_FORMS");
        this.productForms = document.querySelectorAll(".product-form");
        this.formNum = this.productForms.length;
        this.receivedProductsTable = document.getElementById('received-products');
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
                twoColumnDropdown(`#id_transferred_products-${this.formNum - 1}-product_name`);
                // getProductPrice(this.formNum - 1, "id_sold_products", "product_price_before_tax", "product_price", "product_retail_price");
                updateRowTotal(this.formNum - 1,"id_transferred_products", "product_purchase_price", "product_value");
                scrollToBottom('receive-wrapper');
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
    const receivedProductsFormManager = new ReceivedProductsFormManager();
    receivedProductsFormManager.attachBlurEventToLastField();
    initialReceiveProductRowFunctions();
    receiveEnterKeyBehavior();
});