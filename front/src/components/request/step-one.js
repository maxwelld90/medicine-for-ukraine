import React, { useContext, useEffect, useState } from "react";
import { RequestContext } from "./request-context";
import StepNavigation from "./components/StepNavigation";

import { useTranslation } from "react-i18next";
import { fetchCountries } from "../../api";
import Loader from "../loader";
import Error from "../error";

export default function StepOne({ onNext, onBack }) {
  const [request, setRequest] = useContext(RequestContext);
  const [t] = useTranslation(["translation", "common"]);

  const [error, setError] = useState(null);
  const [isLoaded, setIsLoaded] = useState(false);
  const [partners, setPartners] = useState([]);

  const handleSelect = (partner) => {
    setRequest({ ...request, countryCode: partner.code });

    if (typeof onNext === "function") {
      onNext();
    }
  };

  useEffect(() => {
    fetchCountries().then(
      (result) => {
        setIsLoaded(true);
        setPartners(result);
      },
      (error) => {
        setIsLoaded(true);
        setError(error);
      }
    );
  }, []);

  return (
    <>
      {error && <Error />}
      {!isLoaded && <Loader />}
      {!error && isLoaded && (
        <div>
          <h1>
            {t("common:STEP_TWO.TITLE")}
            <span>1/5</span>
          </h1>

          <p>{t("common:STEP_TWO.FIRST_LINE")}</p>

          <ul className="item-list countries direction">
            {partners.map((partner, i) => (
              <li
                key={i}
                onClick={() => handleSelect(partner)}
                className={
                  partner.code === request.countryCode ? "selected" : ""
                }
                style={{
                  display: "flex",
                  justifyContent: "space-between",
                  alignItems: "baseline",
                }}
              >
                <div style={{width: "70%"}}>
                  <div>Partner Name</div>
                  <div style={{ fontWeight: 100, fontSize: "16pt", padding: "10px 0" }}>
                    {partner.description ||
                      "Partner collects medical equipment and products"}
                  </div>
                </div>

                <div>
                  <div
                    style={{
                      fontWeight: 100,
                      fontSize: "12pt",
                    }}
                  >
                    Delivery to: {partner.name}
                  </div>
                  <img
                    style={{ width: "50px" }}
                    src={partner.flag_url}
                    alt={`Flag of ${partner.name}`}
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
