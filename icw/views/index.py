import collections
from datetime import timedelta

from django.utils.timezone import now
from django.views.generic import TemplateView

from .. import models

__all__ = ['IndexView']


class IndexView(TemplateView):
    template_name = 'icw/index.html'

    def get_context_data(self, **kwargs):
        import icw.rewards.models
        context = super().get_context_data()

        recent_leaderboard = collections.defaultdict(int)
        for points_award in icw.rewards.models.PointsReward.objects.filter(
                created__gte=now()-timedelta(7)).select_related('action', 'user'):
            recent_leaderboard[points_award.user] += points_award.action.value
        recent_leaderboard = sorted(recent_leaderboard.items(), key=lambda i: -i[1])[:10]

        context.update({
            'recent_citations': models.Citation.objects.filter(status='200').order_by('-created')[:5],
            'earliest': models.Accident.objects.order_by('date')[0],
            'latest': models.Accident.objects.order_by('-date')[0],
            'fatality_count': models.Casualty.objects.filter(severity_id=1).count(),
            'full_leaderboard': icw.rewards.models.Profile.objects.order_by('-points_pending')[:10],
            'recent_leaderboard': recent_leaderboard,
        })
        return context

