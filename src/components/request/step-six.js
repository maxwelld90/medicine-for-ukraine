import React, { useEffect } from "react";
import { useTranslation } from "react-i18next";

export default function StepSix({onComplete}) {
  const [t] = useTranslation(["translation", "common"]);

  const storageAddress = {
    street: "22 Rue du Grenier Saint-Lazare",
    postalCode: "75003",
    city: "Paris",
    countryCode: "FRA",
    country: "France",
    text: "22 Rue du Grenier Saint-Lazare\n75003 Paris\nFrance",
  };

  useEffect(() => {
    typeof onComplete === 'function' && onComplete()
  },[onComplete])

  return (
    <div>
      <h1 className="multilingual en">
        {t("common:STEP_SIX.TITLE")}
        <span>6/6</span>
      </h1>

      <p className="multilingual en">{t("common:STEP_SIX.FIRST_LINE")}</p>

      <div>
        <div>{storageAddress.street}</div>
        <div>{storageAddress.postalCode} {storageAddress.city}</div>
        <div>{storageAddress.country}</div>
      </div>

      <p className="multilingual en">{t("common:STEP_SIX.SECOND_LINE")}</p>

    </div>
  );
}
