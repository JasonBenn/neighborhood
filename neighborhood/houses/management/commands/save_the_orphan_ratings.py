from django.core.management.base import BaseCommand
from tqdm import tqdm

from houses.models import Rating, ZillowAddresses


class Command(BaseCommand):

    def handle(self, *args, **options):
        for rating in tqdm(Rating.objects.filter(zillow_snapshot_id=None)):
            rating.zillow_snapshot_id = ZillowAddresses.objects.filter(scraped_address=rating.zillow_scraped_address).order_by('created').last().id
            rating.save()