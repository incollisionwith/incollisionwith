from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.views import LogoutView

from . import views

admin.autodiscover()


urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^incident/$', views.AccidentListView.as_view(), name='accident-list'),
    url(r'^casualty-distribution/$', views.CasualtyDistributionListView.as_view(), name='casualty-distribution-list'),
    url(r'^vehicle-distribution/$', views.VehicleDistributionListView.as_view(), name='vehicle-distribution-list'),
    url(r'^incident/(?P<pk>[A-Z0-9]{13})/$', views.AccidentDetailView.as_view(), name='accident-detail'),
    url(r'^incident/(?P<accident_pk>[A-Z0-9]{13})/citation/new/$', views.CitationCreateView.as_view(), name='citation-create'),
    url(r'^admin/', admin.site.urls),
    url(r'^reference/$', views.CitationListView.as_view(), name='citation-list'),
    url(r'', include('social_django.urls', namespace='social')),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^profile/$', views.ProfileView.as_view(), name='profile'),
]


if settings.DEBUG and 'debug_toolbar' in settings.INSTALLED_APPS:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns