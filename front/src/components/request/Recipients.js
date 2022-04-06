import React, { useContext } from "react";
import { useAsync } from "react-use";
import { useTranslation } from "react-i18next";

import { fetchRecipients } from "../../api";

import Loader from "../loader";
import Error from "../error";

import { RequestContext } from "./requestContext";
import StepNavigation from "./components/StepNavigation";
import StepDescription from "./components/StepDescription";

export default function Recipients({ onNext, onBack, language }) {
  const { loading, error, value } = useAsync(fetchRecipients);

  const [request, setRequest] = useContext(RequestContext);
  const [t] = useTranslation(["translation", "common"]);

  const handleSelect = (recipient) => {
    setRequest({ ...request, recipientId: recipient.recipient_id });

    typeof onNext === "function" && onNext();
  };


  return (
    <>
      {error && <Error />}
      {loading && <Loader />}
      {!error && !loading && (
        <div>
          <StepDescription
            step="1/5"
            title={t("common:STEP_ONE.TITLE")}
            firstLine={t("common:STEP_ONE.FIRST_LINE")}
          />

          <ul className="item-list countries direction">
            {value.map((recipient, i) => (
              <li
                key={i}
                onClick={() => handleSelect(recipient)}
                // className={
                //   recipient.code === request.countryCode ? "selected" : ""
                // }
                style={{
                  display: "flex",
                  justifyContent: "space-between",
                  alignItems: "baseline",
                }}
              >
                <div style={{ width: "70%" }}>
                  <div>
                    {recipient.names[language] || recipient.names["default"]}
                  </div>
                  <div
                    style={{
                      fontWeight: 100,
                      fontSize: "16pt",
                      padding: "10px 0",
                    }}
                  >
                    {recipient.tagline[language] ||
                      recipient.tagline["default"]}
                  </div>
                </div>

                <div>
                  <div
                    style={{
                      fontWeight: 100,
                      fontSize: "12pt",
                    }}
                  >
                    Delivery to:{" "}
                    {recipient.warehouse_country.names[language] ||
                      recipient.warehouse_country.names["default"]}
                  </div>
                  <img
                    style={{ width: "50px" }}
                    src={recipient.warehouse_country.flag_url}
                    alt={`Flag of ${
                      recipient.warehouse_country.names[language] ||
                      recipient.warehouse_country.names["default"]
                    }`}
                  />
                </div>
              </li>
            ))}
          </ul>

          <StepNavigation
            prevButtonTitle={t("common:PREV_BUTTON")}
            onClickPrev={onBack}
          />
        </div>
      )}
    </>
  );
}
