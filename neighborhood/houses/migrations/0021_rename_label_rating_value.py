# Generated by Django 3.2 on 2022-03-09 06:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('houses', '0020_auto_20220308_2358'),
    ]

    operations = [
        migrations.RenameField(
            model_name='rating',
            old_name='label',
            new_name='value',
        ),
    ]
