import React, { useContext, useEffect } from "react";
import { RequestContext } from "./request-context";
import { useTranslation } from "react-i18next";

export default function StepFour({ onComplete }) {
  const [request, setRequest] = useContext(RequestContext);
  const [t] = useTranslation(["translation", "common"]);

  const selectProduct = (name) => {
    setRequest({ ...request, productName: name });
  };

  const productList = [
    { name: "Hemostatic Celox", highPriority: true },
    { name: "Aspirin 2", highPriority: false },
    { name: "Aspirin 3", highPriority: false },
  ];

  useEffect(() => {
    if (request.productName && typeof onComplete === "function") {
      onComplete();
    }
  }, [request, onComplete]);

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
