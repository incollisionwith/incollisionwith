from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin

from . import views

admin.autodiscover()


urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^incident/$', views.AccidentListView.as_view(), name='accident-list'),
    url(r'^casualty-distribution/$', views.CasualtyDistributionListView.as_view(), name='casualty-distribution-list'),
    url(r'^vehicle-distribution/$', views.VehicleDistributionListView.as_view(), name='vehicle-distribution-list'),
    url(r'^incident/(?P<pk>[A-Z0-9]{13})/$', views.AccidentDetailView.as_view(), name='accident-detail'),
    url(r'^admin/', admin.site.urls),
]


if settings.DEBUG and 'debug_toolbar' in settings.INSTALLED_APPS:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns