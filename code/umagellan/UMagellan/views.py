from django.http import HttpResponse
from django.shortcuts import render_to_response, render
from django.template import RequestContext, loader
from bs4 import BeautifulSoup

# views go here
def index(request):
    soup = BeautifulSoup("bla")
    return render_to_response('index.html', {}, context_instance=RequestContext(request))

