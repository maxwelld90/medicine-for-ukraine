import { createContext } from "react";

let request = {
  userContact: "",
  country: "",
  donationType: "",
  productLink: "",
  stores: {},
};

const setRequest = (newRequest) => {
  request = newRequest;
};

export const RequestContext = createContext([request, setRequest]);
