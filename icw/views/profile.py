from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView
from social_core.tests.models import User

from .. import forms

__all__ = ['ProfileView']


class ProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = forms.ProfileForm

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return self.request.build_absolute_uri()
