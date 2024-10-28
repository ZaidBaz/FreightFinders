# Generated by Django 5.1.2 on 2024-10-27 02:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="LoadPosting",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("load_id", models.CharField(max_length=255)),
                ("posting_status", models.CharField(max_length=255)),
                ("source_system", models.CharField(max_length=255)),
                ("has_appointments", models.BooleanField()),
                ("is_hazardous", models.BooleanField()),
                ("is_high_value", models.BooleanField()),
                ("is_temperature_controlled", models.BooleanField()),
                ("total_distance", models.FloatField()),
                ("distance_uom", models.CharField(max_length=10)),
                ("total_weight", models.FloatField()),
                ("weight_uom", models.CharField(max_length=10)),
                ("number_of_stops", models.IntegerField()),
                ("transport_mode", models.CharField(max_length=255)),
                ("created_date", models.DateTimeField()),
                ("updated_date", models.DateTimeField()),
                ("managed_equipment", models.BooleanField()),
                ("load_number_alias", models.CharField(max_length=255)),
                ("is_carb", models.BooleanField()),
                ("fpc", models.BooleanField()),
                ("fpo", models.BooleanField()),
                ("division", models.CharField(max_length=255)),
            ],
            options={
                "db_table": "load_posting",
            },
        ),
        migrations.CreateModel(
            name="LoadStop",
            fields=[
                (
                    "stop_id",
                    models.CharField(max_length=255, primary_key=True, serialize=False),
                ),
                ("id", models.BigIntegerField()),
                ("load_id", models.CharField(db_index=True, max_length=255)),
                ("stop_sequence", models.SmallIntegerField(db_index=True)),
                ("stop_type", models.CharField(max_length=255)),
                ("activity_type", models.CharField(max_length=255)),
                ("appointment_from", models.DateTimeField()),
                ("appointment_to", models.DateTimeField()),
                ("city", models.CharField(max_length=255)),
                ("state", models.CharField(max_length=255)),
                ("postal_code", models.CharField(max_length=20)),
                ("time_zone", models.CharField(max_length=100)),
                ("country", models.CharField(max_length=100)),
                ("created_date", models.DateTimeField()),
                ("updated_date", models.DateTimeField()),
                ("appointment_state", models.CharField(max_length=255)),
            ],
            options={
                "db_table": "load_stop",
                "indexes": [
                    models.Index(
                        fields=["load_id", "stop_sequence"],
                        name="load_stop_load_id_780baf_idx",
                    )
                ],
            },
        ),
    ]