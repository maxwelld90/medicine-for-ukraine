import os
from medicine_api.readers.price_reader import PriceReader


if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api.settings')
    import django
    django.setup()
    from medicine_api.models import LinkMetadata

    price_reader = PriceReader(using_cache=True)
    df_prices = price_reader.get_prices()
    
    for row in df_prices.itertuples():
        metadata_object = LinkMetadata()
        metadata_object.set_from_named_tuple(row)