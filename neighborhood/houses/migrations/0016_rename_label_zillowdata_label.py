# Generated by Django 3.2 on 2022-03-06 05:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('houses', '0015_addresses'),
    ]

    operations = [
        migrations.RenameField(
            model_name='zillowdata',
            old_name='Label',
            new_name='label',
        ),
    ]