# Generated by Django 3.2.12 on 2024-04-26 05:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app2', '0009_alter_booking_booked_by'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking',
            name='seller_listing',
        ),
    ]
