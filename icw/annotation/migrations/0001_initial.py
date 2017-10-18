# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-18 09:04
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('icw', '0033_auto_20171018_0904'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccidentAnnotation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(blank=True)),
                ('description', models.TextField(blank=True)),
                ('accident', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='_annotation', to='icw.Accident')),
            ],
        ),
    ]
