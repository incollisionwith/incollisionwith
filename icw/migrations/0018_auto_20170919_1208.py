# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-19 12:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('icw', '0017_auto_20170919_0518'),
    ]

    operations = [
        migrations.CreateModel(
            name='VehicleDistribution',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('distribution', models.TextField(unique=True)),
                ('count', models.IntegerField(default=0)),
            ],
        ),
        migrations.AddField(
            model_name='accident',
            name='vehicle_distribution',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='icw.VehicleDistribution'),
        ),
    ]
