import http.client

import collections
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError
from django.db.models import Count
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.generic import CreateView, TemplateView
from django_jinja.views.generic import ListView

from .. import forms, models

__all__ = ['CitationListView', 'CitationCreateView', 'CitationProgressView']


class CitationListView(ListView):
    model = models.Citation
    paginate_by = 200
    ordering = ['-created']


class CitationCreateView(LoginRequiredMixin, CreateView):
    model = models.Citation
    form_class = forms.NewCitationForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        accident = get_object_or_404(models.Accident, pk=self.kwargs['accident_pk'])
        kwargs['instance'] = models.Citation(created_by=self.request.user,
                                             accident=accident)
        return kwargs

    def form_valid(self, form):
        try:
            return super().form_valid(form)
        except IntegrityError:
            return render(self.request, 'icw/citation_already_exists.html', context={
                'accident_pk': self.kwargs['accident_pk']
            }, status=http.client.CONFLICT)

    def get_success_url(self):
        return reverse('accident-detail', kwargs={'pk': self.kwargs['accident_pk']}) + '#citations'


class CitationProgressView(TemplateView):
    template_name = 'icw/citation_progress.html'

    def get_context_data(self, **kwargs):
        categories = [
            ('Pedestrians killed on a footway or verge',
             {'casualties__in': models.Casualty.objects.filter(severity_id=1, pedestrian_location_id=6)}),
            ('Pedestrians killed',
             {'casualties__in': models.Casualty.objects.filter(severity_id=1, type_id=0)}),
            ('Pedestrians killed in collision with a pedal cycle',
             {'casualties__in': models.Casualty.objects.filter(severity_id=1, pedestrian_hit_by=1)}),
            ('Cyclists killed',
             {'casualties__in': models.Casualty.objects.filter(severity_id=1, type_id=1)}),
            ('All road deaths',
             {'severity_id': 1}),
        ]

        counts = []
        for label, filter in categories:
            category_counts = collections.defaultdict(lambda: {'yes': 0, 'no': 0})
            queryset = models.Accident.objects \
                .filter(**filter) \
                .extra(select={'year': 'EXTRACT(year FROM date)'}).values('year', 'has_citations') \
                .annotate(count=Count('*'))
            for result in queryset:
                category_counts[int(result['year'])]['yes' if result['has_citations'] else 'no'] = result['count']
            for value in category_counts.values():
                value['total'] = value['yes'] + value['no']
            counts.append({
                'label': label,
                'counts': sorted(category_counts.items(), reverse=True),
            })
        return {'counts': counts}
