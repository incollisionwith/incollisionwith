from django import forms
from django.contrib.auth.models import User

from . import models


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