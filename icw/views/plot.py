import calendar
import collections
import operator

from django.db.models import Count
from django.views.generic import TemplateView
import plotly.offline as opy
import plotly.graph_objs as go

from .. import filters, forms, models

__all__ = ['AccidentPlotView', 'CasualtyPlotView']


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

