from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='rewards_profile')
    points_confirmed = models.PositiveIntegerField(default=0,
        help_text="Points that have been confirmed through moderation")
    points_pending = models.PositiveIntegerField(default=0,
        help_text="Points that would be accrued if everything were moderated")


class PointsAction(models.Model):
    id = models.SlugField(primary_key=True)
    text = models.TextField(blank=True)
    font_awesome = models.CharField(max_length=16)
    value = models.PositiveIntegerField()


class PointsReward(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='points_rewards')
    action = models.ForeignKey(PointsAction)
    confirmed = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True)

    subject_content_type = models.ForeignKey(ContentType, null=True, blank=True)
    subject_id = models.CharField(max_length=64)
    subject = GenericForeignKey('subject_content_type', 'subject_id')

