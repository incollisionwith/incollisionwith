import calendar

import operator

import collections
import http.client

from datetime import timedelta
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.db.models import Count, Sum
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils.timezone import now
from django.views.generic import DetailView, ListView, TemplateView, UpdateView, CreateView
from django.views.generic.edit import ProcessFormView, FormView
from django_filters.views import FilterView
import plotly.offline as opy
import plotly.graph_objs as go

from . import filters, models, forms


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


class AccidentListView(FilterView):
    model = models.Accident
    queryset = models.Accident.objects.select_related('vehicle_distribution', 'casualty_distribution', 'severity')
    paginate_by = 100
    filterset_class = filters.AccidentFilter
    ordering = ['date', 'date_and_time']


class CasualtyListView(FilterView):
    model = models.Casualty
    queryset = models.Casualty.objects.select_related('accident').prefetch_related(
        'severity', 'vehicle', 'type', 'sex', 'type', 'vehicle', 'vehicle__type', 'pedestrian_location',
        'vehicle__location')
    paginate_by = 100
    filterset_class = filters.CasualtyFilter
    ordering = ['accident__date', 'accident__date_and_time']


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

    def form_valid(self, form):
        try:
            return super().form_valid(form)
        except IntegrityError:
            return render(self.request, 'icw/citation_already_exists.html', context={
                'accident_pk': self.kwargs['accident_pk']
            }, status=http.client.CONFLICT)

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


class ReferenceProgressView(TemplateView):
    template_name = 'icw/reference_progress.html'

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


class PlotView(TemplateView):
    template_name = 'icw/plot.html'
    model = None
    form_class = None
    filter_class = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        form = context['form'] = self.form_class(self.request.GET)

        filter = context['filter'] = self.filter_class(self.request.GET,
                                                       self.model.objects.order_by())
        queryset = filter.qs

        plots = {
            'main': {
                'title': '',
                'variables': (),
                'rename': lambda x: x,
            },
            'sub': {
                'title': '',
                'variables': (),
                'rename': lambda x: x,
            }
        }

        if form.is_valid():
            if self.model != models.Accident:
                queryset = queryset.extra(tables=['icw_accident'], where=['icw_casualty.accident_id = icw_accident.id'])
            for plot_name, plot in plots.items():
                if form.cleaned_data[plot_name] == 'month':
                    plot['variables'] = ('year', 'month')
                    plot['title'] = 'Month'
                    queryset = queryset.extra(select={'year': 'EXTRACT(year FROM date)', 'month': 'EXTRACT(month FROM date)'})
                elif form.cleaned_data[plot_name] == 'month-of-year':
                    plot['variables'] = ('month',)
                    plot['title'] = 'Month of year'
                    plot['rename'] = lambda month_number: calendar.month_abbr[int(month_number)]
                    queryset = queryset.extra(select={'month': 'EXTRACT(month FROM date)'})
                elif form.cleaned_data[plot_name] == 'police-force':
                    plot['variables'] = ('police_force_id',)
                    plot['title'] = 'Police force'
                    plot['rename'] = {p.id: p.label for p in models.PoliceForce.objects.all()}.get
                    queryset = queryset.extra(select={'police_force_id': 'icw_accident.police_force_id'})
                elif form.cleaned_data[plot_name] == 'pedestrian-hit-by':
                    plot['variables'] = ('pedestrian_hit_by_id',)
                    plot['title'] = 'Vehicle type that hit pedestrian'
                    plot['rename'] = {s.id: s.label for s in models.VehicleType.objects.all()}.get
                    queryset = queryset.filter(pedestrian_hit_by__isnull=False)
                elif form.cleaned_data[plot_name] == 'pedestrian-location':
                    plot['variables'] = ('pedestrian_location_id',)
                    plot['title'] = 'Pedestrian location'
                    plot['rename'] = {s.id: s.label for s in models.PedestrianLocation.objects.all()}.get
                    queryset = queryset.filter(pedestrian_location__isnull=False)
                elif form.cleaned_data[plot_name] == 'severity':
                    plot['variables'] = ('severity_id',)
                    plot['title'] = 'Severity'
                    plot['rename'] = {s.id: s.label for s in models.CasualtySeverity.objects.all()}.get
                elif form.cleaned_data[plot_name] == 'pedestrian-hit-by':
                    plot['variables'] = ('pedestrian_hit_by_id',)
                    plot['title'] = 'Pedestrian hit by'
                    plot['rename'] = {s.id: s.label for s in models.VehicleType.objects.all()}.get
                    queryset = queryset.filter(pedestrian_hit_by__isnull=False)
                elif form.cleaned_data[plot_name] == 'year' or plot_name == 'main':  # this is the default for the main plot
                    plot['variables'] = ('year',)
                    plot['title'] = 'Year'
                    queryset = queryset.extra(select={'year': 'EXTRACT(year FROM date)'})


            queryset = queryset.values(*plots['main']['variables'], *plots['sub']['variables']).annotate(count=Count('*'))

            print(queryset.query)

            main_values, sub_values = set(), set()
            yss = collections.defaultdict(lambda: collections.defaultdict(int))
            get_main_plot = operator.itemgetter(*plots['main']['variables'])
            get_sub_plot = operator.itemgetter(*plots['sub']['variables']) if plots['sub']['variables'] else lambda result: None

            for result in queryset:
                main_plot = get_main_plot(result)
                sub_plot = get_sub_plot(result)

                main_values.add(main_plot)
                sub_values.add(sub_plot)

                print("P", result, main_plot, sub_plot)

                yss[main_plot][sub_plot] = result['count']

            traces = []
            for y_key in sorted(sub_values, key=plots['sub']['rename']):
                xs = sorted(main_values, key=plots['main']['rename'])
                ys = [yss[x][y_key] for x in xs]
                print(xs, ys, y_key)
                trace = go.Bar(x=list(map(plots['main']['rename'], xs)),
                               y=ys,
                               name=plots['sub']['rename'](y_key))
                print()
                traces.append(trace)

            import pprint
            pprint.pprint(yss)

            data=go.Data(traces)
            layout=go.Layout(title=form.cleaned_data.get('title', 'Plot'),
                             xaxis={'title': plots['main']['title']},
                             yaxis={'title': 'Count'},
                             barmode=form.cleaned_data.get('layout', 'group'))
            figure=go.Figure(data=data,layout=layout)
            div = opy.plot(figure, auto_open=False, output_type='div')

            context['graph'] = div

        return context


class AccidentPlotView(PlotView):
    model = models.Accident
    form_class = forms.PlotForm
    filter_class = filters.AccidentFilter


class CasualtyPlotView(PlotView):
    model = models.Casualty
    form_class = forms.PlotForm
    filter_class = filters.CasualtyFilter


class MapView(TemplateView):
    template_name = 'icw/map.html'

    def get_context_data(self, **kwargs):
        return {
            'form': filters.AccidentFilter().form,
        }