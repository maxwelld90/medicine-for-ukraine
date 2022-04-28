import React, { useState } from "react";
import { Route, Routes } from "react-router-dom";

import Request from "./components/request/index";
import Header from "./components/header";
import Footer from "./components/footer";

import i18n from "./i18n";
import "./app.css";

import availableLanguages from "./LANGUAGES.json";
import { getLanguagesObject } from "./helpers";

function App() {
  const [step, setStep] = useState(null);
  const [currentLanguage, setCurrentLanguage] = useState(i18n.language);
  const [languages, setLanguages] = useState(
    getLanguagesObject(availableLanguages)
  );

  const changeLanguageOnClick = (language) => {
    i18n.changeLanguage(language);

    window.localStorage.setItem("MEDICINE-LANGUAGE", language);

    const newLanguageState = languages.map((lng) => {
      lng.isActive = lng.name === language;
      return lng;
    });

    setCurrentLanguage(language)
    setLanguages(newLanguageState);
  };

  const onStepChange = (step) => {
    setStep(step);
  };

  return (
    <div>
      <Header
        step={step}
        languages={languages}
        changeLanguageOnClick={changeLanguageOnClick}
      />

      <main>
        <div className="container">
          <div className="basic-router">
            <Routes>
              <Route
                path="/request/"
                element={<Request onStepChange={onStepChange} language={currentLanguage}/>}
              />
            </Routes>
          </div>
        </div>
      </main>

      <Footer />
    </div>
  );
}

export default App;
