import React from "react";
import classes from "./progressBar.module.css";

export default function ProgressBar({ currentStep = 0 }) {
  return <div className={[classes.progressLine, classes[`step-${currentStep}`]].join(" ")}></div>;
}
