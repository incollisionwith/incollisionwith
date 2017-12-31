from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.core import serializers
from django.db import transaction
from django.forms import BaseFormSet
from django.forms import ModelForm
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, View
from django_filters.views import FilterView
from django.views.generic.edit import CreateView, UpdateView
from django_jinja.views.generic import ListView
from sequences import get_next_value
from waffle.decorators import waffle_flag

from .. import filters, forms, models


__all__ = ['AccidentListView', 'AccidentCreateView', 'AccidentDetailView',
           'AccidentUpdateView', 'EditedAccidentListView', 'EditedAccidentDetailView']


def get_formset_objects(formset):
    objects = []
    for form in formset.initial_forms:
        if form.instance.pk and form not in formset.deleted_forms:
            objects.append(form.instance)
    for form in formset.extra_forms:
        if form.has_changed() and not (formset.can_delete and formset._should_delete_form(form)):
            objects.append(form.instance)
    return objects

def get_field_data(form, obj):
    return {f: getattr(obj, f) for f in form._meta.fields}

class AccidentListView(FilterView):
    model = models.Accident
    queryset = models.Accident.objects.select_related('vehicle_distribution', 'casualty_distribution', 'severity')
    paginate_by = 100
    filterset_class = filters.AccidentFilter
    ordering = ['date', 'date_and_time']


class AccidentEditView(PermissionRequiredMixin, View):
    model = models.EditedAccident
    form_class = forms.AccidentForm
    accident = None
    object = None

    def get_object(self, **kwargs):
        object = super().get_object()
        self.accident = object.to_accident()
        return object

    def get_form_kwargs(self, **kwargs):
        kwargs = super().get_form_kwargs(**kwargs)
        kwargs['instance'] = self.accident
        return kwargs

    def get_context_data(self, **kwargs):
        # import logging
        # logging.basicConfig(level=logging.DEBUG)
        # logging.getLogger('django.db').setLevel(logging.DEBUG)
        context = super().get_context_data(**kwargs)
        context.update({
            'accident': self.accident,
            'vehicle_formset': forms.VehicleFormSet(self.request.POST or None,
                                                    initial=[get_field_data(forms.VehicleForm, v) for v in self.accident.all_vehicles] if self.accident else None,
                                                    prefix='vehicle'),
            'casualty_formset': forms.CasualtyFormSet(self.request.POST or None,
                                                    initial=[get_field_data(forms.CasualtyForm, v) for v in self.accident.all_casualties] if self.accident else None,
                                                    prefix='casualty'),
            'citation_formset': forms.NewCitationFormSet(self.request.POST or None, prefix='citation',
                                                         queryset=models.Citation.objects.none()),
        })
        return context

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        #self.object = self.get_object(**kwargs)
        context = self.context = self.get_context_data()
        is_valid = True
        for k in context:
            if isinstance(context[k], (ModelForm, BaseFormSet)):
                is_valid = context[k].is_valid() and is_valid
        if is_valid:
            if not context['form'].instance.id:
                year = context['form'].cleaned_data['date'].year
                context['form'].instance.id = 'ICW{:4}{:006}'.format(year,
                                                                     get_next_value('user-accident-{}'.format(year)))
            context['form'].instance.number_of_vehicles = len(get_formset_objects(context['vehicle_formset']))
            context['form'].instance.number_of_casualties = len(get_formset_objects(context['casualty_formset']))
            context['form'].instance.severity_id = min(
                cd['severity'].id for cd in context['casualty_formset'].cleaned_data if cd)
            for i, form in enumerate(context['vehicle_formset'], 1):
                if form.cleaned_data and not form.instance.vehicle_ref:
                    form.instance.vehicle_ref = i
            for i, form in enumerate(context['casualty_formset'], 1):
                if form.cleaned_data and not form.instance.vehicle_ref:
                    form.instance.casualty_ref = i
            for form in context['citation_formset']:
                form.instance.accident_id = context['form'].instance.id
                form.instance.created_by = request.user
            return self.form_valid(context['form'])
        else:
            return self.form_invalid(context['form'])

    def form_valid(self, form):
        json_serializer = serializers.get_serializer("json")()
        edited_accident = models.EditedAccident(
            accident_id=form.instance.id,
            accident=json_serializer.serialize([form.instance]),
            vehicles=json_serializer.serialize(get_formset_objects(self.context['vehicle_formset'])),
            casualties=json_serializer.serialize(get_formset_objects(self.context['casualty_formset'])),
            citations=json_serializer.serialize(get_formset_objects(self.context['citation_formset'])),
            created_by=self.request.user,
            modified_by=self.request.user,
        )
        edited_accident.save()
        return HttpResponseRedirect(edited_accident.get_absolute_url())


@method_decorator(waffle_flag('beta'), 'dispatch')
#@method_decorator(flow.flow_start_view, 'dispatch')
class AccidentCreateView(AccidentEditView, CreateView):
    permission_required = 'icw.add_accident'

    # def get_form_kwargs(self):
    #     kwargs = super().get_form_kwargs()
    #     kwargs['instance'] = models.Accident(record_state_id=1)  # User-submitted, not yet moderated
    #     return kwargs


@method_decorator(waffle_flag('beta'), 'dispatch')
class AccidentUpdateView(AccidentEditView, UpdateView):
    permission_required = 'icw.modify_accident'

    def get(self, request, **kwargs):
        return super().get(request, **kwargs)


class AccidentDetailView(DetailView):
    model = models.Accident

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'citation_form': forms.NewCitationForm(),
        })
        return context


class EditedAccidentListView(LoginRequiredMixin, FilterView):
    model = models.EditedAccident
    paginate_by = 100


class EditedAccidentDetailView(LoginRequiredMixin, DetailView):
    model = models.EditedAccident

    template_name = 'icw/accident_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'accident': context['object'].to_accident(),
        })
        return context

    @method_decorator(permission_required('icw.moderate_accident'))
    def post(self, request, **kwargs):
        object = self.get_object()
        if 'approve' in request.POST:
            object.moderation_status = True
            object.save()
            return redirect(reverse('accident-detail', kwargs={'pk': object.accident_id}))
        elif 'reject' in request.POST:
            object.moderation_status = False
            object.save()
        return redirect(object.get_absolute_url())