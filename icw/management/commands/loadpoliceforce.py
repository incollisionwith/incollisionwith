from ctypes import c_void_p

import functools
import pkgutil
import shutil
import tempfile
import zipfile

import rdflib
import requests
import yaml
from SPARQLWrapper import SPARQLWrapper2, JSON
from django.contrib.gis.gdal import DataSource, OGRGeometry
from django.contrib.gis.gdal.libgdal import lgdal
from django.contrib.gis.gdal.prototypes.generation import void_output
from django.contrib.gis.gdal.prototypes.geom import geom_union
from django.core.management import BaseCommand

from ... import models

flatten_to_2d = void_output(lgdal.OGR_G_FlattenTo2D, [c_void_p])


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

    area_url = 'https://data.police.uk/data/boundaries/force_kmls.zip'

    def handle(self, *args, **options):
        data = yaml.load(pkgutil.get_data('icw', 'data/police_force.yaml'))
        for datum in data:
            datum['uri'] = rdflib.URIRef(self.dbpedia_resource_prefix + datum['dbpedia'])
            datum['kml'] = datum.get('kml', datum['dbpedia'].lower().rsplit('_', 1)[0].replace('_', '-'))

        data_by_uri = {str(datum['uri']): datum for datum in data}

        dbpedia = SPARQLWrapper2('http://dbpedia.org/sparql')

        dbpedia.setQuery(self.query_pattern.format(uris=' '.join(d['uri'].n3() for d in data)))
        dbpedia.setReturnFormat(JSON)
        results = dbpedia.query().convert()

        for binding in results.bindings:
            data_by_uri[binding['uri'].value]['dbpedia'] = binding

        with tempfile.NamedTemporaryFile(suffix='.zip') as f:
            response = requests.get(self.area_url, stream=True)
            response.raw.read = functools.partial(response.raw.read, decode_content=True)
            shutil.copyfileobj(response.raw, f)
            response.close()
            f.seek(0)
            boundary_zip = zipfile.ZipFile(f)

            for datum in data:
                police_force = models.PoliceForce(id=datum['id'],
                                         **{k: v.value for k, v in datum['dbpedia'].items()})

                try:
                    kml = boundary_zip.open('force kmls/' + datum['kml'] + '.kml')
                except KeyError as e:
                    if datum.get('authorities'):
                        authorities = models.HighwayAuthority.objects.filter(id__in=datum['authorities'])
                        geoms = [a.geometry for a in authorities]
                        assert len(geoms) == len(datum['authorities'])
                        geom = geoms[0]
                        for g in geoms[1:]:
                            geom = geom.union(g)
                        police_force.geometry = geom
                    else:
                        police_force.geometry = None
                else:
                    with tempfile.NamedTemporaryFile(suffix='.kml') as kml_f:
                        shutil.copyfileobj(kml, kml_f)
                        kml_f.flush()
                        for layer in DataSource(kml_f.name):
                            for feature in layer:
                                geom = OGRGeometry(feature.geom.wkt)
                                flatten_to_2d(geom.ptr)
                                police_force.geometry = geom.geos

                police_force.save()
