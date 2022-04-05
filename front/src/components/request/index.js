import React, { useState, useEffect } from "react";

import Greeting from "./components/Greeting";
import Recipients from "./Recipients";
import Supplies from "./Supplies";
import Basket from "./Basket";
import ActionItem from "./ActionItem";
import Confirmation from "./Confirmation";
import Gratitude from "./Gratitude";

import { RequestContext } from "./requestContext";

const FIRST_STEP = 0;
const LAST_STEP = 6;

export default function Request({ onStepChange, language }) {
  const [step, setStep] = useState(FIRST_STEP);
  const [request, setRequest] = useState({
    contact: "",
    stores: {},
  });

  const nextStep = () => {
    if (step === LAST_STEP) {
      setRequest({ contact: request.contact, stores: {} });
      setStep(1);
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
        return <Recipients onNext={nextStep} onBack={prevStep} />;
      case 2:
        return <Supplies onNext={nextStep} onBack={prevStep} language={language} />;
      case 3:
        return <Basket onNext={nextStep} onBack={prevStep} language={language}/>;
      case 4:
        return <ActionItem onNext={nextStep} onBack={prevStep} />;
      case 5:
        return <Confirmation onNext={nextStep} onBack={prevStep} />;
      case 6:
        return <Gratitude onNext={nextStep} onBack={prevStep} />;
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
