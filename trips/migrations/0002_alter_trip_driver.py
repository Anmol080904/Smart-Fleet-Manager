# Generated by Django 5.2.3 on 2025-07-01 12:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("drivers", "0001_initial"),
        ("trips", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="trip",
            name="driver",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="drivers.driver"
            ),
        ),
    ]
