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

admin.site.register(models.Accident, AccidentAdmin)


class VehicleAdmin(admin.ModelAdmin):
    list_display = ('id', 'accident_id', 'type')
    readonly_fields = ('accident',)

admin.site.register(models.Vehicle, VehicleAdmin)


class CasualtyAdmin(admin.ModelAdmin):
    list_display = ('id', 'accident_id', 'type', 'severity')
    readonly_fields = ('accident', 'vehicle')

admin.site.register(models.Casualty, CasualtyAdmin)

