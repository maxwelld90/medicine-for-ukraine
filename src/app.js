import React, { useState } from "react";
import { Route, Routes } from "react-router-dom";

import About from "./components/about";
import Request from "./components/request/index";

import i18n from "./i18n";
import "./app.css";

function App() {
  const [step, setStep] = useState(null);
  const [languages, setLanguage] = useState([
    { name: "en", isActive: true },
    { name: "pl", isActive: false },
    { name: "es", isActive: false },
    { name: "de", isActive: false },
  ]);

  const publicFolder = process.env.PUBLIC_URL;

  const changeLanguageOnClick = (language) => {
    i18n.changeLanguage(language);

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
        <div className="container">
          <a href="https://medicineforukraine.org">
            <picture>
              <source
                srcSet={publicFolder + "img/animated-dark.svg"}
                media="(prefers-color-scheme: dark)"
              />
              <img
                src={publicFolder + "img/animated.svg"}
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
