from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
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


def ESsearch(pkgname):
    cvelist = []
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
