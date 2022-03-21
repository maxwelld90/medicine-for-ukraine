import React, { useState, useEffect } from "react";

export default function ProgressBar({ currentStep = 0 }) {
  return (
    <div className={"progress " + ("step" + currentStep)}></div>
  );
}
