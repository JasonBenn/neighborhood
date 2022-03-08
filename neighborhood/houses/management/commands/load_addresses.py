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
                # print(f"Missing {row['address']}")
                continue
            try:
                # {"zip_code":"94124","latitude":"37.72687542","address_number_suffix":null,"supdistpad":"10","eas_fullid":"474427-729584-568490","cnn":"2711000","longitude":"-122.39464177","street_name":"BANCROFT","supdist":"SUPERVISORIAL DISTRICT 10","eas_baseid":"474427","nhood":"Bayview Hunters Point","block":"5421","supname":"Walton","street_type":"AVE","eas_subid":"729584","lot":"024","address":"1740 BANCROFT AVE #111","unit_number":"111","supervisor":"10","address_number":"1740","parcel_number":"5421024","numbertext":"TEN"},
                Addresses.objects.create(
                    apn=row['block'] + '-' + row['lot'],
                    eas_fullid=row['eas_fullid'],
                    eas_baseid=row['eas_baseid'],
                    eas_subid=row['eas_subid'],
                    address=row['address'],
                    address_number=row['address_number'],
                    address_number_suffix=row['address_number_suffix'],
                    unit_number=row['unit_number'],
                    street_name=row['street_name'],
                    street_type=row['street_type'],
                    zip_code=row['zip_code'],
                    parcel_number=row['parcel_number'],
                )
            except:
                import ipdb;
                ipdb.set_trace()
