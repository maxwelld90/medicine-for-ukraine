import React, { useContext } from "react";
import { RequestContext } from "./request-context";
import { useTranslation } from "react-i18next";

export default function StepThree({ onNext, onBack }) {
  const [request, setRequest] = useContext(RequestContext);
  const [t] = useTranslation(["translation", "common"]);

  const selectDonation = (type) => {
    setRequest({ ...request, donationType: type });
    if (typeof onNext === "function") {
      onNext();
    }
  };

  return (
    <div>
      <h1>
        {t("common:STEP_THREE.TITLE")}
        <span>3/7</span>
      </h1>

      <p>{t("common:STEP_THREE.FIRST_LINE")}</p>

      <ul className="item-list direction">
        <li
          onClick={() => selectDonation("meds")}
          className={"meds" === request.donationType ? "selected" : ""}
        >
          {t("common:STEP_THREE.MED_EQUIPMENT_LABEL")}
        </li>
        <li
          onClick={() => selectDonation("defence")}
          className={"defence" === request.donationType ? "selected" : ""}
        >
          {t("common:STEP_THREE.OTHER_EQUIPMENT_LABEL")}
        </li>
      </ul>

      <p className="direction">
        <button className={"button-back"} onClick={onBack}>
          {t("common:PREV_BUTTON")}
        </button>
      </p>
    </div>
  );
}
