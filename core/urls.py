from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^search$', views.search),
    url(r'^docker$', views.docker),
    url(r'^analyzeDocker$', views.analyzeDocker),
    url(r'^analyzeDockerName', views.analyzeDockerName),
]
