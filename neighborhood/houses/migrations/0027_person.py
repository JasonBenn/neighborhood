# Generated by Django 3.2 on 2022-04-18 20:59

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('houses', '0026_zillowaddresses'),
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('first_name', models.CharField(max_length=64)),
                ('last_name', models.CharField(max_length=64)),
                ('location', django.contrib.gis.db.models.fields.MultiPointField(srid=4326)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]