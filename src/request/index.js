import React, { useState } from "react";

import Contact from "./contact";
import CountrySelector from "./country-selector";
import DonationType from "./donation-type";
import ProductList from "./product-list";
import ReceiptScreenshot from "./receipt-screenshot";
import OrderCompletion from "./order-completion";
import { RequestContext } from "./request-context";

const FIRST_STEP = 1;
const LAST_STEP = 6;

export default function Request() {
  const [step, setStep] = useState(FIRST_STEP);
  const [request, setRequest] = useState({ contact: "" });

  const nextStep = () => {
    if (step === LAST_STEP) return;

    return setStep(step + 1);
  };

  const multiStepForm = () => {
    switch (step) {
      case 1:
        return <Contact></Contact>;
      case 2:
        return <CountrySelector>2</CountrySelector>;
      case 3:
        return <DonationType>3</DonationType>;
      case 4:
        return <ProductList>4</ProductList>;
      case 5:
        return <ReceiptScreenshot>5</ReceiptScreenshot>;
      case 6:
        return <OrderCompletion>5</OrderCompletion>;
      default:
      // do nothing
    }
  };

  return (
    <RequestContext.Provider value={[request, setRequest]}>
      <div>
        <div>{multiStepForm()}</div>
        {step !== LAST_STEP && <button onClick={nextStep}>Next</button>}
      </div>
    </RequestContext.Provider>
  );
}
