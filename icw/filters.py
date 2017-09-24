import django_filters

from . import models


class AccidentFilter(django_filters.FilterSet):
    date = django_filters.DateFromToRangeFilter(label='Date range')
    casualty_distribution = django_filters.ModelMultipleChoiceFilter(queryset=models.CasualtyDistribution.objects.order_by('-count'))
    vehicle_distribution = django_filters.ModelMultipleChoiceFilter(queryset=models.VehicleDistribution.objects.order_by('-count'))
    citations = django_filters.BooleanFilter()

    class Meta:
        model = models.Accident
        fields = ['date', 'severity', 'citations', 'casualty_distribution', 'vehicle_distribution']
