import React, { useContext, useEffect, useState } from "react";
import { RequestContext } from "./request-context";
import { useTranslation } from "react-i18next";
import { fetchLinks } from "../../api";
import QuantityPicker from "../quantity-picker";
import Loader from "../loader";
import Error from "../error";
import ItemDeliveryConfirmation from "../itemDeliveryConfirmation";

export default function StepFive({ onNext, onBack }) {
  const [isCompletedStep, setIsCompletedStep] = useState(false);
  const [onlineStores, setOnlineStores] = useState([]);
  const [country, setCountry] = useState(null);
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
        setCountry(result.country);
        setOnlineStores(result.links);
        setIsLoaded(true);
      },
      (error) => {
        setIsLoaded(true);
        setError(error);
      }
    );
  }, [request.donationType, request.countryCode, request.selectedProduct]);
  
  return (
    <>
      {error && <Error />}
      {!isLoaded && <Loader />}
      {!error && isLoaded && (
        <div>
          <h1>
            {t("common:STEP_FIVE.TITLE")}
            <span>5/7</span>
          </h1>

          <ItemDeliveryConfirmation itemName={request.selectedProduct.name} country={country} />

          <p>
            {t("common:STEP_FIVE.FIRST_LINE", {
              product: request.selectedProduct.name,
              country: request.countryCode,
            })}
          </p>

          <ul className="item-list stores nohover">
            {onlineStores.map((item, i) => (
              <li key={i}>
                <a href={item.link} target="_blank" rel="noreferrer noopener"><span>{item.domain}</span></a>
                <ul className="right-options">
                  <li className="price">
                    <span class="approx">Approx.</span>
                    <span class="price">&euro;3.50</span>
                    <span class="date">Checked 2022-03-15</span>
                  </li>
                  <QuantityPicker
                    key={i + i}
                    value={getQty(item)}
                    onChange={(value) => onQuantityChangeHandler(item, value)}
                  />
                </ul>
              </li>
            ))}
          </ul>

          {/* <ul className="item-list stores">
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
          </ul> */}

          <p className="direction">
            <button className={"button-back"} onClick={onBack}>
              {t("common:PREV_BUTTON")}
            </button>
            <button disabled={!isCompletedStep} onClick={onNext}>
              {t("common:NEXT_BUTTON")}
            </button>
          </p>
        </div>
      )}
    </>
  );
}
