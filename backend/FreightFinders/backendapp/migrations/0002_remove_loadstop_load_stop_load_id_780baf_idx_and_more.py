# Generated by Django 5.1.2 on 2024-10-28 05:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backendapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='loadstop',
            name='load_stop_load_id_780baf_idx',
        ),
        migrations.RemoveField(
            model_name='loadposting',
            name='id',
        ),
        migrations.AlterField(
            model_name='loadposting',
            name='load_id',
            field=models.CharField(max_length=255, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='loadstop',
            name='load_id',
            field=models.ForeignKey(db_column='load_id', on_delete=django.db.models.deletion.CASCADE, related_name='loadid_stops', to='backendapp.loadposting'),
        ),
        migrations.AlterField(
            model_name='loadstop',
            name='stop_sequence',
            field=models.SmallIntegerField(),
        ),
    ]
