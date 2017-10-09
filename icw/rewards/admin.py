from django.contrib import admin

from . import models

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'points_confirmed', 'points_pending')

admin.site.register(models.PointsAction)
admin.site.register(models.PointsReward)
admin.site.register(models.Profile, ProfileAdmin)
