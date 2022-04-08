import React, { useContext } from "react";
import { useAsync } from "react-use";
import { useTranslation } from "react-i18next";

import { saveRequest } from "../../api";
import { RequestContext } from "./requestContext";
import StepDescription from "./components/StepDescription";
import StepNavigation from "./components/StepNavigation";
import Loader from "../loader";
import Error from "../error";

export default function Gratitude({ onNext, onBack }) {
  const [request] = useContext(RequestContext);
  const [t] = useTranslation(["translation", "common"]);

  const { loading, error } = useAsync(() => saveRequest(request))

  return (
    <>
      {error && <Error />}
      {loading && <Loader />}
      {!error && !loading && (
        <StepDescription
          title={t("common:STEP_SIX.TITLE")}
          firstLine={t("common:STEP_SIX.FIRST_LINE")}
          secondLine={t("common:STEP_SIX.SECOND_LINE")}
        />
      )}

      <StepNavigation
        prevButtonTitle={t("common:PREV_BUTTON")}
        onClickPrev={onBack}
        nextButtonTitle={t("common:STEP_SIX.RESTART_PROCESS")}
        onClickNext={onNext}
      />
    </>
  );
}
