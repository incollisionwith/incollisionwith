from django_filters.views import FilterView

from .. import filters, models

__all__ = ['CasualtyListView']


class CasualtyListView(FilterView):
    model = models.Casualty
    queryset = models.Casualty.objects.select_related('accident').prefetch_related(
        'severity', 'vehicle', 'type', 'sex', 'type', 'vehicle', 'vehicle__type', 'pedestrian_location',
        'vehicle__location')
    paginate_by = 100
    filterset_class = filters.CasualtyFilter
    ordering = ['accident__date', 'accident__date_and_time']
