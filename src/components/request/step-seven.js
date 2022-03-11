import React, {useContext, useEffect, useState} from "react";
import {useTranslation} from "react-i18next";

import ImageLoader from "../imageLoader";
import {RequestContext} from "./request-context";

// Check if each store has at least one file
const isValidRequest = (request) => {
  return Object.values(request.stores).every((s) => {
    return s.screenshots && s.screenshots.length > 0;
  });
}

export default function StepSeven({onNext}) {
  const [request] = useContext(RequestContext);
  console.log('request:', request);
  const [isCompletedStep, setIsCompletedStep] = useState(false);
  const [t] = useTranslation(["translation", "common"]);

  //@TODO fetch from API
  const storageAddress = {
    street: "22 Rue du Grenier Saint-Lazare",
    postalCode: "75003",
    city: "Paris",
    countryCode: "FRA",
    country: "France",
    text: "22 Rue du Grenier Saint-Lazare\n75003 Paris\nFrance",
  };

  const getOnUploadHandler = (index) => {
    return (files) => {
      request.stores[index].screenshots = files;
      setIsCompletedStep(isValidRequest(request));
    };
  }

  return (
    <div>
      <h1 className="multilingual en">
        {t("common:STEP_SEVEN.TITLE")}
        <span>7/7</span>
      </h1>

      <p className="multilingual en">{t("common:STEP_SEVEN.FIRST_LINE")}</p>

      <div>
        <div>{storageAddress.street}</div>
        <div>{storageAddress.postalCode} {storageAddress.city}</div>
        <div>{storageAddress.country}</div>
      </div>

      <p className="multilingual en">{t("common:STEP_SEVEN.SECOND_LINE")}</p>

      <ul className={'file-list'}>
        {Object.entries(request.stores).map(([i, store]) => (
          <li key={i}>
            <span>{store.store_domain}</span>
            <ImageLoader onUpload={getOnUploadHandler(i)}/>
          </li>
        ))}
      </ul>

      <div className={'btn-wrap'}>
        <button disabled={!isCompletedStep} onClick={onNext}>
          {t("common:NEXT_BUTTON")}
        </button>
      </div>
    </div>
  );
}
