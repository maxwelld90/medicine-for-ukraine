import React, {useContext, useEffect, useState} from "react";
import { useTranslation } from "react-i18next";

import { RequestContext } from "./request-context";

//import "./request.css";

const isValidEmail = (email) => {
    return (/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/.test(email));
}

export default function StepOne({ onNext, onBack }) {
  const [isCompletedStep, setIsCompletedStep] = useState(false);
  const [request, setRequest] = useContext(RequestContext);
  const [t] = useTranslation(["translation", "common"]);

  const onEmailChange = (event) => {
    setRequest({ ...request, contact: event.target.value });
  };

  const isValidRequest = (request) => {
    return request.contact && isValidEmail(request.contact);
  }

  const handleKeypress = (event) => {
    console.log(event.keyCode)
    if (event.charCode === 13 && isCompletedStep) {
      onNext();
    }
  }

  useEffect(() => {
    setIsCompletedStep(isValidRequest(request));
  }, [request])

  return (
    <div>
      <h1 className="multilingual en">
        {t("common:STEP_ONE.TITLE")}
        <span>1/7</span>
      </h1>

      <p className="multilingual en">{t("common:STEP_ONE.FIRST_LINE")}</p>
      
      <p>{t("common:STEP_ONE.SECOND_LINE")}</p>

      <p className="form-element">
        <input
          type="text"
          id="email"
          placeholder={t("common:STEP_ONE.EMAIL_LABEL")}
          value={request.contact}
          onChange={onEmailChange}
          onKeyPress={handleKeypress}
        />
      </p>

      <p className="direction">
        {/* <button onClick={onBack}>
              {t("common:PREV_BUTTON")}
        </button> */}
        <button disabled={!isCompletedStep} onClick={onNext}>
          {t("common:NEXT_BUTTON")}
        </button>
      </p>
    </div>

  );
}
