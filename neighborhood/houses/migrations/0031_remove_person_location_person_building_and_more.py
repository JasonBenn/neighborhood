# Generated by Django 4.0 on 2022-04-25 00:40

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('houses', '0030_event'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='person',
            name='location',
        ),
        migrations.AddField(
            model_name='person',
            name='building',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='houses.building'),
        ),
        migrations.AlterField(
            model_name='event',
            name='building',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='houses.building'),
        ),
        migrations.AlterField(
            model_name='event',
            name='location',
            field=django.contrib.gis.db.models.fields.PointField(blank=True, srid=4326),
        ),
    ]