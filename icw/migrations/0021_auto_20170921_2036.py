# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-21 20:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('icw', '0020_auto_20170921_0936'),
    ]

    operations = [
        migrations.AddField(
            model_name='casualtydistribution',
            name='as_html',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='casualtydistribution',
            name='as_text',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='vehicledistribution',
            name='as_html',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='vehicledistribution',
            name='as_text',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
