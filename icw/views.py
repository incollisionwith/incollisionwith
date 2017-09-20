import collections
from django.apps import apps
from django.views.generic import DetailView, ListView, TemplateView
from django_filters.views import FilterView

from . import filters, models


class IndexView(TemplateView):
    template_name = 'icw/index.html'


class AccidentListView(FilterView):
    model = models.Accident
    #queryset = models.Accident.objects.select_related('vehicles', 'casualties')
    paginate_by = 100
    filterset_class = filters.AccidentFilter
    ordering = ['date', 'date_and_time']

    def get_reference_data(self):
        data = {}
        for model in apps.get_models():
            if issubclass(model, models.ReferenceModel) and not model._meta.abstract:
                data[model.__name__] = collections.OrderedDict([(instance.id, instance) for instance in model.objects.all()])
        return data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'referenceData': self.get_reference_data(),
        })
        print(context)
        return context


class AccidentDetailView(DetailView):
    model = models.Accident


class CasualtyDistributionListView(ListView):
    model = models.CasualtyDistribution
    paginate_by = 200
    ordering = ['-count']


class VehicleDistributionListView(ListView):
    model = models.VehicleDistribution
    paginate_by = 200
    ordering = ['-count']
