from django.views.generic import ListView

from .. import models

__all__ = ['CasualtyDistributionListView', 'VehicleDistributionListView']


class CasualtyDistributionListView(ListView):
    model = models.CasualtyDistribution
    paginate_by = 200
    ordering = ['-count']


class VehicleDistributionListView(ListView):
    model = models.VehicleDistribution
    paginate_by = 200
    ordering = ['-count']


