import React, {useContext, useEffect, useState} from "react";
import { RequestContext } from "./request-context";
import { useTranslation } from "react-i18next";
import { fetchLinks } from "../../api";

export default function StepFive({ onNext }) {
  const [isCompletedStep, setIsCompletedStep] = useState(false);
  const [request, setRequest] = useContext(RequestContext);
  const [t] = useTranslation(["translation", "common"]);

  const getOnQuantityChangeHandler = (item, index) => {
    return (event) => {
      if (event.target.value > 0) {
        const store = request.stores[item.domain] || {
          store_domain: item.domain,
          items: {}
        };

        const storeItem = store.items[item.link] || {
          row_number: request.selectedProduct.id,
          name: request.selectedProduct.name,
          type: request.donationType,
          url: item.link,
        };
        storeItem.quantity = event.target.value;

        setRequest({ ...request, stores: {...request.stores, [item.domain]: {
          ...store,
          [item.link]: storeItem,
        }}});
        setIsCompletedStep(true);
      }
    };
  };

  const [error, setError] = useState(null);
  const [isLoaded, setIsLoaded] = useState(false);
  const [onlineStores, setOnlineStores] = useState([]);


  useEffect( () => {
    fetchLinks(request.donationType, request.countryCode, request.selectedProduct.id)
      .then(
        (result) => {
          setIsLoaded(true);
          setOnlineStores(result);
        },
        (error) => {
          setIsLoaded(true);
          setError(error);
        }
      )
  }, [request.donationType, request.countryCode, request.selectedProduct]);

  if (error) {
    return <div>Error: {error.message}</div>;
  } else if (!isLoaded) {
    return <div>Loading...</div>;
  }

  return (
    <div>
      <h1 className="multilingual en">
        {t("common:STEP_FIVE.TITLE")}
        <span>5/7</span>
      </h1>

      <p className="multilingual en">
        {t("common:STEP_FIVE.FIRST_LINE", {
          product: request.selectedProduct.name,
          country: request.countryCode,
        })}
      </p>

      <ul className="item-list stores">
        {onlineStores.map((item, i) => (
          <li key={i}>
            <a href={item.link} target="_blank" rel="noreferrer noopener">
              {item.domain}
            </a>

            <input type="number" onChange={getOnQuantityChangeHandler(item, i)}/>
          </li>
        ))}
      </ul>
      <div className={'btn-wrap'}>
        <button disabled={!isCompletedStep} onClick={onNext}>
          {t("common:NEXT_BUTTON")}
        </button>
      </div>
    </div>
  );
}
