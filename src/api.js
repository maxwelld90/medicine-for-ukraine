const API_HOST = process.env.NODE_ENV !== 'production' ? 'http://127.0.0.1:8000' : 'https://api.medicineforukraine.org';
const PUBLIC_FOLDER = process.env.PUBLIC_URL;

export const fetchCountries = async () => {
    return [
        {name: "Spain", flag_url: `${PUBLIC_FOLDER}img/flags/es.svg`},
        {name: "Poland", flag_url: `${PUBLIC_FOLDER}img/flags/pl.svg`},
    ];

    // @TODO uncomment when API will be available
    // return await (await fetch(`${API_HOST}/countries`)).json();
}

export const fetchItems = async (donationType, country) => {
    return await fetch(`${API_HOST}/items/${donationType}/${country}`);
}

export const fetchLinks = async (donationType, country, itemId) => {
    return await fetch(`${API_HOST}/links/${donationType}/${country}/${itemId}`);
}