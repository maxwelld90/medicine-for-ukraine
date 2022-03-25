import React, { useState, useEffect } from "react";
import "./quantity-picker.css";

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
    <li className="quantity-picker">
      <span className="button minus" onClick={onMinusClick}>-</span>
      <span className="quantity">{quantity}</span>
      <span className="button plus" onClick={onPlusClick}>+</span>
    </li>
  );
}
