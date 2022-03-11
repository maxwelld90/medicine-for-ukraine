import React, { useState, useEffect } from "react";
import { useTranslation } from "react-i18next";

import StepOne from "./step-one";
import StepTwo from "./step-two";
import StepThree from "./step-three";
import StepFour from "./step-four";
import StepFive from "./step-five";
import StepSix from "./step-six";
import StepSeven from "./step-seven";
import StepEight from "./step-eight";
import { RequestContext } from "./request-context";

const FIRST_STEP = 1;
const LAST_STEP = 8;

export default function Request() {
  const [step, setStep] = useState(FIRST_STEP);
  const [request, setRequest] = useState({
    contact: "",
    stores: {},
  });
  const [t] = useTranslation(["translation", "common"]);

  const nextStep = () => {
    if (step === LAST_STEP) return;

    setStep(step + 1);
  };

  const prevStep = (toStep) => {
    if (step === FIRST_STEP) return;

    if (typeof toStep === 'number') {
      setStep(toStep);
    } else {
      setStep(step - 1);
    }
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
        return <StepOne onNext={nextStep}/>;
      case 2:
        return <StepTwo onNext={nextStep}/>;
      case 3:
        return <StepThree onNext={nextStep}/>;
      case 4:
        return <StepFour onNext={nextStep}/>;
      case 5:
        return <StepFive onNext={nextStep}/>;
      case 6:
        return <StepSix onNext={nextStep} onBack={prevStep}/>;
      case 7:
        return <StepSeven onNext={nextStep}/>;
      case 8:
        return <StepEight onNext={nextStep}/>;
      default:
      // do nothing
    }
  };

  return (
    <RequestContext.Provider value={[request, setRequest]}>
      <div>
        <div>{multiStepForm()}</div>
        {step !== FIRST_STEP && (
          <button className={'button-back'} onClick={prevStep}>
            {t("common:PREV_BUTTON")}
          </button>
        )}
      </div>
    </RequestContext.Provider>
  );
}
