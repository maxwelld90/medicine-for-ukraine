import React, {useContext, useEffect, useState} from "react";
import { RequestContext } from "./request-context";
import { useTranslation } from "react-i18next";
import { fetchItems } from "../../api";

export default function StepFour({ onComplete }) {
  const [request, setRequest] = useContext(RequestContext);
  const [t] = useTranslation(["translation", "common"]);

  const selectProduct = (product) => {
    setRequest({ ...request, productName: product.name, productId: product.id });
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
    fetchItems(request.donationType, request.countryCode)
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
  }, [request.donationType, request.countryCode]);

  if (error) {
    return <div>Error: {error.message}</div>;
  } else if (!isLoaded) {
    return <div>Loading...</div>;
  }

  const getProductClasses = (product) => {
    const classes = [];
    if (product.highPriority) {
      classes.push("high-priority")
    }
    if (product.id === request.productId) {
      classes.push("selected")
    }
    return classes.join(' ');
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
            className={getProductClasses(product)}
            key={i}
            onClick={() => selectProduct(product)}
          >
            {product.name}
          </li>
        ))}
      </ul>
    </div>
  );
}
