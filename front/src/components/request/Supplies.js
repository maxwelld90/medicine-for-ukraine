import React, { useContext } from "react";
import { useAsync } from "react-use";
import { useTranslation } from "react-i18next";

import { RequestContext } from "./requestContext";
import StepNavigation from "./components/StepNavigation";
import StepDescription from "./components/StepDescription";
import Loader from "../loader";
import Error from "../error";
import { fetchItems } from "../../api";

const DEFAULT_LANGUAGE = 'en';

export default function Supplies({ onNext, onBack, language }) {
  const [request, setRequest] = useContext(RequestContext);
  const [t] = useTranslation(["translation", "common"]);

  console.log('re', request)

  const { loading, error, value } = useAsync(() => fetchItems(request.recipientId));

  const selectProduct = (product) => {
    setRequest({ ...request, selectedProduct: product });

    if (typeof onNext === "function") {
      onNext();
    }
  };

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
      {loading && <Loader />}
      {!error && !loading && (
        <div>
          <StepDescription
            step="2/5"
            title={t("common:STEP_TWO.TITLE")}
            firstLine={t("common:STEP_TWO.FIRST_LINE")}
          />

          <ul className="item-list items direction">
            {value.map((product, i) => (
              <li
                className={getProductClasses(product)}
                key={i}
                onClick={() => selectProduct(product)}
              >
                <span className="name">{product.names[language] || product.names[DEFAULT_LANGUAGE]}</span>
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
