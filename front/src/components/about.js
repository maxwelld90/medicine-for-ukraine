import React from "react";
import { Link } from "react-router-dom";

import { useTranslation } from "react-i18next";

export default function About() {
  const [t] = useTranslation(["translation", "common"]);

  return (
    <div>
      <h1>{t("common:title")}</h1>
      <p>
        We need your help in buying and shipping the supplies that will save
        lives of Ukrainian soldiers: medical items and defence equipment. On{" "}
        <a href="https://www.amazon.es/gp/registry/wishlist/3625H8NO7K4RJ/ref=cm_wl_huc_view">
          this page (for Spain)
        </a>{" "}
        or{" "}
        <a href="https://www.amazon.de/-/en/hz/wishlist/ls/UO8ID4CBE2FJ">
          this page (for Poland)
        </a>{" "}
        you will find a list of the supplies with links to online shops.
      </p>
      <p>
        If you see an item being unavailable, please find alternative shop links
        and add them in the comments. There are item names and shop links for
        different EU countries – please try to order items in the online shops
        located in the same country where you are sending to avoid shipping
        around. When ordering through Amazon ES and prompted for "Añadir
        identificación para la tramitación de permisos aduaneros" please select
        "Omitir por ahora". For delivery addresses contact one of us:{" "}
        <a href="https://t.me/thedefinitionof42">
          https://t.me/thedefinitionof42
        </a>
        , <a href="https://t.me/Vendi12">https://t.me/Vendi12</a>,{" "}
        <a href="https://t.me/Vientosolar">https://t.me/Vientosolar</a>,{" "}
        <a href="https://t.me/Yar_1nna">https://t.me/Yar_1nna</a>.
      </p>
      <p>Thank you for supporting Ukraine. &#10084;&#65039;</p>
      <p className="urgent">
        We need lots of walkie talkies for frontline troops. Here is the{" "}
        <a href="https://www.amazon.es/dp/B09GTXQB9Y/ref=cm_sw_r_apan_glt_i_CN1QM074D2WEHAT758X2">
          link
        </a>
        to buy them – for the delivery address please contact one of the
        volunteers mentioned above.
      </p>

      <div>
        <button type="button">
          <Link to="/request">Start Request</Link>
        </button>
      </div>
    </div>
  );
}
