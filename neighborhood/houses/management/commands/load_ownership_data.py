from glob import glob

import numpy as np
import pandas as pd
import re
from django.core.management.base import BaseCommand
from tqdm import tqdm

from houses.models import Owners
from neighborhood.settings import BASE_DIR
from utils import currency_to_int, parse_date


class Command(BaseCommand):

    def handle(self, *args, **options):
        print('truncating Owners...')
        Owners.truncate()
        print('loading csv...')
        csv_files = glob(str(BASE_DIR / 'data/mls_*/*.csv'))
        print(f'processing {len(csv_files)} files...')
        for csv_file in csv_files:
            df = pd.read_csv(str(csv_file))
            for index, row in tqdm(df.replace({np.nan: None}).iterrows()):
                try:
                    Owners.objects.update_or_create(
                        property_id=row['PropertyID'],
                        defaults=dict(
                            apn=row['APN'],
                            owner_name=row['OwnerName'],
                            owner_1_full_name=row['Owner1FullName'],
                            owner_2_full_name=row['Owner2FullName'],
                            do_not_mail=bool(row['DoNotMail']),
                            site_address=row['SiteStreetAddress'],
                            mailing_address=row['MailingStreetAddress'],
                            legal_description=row['LegalDescription'],

                            lot_sqft=row['LotSq.Ft.'],
                            total_sqft=row['TotalSq.Ft.'],
                            year_built=row['YearBuilt'],
                            total_stories=row['TotalStories'],
                            comm_num_units=row['Comm.#ofUnits'],
                            res_full_baths=row['Res.FullBaths'],
                            res_half_baths=row['Res.HalfBaths'],
                            parking_count=row['ParkingCount'],
                            parking_sqft=row['ParkingSqFt'],
                            parking_desc=row['ParkingDesc'],

                            improvement_value=currency_to_int(row['ImprovementValue']) if row['ImprovementValue'] else None,
                            land_value=currency_to_int(row['LandValue']) if row['LandValue'] else None,
                            total_assessed_value=currency_to_int(row['TotalAssessedValue']) if row['TotalAssessedValue'] else None,
                            tax_amount=currency_to_int(row['TaxAmount']) if row['TaxAmount'] else None,

                            ot_sale_date=parse_date(row['OTSaleDate']) if row['OTSaleDate'] else None,
                            ot_sale_price=currency_to_int(row['OTSalePrice']) if row['OTSalePrice'] else None,
                            ot_deed_type=row['OTDeedType'],
                            ot_sale_recording_date=parse_date(row['OTRecordingDate']) if row['OTRecordingDate'] else None,

                            market_sale_date=parse_date(row['LastMarketSaleDate']) if row['LastMarketSaleDate'] else None,
                            market_sale_price=currency_to_int(row['LastMarketSalePrice']) if row['LastMarketSalePrice'] else None,
                            market_sale_recording_date=parse_date(row['LastMarketSaleRecordingDate']) if row['LastMarketSaleRecordingDate'] else None,

                            prior_sale_date=parse_date(row['PriorSaleDate']) if row['PriorSaleDate'] else None,
                            prior_sale_price=currency_to_int(row['PriorSalePrice']) if row['PriorSalePrice'] else None,
                            prior_sale_recording_date=parse_date(row['PriorSaleRecordingDate']) if row['PriorSaleRecordingDate'] else None,
                        )
                    )
                except:
                    import ipdb;
                    ipdb.set_trace()
