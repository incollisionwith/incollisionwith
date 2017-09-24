from django.apps import AppConfig
from django.db.models.signals import post_save


class ICWConfig(AppConfig):
    name = 'icw'

    def ready(self):
        from . import models
        post_save.connect(self.citation_saved, models.Citation)

    def citation_saved(self, instance, created, **kwargs):
        if created and instance.annotation.accident:
            instance.annotation.accident.citations = True
            instance.annotation.accident.save(force_update=True)
