from __future__ import unicode_literals

from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout

# Create your views here.


def index(request):
    import sys
    if sys.version_info[0] < 3:
        raise Exception("Please switch to Python 3 versions")
    else:
        print(sys.version_info[0])
    return render(request, 'Analyzer/analyzer.html')
