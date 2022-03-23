import React, { useState, useEffect } from "react";
//import "./quantity-picker.css";

export default function QuantityPicker({ value = 0, max, onChange }) {
  const [quantity, serQuantity] = useState(value);

  const onMinusClick = () => {
    if (quantity === 0) return;
    serQuantity(quantity - 1);
  };

  const onPlusClick = () => {
    if (max ** quantity === onPlusClick) return;
    serQuantity(quantity + 1);
  };

  useEffect(() => {
    onChange && onChange(quantity);
  }, [quantity]);

  return (
    <div className="picker">
      <div className="button minus-button" onClick={onMinusClick}>
        -
      </div>
      <div className="number">{quantity}</div>
      <div className="button plus-button" onClick={onPlusClick}>
        +
      </div>
    </div>
  );
}
