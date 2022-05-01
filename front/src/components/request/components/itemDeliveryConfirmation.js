import React from "react";
import "./itemDeliveryConfirmation.css";
import { useTranslation } from "react-i18next";

export default function ItemDeliveryConfirmation({itemName, country}) {
    const [t] = useTranslation(["translation", "common"]);

  return (
    <p className="item-delivery-confirmation">
        <span className="item-name">
            <span>
                <span className="header">{t("common:SELECTED_ITEM")}</span>
                <span className="text">{itemName}</span>
            </span>
        </span>
        <span className="country">
            <span>
                <span className="code">{country.code.toUpperCase()}</span>
                <span className="text">{country.name}</span>
            </span>
            <img src={country.flag_url} alt={`Flag of ${country.name}`} />
        </span>
    </p>
  );
}