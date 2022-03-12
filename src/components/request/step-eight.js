import React, {useContext, useEffect, useState} from "react";
import { useTranslation } from "react-i18next";
import { saveRequest} from "../../api";
import { RequestContext } from "./request-context";

export default function StepEight({ onNext }) {
  const [request] = useContext(RequestContext);
  const [t] = useTranslation(["translation", "common"]);

  const [error, setError] = useState(null);
  const [isLoaded, setIsLoaded] = useState(false);

  useEffect( () => {
    saveRequest(request)
      .then(
        (_) => {
          setIsLoaded(true);
        },
        (error) => {
          setIsLoaded(true);
          setError(error);
        }
      )
  }, [request]);

  if (error) {
    return <div>Error: {error.message}</div>;
  } else if (!isLoaded) {
    return <div>Loading...</div>;
  }

  return (
    <div>
     <h1 className="multilingual en">
        {t("common:STEP_SEVEN.TITLE")}
      </h1>

      <p className="multilingual en">
        {t("common:STEP_SEVEN.FIRST_LINE")}
      </p>

      <p className="multilingual en">
        {t("common:STEP_SEVEN.SECOND_LINE")}
      </p>

      <div className={'btn-wrap'}>
        <button onClick={onNext}>
          {t("common:NEXT_BUTTON")}
        </button>
      </div>
    </div>
  );
}
