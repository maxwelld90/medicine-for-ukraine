import React, {useContext, useEffect, useState} from "react";
import { RequestContext } from "./request-context";
import { useTranslation } from "react-i18next";
import {fetchItems} from "../../api";

export default function StepFour({ onComplete }) {
  const [request, setRequest] = useContext(RequestContext);
  const [t] = useTranslation(["translation", "common"]);

  const selectProduct = (name) => {
    setRequest({ ...request, productName: name });
  };

  useEffect(() => {
    if (request.productName && typeof onComplete === "function") {
      onComplete();
    }
  }, [request, onComplete]);

  const [error, setError] = useState(null);
  const [isLoaded, setIsLoaded] = useState(false);
  const [productList, setProductList] = useState([]);

  useEffect( () => {
    fetchItems(request.donationType, request.country)
      .then(
        (result) => {
          setIsLoaded(true);
          setProductList(result);
        },
        (error) => {
          setIsLoaded(true);
          setError(error);
        }
      )
  }, [request]);

  if (error) {
    return <div>Error: {error.message}</div>;
  } else if (!isLoaded) {
    return <div>Loading...</div>;
  }

  return (
    <div>
      <h1 className="multilingual en">
        {t("common:STEP_FOUR.TITLE")}
        <span>4/6</span>
      </h1>

      <p className="multilingual en">{t("common:STEP_FOUR.FIRST_LINE")}</p>

      <ul className="item-list">
        {productList.map((product, i) => (
          <li
            className={product.highPriority ? "high-priority" : ""}
            key={i}
            onClick={() => selectProduct(product.name)}
          >
            {product.name}
          </li>
        ))}
      </ul>
    </div>
  );
}
