# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-09 20:23
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


def populate(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    ContentType = apps.get_model('contenttypes', 'ContentType')
    Citation = apps.get_model('icw', 'Citation')
    Profile = apps.get_model('rewards', 'Profile')
    PointsReward = apps.get_model('rewards', 'PointsReward')
    PointsAction = apps.get_model('rewards', 'PointsAction')

    add_citation = PointsAction.objects.create(id='add-citation', value=2)

    # Create profiles for all existing users
    for user in User.objects.all():
        Profile.objects.get_or_create(user=user)

    for citation in Citation.objects.all():
        PointsReward.objects.create(user=citation.created_by,
                                    confirmed=True,
                                    created=citation.created,
                                    subject_content_type=ContentType.objects.get_for_model(citation),
                                    subject_id=citation.id,
                                    action=add_citation)


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PointsAction',
            fields=[
                ('id', models.SlugField(primary_key=True, serialize=False)),
                ('text', models.TextField(blank=True)),
                ('font_awesome', models.CharField(max_length=16)),
                ('value', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='PointsReward',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('confirmed', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('subject_id', models.CharField(max_length=64)),
                ('action', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rewards.PointsAction')),
                ('subject_content_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='points_rewards', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('points_confirmed', models.PositiveIntegerField(default=0, help_text='Points that have been confirmed through moderation')),
                ('points_pending', models.PositiveIntegerField(default=0, help_text='Points that would be accrued if everything were moderated')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='rewards_profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RunPython(populate, migrations.RunPython.noop),
    ]
