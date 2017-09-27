import collections
from django.apps import apps
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import DetailView, ListView, TemplateView, UpdateView, CreateView
from django_filters.views import FilterView

from . import filters, models, forms


class IndexView(TemplateView):
    template_name = 'icw/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context.update({
            'recent_citations': models.Citation.objects.filter(status='200').order_by('-created')[:10],
            'earliest': models.Accident.objects.order_by('date')[0],
            'latest': models.Accident.objects.order_by('-date')[0],
            'fatality_count': models.Casualty.objects.filter(severity_id=1).count(),
        })
        return context


class AccidentListView(FilterView):
    model = models.Accident
    queryset = models.Accident.objects.select_related('vehicle_distribution', 'casualty_distribution', 'severity')
    paginate_by = 100
    filterset_class = filters.AccidentFilter
    ordering = ['date', 'date_and_time']

    def get_reference_data(self):
        data = {}
        for model in apps.get_models():
            if issubclass(model, models.ReferenceModel) and not model._meta.abstract:
                data[model.__name__] = collections.OrderedDict([(instance.id, instance) for instance in model.objects.all()])
        return data


class AccidentDetailView(DetailView):
    model = models.Accident

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'citation_form': forms.NewCitationForm(),
        })
        return context


class CitationCreateView(LoginRequiredMixin, CreateView):
    model = models.Citation
    form_class = forms.NewCitationForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        accident = get_object_or_404(models.Accident, pk=self.kwargs['accident_pk'])
        kwargs['instance'] = models.Citation(created_by=self.request.user,
                                             accident=accident)
        return kwargs

    def get_success_url(self):
        return reverse('accident-detail', kwargs={'pk': self.kwargs['accident_pk']}) + '#citations'


class CasualtyDistributionListView(ListView):
    model = models.CasualtyDistribution
    paginate_by = 200
    ordering = ['-count']


class VehicleDistributionListView(ListView):
    model = models.VehicleDistribution
    paginate_by = 200
    ordering = ['-count']


class CitationListView(ListView):
    model = models.Citation
    paginate_by = 200
    ordering = ['-created']


class ProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = forms.ProfileForm

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return self.request.build_absolute_uri()