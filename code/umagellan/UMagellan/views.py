from bs4 import BeautifulSoup
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render_to_response, render
from django.template import RequestContext, loader
from UMagellan.models import Course

# views go here
def index(request):
    courses = Course.objects.filter(user = request.user.id)

    return HttpResponse('index.html', {'courses': courses}, 
        context_instance = RequestContext(request))