import React from "react";
import {useTranslation} from "react-i18next";


export default function StepSix({onNext, onBack}) {
  const [t] = useTranslation(["translation", "common"]);

  return (
    <div>
      <h1>
        {t("common:STEP_SIX.TITLE")}
        <span>6/7</span>
      </h1>

      <p>
        {t("common:STEP_SIX.FIRST_LINE")}
      </p>

      <p className="direction">
        <button className="one-per-line" onClick={() => onBack(3)}>
          {t("common:STEP_SIX.BACK_BUTTON")}
        </button>
        <button className="one-per-line" onClick={onNext}>
          {t("common:STEP_SIX.NEXT_BUTTON")}
        </button>
      </p>
    </div>
  )
}