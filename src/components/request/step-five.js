import React, { useContext } from "react";
import { RequestContext } from "./request-context";
import { useTranslation } from "react-i18next";

export default function StepFIve({onComplete}) {
  const [request, setRequest] = useContext(RequestContext);
  const [t] = useTranslation(["translation", "common"]);

  const onQuantityChange = (event) => {
    if (event.target.value > 0 && typeof onComplete === "function") {
      onComplete();
    }
  };

  const onlineStores = [
    {
      name: "Issosa",
      link: "https://issosa.com/shop/gasa-hemostatico-chitogauze",
    },
    {
      name: "Amazon ES",
      link: "https://www.amazon.es/Celox-Rapid-Gasa-hemost%C3%A1tica-forma/dp/B07RWLJ3G7/ref=asc_df_B07RWLJ3G7/?tag=googshopes-21&linkCode=df0&hvadid=420332014314&hvpos=&hvnetw=g&hvrand=12962910197763725794&hvpone=&hvptwo=&hvqmt=&hvdev=m&hvdvcmdl=&hvlocint=&hvlocphy=1005424&hvtargid=pla-785149914233&psc=1&tag=&ref=&adgrpid=96502138512&hvpone=&hvptwo=&hvadid=420332014314&hvpos=&hvnetw=g&hvrand=12962910197763725794&hvqmt=&hvdev=m&hvdvcmdl=&hvlocint=&hvlocphy=1005424&hvtargid=pla-785149914233",
    },
    {
      name: "Ekipol",
      link: "https://www.ekipol.es/control-de-hemorragias/12548-venda-hemostatica-control-del-sangrado-celox-g.htmlhttps://www.ekipol.es/control-de-hemorragias/12548-venda-hemostatica-control-del-sangrado-celox-g.html",
    },
  ];

  return (
    <div>
      <h1 className="multilingual en">
        {t("common:STEP_FIVE.TITLE")}
        <span>5/6</span>
      </h1>

      <p className="multilingual en">
        {t("common:STEP_FIVE.FIRST_LINE", {
          product: request.productName,
          country: request.country,
        })}
      </p>

      <ul className="item-list">
        {onlineStores.map((store, i) => (
          <li key={i}>
            {store.name}
            <a href={store.link} target="_blank" rel="noreferrer noopener">
              Link
            </a>

            <input type="number" onChange={onQuantityChange}></input>
          </li>
        ))}
      </ul>
    </div>
  );
}
