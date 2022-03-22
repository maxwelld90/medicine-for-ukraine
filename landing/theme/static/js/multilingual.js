document.addEventListener("DOMContentLoaded", function() {
    let languageButtons = document.querySelectorAll('.multilingual-selector');

    if (SELECTED_LANGUAGE) {
        window.localStorage.setItem('MEDICINE-LANGUAGE', SELECTED_LANGUAGE);
    }
});