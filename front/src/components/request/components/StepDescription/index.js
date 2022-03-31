import React from "react";

import { header, stepAnchor } from "./styles";

export default function StepDescription({
  title = null,
  firstLine = null,
  secondLine = null,
  step = true,
}) {
  return (
    <div>
      <h1 style={header} className="multilingual en">
        {title}
      </h1>
      {step && <span style={stepAnchor}>{step}</span>}

      {firstLine && <p>{firstLine}</p>}

      {secondLine && <p>{secondLine}</p>}
    </div>
  );
}
