import pandas as pd
from django.core.management.base import BaseCommand
from tqdm import tqdm

from houses.models import AssessorClassCodes
from neighborhood.settings import BASE_DIR


class Command(BaseCommand):

    def handle(self, *args, **options):
        AssessorClassCodes.objects.all().delete()
        df = pd.read_csv(str(BASE_DIR / 'data/Reference__Assessor-Recorder_Property_Class_Codes.csv'))
        for index, row in tqdm(df.iterrows()):
            AssessorClassCodes.objects.create(
                use_code=row['Use Code'],
                use_definition=row['Use Definition'],
                property_class_code=row['Class Code'],
                property_class_definition=row['Class Definition'],
            )
