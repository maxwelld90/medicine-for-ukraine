import React, { useContext, useEffect, useState } from "react";
import { RequestContext } from "./request-context";
import { useTranslation } from "react-i18next";
import { fetchLinks } from "../../api";
import QuantityPicker from "../quantity-picker";
import Loader from "../loader";
import Error from "../error";

export default function StepFive({ onNext }) {
  const [isCompletedStep, setIsCompletedStep] = useState(false);
  const [onlineStores, setOnlineStores] = useState([]);
  const [error, setError] = useState(null);
  const [isLoaded, setIsLoaded] = useState(false);

  const [request, setRequest] = useContext(RequestContext);
  const [t] = useTranslation(["translation", "common"]);

  const onQuantityChangeHandler = ({ domain, link }, value) => {
    if (!request.stores[domain] && !value) return;

    if (request.stores[domain] && !value) {
      const { [domain]: remove, ...restStores } = request.stores;

      setRequest({ ...request, stores: restStores });
      setIsCompletedStep(!!Object.values(restStores).length);
      return;
    }

    const store = request.stores[domain] || {
      store_domain: domain,
      items: {},
    };

    const storeItem = store.items[link] || {
      row_number: request.selectedProduct.id,
      name: request.selectedProduct.name,
      type: request.donationType,
      url: link,
    };

    storeItem.quantity = parseInt(value) || 0;

    const stores = {
      ...request.stores,
      [domain]: {
        ...store,
        items: {
          ...store.items,
          [link]: storeItem,
        },
      },
    };

    setRequest({ ...request, stores });
    setIsCompletedStep(!!Object.values(stores).length);
  };

  const getQty = ({ domain, link }) => {
    const { stores } = request;
    if (stores[domain] && stores[domain].items[link]) {
      return stores[domain].items[link].quantity;
    }
    return 0;
  };

  useEffect(() => {
    fetchLinks(
      request.donationType,
      request.countryCode,
      request.selectedProduct.id
    ).then(
      (result) => {
        setIsLoaded(true);
        setOnlineStores(result);
      },
      (error) => {
        setIsLoaded(true);
        setError(error);
      }
    );
  }, [request.donationType, request.countryCode, request.selectedProduct]);

  if (error) {
    return <Error />;
  } else if (!isLoaded) {
    return <Loader/>;
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

            <QuantityPicker
              key={i + i}
              value={getQty(item)}
              onChange={(value) => onQuantityChangeHandler(item, value)}
            />
          </li>
        ))}
      </ul>
      <div className={"btn-wrap"}>
        <button disabled={!isCompletedStep} onClick={onNext}>
          {t("common:NEXT_BUTTON")}
        </button>
      </div>
    </div>
  );
}
