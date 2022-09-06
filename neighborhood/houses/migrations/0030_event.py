# Generated by Django 4.0 on 2022-04-19 01:29

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('houses', '0029_building'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=64)),
                ('location', django.contrib.gis.db.models.fields.PointField(srid=4326)),
                ('when', models.DateTimeField()),
                ('building', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='houses.building')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]