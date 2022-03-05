import json

import pandas as pd
import numpy as np
import geopandas as gpd
from django.core.management.base import BaseCommand, CommandError
from tqdm import tqdm

from houses.models import TaxAssessorData
from neighborhood.settings import BASE_DIR


class Command(BaseCommand):

    def handle(self, *args, **options):
        print('truncating TaxAssessorData...')
        TaxAssessorData.truncate()
        print('loading GEOJSON...')
        df = gpd.read_file(str(BASE_DIR / 'data/tax_assessor_property_rolls_2019.geojson'))
        for index, row in tqdm(df.replace({np.nan: None}).iterrows()):
            try:
                TaxAssessorData.objects.create(
                    apn=row['block'] + '-' + row['lot'],
                    row_id=row['row_id'],
                    block=row['block'],
                    lot=row['lot'],
                    parcel_number=row['parcel_number'],
                    property_location=row['property_location'],
                    lot_area=row['lot_area'],
                    property_area=row['property_area'],
                    basement_area=row['basement_area'],
                    number_of_units=row['number_of_units'],
                    number_of_stories=row['number_of_stories'],
                    number_of_rooms=row['number_of_rooms'],
                    number_of_bedrooms=row['number_of_bedrooms'],
                    number_of_bathrooms=row['number_of_bathrooms'],
                    lot_depth=row['lot_depth'],
                    lot_frontage=row['lot_frontage'],
                    use_code=row['use_code'],
                    property_class_code=row['property_class_code'],
                    year_property_built=row['year_property_built'],
                    percent_of_ownership=row['percent_of_ownership'],
                    exemption_code=row['exemption_code'],
                    assessed_land_value=row['assessed_land_value'],
                    assessed_improvement_value=row['assessed_improvement_value'],
                    assessed_fixtures_value=row['assessed_fixtures_value'],
                )
            except:
                import ipdb; ipdb.set_trace()
