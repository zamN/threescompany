from django.http import HttpResponse
from django.shortcuts import render_to_response, render
from django.template import RequestContext, loader

# views go here
def index(request):
    return render_to_response('example.html', {}, context_instance=RequestContext(request))