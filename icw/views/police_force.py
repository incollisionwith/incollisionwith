from django.views.generic import DetailView, ListView

from .. import models

__all__ = ['PoliceForceListView', 'PoliceForceDetailView']

class PoliceForceListView(ListView):
    model = models.PoliceForce


class PoliceForceDetailView(DetailView):
    model = models.PoliceForce
