function isProduction(){
    if (process.env.REACT_APP_MEDICINE_ENVIRONMENT === 'production') {
        return true;
    }

    return false;
}

function getStaticPath(path) {
    if (isProduction()) {
        return process.env.REACT_APP_STATIC_ROOT + '/' + path;
    }

    return '/static/' + path;
}

function getLanguagesObject(languages) {
    let returnArray = [];
    let currentDefault = window.localStorage.getItem('MEDICINE-LANGUAGE');
    let setLanguage = false;

    for (let language in languages) {
        let isActive = false;

        if (currentDefault === language) {
            isActive = true;
            setLanguage = true;
        }

        returnArray.push({
            name: language,
            isActive: isActive,
        });
    }

    if (!setLanguage) {
        for (let language of returnArray) {
            if (language.name === 'en') {
                language.isActive = true;
            }
        }
    }

    return returnArray;
}

export {
    isProduction,
    getStaticPath,
    getLanguagesObject
}