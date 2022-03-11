const API_HOST = process.env.NODE_ENV !== 'production' ? 'http://127.0.0.1:8000' : 'https://api.medicineforukraine.org';
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
    });
}

export const fetchLinks = async (donationType, countryCode, itemId) => {
    const jsonResponse = await (await fetch(`${API_HOST}/links/${donationType}/${countryCode}/${itemId}`)).json();

    return jsonResponse.links.map(r => {
        const url = new URL(r.url);
        return {link: r.url, name: url.hostname};
    });
}

export const saveRequest = async (request) => {
    const formData = new FormData();
    formData.append('email', request.contact);
    formData.append('countryCode', request.countryCode);
    formData.append('donationType', request.donationType);

    // formData.append('files', selectedFile);
    //@TODO
    console.log('@TODO implement sending request to backend', request);
    console.log(formData);

    return await fetch(`${API_HOST}/request`, {
        method: 'POST',
        body: formData,
    });
}