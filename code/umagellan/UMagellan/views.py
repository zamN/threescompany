from bs4 import BeautifulSoup
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render_to_response, render
from django.template import RequestContext, loader
from UMagellan.models import Course
from bs4 import BeautifulSoup
import urllib2
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

def derp(request):
    course = request.GET.get('course')
    section = request.GET.get('section')

    print course
    print section

    if len(section) != 4:
      if len(section) == 3:
        section = "0" + section
      else:
        print 'error with section id!'


    test = urllib2.urlopen("https://ntst.umd.edu/soc/all-courses-search.html?course=" + course + "&section=" + section + "&term=201308&level=ALL&time=12%3A00+PM&center=ALL").read()
    soup = BeautifulSoup(test)

    if soup.find("div", {"class" : "no-courses-message"}) == None:
      print 'derp'

    x = Course()
    x.department = request.user
    x.number = 5
    x.section = 123
    x.building = csi
    x.room = 1122
    x.user = request.user
    x.save()

    # returns:
    # all section($)
    # section times
    # building-code

    # error = true
    # error_msg = blah blah

    return render_to_response('test.html', {'soup':soup}, context_instance=RequestContext(request))
