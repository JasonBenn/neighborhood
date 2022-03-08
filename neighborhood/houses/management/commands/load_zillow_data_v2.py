import json

import pandas as pd
import numpy as np
import pytz
from django.core.management.base import BaseCommand
from tqdm import tqdm

from houses.models import ZillowData
from neighborhood.settings import BASE_DIR
from utils import currency_to_int
from dateutil import parser



class Command(BaseCommand):

    def handle(self, *args, **options):
        print('truncating ZillowData...')
        ZillowData.truncate()
        print('loading csv...')
        df = pd.read_csv(str(BASE_DIR / 'page st scraping test.csv'))
        for index, row in tqdm(df.replace({np.nan: None}).iterrows()):
            try:
                ZillowData.objects.create(
                    apn=row['apn'],
                    address=row['address'],
                    scraped_address=row['scraped_address'],
                    zillow_url=row['zillow_url'],
                    zestimate=currency_to_int(row["zestimate"]) if row["zestimate"] else None,
                    rent_zestimate=currency_to_int(row["rent_zestimate"]) if row["rent_zestimate"] else None,
                    rent=currency_to_int(row["rent"]) if row["Rent"] else None,
                    bedrooms=row["bedrooms"],
                    baths=row["baths"],
                    sqft=currency_to_int(row["sqft"]) if row["sqft"] else None,
                    time_scraped=parser.parse(row["time_scraped"]).replace(tzinfo=pytz.UTC) if row["time_scraped"] else None,
                    price_history=json.loads(row["price_history"]) if row["price_history"] else None,
                    num_units=row['num_units'],
                    filenames=row['filenames'],
                    label=row["label"],
                )
            except:
                import ipdb;
                ipdb.set_trace()
