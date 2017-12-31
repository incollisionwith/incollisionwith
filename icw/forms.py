import re
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from leaflet.forms.fields import PointField

from . import models


class AccidentForm(forms.ModelForm):
    location = PointField()
    time = forms.TimeField(required=False)
    road_1 = forms.CharField(required=False)
    road_2 = forms.CharField(required=False)
    police_attended = forms.NullBooleanField()
    record_state = forms.ModelChoiceField(queryset=models.AccidentRecordState.objects.exclude(official=True))

    def clean_location(self):
        location = self.cleaned_data['location']
        try:
            self.instance.highway_authority = models.HighwayAuthority.objects.get(geometry__contains=location)
        except models.HighwayAuthority.DoesNotExist:
            raise ValidationError("Location does not fall within the boundary of any UK highway authority")
        try:
            self.instance.police_force = models.PoliceForce.objects.get(geometry__contains=location)
        except models.PoliceForce.DoesNotExist:
            raise ValidationError("Location does not fall within the boundary of any UK police force")
        return location

    def get_initial_for_field(self, field, field_name):
        if field_name == 'time':
            return self.instance.date_and_time.time() if self.instance.date_and_time else None
        elif field_name == 'road_1':
            if self.instance.road_1_class_id:
                return self.instance.road_1_class.pattern.format(self.instance.road_1_number)
        elif field_name == 'road_2':
            if self.instance.road_2_class_id:
                return self.instance.road_2_class.pattern.format(self.instance.road_2_number)
        else:
            return super().get_initial_for_field(field, field_name)

    def clean(self):
        cleaned_data = self.cleaned_data
        self.instance.road_1_class_id, self.instance.road_2_class_id = 0, 0
        self.instance.road_1_number, self.instance.road_2_number = None, None
        for rc in models.RoadClass.objects.exclude(id=0):
            match = re.match(re.escape(rc.pattern).replace(r'\{\}', r'(\d+)'), cleaned_data['road_1'])
            if match:
                self.instance.road_1_class = rc
                self.instance.road_1_number = int(match.group(1)) if len(match.groups()) > 1 else None
            match = re.match(re.escape(rc.pattern).replace(r'\{\}', r'(\d+)'), cleaned_data['road_2'])
            if match:
                self.instance.road_2_class = rc
                self.instance.road_2_number = int(match.group(1)) if len(match.groups()) > 1 else None


    class Meta:
        model = models.Accident
        fields = ('location', 'record_state', 'description', 'date', 'time', 'police_attended', 'junction_control',
                  'junction_detail', 'road_1', 'road_2', 'road_type',
                  'speed_limit', 'pedestrian_crossing_human', 'pedestrian_crossing_physical', 'light_conditions',
                  'weather', 'road_surface', 'special_conditions', 'carriageway_hazards', 'urban_rural')


class VehicleForm(forms.ModelForm):
    type = forms.ModelChoiceField(queryset=models.VehicleType.objects.exclude(id=0))

    class Meta:
        model = models.Vehicle
        fields = ('type', 'towing_and_articulation', 'location', 'manoeuvre', 'junction_location',
                  'hit_object_in_carriageway', 'hit_object_off_carriageway', 'first_point_of_impact',
                  'skidding_and_overturning', 'leaving_carriageway', )


VehicleFormSet = forms.inlineformset_factory(models.Accident, models.Vehicle, VehicleForm,
                                             extra=3, min_num=1, validate_min=1)
VehicleFormSet = forms.formset_factory(VehicleForm, extra=3, min_num=1, validate_min=1)


class CasualtyForm(forms.ModelForm):
    vehicle_ref = forms.IntegerField()
    severity = forms.ModelChoiceField(queryset=models.CasualtySeverity.objects.all())

    class Meta:
        model = models.Casualty
        fields = ('vehicle_ref', 'casualty_class', 'severity', 'sex', 'age_band', 'age', 'pedestrian_location',
                  'pedestrian_movement')

CasualtyFormSet = forms.inlineformset_factory(models.Accident, models.Casualty, CasualtyForm,
                                              extra=3, min_num=1, validate_min=1)
CasualtyFormSet = forms.formset_factory(CasualtyForm, extra=3, min_num=1, validate_min=1)


class ProfileForm(forms.ModelForm):
    date_joined = forms.DateTimeField(disabled=True)
    username = forms.CharField(disabled=True)

    class Meta:
        model = User
        fields = ('date_joined', 'username', 'first_name', 'last_name')


class NewCitationForm(forms.ModelForm):
    class Meta:
        model = models.Citation
        fields = ('href',)

NewCitationFormSet = forms.modelformset_factory(models.Citation, NewCitationForm, extra=3, min_num=1, validate_min=True)

MAIN_PLOT_CHOICES = (
    ('year', 'year'),
    ('month', 'month'),
    ('month-of-year', 'month of year'),
    ('hour-of-day', 'hour of day'),
    ('police-force', 'police force'),
    ('pedestrian-hit-by', 'pedestrian hit by'),
    ('pedestrian-location', 'pedestrian location'),
    ('severity', 'severity'),
)

SUB_PLOT_CHOICES = (
    ('', '-' * 8),
) + MAIN_PLOT_CHOICES

LAYOUT_CHOICES = (
    ('', '-' * 8),
    ('group', 'group'),
    ('stack', 'stack'),
    ('relative', 'relative'),
)


class PlotForm(forms.Form):
    title = forms.CharField(required=False)
    main = forms.ChoiceField(label='X', choices=MAIN_PLOT_CHOICES, required=False)
    sub = forms.ChoiceField(label='Subplot', choices=SUB_PLOT_CHOICES, required=False)
    layout = forms.ChoiceField(choices=LAYOUT_CHOICES, required=False)