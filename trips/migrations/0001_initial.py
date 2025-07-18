# Generated by Django 5.2.3 on 2025-06-29 18:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("routes", "0001_initial"),
        ("users", "0001_initial"),
        ("vehicles", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Trip",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("start_time", models.DateTimeField()),
                ("end_time", models.DateTimeField(blank=True, null=True)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("scheduled", "Scheduled"),
                            ("in_progress", "In Progress"),
                            ("completed", "Completed"),
                        ],
                        default="scheduled",
                        max_length=20,
                    ),
                ),
                (
                    "driver",
                    models.ForeignKey(
                        limit_choices_to={"role": "driver"},
                        on_delete=django.db.models.deletion.CASCADE,
                        to="users.profile",
                    ),
                ),
                (
                    "route",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="routes.route"
                    ),
                ),
                (
                    "vehicle",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="vehicles.vehicle",
                    ),
                ),
            ],
        ),
    ]
