import React, { useContext, useEffect, useState } from "react";
import { useTranslation } from "react-i18next";
import { saveRequest } from "../../api";
import { RequestContext } from "./request-context";
import StepDescription from "./components/StepDescription";
import StepNavigation from "./components/StepNavigation";
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
        <StepDescription
          title={t("common:STEP_SIX.TITLE")}
          firstLine={t("common:STEP_SIX.FIRST_LINE")}
          secondLine={t("common:STEP_SIX.SECOND_LINE")}
        />
      )}

      <StepNavigation
        prevButtonTitle={t("common:PREV_BUTTON")}
        onClickPrev={onBack}
        nextButtonTitle={t("common:RESTART_PROCESS")}
        onClickNext={onNext}
      />
    </>
  );
}
