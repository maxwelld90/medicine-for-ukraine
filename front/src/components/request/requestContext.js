import { createContext } from "react";

let request = {
  recipientId: "",
  country: "",
  donationType: "",
  stores: {},
};

const setRequest = (newRequest) => {
  request = newRequest;
};

export const RequestContext = createContext([request, setRequest]);
