def read_languages():
    """
    Returns a Python dictionary representing the languages defined in the root's LANGUAGES.json file.
    """
    from os import path
    from json import load
    from pathlib import Path
    root = Path(__file__).resolve().parent.parent
    
    with open(path.join(root, 'LANGUAGES.json')) as f:
        json_object = load(f)

    return json_object

def get_pelican_languages_object(site_url):
    """
    Reads in languages from the read_languages() function, and returns a dictionary suitable for Pelican to use.
    """
    languages_object = read_languages()
    return_object = {}
    
    for language_code in languages_object.keys():
        return_object[language_code] = {
            'SITENAME': languages_object[language_code]['SITENAME'],
            'SITEURL': f'{site_url}{language_code}',
            'SITEURL_ABSOLUTE': f'{site_url}{language_code}/',
            'SITELINKS': languages_object[language_code]['SITELINKS'],
        }
    
    return return_object