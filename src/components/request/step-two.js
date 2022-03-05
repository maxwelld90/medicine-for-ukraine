import React, { useContext } from "react";
import { RequestContext } from "./request-context";
import { useTranslation } from "react-i18next";

export default function StepTwo() {
  const [request, setRequest] = useContext(RequestContext);
  const [t] = useTranslation(["translation", "common"]);

  const publicFolder = process.env.PUBLIC_URL;

  const countries = [
    { name: "Poland", flag_url: `${publicFolder}img/flags/pl.svg` },
    { name: "Spain", flag_url: `${publicFolder}img/flags/es.svg` },
  ];

  const handleSelect = (country) => {
    setRequest({...request, country: country})
  };

  return (
    <div>
      <h1 className="multilingual en">
        {t("common:STEP_TWO.TITLE")}
        <span>2/9</span>
      </h1>

      <p className="multilingual en">{t("common:STEP_TWO.FIRST_LINE")}</p>

      <div>
        <ul className="item-list countries">
          {countries.map((country, i) => (
            <li key={i} onClick={() => handleSelect(country.name)}>
              <img src={country.flag_url} alt="Flag of Spain" />
              <span>{country.name}</span>
            </li>
          ))}
        </ul>

        <p className="multilingual en">
          Select the country you wish to send items to, and click/tap continue.
        </p>
      </div>
    </div>
  );
}
