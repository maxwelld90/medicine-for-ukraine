import React, {useContext, useEffect, useState} from "react";
import { RequestContext } from "./request-context";
import { useTranslation } from "react-i18next";
import { fetchItems } from "../../api";
import Loader from "../loader";
import Error from "../error";

export default function StepFour({ onNext }) {
  const [request, setRequest] = useContext(RequestContext);
  const [t] = useTranslation(["translation", "common"]);

  const selectProduct = (product) => {
    setRequest({ ...request, selectedProduct: product});
    if (typeof onNext === "function") {
      onNext();
    }
  };

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
    return <Error />;
  } else if (!isLoaded) {
    return <Loader/>;
  }

  const getProductClasses = (product) => {
    const classes = [];
    if (product.highPriority) {
      classes.push("high-priority")
    }
    if (request.selectedProduct && product.id === request.selectedProduct.id) {
      classes.push("selected")
    }
    return classes.join(' ');
  }

  return (
    <div>
      <h1 className="multilingual en">
        {t("common:STEP_FOUR.TITLE")}
        <span>4/7</span>
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
