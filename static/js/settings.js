function scrollToSection (section) {
    const scrollOffset = section.offsetTop - window.innerHeight/9;
    window.scrollTo({ top: scrollOffset, behavior: 'smooth' });
}

/** Scroll to s section of settings form when corresponding nav button is clicked*/
function settingsNavigation () {
    const navButtons = document.querySelectorAll('#settings-navigation button');
    const navSections = document.querySelectorAll('#settings-list form section');
    for (let i=0; i<navButtons.length; i++) {
        navButtons[i].addEventListener('click', () => { scrollToSection(navSections[i]) })
    }
}

document.addEventListener("DOMContentLoaded", () => {settingsNavigation()})