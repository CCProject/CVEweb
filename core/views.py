from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
from elasticsearch_dsl import Search
import config
import json
import subprocess
import os

class cve(object):
    def __init__(self, data):
        self.cid = data['cveid']
        self.refs = data['references']
        self.summary = data['summary']
        self.cpe2 = data['cpe2']
        self.cpe3 = data['cpe3']
        self.vendor = data['vendor']
        self.product = data['product']

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
        cveitem = cve(hit)
        cvelist.append(cveitem)
    # print cvelist
    return cvelist


def index(request):
    return render_to_response('index.html')


def docker(request):
    return render_to_response('docker.html')


@csrf_exempt
def search(request):
    if (request.method=="POST"):
        pkgname = request.POST['pkgname']
    elif (request.method=="GET"):
        pkgname = request.GET['pkgname']
    cvelist = ESsearch(pkgname)
    return render_to_response('result.html', {"cvelist": cvelist})

@csrf_exempt
def analyzeDocker(request):
    return render_to_response('docker.html')

@csrf_exempt
def analyzeDockerName(request):
    dname = request.POST['dname']
    # print dname
    res = os.popen('./script.sh ' + dname)
    for i in range(4):
        res.readline()
    pkglist = res.read().split()
    # print "pkg list"
    # print pkglist
    # for pkg in pkglist:
      #  reslist += ESsearch(pkg)
    return render_to_response('packages.html', {"pkglist": pkglist})







