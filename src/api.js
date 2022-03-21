const API_HOST = process.env.REACT_APP_NODE_ENV !== 'production' ? 'http://127.0.0.1:8000' : 'https://api.medicineforukraine.org';
const PUBLIC_FOLDER = process.env.PUBLIC_URL;

export const fetchCountries = async () => {
  const jsonResponse = await (await fetch(`${API_HOST}/countries`)).json();

  return jsonResponse.map(r => {
    r.flag_url = PUBLIC_FOLDER + 'img/flags/' + r.flag_url;
    return r;
  });
}

export const fetchItems = async (donationType, countryCode) => {
  const jsonResponse = await (await fetch(`${API_HOST}/items/${donationType}/${countryCode}`)).json();

  return jsonResponse.items.map(r => {
    return {id: r.row_number, name: r.item_names_by_language[countryCode], highPriority: r.is_high_priority};
  }).filter(r => r.name);
}

export const fetchLinks = async (donationType, countryCode, itemId) => {
  const jsonResponse = await (await fetch(`${API_HOST}/links/${donationType}/${countryCode}/${itemId}`)).json();

  return jsonResponse.links.map(r => {
    const url = new URL(r.url);
    return {link: r.url, domain: url.hostname};
  });
}

export const fetchAddress = async (countryCode) => {
  const jsonResponse = await (await fetch(`${API_HOST}/countries/address/${countryCode}`)).json();

  if (jsonResponse.length > 0) {
    return jsonResponse[0];
  }

  throw Error("Can't find address");
}

export const saveRequest = async (request) => {

  const stores = Object.entries(request.stores).map(([_, store]) => {
    const items = Object.entries(store.items).map(([_, item]) => {
      console.log(item);
      return {
        'url': item.url,
        'name': item.name,
        'quantity': item.quantity,
        'row_number': item.row_number,
        'type': item.type,
      }
    });

    const screenshots = Object.entries(store.screenshots).map(([_, screenshot]) => {
      return screenshot.base64;
    });

    return {
      'store_domain': store.store_domain,
      'screenshots': screenshots,
      'selected_items': items,
    }
  });

  const payload = {
    'user_agent': window.navigator.userAgent,
    'email': request.contact,
    'country_to': request.countryCode,
    'address': request.addressId,
    'selected': stores,
  }

  return await fetch(`${API_HOST}/save/`, {
    method: 'POST',
    body: JSON.stringify(payload),
  });
}