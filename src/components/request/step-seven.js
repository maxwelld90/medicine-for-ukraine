import React, { useEffect } from "react";
import { useTranslation } from "react-i18next";

export default function StepSix({onComplete}) {
  const [t] = useTranslation(["translation", "common"]);

  useEffect(() => {
    typeof onComplete === 'function' && onComplete()
  },[onComplete])

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
    </div>
  );
}
