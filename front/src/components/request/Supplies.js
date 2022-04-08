import React, { useContext } from "react";
import { useAsync } from "react-use";
import { useTranslation } from "react-i18next";

import { fetchItems } from "../../api";
import Content from "../Content";

import { RequestContext } from "./requestContext";
import StepNavigation from "./components/StepNavigation";
import StepDescription from "./components/StepDescription";

export default function Supplies({ onNext, onBack, language }) {
  const [request, setRequest] = useContext(RequestContext);
  const [t] = useTranslation(["translation", "common"]);

  const { loading, error, value } = useAsync(() =>
    fetchItems(request.recipientId)
  );

  const selectProduct = (product) => {
    setRequest({ ...request, selectedProduct: product });

    typeof onNext === "function" && onNext();
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
    <Content error={error} loading={loading}>
      {() => (
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
                <span className="name">
                  {product.names[language] || product.names["default"]}
                </span>
                <span className="right-background"></span>
                {product.highPriority && (
                  <span className="high-priority"></span>
                )}
                {product.lowestPrice && (
                  <>
                    <span className="from">From</span>
                    <span className="price">&euro;{product.lowestPrice}</span>
                  </>
                )}
              </li>
            ))}
          </ul>

          <StepNavigation
            prevButtonTitle={t("common:PREV_BUTTON")}
            onClickPrev={onBack}
          />
        </div>
      )}
    </Content>
  );
}
