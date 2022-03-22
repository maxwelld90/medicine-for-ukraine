import React, { useState } from "react";
import { Route, Routes } from "react-router-dom";

import About from "./components/about";
import Request from "./components/request/index";
import ProgressBar from './components/progressBar';

import i18n from "./i18n";
import "./app.css";

import availableLanguages from './LANGUAGES.json';
import {getStaticPath, getLanguagesObject} from "./helpers";

function App() {
  const [step, setStep] = useState(null);
  const [languages, setLanguage] = useState(getLanguagesObject(availableLanguages));

  const publicFolder = process.env.PUBLIC_URL;

  const changeLanguageOnClick = (language) => {
    i18n.changeLanguage(language);

    window.localStorage.setItem('MEDICINE-LANGUAGE', language);

    const newLanguageState = languages.map((lng) => {
      lng.isActive = lng.name === language;
      return lng;
    });
    setLanguage(newLanguageState);
  };

  const onStepChange = (step) => {
    setStep(step);
  };

  return (
    <div>
      <header>
        <ProgressBar currentStep={step} />
        <div className="container">
          <a href="https://medicineforukraine.org">
            <picture>
              <source
                srcSet={getStaticPath("/img/animated-dark.svg")}
                media="(prefers-color-scheme: dark)"
              />
              <img
                src={getStaticPath("/img/animated.svg")}
                alt="Medicine for Ukraine"
              />
            </picture>
          </a>
          <ul>
            {languages.map((language, i) => (
              <li key={i} onClick={() => changeLanguageOnClick(language.name)}>
                <span
                  className={`multilingual-selector ${
                    language.isActive ? "selected" : ""
                  }`}
                >
                  {language.name.toUpperCase()}
                </span>
              </li>
            ))}
          </ul>
        </div>
      </header>
      <main>
        <div className="container">
          <div className="basic-router">
            <Routes>
              <Route path="/" element={<About />} />
              <Route
                path="/request"
                element={<Request onStepChange={onStepChange} />}
              />
            </Routes>
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;
