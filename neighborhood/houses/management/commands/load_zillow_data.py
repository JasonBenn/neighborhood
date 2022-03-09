import json
import uuid

import pandas as pd
import numpy as np
import pytz
from django.core.management.base import BaseCommand
from tqdm import tqdm

from houses.models import ZillowSnapshot
from neighborhood.settings import BASE_DIR
from utils import currency_to_int, format_address
from dateutil import parser


class Command(BaseCommand):

    def handle(self, *args, **options):
        print('truncating ZillowData...')
        ZillowSnapshot.truncate()
        print('loading csv...')
        df = pd.read_csv(str(BASE_DIR / 'data/page st scraping test - main.csv'))
        for index, row in tqdm(df.replace({np.nan: None}).iterrows()):
            if not row['zillow_url']:
                continue
            try:
                ZillowSnapshot.objects.create(
                    id=uuid.uuid4(),
                    apn=row['apn'],
                    address=format_address(row['address']) if row['address'] else None,
                    zillow_url=row['zillow_url'],
                    scraped_address=format_address(row['scraped address']),
                    zestimate=currency_to_int(row["zestimate"]) if row["zestimate"] else None,
                    rent_zestimate=currency_to_int(row["rent_zestimate"]) if row["rent_zestimate"] else None,
                    price=currency_to_int(row["price"]) if row["price"] else None,
                    rent=currency_to_int(row["rent"]) if row["rent"] else None,
                    bedrooms=row["bedrooms"],
                    baths=row["baths"],
                    sqft=currency_to_int(row["sqft"]) if row["sqft"] else None,
                    price_history=json.loads(row["price_history"]) if row["price_history"] else None,
                    time_scraped=parser.parse(row["time_scraped"]).replace(tzinfo=pytz.UTC) if row["time_scraped"] else None,
                    filenames=row['filenames'].split(', ') if row['filenames'] else None,
                    units_info=json.loads(row["units info"]) if row["units info"] else None,
                )
            except:
                import ipdb;
                ipdb.set_trace()
