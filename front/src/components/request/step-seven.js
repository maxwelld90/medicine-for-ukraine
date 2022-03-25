import React, { useContext, useEffect, useState } from "react";
import { useTranslation } from "react-i18next";

import ImageLoader from "../imageLoader";
import { RequestContext } from "./request-context";
import { fetchAddress } from "../../api";
import Loader from "../loader";
import Error from "../error";

// Check if each store has at least one file
const isValidRequest = (request) => {
  return Object.values(request.stores).every((s) => {
    return s.screenshots && s.screenshots.length > 0;
  });
};

export default function StepSeven({ onNext, onBack }) {
  const [request] = useContext(RequestContext);
  const [isCompletedStep, setIsCompletedStep] = useState(false);
  const [t] = useTranslation(["translation", "common"]);
  const [error, setError] = useState(null);
  const [isLoaded, setIsLoaded] = useState(false);
  const [address, setAddress] = useState({});

  const getOnUploadHandler = (index) => {
    return (files) => {
      request.stores[index].screenshots = files;
      setIsCompletedStep(isValidRequest(request));
    };
  };

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

  return (
    <>
      {error && <Error />}
      {!isLoaded && <Loader />}
      {!error && isLoaded && (
        <div>
          <h1>
            {t("common:STEP_SEVEN.TITLE")}
            <span>7/7</span>
          </h1>

          <p>{t("common:STEP_SEVEN.FIRST_LINE")}</p>

          <div className="address-text">{address.address_lines}</div>

          <h2>Upload Screenshot(s)</h2>

          <p>
            {t("common:STEP_SEVEN.SECOND_LINE")}
          </p>

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

          <p className="direction">
            {/* <button onClick={onBack}>
              {t("common:PREV_BUTTON")}
            </button> */}
            <button disabled={!isCompletedStep} onClick={onNext}>
              {t("common:FINAL_BUTTON")}
            </button>
          </p>
        </div>
      )}
    </>
  );
}
