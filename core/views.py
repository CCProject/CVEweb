from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
from elasticsearch_dsl import Search
import config
import json


class cve(object):
    def __init__(self, _vid, _refs, _summary, _cpe2, _cpe3, _vender, _product):
        self.vid = _vid
        self.refs = _refs
        self.summary = _summary
        self.cpe2 = _cpe2
        self.cpe3 = _cpe3
        self.vender = _vender
        self.product = _product

    def toJSON(self):
        return json.dumps(self.__dict__)

def createESConnection():
    awsauth = AWS4Auth(config.es_access_key, config.es_access_secret, config.es_region, config.es_name)
    es = Elasticsearch(
        hosts=[{'host': config.es_host, 'port': config.es_port}],
        http_auth=awsauth,
        use_ssl=True,
        verify_certs=True,
        connection_class=RequestsHttpConnection
    )
    return es

def ESsearch(pkgname):
    es = createESConnection()
    query = Search(index='t2').using(es).query("match", product=pkgname)
    res = query.scan()
    cvelist = []
    for hit in res:
        cvelist.append(hit)
    return cvelist


def index(request):
    return render_to_response('index.html')


def docker(request):
    return render_to_response('docker.html')


@csrf_exempt
def search(request):
    pkgname = request.POST['pkgname']
    cvelist = ESsearch(pkgname)
    return render_to_response('result.html')


@csrf_exempt
def analyzeDocker(request):
    return render_to_response('docker.html')
