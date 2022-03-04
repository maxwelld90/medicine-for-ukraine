import i18n from "i18next";
import { initReactI18next } from "react-i18next";
import Backend from "i18next-http-backend";
import LanguageDetector from "i18next-browser-languagedetector";

// the translations
// (tip move them in a JSON file and import them,
// or even better, manage them separated from your code: https://react.i18next.com/guides/multiple-translation-files)
const languages = ["en", "es"];

i18n
  /*
    load translation using http -> see /public/locales (i.e. https://github.com/i18next/react-i18next/tree/master/example/react/public/locales)
    learn more: https://github.com/i18next/i18next-http-backend
  */
  .use(Backend)
  /*
    detect user language
    learn more: https://github.com/i18next/i18next-browser-languageDetector
  */
  .use(LanguageDetector)
  .use(initReactI18next) // passes i18n down to react-i18next
  .init({
    lng: "en", // language to use, more information here: https://www.i18next.com/overview/configuration-options#languages-namespaces-resources
    // you can use the i18n.changeLanguage function to change the language manually: https://www.i18next.com/overview/api#changelanguage
    whitelist: languages,
    debug: true,
    interpolation: {
      escapeValue: false, // react already safes from xss
    },

    react: {
      useSuspense: false
    }
  });

export default i18n;
