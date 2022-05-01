import React, { useContext } from "react";
import { useAsync } from "react-use";
import { useTranslation } from "react-i18next";

import { fetchRecipients } from "../../api";
import Content from "../Content";

import { RequestContext } from "./requestContext";
import StepNavigation from "./components/StepNavigation";
import StepDescription from "./components/StepDescription";

import './request.css';

export default function Recipients({ onNext, onBack, language }) {
  const { loading, error, value } = useAsync(fetchRecipients);

  const [request, setRequest] = useContext(RequestContext);
  const [t] = useTranslation(["translation", "common"]);

  const handleSelect = (recipient) => {
    setRequest({ ...request, recipientId: recipient.recipient_id });

    typeof onNext === "function" && onNext();
  };

  return (
    <Content error={error} loading={loading}>
      {() => (
        <div>
          <StepDescription
            step="1/5"
            title={t("common:STEP_ONE.TITLE")}
            firstLine={t("common:STEP_ONE.FIRST_LINE")}
            secondLine={t("common:STEP_ONE.SECOND_LINE")}
          />

          <ul className="item-list recipients direction">
            {value.map((recipient, i) => (
              <li
                key={i}
                onClick={() => handleSelect(recipient)}
                // className={
                //   recipient.code === request.countryCode ? "selected" : ""
                // }
              >
                <span className="text">
                  <span className="name">{recipient.names[language] || recipient.names["default"]}</span>
                  <span className="warehouse">{t("common:STEP_ONE.WAREHOUSE_LOCATED")} <strong>{recipient.warehouse_country.names[language] || recipient.warehouse_country.names["default"]}</strong></span>
                  <span className="tagline">{recipient.tagline[language] || recipient.tagline["default"]}</span>
                </span>
                <img
                    src={recipient.warehouse_country.flag_url}
                    alt={`Flag of ${
                      recipient.warehouse_country.names[language] ||
                      recipient.warehouse_country.names["default"]
                    }`}
                  />
              </li>
            ))}
          </ul>

          <StepNavigation
            prevButtonTitle={t("common:PREV_BUTTON")}
            onClickPrev={onBack}
          />
        </div>
      )}
    </Content>
  );
}
