# Generated by Django 3.2.12 on 2024-04-22 10:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app2', '0005_alter_listing_country'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='latitude',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='listing',
            name='longitude',
            field=models.FloatField(default=0),
        ),
    ]