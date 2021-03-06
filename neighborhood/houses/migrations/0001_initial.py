# Generated by Django 3.2 on 2022-03-05 21:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TaxAssessorData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('row_id', models.TextField()),
                ('block', models.CharField(max_length=6)),
                ('lot', models.CharField(max_length=6)),
                ('parcel_number', models.CharField(max_length=12)),
                ('lot_area', models.IntegerField()),
                ('property_area', models.IntegerField()),
                ('basement_area', models.IntegerField()),
                ('number_of_units', models.IntegerField()),
                ('number_of_stories', models.FloatField()),
                ('number_of_rooms', models.IntegerField()),
                ('number_of_bedrooms', models.FloatField()),
                ('number_of_bathrooms', models.FloatField()),
                ('lot_depth', models.IntegerField(help_text='Depth of lot in linear feet')),
                ('lot_frontage', models.IntegerField(help_text='Linear footage of front facing side of lot (front foot)')),
                ('use_code', models.CharField(help_text='https://data.sfgov.org/Housing-and-Buildings/Reference-Assessor-Recorder-Property-Class-Codes/pa56-ek2h', max_length=6)),
                ('property_class_code', models.CharField(help_text='https://data.sfgov.org/Housing-and-Buildings/Reference-Assessor-Recorder-Property-Class-Codes/pa56-ek2h', max_length=6)),
                ('year_property_built', models.IntegerField()),
                ('percent_of_ownership', models.FloatField()),
                ('exemption_code', models.CharField(help_text='https://data.sfgov.org/Housing-and-Buildings/Reference-Assessor-Recorder-Exemption-Codes/g77e-ikb4', max_length=3)),
                ('assessed_land_value', models.IntegerField()),
                ('assessed_improvement_value', models.IntegerField()),
                ('assessed_fixtures_value', models.IntegerField()),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
