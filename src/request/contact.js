import React, { useContext } from "react";
import { RequestContext } from "./request-context";

export default function Contact() {
  const [request, setRequest] = useContext(RequestContext);

  const onEmailChange = (event) => {
    setRequest({ contact: event.target.value });
  };
  
  return (
    <div>
      <h2>What is your E-mail Address?</h2>

      <input
        type="text"
        name="email"
        placeholder="Email"
        onChange={onEmailChange}
      ></input>
    </div>
  );
}
