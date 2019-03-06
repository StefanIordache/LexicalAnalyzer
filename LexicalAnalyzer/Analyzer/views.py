from __future__ import unicode_literals

from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.http.response import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.


def index(request):
    return render(request, 'Analyzer/analyzer.html')


@csrf_exempt
def analyze(request):
    if request.POST:
        selected_language = request.POST['language']
        input_code = request.POST['code']
        print('ceva')
        return HttpResponse(selected_language, content_type="application/json")
    else:
        return render(request, 'Analyzer/analyzer.html')

