let productNamesDict = {};

function fetchAllProducts() {
    let url = `/common/products-dropdown-update/?department_id=${departmentId}`;
    return fetch(url)
        .then(response => response.json())
        .then(data => {
            productNamesDict = data;
            return productNamesDict;
        })
    }
}