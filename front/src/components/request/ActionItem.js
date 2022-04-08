import React from "react";
import { useTranslation } from "react-i18next";

import StepDescription from "./components/StepDescription";

export default function ActionItem({ onNext, onBack }) {
  const [t] = useTranslation(["translation", "common"]);

  return (
    <div>
      <StepDescription
        step="4/5"
        title={t("common:STEP_FOUR.TITLE")}
        firstLine={t("common:STEP_FOUR.FIRST_LINE")}
      />

      <p className="direction">
        <button className="one-per-line" onClick={() => onBack(2)}>
          {t("common:STEP_FOUR.BACK_BUTTON")}
        </button>
        <button className="one-per-line" onClick={onNext}>
          {t("common:STEP_FOUR.NEXT_BUTTON")}
        </button>
      </p>
    </div>
  );
}
