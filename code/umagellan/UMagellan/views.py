from bs4 import BeautifulSoup
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render_to_response, render
from django.template import RequestContext, loader
from UMagellan.models import Course, Spot
from bs4 import BeautifulSoup
import urllib2
import json
# from UMagellan.models import Route
from UMagellan.forms import UserForm
from django.views.generic.base import View
from UMagellan.models import Spot
from dateutil import parser
from django.core import serializers

# views go here
def index(request):
    courses = Course.objects.filter(user = request.user.id)
    routes = None
    spots = Spot.objects.filter(user = request.user.id)
    
    try:
        user = User.objects.get(id=request.user.id)
    except:
        user = None

    return render_to_response('index.html', 
        {'courses': courses, 'routes': routes, 'spots': spots, 'user': user}, 
        context_instance = RequestContext(request))

'''    
form to create/register new user
'''
class UserCreate(View):
    form_class = UserForm
    template_name = 'user_create.html'
    
    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            try:
                user = User.objects.get(id = request.user.id)
            except:
                user = User()
                
            user.first_name = cd['first_name']
            user.last_name = cd['last_name']
            user.email = cd['email']
            user.password = cd['password']
            user.save()
                
            return HttpResponseRedirect('home')

        return render(request, self.template_name, {'form': form})
        context_instance = RequestContext(request)

def add_course(request):
    course = request.GET.get('course')
    section = request.GET.get('section')
    response_data = {}
    response_data['error'] = False
    response_data['error_msg'] = ''
    response_data['course'] = None

    print course
    print section

    if len(section) != 4:
      if len(section) == 3:
        section = "0" + section
      else:
        response_data['error'] = True
        response_data['error_msg'] = 'Section ID is Invalid!'
        return HttpResponse(json.dumps(response_data), mimetype="application/json")


    test = urllib2.urlopen("https://ntst.umd.edu/soc/all-courses-search.html?course=" + course + "&section=" + section + "&term=201308&level=ALL&time=12%3A00+PM&center=ALL").read()
    soup = BeautifulSoup(test)

    if soup.find("div", {"class" : "no-courses-message"}) != None:
      response_data['error'] = True
      response_data['error_msg'] = 'Course does not exist!'
      return HttpResponse(json.dumps(response_data), mimetype="application/json")

    #x = Course()
    #x.name = "Hello"
    #x.section = "1234"
    #x.build_code = "CSI"
    #x.user = User.objects.get(id = request.user.id)
    #x.save()

    #class_days = cmsc131.find('div', {'class' : 'class-days-container'}).prettify()
    #cmsc131 =  coursec.find("div", {"class" : "course"}, {"id" : "CMSC131"})
    #coursec = soup.find("div", {"class" : "courses-container"})

    course_container = soup.find("div", {"class" : "courses-container"})
    first_block = course_container.find("div", {"class" : "course"}, {"id": course})

    if first_block == None:
      response_data['error'] = True
      response_data['error_msg'] = 'Course does not exist!'
      return HttpResponse(json.dumps(response_data), mimetype="application/json")
    else:
      class_block = first_block.find('div', {'class' : 'class-days-container'})
      classes = class_block.findAll('div', {'class' : 'row'})
      for i in range(0, len(classes)):
        c = Course()
        c.name = course
        c.section = section
        c.build_code = classes[i].find('span', {'class' : 'building-code'}).text

        class_start = classes[i].find('span', {'class' : 'class-start-time'}).text
        c.start_time =  parser.parse(class_start)

        class_end = classes[i].find('span', {'class' : 'class-end-time'}).text
        c.end_time = parser.parse(class_end)

        c.section_days = classes[i].find('span', {'class' : 'section-days'}).text
        c.user = User.objects.get(id = request.user.id)
        c.save()

    # returns:
    # all section($)
    # section times
    # building-code

    # error = true
    # error_msg = blah blah

    response_data['error'] = False
    response_data['error_msg'] = ''
    response_data['course-name'] = c.name
    response_data['course-section'] = c.section
    response_data['course-build_code'] = c.build_code
    response_data['course-start_time'] = c.start_time.strftime('%H:%M')
    response_data['course-end_time'] = c.end_time.strftime('%H:%M')
    response_data['course-section_days'] = c.section_days
    return HttpResponse(json.dumps(response_data), mimetype="application/json")
