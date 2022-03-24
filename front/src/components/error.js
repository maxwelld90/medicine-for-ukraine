import React from "react";
import { useTranslation } from "react-i18next";

import "./loader.css";

export default function Error({ errorText }) {
  const [t] = useTranslation(["translation", "common"]);

  return (
    <div className="text-center error-container">
        {/* TODO replace with appropriate translation */}
      {errorText ? t(errorText) : "Oops! Something went wrong"}
    </div>
  );
}
