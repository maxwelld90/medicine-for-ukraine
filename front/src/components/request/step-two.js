import React, { useContext, useEffect, useState } from "react";
import { RequestContext } from "./request-context";
import { useTranslation } from "react-i18next";
import { fetchCountries } from "../../api";
import Loader from "../loader";
import Error from "../error";

export default function StepTwo({ onNext, onBack }) {
  const [request, setRequest] = useContext(RequestContext);
  const [t] = useTranslation(["translation", "common"]);

  const handleSelect = (country) => {
    setRequest({ ...request, countryCode: country.code });

    if (typeof onNext === "function") {
      onNext();
    }
  };

  const [error, setError] = useState(null);
  const [isLoaded, setIsLoaded] = useState(false);
  const [countries, setCountries] = useState([]);

  useEffect(() => {
    fetchCountries().then(
      (result) => {
        setIsLoaded(true);
        setCountries(result);
      },
      (error) => {
        setIsLoaded(true);
        setError(error);
      }
    );
  }, []);

  return (
    <>
      {error && <Error />}
      {!isLoaded && <Loader />}
      {!error && isLoaded && (
        <div>
          <h1 className="multilingual en">
            {t("common:STEP_TWO.TITLE")}
            <span>2/7</span>
          </h1>

          <p className="multilingual en">{t("common:STEP_TWO.FIRST_LINE")}</p>

          <ul className="item-list countries">
            {countries.map((country, i) => (
              <li
                key={i}
                onClick={() => handleSelect(country)}
                className={
                  country.code === request.countryCode ? "selected" : ""
                }
              >
                <img src={country.flag_url} alt={`Flag of ${country.name}`} />
                <span>{country.name}</span>
              </li>
            ))}
          </ul>
        </div>
      )}
      <button className={"button-back"} onClick={onBack}>
        {t("common:PREV_BUTTON")}
      </button>
    </>
  );
}
