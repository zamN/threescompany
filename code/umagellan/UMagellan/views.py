from bs4 import BeautifulSoup
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render_to_response, render
from django.template import RequestContext, loader
from UMagellan.models import Course
# from UMagellan.models import Route
from UMagellan.models import Spot

# views go here
def index(request):
    courses = Course.objects.filter(user = request.user.id)
    routes = None
    spots = Spot.objects.filter(user = request.user.id)

    return render_to_response('index.html', 
        {'courses': courses, 'routes': routes, 'spots': spots}, 
        context_instance = RequestContext(request))