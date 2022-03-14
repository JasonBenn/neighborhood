from django.core.management.base import BaseCommand

from utils import execute_sql


class Command(BaseCommand):

    def handle(self, *args, **options):
        execute_sql("""update houses_rating rating
        set zillow_snapshot_id = (
        select id from zillow_addresses add
        where rating.zillow_scraped_address = add.scraped_address
        );
        """)
