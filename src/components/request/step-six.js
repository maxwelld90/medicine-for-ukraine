import React, { useContext, useEffect } from "react";
import { useTranslation } from "react-i18next";

import ImageLoader from "../imageLoader";
import { RequestContext } from "./request-context";

// Check if each store has at least one file
const isValidRequest = (request) => {
  return Object.values(request.stores).every((s) => {
    return s.files && s.files.length > 0;
  });
}

export default function StepSix({onComplete}) {
  const [request, setRequest] = useContext(RequestContext);
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

  // cache handlers to prevent infinity loop
  const uploadHandlers = {};
  const getOnUploadHandler = (index) => {
    if (!uploadHandlers[index]) {
      const cb = (files) => {
        // Add new files to store
        const currentStore = {
          ...request.stores[index],
          files: files,
        };
        // Update store at request object
        setRequest({
          ...request,
          stores: {
            ...request.stores,
            [index]: currentStore
          }
        });
      };
      uploadHandlers[index] = cb
    }
    return uploadHandlers[index];
  }

  useEffect(() => {
    console.log('request:', request); // for debug
    if (isValidRequest(request) && typeof onComplete === 'function'){
      onComplete();
    }
  }, [request, onComplete]);

  const stores = JSON.parse(JSON.stringify(request.stores));

  return (
    <div>
      <h1 className="multilingual en">
        {t("common:STEP_SIX.TITLE")}
        <span>6/6</span>
      </h1>

      <p className="multilingual en">{t("common:STEP_SIX.FIRST_LINE")}</p>

      <div>
        <div>{storageAddress.street}</div>
        <div>{storageAddress.postalCode} {storageAddress.city}</div>
        <div>{storageAddress.country}</div>
      </div>

      <p className="multilingual en">{t("common:STEP_SIX.SECOND_LINE")}</p>

      <ul className={'file-list'}>
        {Object.entries(stores).map(([i, storeItem]) => (
          <li key={i}>
            <span>{storeItem.store.name}</span>
            <ImageLoader onUpload={getOnUploadHandler(i)}/>
          </li>
        ))}
      </ul>
    </div>
  );
}
