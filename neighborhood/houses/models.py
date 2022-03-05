from django.db import connection, models


class BaseModel(models.Model):
    class Meta:
        abstract = True

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    @classmethod
    def truncate(cls):
        with connection.cursor() as cursor:
            cursor.execute('TRUNCATE TABLE {} CASCADE'.format(cls._meta.db_table))


class TaxAssessorData(BaseModel):
    """https://data.sfgov.org/Housing-and-Buildings/Assessor-Historical-Secured-Property-Tax-Rolls/wv5m-vpq2"""

    # ID
    row_id = models.TextField(primary_key=True)
    block = models.CharField(max_length=6)  # 5
    lot = models.CharField(max_length=6)  # 4
    apn = models.CharField(max_length=12)
    parcel_number = models.CharField(max_length=12)

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
