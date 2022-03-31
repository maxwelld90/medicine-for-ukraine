import React, { useContext, useEffect, useState } from "react";
import { useTranslation } from "react-i18next";
import { saveRequest } from "../../api";
import { RequestContext } from "./request-context";
import Loader from "../loader";
import Error from "../error";

export default function StepSix({ onNext, onBack }) {
  const [request] = useContext(RequestContext);
  const [t] = useTranslation(["translation", "common"]);

  const [error, setError] = useState(null);
  const [isLoaded, setIsLoaded] = useState(false);

  useEffect(() => {
    saveRequest(request).then(
      () => {
        setIsLoaded(true);
      },
      (error) => {
        setIsLoaded(true);
        setError(error);
      }
    );
  }, [request]);

  return (
    <>
      {error && <Error />}
      {!isLoaded && <Loader />}
      {!error && isLoaded && (
        <div>
          <h1 className="multilingual en">{t("common:STEP_EIGHT.TITLE")}</h1>

          <p className="multilingual en">{t("common:STEP_EIGHT.FIRST_LINE")}</p>

          <p className="multilingual en">
            {t("common:STEP_EIGHT.SECOND_LINE")}
          </p>
        </div>
      )}
      <div className={"btn-wrap"}>
        <button className={"button-back"} onClick={onBack}>
          {t("common:PREV_BUTTON")}
        </button>
        <button onClick={onNext}>
          {t("common:STEP_EIGHT.RESTART_PROCESS")}
        </button>
      </div>
    </>
  );
}
