from django.db import models

from ..models import Accident, Vehicle, Casualty


class Organization(models.Model):
    label = models.TextField()
    homepage = models.URLField(blank=True)


class PersonType(models.Model):
    id = models.SlugField(primary_key=True)
    label = models.CharField(max_length=128)


class Offence(models.Model):
    id = models.SlugField(primary_key=True)
    label = models.CharField(max_length=128)
    alternative_verdicts = models.ManyToManyField('self', blank=True)


class AccidentAnnotation(models.Model):
    accident = models.OneToOneField(Accident, related_name='_annotation')

    title = models.TextField(blank=True)
    description = models.TextField(blank=True)


class VehicleAnnotation(models.Model):
    accident = models.ForeignKey(Accident)
    vehicle = models.OneToOneField(Vehicle, related_name='_annotation')

    operator = models.ForeignKey(Organization)


class Person(models.Model):
    accident = models.ForeignKey(Accident)
    vehicle = models.ForeignKey(Vehicle)
    person_type = models.ForeignKey(PersonType)
    casualty = models.ForeignKey(Casualty, null=True, blank=True)

    name = models.TextField()
    injury_description = models.TextField()
    date_of_death = models.DateField(null=True, blank=True)

    prosecution_started = models.NullBooleanField(default=False)

class Prosecution(models.Model):
    organization = models.ForeignKey(Organization, null=True, blank=True)
    person = models.ForeignKey(Person, null=True, blank=True)
    private = models.BooleanField(default=False)


class ProsecutionOutcome(models.Model):
    id = models.SlugField(primary_key=True)
    label = models.CharField(max_length=128)


class Charge(models.Model):
    prosecution = models.ForeignKey(Prosecution)
    outcome = models.ForeignKey(ProsecutionOutcome)
    charged_offence = models.ForeignKey(Offence, related_name='charged')
    verdict_offence = models.ForeignKey(Offence, null=True, blank=True, related_name='verdict')
