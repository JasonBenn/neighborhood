# Generated by Django 3.2 on 2022-03-10 19:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('houses', '0023_auto_20220310_1825'),
    ]

    operations = [
        migrations.AddField(
            model_name='rating',
            name='zillow_scraped_address',
            field=models.TextField(default='DELETE'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='rating',
            name='zillow_snapshot',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='houses.zillowsnapshot'),
        ),
    ]