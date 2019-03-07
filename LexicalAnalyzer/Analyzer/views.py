from __future__ import unicode_literals

from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.http.response import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from Analyzer.utils.analyzer import analyze_input

# Create your views here.


def index(request):
    return render(request, 'Analyzer/analyzer.html')


@csrf_exempt
def analyze(request):
    if request.POST:
        selected_language = request.POST['language']
        input_code = request.POST['code']
        output = analyze_input(selected_language, input_code)
        return JsonResponse({'output': selected_language})
    else:
        return render(request, 'Analyzer/analyzer.html')

