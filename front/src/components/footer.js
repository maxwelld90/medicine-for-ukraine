import React from "react";
import {getCurrentLanguage} from "../helpers";
import { useTranslation } from "react-i18next";

export default function Header({}) {
    const [t] = useTranslation(["translation", "common"]);

  return (
    <footer>
        <div className="container">
            <div className="left">
                <span className="header">&copy; Medicine for Ukraine, 2022. <span className="version">{process.env.REACT_APP_VERSION}</span></span>
                <span>
                    {t("common:FOOTER")}
                </span>
            </div>
            <div className="right">
                <ul>
                    <li>
                        <a
                            href="https://www.instagram.com/medhelpua/"
                            className="instagram"
                            target="_blank"
                            rel="noreferrer noopener">
                                <span>medhelpua</span>
                        </a>
                    </li>
                    <li>
                        <a
                            href="https://www.instagram.com/hospitallers.ukraine_paramedic/"
                            className="instagram"
                            target="_blank"
                            rel="noreferrer noopener">
                                <span>hospitallers.ukraine_paramedic</span>
                        </a>
                    </li>
                </ul>
            </div>
        </div>
    </footer>);
}