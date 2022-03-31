import React, { useContext, useEffect, useState } from "react";
import { useTranslation } from "react-i18next";

import { RequestContext } from "./request-context";
import StepNavigation from "./components/StepNavigation";
import StepDescription from "./components/StepDescription";
import Loader from "../loader";
import Error from "../error";

import { fetchItems } from "../../api";

export default function StepTwo({ onNext, onBack }) {
  const [request, setRequest] = useContext(RequestContext);
  const [t] = useTranslation(["translation", "common"]);
  const [error, setError] = useState(null);
  const [isLoaded, setIsLoaded] = useState(false);
  const [productList, setProductList] = useState([]);

  const selectProduct = (product) => {
    setRequest({ ...request, selectedProduct: product });

    if (typeof onNext === "function") {
      onNext();
    }
  };

  useEffect(() => {
    // TODO remove default value when API will be ready
    fetchItems(request.donationType = 'meds', request.countryCode = 'pl').then(
      (result) => {
        setIsLoaded(true);
        setProductList(result);
      },
      (error) => {
        setIsLoaded(true);
        setError(error);
      }
    );
  }, [request.donationType, request.countryCode]);

  const getProductClasses = (product) => {
    const classes = [];
    if (product.highPriority) {
      classes.push("high-priority");
    }
    if (request.selectedProduct && product.id === request.selectedProduct.id) {
      classes.push("selected");
    }
    return classes.join(" ");
  };

  return (
    <>
      {error && <Error />}
      {!isLoaded && <Loader />}
      {!error && isLoaded && (
        <div>
          <StepDescription
            step="2/5"
            title={t("common:STEP_TWO.TITLE")}
            firstLine={t("common:STEP_TWO.FIRST_LINE")}
          />

          <ul className="item-list items direction">
            {productList.map((product, i) => (
              <li
                className={getProductClasses(product)}
                key={i}
                onClick={() => selectProduct(product)}
              >
                <span className="name">{product.name}</span>
                <span className="right-background"></span>
                {product.highPriority && <span className="high-priority"></span>}
                {product.lowestPrice && <><span className="from">From</span><span className="price">&euro;100.50</span></>}
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
