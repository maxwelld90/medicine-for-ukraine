import React, { useContext, useEffect, useState } from "react";
import { useAsync } from "react-use";
import { useTranslation } from "react-i18next";

import { RequestContext } from "./requestContext";
import QuantityPicker from "../QuantityPicker";
import ItemDeliveryConfirmation from "./components/itemDeliveryConfirmation";
import StepNavigation from "./components/StepNavigation";
import StepDescription from "./components/StepDescription";
import Loader from "../loader";
import Error from "../error";

import { fetchLinks } from "../../api";

export default function Basket({ onNext, onBack, language }) {
  const [isCompletedStep, setIsCompletedStep] = useState(false);
  // const [onlineStores, setOnlineStores] = useState([]);
  const [country, setCountry] = useState(null);
  // const [error, setError] = useState(null);
  // const [isLoaded, setIsLoaded] = useState(false);

  const [request, setRequest] = useContext(RequestContext);


  const { loading, error, value } = useAsync(() => fetchLinks(request.recipientId, request.item));

  const [t] = useTranslation(["translation", "common"]);

  const DEFAULT_LANGUAGE = "en";

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

  // useEffect(() => {
  //   fetchLinks(
  //     request.recipientId,
  //     request.selectedProduct.id
  //   ).then(
  //     (result) => {
  //       setCountry(result.country);
  //       setOnlineStores(result.links);
  //       setIsLoaded(true);
  //     },
  //     (error) => {
  //       setIsLoaded(true);
  //       setError(error);
  //     }
  //   );
  // }, [request.donationType, request.countryCode, request.selectedProduct]);

  return (
    <>
      {error && <Error />}
      {loading && <Loader />}
      {!error && !loading && (
        <div>
          <StepDescription
            step="3/5"
            title={t("common:STEP_THREE.TITLE")}
            firstLine={t("common:STEP_THREE.FIRST_LINE")}
          />

          <ItemDeliveryConfirmation
            itemName={
              request.selectedProduct.names[language] ||
              request.selectedProduct.names[DEFAULT_LANGUAGE]
            }
            country={country}
          />

          <ul className="item-list stores nohover">
            {value?.links.map((item, i) => (
              <li key={i}>
                <a href={item.link} target="_blank" rel="noreferrer noopener">
                  <span>{item.domain}</span>
                </a>
                <ul className="right-options">
                  <li className="price">
                    <span className="approx">Approx.</span>
                    <span className="price">&euro;3.50</span>
                    <span className="date">Checked 2022-03-15</span>
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

          <StepNavigation
            prevButtonTitle={t("common:PREV_BUTTON")}
            onClickPrev={onBack}
            isNextButtonEnabled={isCompletedStep}
            nextButtonTitle={t("common:NEXT_BUTTON")}
            onClickNext={onNext}
          />
        </div>
      )}
    </>
  );
}
