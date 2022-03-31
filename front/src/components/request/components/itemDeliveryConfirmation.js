import React from "react";
import "./itemDeliveryConfirmation.css";

export default function ItemDeliveryConfirmation({itemName, country}) {
  return (
    // <p className="item-delivery-confirmation">
    //     <span className="item-name">{itemName}</span>
    //     <span className="country-code">{country.name}{country.code}</span>
    // </p>
    <p className="item-delivery-confirmation">
        <span className="item-name">
            <span>
                <span className="header">Selected Item</span>
                <span className="text">{itemName}</span>
            </span>
        </span>
        
        <span className="country">
            <span>
                <span className="header">Deliver To</span>
                <span className="text">{country.name}</span>
            </span>
            <img src={country.flag_url} alt={`Flag of ${country.name}`} />
        </span>
    </p>
  );
}