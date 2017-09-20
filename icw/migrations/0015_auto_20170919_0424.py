# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-19 04:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('icw', '0014_auto_20170919_0413'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='casualty',
            options={'ordering': ('accident', 'casualty_ref')},
        ),
        migrations.AlterModelOptions(
            name='vehicle',
            options={'ordering': ('accident', 'vehicle_ref')},
        ),
        migrations.AlterField(
            model_name='casualty',
            name='age_band',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='icw.AgeBand'),
        ),
        migrations.AlterField(
            model_name='casualty',
            name='casualty_class',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='icw.CasualtyClass'),
        ),
        migrations.AlterField(
            model_name='casualty',
            name='severity',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='icw.CasualtySeverity'),
        ),
        migrations.AlterField(
            model_name='casualty',
            name='sex',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='icw.Sex'),
        ),
        migrations.AlterField(
            model_name='casualty',
            name='type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='icw.VehicleType'),
        ),
    ]
