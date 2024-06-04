function removeValue(...fieldIDs) {
    const resetButton = document.getElementById('reset-button');
    resetButton.addEventListener('click', () => {
        for (let id of fieldIDs) {
            let field = document.getElementById(id);
            if (field) {
                if (field.tagName === 'SELECT') {
                    const selected = field.selectedIndex
                    field.children[selected].removeAttribute('selected')
                } else {
                    field.removeAttribute("value");
                }
            }
        }
    });
}


document.addEventListener('DOMContentLoaded', () => {
    removeValue(
        'date',
        'operator',
        'type',
        'shipper',
        'search-query'
    )
})