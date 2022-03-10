import React, { useContext, useEffect } from "react";
import { RequestContext } from "./request-context";
import { useTranslation } from "react-i18next";

export default function StepThree({ onComplete }) {
  const [request, setRequest] = useContext(RequestContext);
  const [t] = useTranslation(["translation", "common"]);

  const selectDonation = (type) => {
    setRequest({ ...request, donationType: type });
  };

  useEffect(() => {
    if (request.donationType && typeof onComplete === "function") {
      onComplete();
    }
  }, [request, onComplete]);

  return (
    <div>
      <h1 className="multilingual en">
        {t("common:STEP_THREE.TITLE")}
        <span>36</span>
      </h1>

      <p className="multilingual en">{t("common:STEP_THREE.FIRST_LINE")}</p>

      <ul className="item-list">
        <li onClick={() => selectDonation("meds")}
        className={"meds" === request.donationType ? 'selected' : ''}>
          {t("common:STEP_THREE.MED_EQUIPMENT_LABEL")}
        </li>
        <li onClick={() => selectDonation("other")}
        className={"other" === request.donationType ? 'selected' : ''}>
          {t("common:STEP_THREE.OTHER_EQUIPMENT_LABEL")}
        </li>
      </ul>
    </div>
  );
}
