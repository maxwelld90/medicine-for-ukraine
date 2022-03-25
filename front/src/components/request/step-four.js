import React, { useContext, useEffect, useState } from "react";
import { RequestContext } from "./request-context";
import { useTranslation } from "react-i18next";
import { fetchItems } from "../../api";
import Loader from "../loader";
import Error from "../error";

export default function StepFour({ onNext, onBack }) {
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
    fetchItems(request.donationType, request.countryCode).then(
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
          <h1>
            {t("common:STEP_FOUR.TITLE")}
            <span>4/7</span>
          </h1>

          <p>{t("common:STEP_FOUR.FIRST_LINE")}</p>

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

          <p className="direction">
            <button className={"button-back"} onClick={onBack}>
              {t("common:PREV_BUTTON")}
            </button>
          </p>
        </div>
      )}
    </>
  );
}
