import django_filters

from . import models


class AccidentFilter(django_filters.FilterSet):
    date = django_filters.DateFromToRangeFilter(label='Date range')
    casualty_distribution = django_filters.ModelMultipleChoiceFilter(queryset=models.CasualtyDistribution.objects.order_by('-count'))
    vehicle_distribution = django_filters.ModelMultipleChoiceFilter(queryset=models.VehicleDistribution.objects.order_by('-count'))
    has_citations = django_filters.BooleanFilter()
    number_of_vehicles = django_filters.RangeFilter()
    number_of_casualties = django_filters.RangeFilter()

    class Meta:
        model = models.Accident
        fields = ['date', 'severity', 'has_citations', 'number_of_vehicles', 'number_of_casualties',
                  'casualty_distribution', 'vehicle_distribution']

class CasualtyFilter(django_filters.FilterSet):
    date = django_filters.DateFromToRangeFilter(name='accident__date', label='Date range')
    pedestrian_hit_by = django_filters.ModelChoiceFilter(queryset=models.VehicleType.objects.exclude(id=0))

    class Meta:
        model = models.Casualty
        fields = ['date', 'type', 'severity', 'age_band', 'vehicle__location', 'pedestrian_location',
                  'pedestrian_hit_by']
