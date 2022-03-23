import React from "react";
import ProgressBar from "./progressBar";
import {getStaticPath, getCurrentLanguage} from "../helpers";

export default function Header({step, languages, changeLanguageOnClick}) {
  return (
    <header>
        <ProgressBar currentStep={step} />
        <div className="container">
            <a href={`/${getCurrentLanguage()}/`}>
                <picture>
                <source
                    srcSet={getStaticPath("/img/animated-dark.svg")}
                    media="(prefers-color-scheme: dark)" />
                <img
                    src={getStaticPath("/img/animated.svg")}
                    alt="Medicine for Ukraine" />
                </picture>
            </a>
            <div className="links-container">
                <ul className="languages">
                {languages.map((language, i) => (
                    <li key={i}>
                        <a
                            onClick={() => changeLanguageOnClick(language.name)}
                            className={`multilingual-selector ${language.isActive ? ' selected' : ''}`}>
                            {language.name.toUpperCase()}
                        </a>
                    </li>
                ))}
                </ul>
            </div>
        </div>
    </header>);
}