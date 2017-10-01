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

X_CHOICES = (
    ('year', 'year'),
    ('month', 'month'),
    ('month-of-year', 'month of year'),
    ('hour-of-day', 'hour of day'),
    ('police-force', 'police force'),
)


class PlotForm(forms.Form):
    x = forms.ChoiceField(choices=X_CHOICES)