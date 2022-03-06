import re

from uuid import UUID

import json

import pandas as pd
import numpy as np
import geopandas as gpd
from django.core.management.base import BaseCommand, CommandError
from tqdm import tqdm

from houses.models import NeighborhoodBuildings, TaxAssessorData, ZONE_LOOKUP
from neighborhood.settings import BASE_DIR


class Command(BaseCommand):

    def handle(self, *args, **options):
        print('truncating NeighborhoodBuildings...')
        NeighborhoodBuildings.truncate()
        print('loading csv...')
        df = pd.read_csv(str(BASE_DIR / 'data/dbv_buildings_zones.csv'))
        for index, row in tqdm(df.iterrows()):
            if row['mblr'].startswith("CN"):
                continue
            try:
                matches = re.match('SF(\d{4})([\d\w]{3,4})', row['mblr'])
                apn = matches.group(1) + '-' + matches.group(2)
                NeighborhoodBuildings.objects.create(
                    global_id=UUID(row['globalid'][1:-1]),
                    apn=apn,
                    geometry=row['WKT'],
                    mblr=row['mblr'],
                    zone=ZONE_LOOKUP[row['Name']],
                )
            except:
                import ipdb; ipdb.set_trace()
