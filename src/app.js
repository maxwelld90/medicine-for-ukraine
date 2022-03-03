import "./app.css";
import { Route, Routes } from "react-router-dom";

import About from "./components/about";
import Request from "./components/request/index";


function App() {
  const publicFolder = process.env.PUBLIC_URL;

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
            {/* <li><a href="#" className="selected">EN</a></li>
          <li><a href="#">UA</a></li>
          <li><a href="#">DE</a></li> */}
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
