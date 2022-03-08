import React, {useContext, useEffect, useState} from "react";
import { RequestContext } from "./request-context";
import { useTranslation } from "react-i18next";
import {fetchItems, fetchLinks} from "../../api";

export default function StepFIve({onComplete}) {
  const [request, setRequest] = useContext(RequestContext);
  const [t] = useTranslation(["translation", "common"]);

  const onQuantityChange = (event) => {
    if (event.target.value > 0 && typeof onComplete === "function") {
      onComplete();
    }
  };

  const [error, setError] = useState(null);
  const [isLoaded, setIsLoaded] = useState(false);
  const [onlineStores, setOnlineStores] = useState([]);


  useEffect( () => {
    fetchLinks(request.donationType, request.country, request.productId)
      .then(
        (result) => {
          setIsLoaded(true);
          setOnlineStores(result);
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
