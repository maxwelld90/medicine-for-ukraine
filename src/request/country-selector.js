import React, { useContext } from "react";
import { RequestContext } from "./request-context";

export default function CountrySelector() {
  const [request] = useContext(RequestContext);

  return (
    <div>
      <h2>Where do you want to send items to?</h2>
      <div>{request.contact}</div>
    </div>
  );
}
