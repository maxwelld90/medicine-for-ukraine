const API_HOST = process.env.NODE_ENV !== 'production' ? 'http://127.0.0.1:8000' : 'https://api.medicineforukraine.org';
const PUBLIC_FOLDER = process.env.PUBLIC_URL;

export const fetchCountries = async () => {
    // @TODO uncomment when API will be available
    // const jsonResponse = await (await fetch(`${API_HOST}/countries`)).json();

    // @TODO remove when API will be available
    const jsonResponse = [
        {name: "Spain", flag_url: `${PUBLIC_FOLDER}img/flags/es.svg`},
        {name: "Poland", flag_url: `${PUBLIC_FOLDER}img/flags/pl.svg`},
    ];

    return jsonResponse;
}

export const fetchItems = async (donationType, country) => {
    // @TODO uncomment when API will be available
    // const jsonResponse = await (await fetch(`${API_HOST}/items/${donationType}/${country}`)).json();

    // @TODO remove when API will be available
    const jsonResponse =  {"items":[{"row_number":0,"item_names_by_language":{"EN":"Hemostatic Celox","UA,RU":"Кровоoстанавливающее (любой Celox кроме порошка и гранул)","ES":"Hemostática rápida Celox","PL":"Opatrunek hemostatycznyч","FR":"Pansements hémostatiques rapides","NL":"Snellen hemostatische verbanden","CZE":"Hemostatická gáza na zastavení krvácení","RO":""},"is_high_priority":true},{"row_number":2,"item_names_by_language":{"EN":"Sam Junction Tourniquet","UA,RU":"Турнікети для критичних кровотеч","ES":"Torniquetes nodales para sangrado pélvico","PL":"Opaska zaciskowa SAM","FR":"Tourniquets nodaux pour saignement pelvien (garrot médicaux)","NL":"Nodale tourniquet voor bekkenbloeding","CZE":"škrtidlo","RO":""},"is_high_priority":false},{"row_number":3,"item_names_by_language":{"EN":"Sam Pelvic Sling","UA,RU":"Шини для поранень тазу з роздувними манжетами","ES":"Férulas pélvicas","PL":"Pas Sam Pelvic Sling","FR":"Garrot ceinture pelvienne","NL":"Bekkenslinger","CZE":"Pánevní pás SAM Pelvic Sling","RO":""},"is_high_priority":false},{"row_number":4,"item_names_by_language":{"EN":"ambu pocket bvm\n","UA,RU":"Кишеньковий компактний реаніматор BVM","ES":"Resucitador Plegable BVM\n","PL":"BVM Pocket Resuscytator Kompaktowy","FR":"Insufflateur portable BVM","NL":"Zakbeademingsapparaat BVM","CZE":"Kapesní resuscitační vak BVM","RO":""},"is_high_priority":false},{"row_number":5,"item_names_by_language":{"EN":"bandage israelienne","UA,RU":"Ізраїльські бандажі 4\", 6\", 12\"","ES":"Vendaje de emergencia israeli","PL":"Israeli Battle Bandages","FR":"bandage israelienne","NL":"Israëlische verband","CZE":"Izraelský tlakový obvaz","RO":""},"is_high_priority":false},{"row_number":6,"item_names_by_language":{"EN":"Bandages","UA,RU":"Бандажи","ES":"Vendaje hemostático","PL":"bandaż hemostatyczny","FR":"Bandages","NL":"Verbanden","CZE":"Obvazy","RO":""},"is_high_priority":false},{"row_number":7,"item_names_by_language":{"EN":"Anti-burn","UA,RU":"Противоожоговые","ES":"Medicamentos anti-quemaduras","PL":"Ochrona przed poparzeniem","FR":"Médicaments anti-brûlures","NL":"Anti-brandwonden","CZE":"Popáleninové gely (waterjel) a krytí","RO":""},"is_high_priority":false},{"row_number":8,"item_names_by_language":{"EN":"Rescue Hyfin Vent Seal","UA,RU":"Оклюзійні наліпки (з клапаном і без)\n","ES":"Oclusivo sello de pecho no ventilado adhesivo vendaje ","PL":"Rescue Hyfin Vent","FR":"Pansements occlusifs étanches pour blessure à la poitrine Hyfin Vent","NL":"Borstafsluiters Hyfin Ven","CZE":"Hrudní chlopeň Hyfin Ven","RO":""},"is_high_priority":false},{"row_number":10,"item_names_by_language":{"EN":"Quickclot stop bleeding 5x faster","UA,RU":"Марлеві пов'язки для зупинення кровотечі Quickclot","ES":"Vendas de gasa Quikclot","PL":"Bandaże z gazy Quikclot","FR":"Gaze de coagulation Quickclot","NL":"Quickclot stollingsgaas","CZE":"Gáza s rychlou srážlivosti (Quickclot stop bleeding 5x faster)","RO":""},"is_high_priority":false},{"row_number":11,"item_names_by_language":{"EN":" foil mylar rescue blanket","UA,RU":"рятувальна ковдра з фольги","ES":"Manta térmica de Emergencia","PL":"koc ratunkowy","FR":"Couverture de survie Mylar","NL":"Mylar reddingsdeken","CZE":"Izotermická záchranná přikrývka z hliníkové fólie Mylar","RO":""},"is_high_priority":false},{"row_number":14,"item_names_by_language":{"EN":"pulse oximeter","UA,RU":"пульсометр","ES":"pulsómetro","PL":"pulsoksimetr","FR":"pulsomètre","NL":"pulsoximeter","CZE":"pulzní oxymetr","RO":""},"is_high_priority":false},{"row_number":15,"item_names_by_language":{"EN":"kit for cardiopulmonary resuscitation\n","UA,RU":"набор для сердечно легочной реанимации","ES":"equipo de resucitación cardiopulmonar","PL":"zestaw do resuscytacji krążeniowo-oddechowej","FR":"Kit de ressuscitation cardio-pulmonaire","NL":"Cardiopulmonale reanimatie kit","CZE":"Kardiopulmonární resuscitační sada","RO":""},"is_high_priority":false},{"row_number":16,"item_names_by_language":{"EN":"intubation kit","UA,RU":"набор для интубации","ES":"kit de intubación","PL":"zestaw do intubacji","FR":"Kit d'intubation","NL":"Intubatie kit","CZE":"Intubační souprava ","RO":""},"is_high_priority":false},{"row_number":17,"item_names_by_language":{"EN":"locking collar\n","UA,RU":"фиксирующий воротник","ES":"collarín de fijación","PL":"Regulowany kołnierz szyjny","FR":"Collier cervical ajustable","NL":"Verstelbare vergrendelingskraag","CZE":"fixační krční límec","RO":""},"is_high_priority":false},{"row_number":23,"item_names_by_language":{"EN":"IGel size 4, 5, 6  (adult size)\n","UA,RU":"IGel розміри 4, 5, 6  (дорослі)","ES":"Dispositivo supraglótico I-gel  o King -LT  ( tamaño adultos)","PL":"Maska krtaniowa żelowa I-GEL (rozmiar dla dorosłych)","FR":"Canule supraglottique I-GEL (taille adulte)","NL":"Supraglottische canule, maat volwassene","CZE":"Supraglotické zajištění dýchacích cest - IGel size 4, 5, 6  (pro dospělé)","RO":""},"is_high_priority":false},{"row_number":24,"item_names_by_language":{"EN":"splints for limbs","UA,RU":"Шини для кінцівок","ES":"férulas para las extremidades","PL":"szyna na kończyny","FR":"Attelle pour membres ","NL":"Spalken voor ledematen","CZE":"dlahy na končetiny","RO":""},"is_high_priority":false}],"df_str":"meds","count":16};

    // @TODO remove hardcode when country code will be added
    const countryCode = 'EN';

    return jsonResponse.items.map(r => {
        return {id: r.row_number, name: r.item_names_by_language[countryCode], highPriority: r.is_high_priority};
    });
}

export const fetchLinks = async (donationType, country, itemId) => {
    return await fetch(`${API_HOST}/links/${donationType}/${country}/${itemId}`);
}