import React from "react";

import classes from "./StepDescription.module.css";

export default function StepDescription({
  title = null,
  firstLine = null,
  secondLine = null,
  step = true,
}) {
  return (
    <div>
      <h1 className={classes.header} >
        {title}
      </h1>
      {step && <span className={classes.stepAnchor}>{step}</span>}

      {firstLine && <p>{firstLine}</p>}

      {secondLine && <p>{secondLine}</p>}
    </div>
  );
}
