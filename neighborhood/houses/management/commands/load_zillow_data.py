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
        df = pd.read_csv(str(BASE_DIR / 'data/2022-01-15 zillow_data.csv'))
        for index, row in tqdm(df.replace({np.nan: None}).iterrows()):
            try:
                ZillowData.objects.create(
                    apn=row['block'] + '-' + row['lot'],
                    block=row['block'],
                    lot=row['lot'],
                    zillow_url=row['Zillow URL'],
                    zestimate=currency_to_int(row["Zestimate"]) if row["Zestimate"] else None,
                    rent_zestimate=currency_to_int(row["Rent Zestimate"]) if row["Rent Zestimate"] else None,
                    rent=currency_to_int(row["Rent"]) if row["Rent"] else None,
                    bedrooms=row["Bedrooms"],
                    baths=row["Baths"],
                    sqft=currency_to_int(row["Sqft"]) if row["Sqft"] else None,
                    time_scraped=parser.parse(row["Time Scraped"]).replace(tzinfo=pytz.UTC) if row["Time Scraped"] else None,
                    price_history=json.loads(row["Price History"]) if row["Price History"] else None,
                    Label=row["Label"],
                )
            except:
                import ipdb;
                ipdb.set_trace()
