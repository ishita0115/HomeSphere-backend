# Generated by Django 4.2.11 on 2024-05-01 06:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0002_alter_user_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='profilephoto',
            field=models.ImageField(null=True, upload_to='profilephoto'),
        ),
    ]
