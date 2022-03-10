import "./app.css";
import { Route, Routes } from "react-router-dom";

import About from "./components/about";
import Request from "./components/request/index";

import i18n from "./i18n";

function App() {
  const publicFolder = process.env.PUBLIC_URL;

  const changeLanguageOnClick = (language) => {
    i18n.changeLanguage(language);
  }

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
            <li onClick={() => changeLanguageOnClick("en")}><a href="#" className="multilingual-selector selected" data-language="EN" className="selected">EN</a></li>
            <li onClick={() => changeLanguageOnClick("es")}><a href="#" className="multilingual-selector" data-language="ES">ES</a></li>
            <li onClick={() => changeLanguageOnClick("pl")}><a href="#" className="multilingual-selector" data-language="PL">PL</a></li>
            <li onClick={() => changeLanguageOnClick("de")}><a href="#" className="multilingual-selector" data-language="DE">DE</a></li>
          </ul>
        </div>
      </header>
      <main>
        <div className="container">
          <div className="basic-router">
            <Routes>
              <Route path="/" element={<About />} />
              <Route path="/request"  element={<Request />} />
            </Routes>
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;
