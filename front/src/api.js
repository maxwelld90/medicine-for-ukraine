import { getStaticPath } from "./helpers";

const API_HOST =
  process.env.REACT_APP_NODE_ENV !== "production"
    ? "http://127.0.0.1:8000"
    : "https://api.medicineforukraine.org";

export const fetchRecipients = async () => {
  const { recipients } = await (await fetch(`${API_HOST}/recipients`)).json();

  return recipients.map((r) => {
    r.warehouse_country = {
      ...r.warehouse_country,
      flag_url: getStaticPath("/img/flags/" + r.warehouse_country.flag_url),
    };
    return r;
  });
};

export const fetchItems = async (recipientId) => {
  const jsonResponse = await (
    await fetch(`${API_HOST}/items/${recipientId}`)
  ).json();

  return jsonResponse.items.map((r) => {
    return {
      id: r.row_number,
      names: r.item_name_by_language,
      highPriority: r.is_high_priority,
      lowestPrice: r.lowest_price,
    };
  });
};

// export const fetchItems = async (donationType, countryCode) => {
//   const jsonResponse = await (
//     await fetch(`${API_HOST}/items/${donationType}/${countryCode}`)
//   ).json();

//   return jsonResponse.items.map((r) => {
//     return {
//       id: r.row_number,
//       names: r.item_names_by_language,
//       highPriority: r.is_high_priority,
//       lowestPrice: r.lowest_price,
//     };
//   });
// };

export const fetchLinks = async (recipientId, itemId) => {
  const jsonResponse = await (
    await fetch(`${API_HOST}/links/${recipientId}/${itemId}`)
  ).json();

  const { warehouse_address } = await fetchAddress(recipientId);

  warehouse_address.country.flag_url = getStaticPath(
    "/img/flags/" + warehouse_address.country.flag_url
  );

  return {
    country: warehouse_address.country,
    links: jsonResponse.links.map(({ url }) => ({
      link: url,
      domain: new URL(url).hostname,
    })),
  };
};

export const fetchAddress = async (recipientId) => {
  const jsonResponse = await (
    await fetch(`${API_HOST}/recipients/address/${recipientId}`)
  ).json();

  return jsonResponse;
};

function getSelectedObjects(value) {
  return Object.values(value.stores).map(
    ({ items, screenshots, store_domain }) => {
      return {
        store_domain,
        screenshots: screenshots.map((v) => v.base64),
        selected_items: Object.values(items).map(
          ({ url, name, quantity, row_number }) => ({
            url,
            name,
            quantity,
            row_number,
          })
        ),
      };
    }
  );
}

export const saveRequest = (request) => {
  const payload = {
    user_agent: window.navigator.userAgent,
    recipient_id: request.recipientId,
    selected: getSelectedObjects(request),
  };

  return fetch(`${API_HOST}/save/`, {
    method: "POST",
    body: JSON.stringify(payload),
  });
};
