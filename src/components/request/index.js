import React, { useState } from "react";
import { useTranslation } from "react-i18next";

import StepOne from "./step-one";
import StepTwo from "./step-two";
import StepThree from "./step-three";
import StepFour from "./step-four";
import StepFive from "./step-five";
import StepSix from "./step-six";
import { RequestContext } from "./request-context";

const FIRST_STEP = 1;
const LAST_STEP = 6;

export default function Request() {
  const [step, setStep] = useState(FIRST_STEP);
  const [request, setRequest] = useState({ contact: "" });
  const [t] = useTranslation(["translation", "common"]);

  const nextStep = () => {
    if (step === LAST_STEP) return;

    return setStep(step + 1);
  };

  const multiStepForm = () => {
    switch (step) {
      case 1:
        return <StepOne></StepOne>;
      case 2:
        return <StepTwo>2</StepTwo>;
      case 3:
        return <StepThree>3</StepThree>;
      case 4:
        return <StepFour>4</StepFour>;
      case 5:
        return <StepFive>5</StepFive>;
      case 6:
        return <StepSix>5</StepSix>;
      default:
      // do nothing
    }
  };

  return (
    <RequestContext.Provider value={[request, setRequest]}>
      <div>
        <div>{multiStepForm()}</div>
        {step !== LAST_STEP && <button onClick={nextStep}>{t("common:NEXT_BUTTON")}</button>}
      </div>
    </RequestContext.Provider>
  );
}
