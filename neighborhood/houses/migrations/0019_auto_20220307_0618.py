# Generated by Django 3.2 on 2022-03-07 06:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('houses', '0018_alter_addresses_parcel_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='addresses',
            name='address_number',
            field=models.CharField(max_length=16, null=True),
        ),
        migrations.AddField(
            model_name='addresses',
            name='address_number_suffix',
            field=models.CharField(max_length=16, null=True),
        ),
        migrations.AddField(
            model_name='addresses',
            name='eas_baseid',
            field=models.CharField(default='DELETE', max_length=6),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='addresses',
            name='eas_fullid',
            field=models.CharField(default='DELETE', max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='addresses',
            name='eas_subid',
            field=models.CharField(default='DELETE', max_length=6),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='addresses',
            name='street_name',
            field=models.CharField(max_length=64, null=True),
        ),
        migrations.AddField(
            model_name='addresses',
            name='street_type',
            field=models.CharField(max_length=16, null=True),
        ),
        migrations.AlterField(
            model_name='addresses',
            name='unit_number',
            field=models.CharField(max_length=16, null=True),
        ),
    ]
