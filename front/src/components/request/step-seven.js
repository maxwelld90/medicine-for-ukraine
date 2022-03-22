import React, { useContext, useEffect, useState } from "react";
import { useTranslation } from "react-i18next";

import ImageLoader from "../imageLoader";
import { RequestContext } from "./request-context";
import { fetchAddress } from "../../api";

// Check if each store has at least one file
const isValidRequest = (request) => {
  return Object.values(request.stores).every((s) => {
    return s.screenshots && s.screenshots.length > 0;
  });
};

export default function StepSeven({ onNext }) {
  const [request] = useContext(RequestContext);
  const [isCompletedStep, setIsCompletedStep] = useState(false);
  const [t] = useTranslation(["translation", "common"]);

  const getOnUploadHandler = (index) => {
    return (files) => {
      request.stores[index].screenshots = files;
      setIsCompletedStep(isValidRequest(request));
    };
  };

  const [error, setError] = useState(null);
  const [isLoaded, setIsLoaded] = useState(false);
  const [address, setAddress] = useState({});

  useEffect(() => {
    fetchAddress(request.countryCode).then(
      (result) => {
        setAddress(result);
        request.addressId = result.id;
        setIsLoaded(true);
      },
      (error) => {
        setIsLoaded(true);
        setError(error);
      }
    );
  }, [request.countryCode]);

  if (error) {
    return <div>Error: {error.message}</div>;
  } else if (!isLoaded) {
    return <div>Loading...</div>;
  }

  return (
    <div>
      <h1 className="multilingual en">
        {t("common:STEP_SEVEN.TITLE")}
        <span>7/7</span>
      </h1>

      <p className="multilingual en">{t("common:STEP_SEVEN.FIRST_LINE")}</p>

      <div className="address-text">{address.address_lines}</div>

      <p className="multilingual en">{t("common:STEP_SEVEN.SECOND_LINE")}</p>

      <ul className={"file-list"}>
        {Object.entries(request.stores).map(([i, store]) => (
          <li key={i}>
            <span>{store.store_domain}</span>
            <ImageLoader
              onUpload={getOnUploadHandler(i)}
              existingFiles={store.screenshots}
            />
          </li>
        ))}
      </ul>

      <div className={"btn-wrap"}>
        <button disabled={!isCompletedStep} onClick={onNext}>
          {t("common:NEXT_BUTTON")}
        </button>
      </div>
    </div>
  );
}
