import json
import uuid

import numpy as np
import pandas as pd
import pytz
from dateutil import parser
from django.core import management
from django.core.management.base import BaseCommand
from tqdm import tqdm

from houses.models import ZillowAddresses, ZillowSnapshot
from neighborhood.settings import BASE_DIR
from utils import currency_to_int, execute_sql, format_address


class Command(BaseCommand):

    def handle(self, *args, **options):
        print('truncating ZillowData...')
        ZillowAddresses.drop()
        execute_sql("delete from houses_zillowsnapshot;")

        print('loading csv...')
        df = pd.read_csv(str(BASE_DIR / 'data/page st scraping test - main.csv'))
        RESET_DOWNLOADS_FOLDER_TIME = parser.parse("03/09/2022 21:30:42").replace(tzinfo=pytz.UTC)
        for index, row in tqdm(df.replace({np.nan: None}).iterrows()):
            if not row['zillow_url']:
                continue

            time_scraped = parser.parse(row["time_scraped"]).replace(tzinfo=pytz.UTC) if row["time_scraped"] else None
            filenames = row['filenames'].split(', ') if row['filenames'] else None
            if time_scraped >= RESET_DOWNLOADS_FOLDER_TIME and filenames:
                filenames = [f"after-{x}" for x in filenames]

            if row['apn'] == '0797-010':
                print(row['address'], filenames)

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
                    time_scraped=time_scraped,
                    filenames=filenames,
                    units_info=json.loads(row["units info"]) if row["units info"] else None,
                )
            except:
                import ipdb;
                ipdb.set_trace()

        ZillowAddresses.create()
        management.call_command("save_the_orphan_ratings")