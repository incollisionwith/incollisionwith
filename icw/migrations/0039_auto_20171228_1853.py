# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-28 18:53
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('icw', '0038_auto_20171104_2211'),
    ]

    operations = [
        migrations.CreateModel(
            name='EditedAccident',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('accident_id', models.CharField(blank=True, db_index=True, max_length=13)),
                ('accident', models.TextField()),
                ('vehicles', models.TextField()),
                ('casualties', models.TextField()),
                ('citations', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('moderated', models.DateTimeField(blank=True, null=True)),
                ('moderation_status', models.NullBooleanField(default=None)),
                ('version', models.PositiveSmallIntegerField(default=0)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_edited_accidents', to=settings.AUTH_USER_MODEL)),
                ('moderated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='moderated_edited_accidents', to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='modified_edited_accidents', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='Severity',
        ),
    ]