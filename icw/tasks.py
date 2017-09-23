import functools
from io import BytesIO

from celery import shared_task
import dateutil.parser
import html5lib
import newspaper
import requests
import rdflib

from . import models


SCHEMA = rdflib.Namespace('http://schema.org/')


def first_non_null(func):
    @functools.wraps(func)
    def f(*args, **kwargs):
        for item in func(*args, **kwargs):
            if item:
                return item
    return f


@first_non_null
def get_citation_title(doc, uri, og, graph, article):
    if uri:
        yield graph.value(uri, SCHEMA.headline)
    yield og.get('og:title')
    try:
        yield (doc.find('{http://www.w3.org/1999/xhtml}head').find('{http://www.w3.org/1999/xhtml}title').text or '').strip() or None
    except AttributeError:
        pass
    return article.title

@first_non_null
def get_citation_description(doc, uri, og, graph, article):
    if uri:
        yield graph.value(uri, SCHEMA.articleBody)
    yield og.get('og:description', '').strip() or None


@first_non_null
def get_citation_published(doc, uri, og, graph, article):
    try:
        yield dateutil.parser.parse(og.get('article:published_time'))
    except (TypeError, ValueError):
        pass
    if uri:
        published = graph.value(uri, SCHEMA.datePublished)
        if published:
            yield published.toPython()

    return article.publish_date


@first_non_null
def get_citation_publisher(doc, uri, og, graph, article):
    if uri:
        publisher = graph.value(uri, SCHEMA.publisher)
        if publisher:
            yield graph.value(uri, SCHEMA.name)
    yield og.get('og:site_name')


@shared_task
def fetch_citation(pk):
    citation = models.Citation.objects.get(pk=pk)

    try:
        response = requests.get(citation.href)
        response.raise_for_status()
    except requests.ConnectionError:
        citation.status = '444'
    except requests.HTTPError as e:
        citation.status = str(e.response.status_code)[:3]
    else:
        citation.status = response.status_code

        doc = html5lib.parse(response.content)
        article = newspaper.Article(url=citation.href)
        article.download(input_html=response.content)
        article.parse()

        graph = rdflib.Graph()
        for jsonld in doc.iter('{http://www.w3.org/1999/xhtml}script'):
            if jsonld.attrib.get('type') == 'application/ld+json':
                graph.parse(BytesIO(jsonld.text.encode()), response.url, format='json-ld')

        og = [n for n in doc.iter('{http://www.w3.org/1999/xhtml}meta') if
              n.attrib.get('property', '').split(':')[0] in ('og', 'article') and 'content' in n.attrib]
        og = {n.attrib['property']: n.attrib['content'] for n in og}

        uri = graph.value(None, SCHEMA.url, rdflib.URIRef(response.url))

        citation.title = get_citation_title(doc, uri, og, graph, article) or ''
        citation.description = get_citation_description(doc, uri, og, graph, article) or ''
        citation.published = get_citation_published(doc, uri, og, graph, article)
        citation.publisher = get_citation_publisher(doc, uri, og, graph, article) or ''

        citation.image_url = og.get('og:image')
        citation.content = article.text or ''

    citation.save()
