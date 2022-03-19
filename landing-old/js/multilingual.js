document.addEventListener('DOMContentLoaded', function() {
    let languages = document.querySelectorAll('.multilingual-selector');

    for (let languageSelector of languages) {
        languageSelector.addEventListener('click', selectLanguageClick);
    }

    if (window.localStorage.getItem('selectedLanguage')) {
        selectLanguage(window.localStorage.getItem('selectedLanguage'));
        return;
    }

    selectLanguage('EN');
});

function hideAllLanguages() {
    let multilingualElements = document.querySelectorAll('.multilingual');

    for (let element of multilingualElements) {
        element.style.display = 'none';
    }
}

function selectLanguageClick(event) {
    let selectedLanguage = event.target.getAttribute('data-language');

    if (!selectedLanguage) {
        return;
    }

    selectLanguage(selectedLanguage);
}

function selectLanguage(selectedLanguage) {
    let languages = document.querySelectorAll('.multilingual-selector');

    for (let element of languages) {
        let language = element.getAttribute('data-language');

        element.classList.remove('selected');

        if (language.toLowerCase() == selectedLanguage.toLowerCase()) {
            element.classList.add('selected');
        }
    }

    hideAllLanguages();

    let multilingualElements = document.querySelectorAll('.multilingual.' + selectedLanguage.toLowerCase());

    for (let element of multilingualElements) {
        element.style.display = 'inherit';
    }

    window.localStorage.setItem('selectedLanguage', selectedLanguage);
}