import React from "react";
import { useTranslation } from "react-i18next";
import "./loader.css";

export default function Loader() {
  const [t] = useTranslation(["translation", "common"]);
  
  return <div className="loader"><div></div><span>{t("common:LOADING")}</span></div>;
}