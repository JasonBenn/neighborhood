# Generated by Django 3.2 on 2022-03-07 01:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('houses', '0016_rename_label_zillowdata_label'),
    ]

    operations = [
        migrations.AddField(
            model_name='addresses',
            name='parcel_number',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='addresses',
            name='unit_number',
            field=models.CharField(max_length=64, null=True),
        ),
        migrations.AddField(
            model_name='addresses',
            name='zip_code',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
