import React, { useState } from "react";
import { Route, Routes } from "react-router-dom";

import Request from "./components/request/index";
import Header from "./components/header";
import Footer from "./components/footer";

import i18n from "./i18n";
// import "./app.css";

import availableLanguages from './LANGUAGES.json';
import {getStaticPath, getLanguagesObject, getHeaderLogoLink} from "./helpers";

function App() {
  const [step, setStep] = useState(null);
  const [languages, setLanguage] = useState(getLanguagesObject(availableLanguages));

  const publicFolder = process.env.PUBLIC_URL;

  const changeLanguageOnClick = (language) => {
    i18n.changeLanguage(language);

    window.localStorage.setItem('MEDICINE-LANGUAGE', language);

    const newLanguageState = languages.map((lng) => {
      lng.isActive = (lng.name === language);
      return lng;
    });

    setLanguage(newLanguageState);
  };

  const onStepChange = (step) => {
    setStep(step);
  };

  return (
    <div>
      <Header step={step} languages={languages} changeLanguageOnClick={changeLanguageOnClick} />

      <main>
        <div className="container">
          <div className="basic-router">
            <Routes>
              <Route
                path="/request"
                element={<Request onStepChange={onStepChange} />}
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
