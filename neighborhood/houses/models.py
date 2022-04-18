from django.contrib.gis.db import models
from django.db.models import BooleanField

from utils import execute_sql


class BaseModel(models.Model):
    class Meta:
        abstract = True

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class TaxAssessorData(BaseModel):
    """https://data.sfgov.org/Housing-and-Buildings/Assessor-Historical-Secured-Property-Tax-Rolls/wv5m-vpq2"""

    # ID
    row_id = models.TextField(primary_key=True)
    block = models.CharField(max_length=6)  # 5
    lot = models.CharField(max_length=6)  # 4
    apn = models.CharField(max_length=12)
    parcel_number = models.CharField(max_length=12)
    property_location = models.TextField()

    # Size
    lot_area = models.IntegerField()
    property_area = models.IntegerField()
    basement_area = models.IntegerField(null=True)
    number_of_units = models.IntegerField()
    number_of_stories = models.FloatField()
    number_of_rooms = models.IntegerField()
    number_of_bedrooms = models.FloatField()
    number_of_bathrooms = models.FloatField()
    lot_depth = models.IntegerField(help_text="Depth of lot in linear feet")
    lot_frontage = models.IntegerField(help_text="Linear footage of front facing side of lot (front foot)")

    # Use
    use_code = models.CharField(max_length=6, null=True, help_text="https://data.sfgov.org/Housing-and-Buildings/Reference-Assessor-Recorder-Property-Class-Codes/pa56-ek2h")
    property_class_code = models.CharField(max_length=6, help_text="https://data.sfgov.org/Housing-and-Buildings/Reference-Assessor-Recorder-Property-Class-Codes/pa56-ek2h")

    # Niceness
    year_property_built = models.IntegerField(null=True)

    # Ownership, taxes, value
    current_sales_date = models.DateTimeField(null=True)
    percent_of_ownership = models.FloatField()
    exemption_code = models.CharField(max_length=3, help_text="https://data.sfgov.org/Housing-and-Buildings/Reference-Assessor-Recorder-Exemption-Codes/g77e-ikb4")
    assessed_land_value = models.IntegerField()
    assessed_improvement_value = models.IntegerField()
    assessed_fixtures_value = models.IntegerField()


class Zone(models.IntegerChoices):
    PAGE_ST = 1
    DUBOCE_CULDESACS = 2
    EAST_OF_DUBOCE = 3
    EAST_HILL = 4
    DUBOCE_TRIANGLE_BEST = 5
    NORTH_BUENA_VISTA = 6
    ALAMO_SQUARE = 7
    OAK_AND_FELL = 8
    DUBOCE_TRIANGLE_REST = 9
    ASHBURY_HEIGHTS = 10
    NOPA = 11
    NORTH_CORONA_HEIGHTS = 12
    HAIGHT_ST = 13
    EAST_OF_ALAMO = 14
    CORONA_HEIGHTS = 15
    NORTH_MISSION = 16


class NeighborhoodBuildings(BaseModel):
    class Meta:
        unique_together = ["global_id", "zone"]

    global_id = models.UUIDField()
    apn = models.CharField(max_length=12)
    geometry = models.TextField()
    mblr = models.CharField(max_length=15)
    zone = models.IntegerField(choices=Zone.choices)


ZONE_LOOKUP = {
    'Page St': Zone.PAGE_ST,
    'Duboce Culdesacs': Zone.DUBOCE_CULDESACS,
    'East of Duboce': Zone.EAST_OF_DUBOCE,
    'East Hill': Zone.EAST_HILL,
    'Duboce Triangle (the best)': Zone.DUBOCE_TRIANGLE_BEST,
    'North Buena Vista': Zone.NORTH_BUENA_VISTA,
    'Alamo Square': Zone.ALAMO_SQUARE,
    'Oak & Fell': Zone.OAK_AND_FELL,
    'Duboce Triangle (the rest)': Zone.DUBOCE_TRIANGLE_REST,
    'Ashbury Heights': Zone.ASHBURY_HEIGHTS,
    'NoPa': Zone.NOPA,
    'North Corona Heights': Zone.NORTH_CORONA_HEIGHTS,
    'Haight St': Zone.HAIGHT_ST,
    'East of Alamo': Zone.EAST_OF_ALAMO,
    'Corona Heights': Zone.CORONA_HEIGHTS,
    'North Mission': Zone.NORTH_MISSION,
}


class Owners(BaseModel):
    property_id = models.IntegerField(primary_key=True)
    apn = models.CharField(max_length=12)

    # owners
    owner_name = models.TextField(null=True)
    owner_1_full_name = models.TextField(null=True)
    owner_2_full_name = models.TextField(null=True)
    do_not_mail = BooleanField()
    site_address = models.TextField(null=True)
    mailing_address = models.TextField(null=True)
    legal_description = models.TextField(null=True)

    lot_sqft = models.IntegerField(null=True)
    total_sqft = models.IntegerField(null=True)
    year_built = models.IntegerField(null=True)
    total_stories = models.FloatField(null=True)
    comm_num_units = models.IntegerField(null=True)
    res_full_baths = models.IntegerField(null=True)
    res_half_baths = models.IntegerField(null=True)
    parking_count = models.IntegerField(null=True)
    parking_sqft = models.IntegerField(null=True)
    parking_desc = models.CharField(max_length=64, null=True)

    improvement_value = models.IntegerField(null=True)
    land_value = models.IntegerField(null=True)
    total_assessed_value = models.IntegerField(null=True)
    tax_amount = models.IntegerField(null=True)

    ot_sale_date = models.DateField(null=True)
    ot_sale_price = models.IntegerField(null=True)
    ot_deed_type = models.CharField(max_length=128, null=True)
    ot_sale_recording_date = models.DateField(null=True)

    market_sale_date = models.DateField(null=True)
    market_sale_price = models.IntegerField(null=True)
    market_sale_recording_date = models.DateField(null=True)

    prior_sale_date = models.DateField(null=True)
    prior_sale_price = models.IntegerField(null=True)
    prior_sale_recording_date = models.DateField(null=True)


class ZillowSnapshot(BaseModel):
    id = models.UUIDField(primary_key=True)
    apn = models.CharField(max_length=12)
    address = models.TextField()
    zillow_url = models.TextField(null=True)
    scraped_address = models.TextField(null=True)
    zestimate = models.IntegerField(null=True)
    rent_zestimate = models.IntegerField(null=True)
    price = models.IntegerField(null=True)
    rent = models.IntegerField(null=True)
    bedrooms = models.IntegerField(null=True)
    baths = models.FloatField(null=True)
    sqft = models.IntegerField(null=True)
    price_history = models.JSONField(null=True)
    time_scraped = models.DateTimeField(null=True)
    filenames = models.JSONField(null=True)
    units_info = models.JSONField(null=True)


class ZillowAddresses(ZillowSnapshot):
    class Meta:
        managed = False
        db_table = 'zillow_addresses'

    @classmethod
    def drop(cls):
        execute_sql("DROP MATERIALIZED VIEW zillow_addresses;")

    @classmethod
    def create(cls):
        execute_sql("""CREATE MATERIALIZED VIEW zillow_addresses as (
                select distinct on (scraped_address) *
                from houses_zillowsnapshot
                order by scraped_address, time_scraped desc);
                """)


class Addresses(BaseModel):
    apn = models.CharField(max_length=12)
    eas_fullid = models.CharField(max_length=20)
    eas_baseid = models.CharField(max_length=6)
    eas_subid = models.CharField(max_length=6)
    address = models.TextField()
    address_number = models.CharField(max_length=16, null=True)
    address_number_suffix = models.CharField(max_length=16, null=True)
    street_name = models.CharField(max_length=64, null=True)
    street_type = models.CharField(max_length=16, null=True)
    unit_number = models.CharField(max_length=16, null=True)
    zip_code = models.IntegerField()
    parcel_number = models.CharField(max_length=32, null=True)


class Rater(BaseModel):
    name = models.CharField(max_length=64)


class Rating(BaseModel):
    rater = models.ForeignKey(Rater, on_delete=models.SET_NULL, null=True)
    zillow_snapshot = models.ForeignKey(ZillowSnapshot, on_delete=models.SET_NULL, null=True)
    zillow_scraped_address = models.TextField()
    value = models.IntegerField(null=True, help_text="1 through 10, or None if not enough info to tell")


class AssessorClassCodes(BaseModel):
    use_code = models.CharField(max_length=4)
    use_definition = models.TextField()
    property_class_code = models.CharField(max_length=4)
    property_class_definition = models.TextField()


class Person(BaseModel):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    location = models.PointField()

    def __str__(self):
        return self.first_name + " " + self.last_name


class Building(BaseModel):
    name = models.CharField(max_length=64)
    location = models.PointField()

    def __str__(self):
        return self.name
