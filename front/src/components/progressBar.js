import React from "react";
//import "./progressBar.css";

export default function ProgressBar({ currentStep = 0 }) {
  return <div className={"progress " + ("step" + currentStep)}></div>;
}