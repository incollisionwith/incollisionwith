from django.views.generic import TemplateView

from .. import filters

__all__ = ['MapView']


class MapView(TemplateView):
    template_name = 'icw/map.html'

    def get_context_data(self, **kwargs):
        return {
            'form': filters.AccidentFilter().form,
        }