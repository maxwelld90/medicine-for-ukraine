import React, { useState, useEffect } from "react";

import Greeting from "./components/Greeting";
import StepOne from "./step-one";
import StepTwo from "./step-two";
import StepThree from "./step-three";
import StepFour from "./step-four";
import StepFive from "./step-five";
import StepSix from "./step-six";

import { RequestContext } from "./request-context";

const FIRST_STEP = 0;
const LAST_STEP = 8;

export default function Request({ onStepChange, language }) {
  const [step, setStep] = useState(FIRST_STEP);
  const [request, setRequest] = useState({
    contact: "",
    stores: {},
  });

  const nextStep = () => {
    if (step === LAST_STEP) {
      setRequest({ contact: request.contact, stores: {} });
    }

    setStep(step === LAST_STEP ? 1 : step + 1);
  };

  const prevStep = (toStep) => {
    if (step === FIRST_STEP) return;

    if (typeof toStep === "number") {
      setStep(toStep);
    } else {
      setStep(step - 1);
    }
  };

  useEffect(() => {
    // This is a feature that alerts warning if user tries to close a tab
    window.onbeforeunload = confirmExit;
    function confirmExit() {
      return "show warning";
    }

    if (typeof onStepChange === "function") {
      onStepChange(step);
    }

  }, [step]);

  const multiStepForm = () => {
    switch (step) {
      case 0:
        return <Greeting onNext={nextStep} />;
      case 1:
        return <StepOne onNext={nextStep} onBack={prevStep} />;
      case 2:
        return <StepTwo onNext={nextStep} onBack={prevStep} language={language} />;
      case 3:
        return <StepThree onNext={nextStep} onBack={prevStep} language={language}/>;
      case 4:
        return <StepFour onNext={nextStep} onBack={prevStep} />;
      case 5:
        return <StepFive onNext={nextStep} onBack={prevStep} />;
      case 6:
        return <StepSix onNext={nextStep} onBack={prevStep} />;
      default:
      // do nothing
    }
  };

  return (
    <RequestContext.Provider value={[request, setRequest]}>
      <div>
        <div>{multiStepForm()}</div>
      </div>
    </RequestContext.Provider>
  );
}
