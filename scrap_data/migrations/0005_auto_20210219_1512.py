# Generated by Django 3.1.6 on 2021-02-19 09:42

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scrap_data', '0004_auto_20210219_1512'),
    ]

    operations = [
        migrations.AlterField(
            model_name='business',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 2, 19, 15, 12, 50, 320769)),
        ),
        migrations.AlterField(
            model_name='profile',
            name='extracted_datetime',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 2, 19, 15, 12, 50, 319754), null=True),
        ),
    ]
