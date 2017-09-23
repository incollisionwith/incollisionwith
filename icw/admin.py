from django.contrib import admin

from . import models

for name in dir(models):
    model = getattr(models, name, None)
    if isinstance(model, type) and issubclass(model, models.ReferenceModel) and not model._meta.abstract:
        class MA(admin.ModelAdmin):
            list_display = ('id', 'label')
        admin.site.register(model, MA)


class AccidentAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'severity', 'number_of_vehicles', 'number_of_casualties')
    list_filter = ('severity', 'number_of_vehicles', 'number_of_casualties')


class VehicleAdmin(admin.ModelAdmin):
    list_display = ('id', 'accident_id', 'type')
    readonly_fields = ('accident',)


class CasualtyAdmin(admin.ModelAdmin):
    list_display = ('id', 'accident_id', 'type', 'severity')
    readonly_fields = ('accident', 'vehicle')


class DistributionAdmin(admin.ModelAdmin):
    list_display = ('id', '_get_html', 'as_text', 'count')

    def _get_html(self, obj):
        return obj.as_html
    _get_html.allow_tags = True

    class Media:
        css = {
             'all': ('lib/font-awesome-4.7.0/css/font-awesome.min.css',)
        }


class AccidentAnnotationAdmin(admin.ModelAdmin):
    list_display = ('id', 'accident_id', 'title')
    readonly_fields = ('accident',)


class CitationAdmin(admin.ModelAdmin):
    pass


admin.site.register(models.Accident, AccidentAdmin)
admin.site.register(models.Vehicle, VehicleAdmin)
admin.site.register(models.Casualty, CasualtyAdmin)
admin.site.register(models.CasualtyDistribution, DistributionAdmin)
admin.site.register(models.VehicleDistribution, DistributionAdmin)
admin.site.register(models.AccidentAnnotation, AccidentAnnotationAdmin)
admin.site.register(models.Citation, CitationAdmin)