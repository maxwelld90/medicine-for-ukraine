import React from "react";
import {getCurrentLanguage} from "../helpers";

export default function Header({}) {
  return (
    <footer>
        <div className="container">
            <div className="left">
                <span className="header">&copy; Medicine for Ukraine, 2022. <span className="version">{process.env.REACT_APP_VERSION}</span></span>
                <span>Medicine for Ukraine is run by a <a href={`/${getCurrentLanguage()}/about/`} target="_blank" rel="noreferrer noopener">group of volunteers</a> that want to help.
          We get medicine and supplies to those who need it the most.</span>
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