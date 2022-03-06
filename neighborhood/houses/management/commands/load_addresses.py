import geopandas as gpd
from django.core.management.base import BaseCommand
from tqdm import tqdm

from houses.models import Addresses
from neighborhood.settings import BASE_DIR


class Command(BaseCommand):

    def handle(self, *args, **options):
        print('truncating Addresses...')
        Addresses.truncate()
        print('loading csv...')
        df = gpd.read_file(str(BASE_DIR / 'data/Addresses with Units - Enterprise Addressing System.geojson'))
        for index, row in tqdm(df.iterrows()):
            if row['block'] is None or row['lot'] is None:
                print(f"Missing {row['address']}")
                continue
            try:
                Addresses.objects.create(
                    apn=row['block'] + '-' + row['lot'],
                    address=row['address']
                )
            except:
                import ipdb;
                ipdb.set_trace()
