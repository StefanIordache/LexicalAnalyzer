from django.conf.urls import url
from Analyzer.views import index
from Analyzer.views import analyze
from django.conf.urls import (
    handler400, handler403, handler404, handler500
)

urlpatterns = [
    url(r'^analyze/$', analyze, name='analyze'),
    url(r'^', index, name='index'),
]
