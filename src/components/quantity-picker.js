import React, { useState } from "react";

export default function QuantityPicker(props) {
  const [quantity, serQuantity] = useState(0);
  return (
    <div>
      <div class="minus-button">-</div>
      {quantity}
      <div class="plus-button">+</div>
    </div>
  );
}
