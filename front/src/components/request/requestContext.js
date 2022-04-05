import { createContext } from "react";

let request = {
  contact: "",
  country: "",
  donationType: "",
  stores: {},
};

const setRequest = (newRequest) => {
  request = newRequest;
};

export const RequestContext = createContext([request, setRequest]);
