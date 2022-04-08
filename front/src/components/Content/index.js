import React from "react";

import Loader from "../loader";
import Error from "../error";

export default function Content({ error, loading, children }) {
  return (
    <>
      {error && <Error />}
      {loading && <Loader />}
      {!error && !loading && children()}
    </>
  );
}
