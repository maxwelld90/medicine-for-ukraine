import React, { useContext, useState } from "react";
import { useAsync } from "react-use";
import { useTranslation } from "react-i18next";

import { fetchLinks } from "../../api";
import Content from "../Content";

import { RequestContext } from "./requestContext";
import QuantityPicker from "../QuantityPicker";
import ItemDeliveryConfirmation from "./components/itemDeliveryConfirmation";
import StepNavigation from "./components/StepNavigation";
import StepDescription from "./components/StepDescription";

import './request.css';

function getProductName({ names }, language) {
  return names[language] || names.default;
}

export default function Basket({ onNext, onBack, language }) {
  const [isCompletedStep, setIsCompletedStep] = useState(false);

  const [request, setRequest] = useContext(RequestContext);
  const productName = getProductName(request.selectedProduct);

  const { loading, error, value } = useAsync(() =>
    fetchLinks(request.recipientId, request.selectedProduct.id)
  );

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
      name: productName,
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

  return (
    <Content error={error} loading={loading}>
      {() => (
        <div>
          <StepDescription
            step="3/5"
            title={t("common:STEP_THREE.TITLE")}
            firstLine={t("common:STEP_THREE.FIRST_LINE")}
          />
          
          <ItemDeliveryConfirmation
            itemName={productName}
            country={value.country}
          />

          <ul className="item-list stores nohover">
            {value?.links.map((item, i) => (
              <li key={i}>
                <a href={item.link} target="_blank" rel="noreferrer noopener">
                  <span>{item.domain}</span>
                </a>
                <ul className="right-options">
                  <li className="price">
                    <span className="approx">{t("common:APPROXIMATE")}</span>
                    {item.price && (
                      <span className="price">&euro;{item.price}</span>
                    )}
                    {item.last_checked && (
                      <span className="date">
                        Last Checked:{" "}
                        {new Date(item.last_checked).toDateString()}
                      </span>
                    )}
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
    </Content>
  );
}
