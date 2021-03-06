# Generated by Django 3.2 on 2022-03-08 23:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('houses', '0019_auto_20220307_0618'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rater',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=64)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('label', models.IntegerField(help_text='1 through 10')),
                ('rater', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='houses.rater')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ZillowSnapshot',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(primary_key=True, serialize=False)),
                ('apn', models.CharField(max_length=12)),
                ('address', models.TextField()),
                ('zillow_url', models.TextField(null=True)),
                ('scraped_address', models.TextField(null=True)),
                ('zestimate', models.IntegerField(null=True)),
                ('rent_zestimate', models.IntegerField(null=True)),
                ('price', models.IntegerField(null=True)),
                ('rent', models.IntegerField(null=True)),
                ('bedrooms', models.IntegerField(null=True)),
                ('baths', models.FloatField(null=True)),
                ('sqft', models.IntegerField(null=True)),
                ('price_history', models.JSONField(null=True)),
                ('time_scraped', models.DateTimeField(null=True)),
                ('filenames', models.JSONField(null=True)),
                ('units_info', models.JSONField(null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.DeleteModel(
            name='ZillowData',
        ),
        migrations.AddField(
            model_name='rating',
            name='zillow_snapshot',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='houses.zillowsnapshot'),
        ),
    ]
