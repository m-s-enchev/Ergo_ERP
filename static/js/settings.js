
// Auto scroll to section when nav button is clicked
let navButtonSale = document.getElementById('sale-settings-nav')

function scrollToSection (sectionId) {
    let sectionElement = document.getElementById(sectionId);
    const scrollOffset = sectionElement.offsetTop - window.innerHeight/9;
    window.scrollTo({ top: scrollOffset, behavior: 'smooth' });
}
navButtonSale.addEventListener('click', () => { scrollToSection('sale-settings') });