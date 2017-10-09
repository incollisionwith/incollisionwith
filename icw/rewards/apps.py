from django import apps
from django.db.models import Sum
from django.db.models.signals import post_delete, post_save


class RewardsConfig(apps.AppConfig):
    name = 'icw.rewards'

    def ready(self):
        from . import models
        from icw.models import Citation
        post_save.connect(self.update_points, sender=models.PointsReward)
        post_delete.connect(self.update_points, sender=models.PointsReward)
        post_delete.connect(self.delete_rewards)
        post_save.connect(self.award_for_citation, sender=Citation)

    def update_points(self, instance, **kwargs):
        from . import models
        user = instance.user
        points_pending = models.PointsReward.objects.filter(
            user=user).select_related('action').aggregate(Sum('action__value'))['action__value__sum']


        points_confirmed = models.PointsReward.objects.filter(
            user=user,
            confirmed=True).select_related('action').aggregate(Sum('action__value'))['action__value__sum']

        models.Profile.objects.filter(user=user).update(points_confirmed=points_confirmed,
                                                        points_pending=points_pending)

    def delete_rewards(self, instance, **kwargs):
        from . import models
        from django.contrib.contenttypes.models import ContentType
        for reward in models.PointsReward.objects.filter(
                subject_content_type=ContentType.objects.get_for_model(instance),
                subject_id=instance.pk):
            reward.delete()

    def award_for_citation(self, instance, created, **kwargs):
        from . import models
        from django.contrib.contenttypes.models import ContentType

        if created:
            models.PointsReward.objects.create(user=instance.created_by,
                                        confirmed=True,
                                        subject_content_type=ContentType.objects.get_for_model(instance),
                                        subject_id=instance.id,
                                        action_id='add-citation')
