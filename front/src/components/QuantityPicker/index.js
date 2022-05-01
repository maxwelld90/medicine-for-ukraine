import React, { useState, useEffect } from "react";
import "./QuantityPicker.css";

export default function QuantityPicker({ value = 0, max = 50, onChange }) {
  const [quantity, serQuantity] = useState(value);

  const onMinusClick = () => {
    if (quantity === 0) return;
    serQuantity(quantity - 1);
  };

  const onPlusClick = () => {
    if (quantity >= max) return;
    serQuantity(quantity + 1);
  };

  useEffect(() => {
    onChange && onChange(quantity);
  }, [quantity]);

  return (
    <li className="quantity-picker">
      {quantity < max ?
        <button className="plus" onClick={onPlusClick}>+</button>
      :
        <button className="plus" disabled onClick={onPlusClick}>+</button>
      }

      <span className="quantity">{quantity}</span>

      {quantity > 0 ?
        <button className="minus" onClick={onMinusClick}>-</button>
      :
        <button className="minus" disabled onClick={onMinusClick}>-</button>
      }
    </li>
  );
}
