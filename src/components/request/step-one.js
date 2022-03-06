import React, { useContext } from "react";
import { useTranslation } from "react-i18next";

import { RequestContext } from "./request-context";

import "./request.css";

export default function StepOne({onComplete}) {
  const [request, setRequest] = useContext(RequestContext);
  const [t] = useTranslation(["translation", "common"]);

  const onEmailChange = (event) => {
    setRequest({ ...request, contact: event.target.value });

    if(event.target.value) {
      onComplete();
    }
  };

  return (
    <div>
      <h1 className="multilingual en">
        {t("common:STEP_ONE.TITLE")}
        <span>1/6</span>
      </h1>

      <p className="multilingual en">{t("common:STEP_ONE.FIRST_LINE")}</p>
      <p>{t("common:STEP_ONE.SECOND_LINE")}</p>
      <p className="form-element">
        <input
          type="text"
          id="email"
          placeholder={t("common:STEP_ONE.EMAIL_LABEL")}
          onChange={onEmailChange}
        />
      </p>
    </div>
  );
}
