# Generated by Django 4.2.11 on 2024-05-07 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app2', '0012_booking_statusmanage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='statusmanage',
            field=models.CharField(default='pending', max_length=200),
        ),
    ]
