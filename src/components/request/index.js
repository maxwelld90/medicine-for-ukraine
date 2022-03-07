import React, { useState, useEffect } from "react";
import { useTranslation } from "react-i18next";

import StepOne from "./step-one";
import StepTwo from "./step-two";
import StepThree from "./step-three";
import StepFour from "./step-four";
import StepFive from "./step-five";
import StepSix from "./step-six";
import StepSeven from "./step-seven";
import { RequestContext } from "./request-context";

const FIRST_STEP = 1;
const LAST_STEP = 7;

export default function Request() {
  const [step, setStep] = useState(FIRST_STEP);
  const [request, setRequest] = useState({ contact: "" });
  const [isCompletedStep, setIsCompletedStep] = useState(false);
  const [t] = useTranslation(["translation", "common"]);

  const nextStep = () => {
    if (step === LAST_STEP) return;

    setStep(step + 1);
    setIsCompletedStep(false);
  };

  const prevStep = () => {
    if (step === FIRST_STEP) return;

    setStep(step - 1);
    setIsCompletedStep(false);
  };

  const onComplete = () => {
    setIsCompletedStep(true);
  };

  useEffect(() => {
    window.onbeforeunload = confirmExit;
    function confirmExit() {
      return "show warning";
    }
  }, []);

  const multiStepForm = () => {
    switch (step) {
      case 1:
        return <StepOne onComplete={onComplete}></StepOne>;
      case 2:
        return <StepTwo onComplete={onComplete}>2</StepTwo>;
      case 3:
        return <StepThree onComplete={onComplete}>3</StepThree>;
      case 4:
        return <StepFour onComplete={onComplete}>4</StepFour>;
      case 5:
        return <StepFive onComplete={onComplete}>5</StepFive>;
      case 6:
        return <StepSix onComplete={onComplete}>5</StepSix>;
      case 7:
        return <StepSeven onComplete={onComplete}>5</StepSeven>;
      default:
      // do nothing
    }
  };

  return (
    <RequestContext.Provider value={[request, setRequest]}>
      <div>
        <div>{multiStepForm()}</div>
        {step !== FIRST_STEP && (
          <button onClick={prevStep}>
            {t("common:PREV_BUTTON")}
          </button>
        )}
        {step !== LAST_STEP && (
          <button disabled={!isCompletedStep} onClick={nextStep}>
            {t("common:NEXT_BUTTON")}
          </button>
        )}
      </div>
    </RequestContext.Provider>
  );
}
