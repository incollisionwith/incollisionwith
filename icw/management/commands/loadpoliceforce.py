import csv
import datetime
import functools
import pkgutil
import sys

import rdflib
import yaml
from SPARQLWrapper import SPARQLWrapper2, JSON
from django.core.management import BaseCommand

from ... import models
from ...util import indexed

class Command(BaseCommand):
    query_pattern = """\
        SELECT * WHERE {{
            VALUES ?uri {{ {uris} }}
            OPTIONAL {{ ?uri rdfs:label ?label . FILTER (LANG(?label) = "en") }}
            OPTIONAL {{ ?uri rdfs:comment ?comment . FILTER (LANG(?comment) = "en") }}
            OPTIONAL {{ ?uri foaf:homepage ?homepage }}
            OPTIONAL {{ ?uri foaf:depiction ?logo_url }}
        }}
    """

    dbpedia_resource_prefix = 'http://dbpedia.org/resource/'

    def handle(self, *args, **options):
        data = yaml.load(pkgutil.get_data('icw', 'data/police_force.yaml'))
        for datum in data:
            datum['uri'] = rdflib.URIRef(self.dbpedia_resource_prefix + datum.pop('dbpedia'))

        ids = {str(datum['uri']): datum['id'] for datum in data}

        dbpedia = SPARQLWrapper2('http://dbpedia.org/sparql')

        dbpedia.setQuery(self.query_pattern.format(uris=' '.join(d['uri'].n3() for d in data)))
        dbpedia.setReturnFormat(JSON)
        results = dbpedia.query().convert()

        import pprint
        pprint.pprint(results)

        for binding in results.bindings:
            police_force = models.PoliceForce(id=ids[binding['uri'].value],
                                     **{k: v.value for k, v in binding.items()})
            police_force.save()
