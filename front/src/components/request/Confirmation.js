import React, { useContext, useEffect, useState } from "react";
import { useTranslation } from "react-i18next";

import ImageLoader from "../imageLoader";
import { RequestContext } from "./requestContext";
import StepDescription from "./components/StepDescription";
import StepNavigation from "./components/StepNavigation";

import Loader from "../loader";
import Error from "../error";

import { fetchAddress } from "../../api";

// Check if each store has at least one file
const isValidRequest = (request) => {
  return Object.values(request.stores).every((s) => {
    return s.screenshots && s.screenshots.length > 0;
  });
};

export default function Confirmation({ onNext, onBack }) {
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
    fetchAddress(request.recipientId).then(
      ({warehouse_address}) => {
        setAddress(warehouse_address.address);
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
          <StepDescription
            step="5/5"
            title={t("common:STEP_FIVE.TITLE")}
            firstLine={t("common:STEP_FIVE.FIRST_LINE")}
          />

          <div className="address-text">{address}</div>

          <h2>Upload Screenshot(s)</h2>

          <p>{t("common:STEP_FIVE.SECOND_LINE")}</p>

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

          <StepNavigation
            nextButtonTitle={t("common:FINAL_BUTTON")}
            isNextButtonEnabled={isCompletedStep}
            onClickNext={onNext}
          />
        </div>
      )}
    </>
  );
}
