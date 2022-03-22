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

      <div className={'btn-wrap'}>
        <button onClick={() => onBack(3)}>
          {t("common:STEP_SIX.BACK_BUTTON")}
        </button>
      </div>
      <div className={'btn-wrap'}>
        <button onClick={onNext}>
          {t("common:STEP_SIX.NEXT_BUTTON")}
        </button>
      </div>
    </div>
  )
}