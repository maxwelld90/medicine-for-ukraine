const isProduction =
  process.env.REACT_APP_MEDICINE_ENVIRONMENT === "production";

const resourcesPrefix = isProduction
  ? process.env.REACT_APP_STATIC_ROOT
  : "/static";

function getStaticPath(path) {
  return `${resourcesPrefix}/${path}`;
}

function getLanguagesObject(languages) {
  let returnArray = [];
  let currentDefault = window.localStorage.getItem("MEDICINE-LANGUAGE");
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
      if (language.name === "en") {
        language.isActive = true;
      }
    }
  }

  return returnArray;
}

function getCurrentLanguage() {
  let currentDefault = window.localStorage.getItem("MEDICINE-LANGUAGE");

  if (currentDefault) {
    return currentDefault;
  }

  return "en";
}

function getHeaderLogoLink() {
  let currentDefault = window.localStorage.getItem("MEDICINE-LANGUAGE");

  if (currentDefault) {
    return "/" + currentDefault + "/";
  }

  return "/en/";
}

export {
  isProduction,
  getStaticPath,
  getLanguagesObject,
  getCurrentLanguage,
  getHeaderLogoLink,
};
