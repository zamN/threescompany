from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
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
from django.core.exceptions import ObjectDoesNotExist
from models import UserProfile

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

def SetHome(request):
    if request.method == 'POST':
        try:
            profile = UserProfile.objects.get(user=request.user)
        except:
            profile = UserProfile()
            profile.user = request.user
            
        profile.home = request.POST.get('user_home')
        profile.save()

    return render(request, 'index.html', None, context_instance = RequestContext(request))
        

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

        return render(request, self.template_name, {'form': form}, context_instance = RequestContext(request))

'''
delete a course object from the database
'''
def delete_course(request, course_id):
    try:
        course = Course.objects.get(id=course_id)
        course.delete()
    except:
        pass # course doesn't exist
    return HttpResponse("Course deleted successfully") # redirect back to home page

'''
add new course object to the database
'''
def add_course(request):
    course = request.GET.get('course')
    section = request.GET.get('section')
    response_data = {}
    response_data['error'] = False
    response_data['error_msg'] = ''

    # print course
    # print section

    if len(section) != 4:
      if len(section) == 3:
        section = "0" + section
      else:
        response_data['error'] = True
        response_data['error_msg'] = 'Section ID is invalid!'
        return HttpResponse(json.dumps(response_data), mimetype="application/json")


    page_url = "https://ntst.umd.edu/soc/all-courses-search.html?course=" + course + "&section=" + section + "&term=201308&level=ALL"
    page = urllib2.urlopen(page_url).read()
    soup = BeautifulSoup(page)

    if soup.find("div", {"class" : "no-courses-message"}) != None:
      response_data['error'] = True
      response_data['error_msg'] = 'That course does not exist!'
      return HttpResponse(json.dumps(response_data), mimetype="application/json")

    if len(course) <= 4:
      response_data['error'] = True
      response_data['error_msg'] = 'That course does not exist!'
      return HttpResponse(json.dumps(response_data), mimetype="application/json")

    course_container = soup.find("div", {"class" : "courses-container"})
    first_block = course_container.find("div", {"class" : "course"}, {"id": course})

    if first_block == None:
      response_data['error'] = True
      response_data['error_msg'] = 'That course does not exist!'
      return HttpResponse(json.dumps(response_data), mimetype="application/json")

    class_block = first_block.find('div', {'class' : 'class-days-container'})
    classes = class_block.findAll('div', {'class' : 'row'})
    response_data['courses'] = []
    for i in range(0, len(classes)):
      c = Course()
      c.name = course.upper()
      c.section = section

      room = classes[i].find('span', {'class' : 'class-room'}).text

      if room != None:
        if room == 'ONLINE':
          response_data['error'] = True
          response_data['error_msg'] = 'Cannot add online classes!'
          return HttpResponse(json.dumps(response_data), mimetype="application/json")
        else:
          c.room_number = room

      c.build_code = classes[i].find('span', {'class' : 'building-code'}).text

      class_start = classes[i].find('span', {'class' : 'class-start-time'}).text
      c.start_time =  parser.parse(class_start)

      class_end = classes[i].find('span', {'class' : 'class-end-time'}).text
      c.end_time = parser.parse(class_end)

      c.section_days = classes[i].find('span', {'class' : 'section-days'}).text
      c.link = page_url


      if classes[i].find('span', {'class' : 'class-type'}) != None:
        c.tag = classes[i].find('span', {'class' : 'class-type'}).text
      try:
        c.user = User.objects.get(id = request.user.id)
      except ObjectDoesNotExist:
        response_data['error'] = True
        response_data['error_msg'] = 'User not logged in.'
        return HttpResponse(json.dumps(response_data), mimetype="application/json")
      if Course.objects.filter(name=c.name, start_time=c.start_time, section_days=c.section_days, user=c.user).exists() != True:
        course_info = {}
        course_info = {}
        course_info['name']         = c.name
        course_info['section']      = c.section
        course_info['build_code']   = c.build_code
        course_info['room_number']  = c.room_number
        course_info['start_time']   = c.start_time.strftime("%H:%M")
        course_info['end_time']     = c.end_time.strftime("%H:%M")
        course_info['section_days'] = []
        split_days(course_info['section_days'], c.section_days)
        course_info['user']         = c.user.username
        course_info['link']         = c.link
        course_info['tag']          = '' if c.tag == None else c.tag
        c.save()
        course_info['id']           = c.id
        response_data['courses'].append(course_info)
      else:
        response_data['error'] = True
        response_data['error_msg'] = 'Course already exists!'
        return HttpResponse(json.dumps(response_data), mimetype="application/json")

    response_data['error'] = False
    response_data['error_msg'] = ''
    return HttpResponse(json.dumps(response_data), mimetype="application/json")

def get_course(request):
    course = request.GET.get('course')
    section = request.GET.get('section')
    response_data = {}

    if course == None and section == None:
      try:
        resp = Course.objects.filter(user=User.objects.get(id = request.user.id))
        response_data['courses'] = []
        fill_table(response_data, resp)
        response_data['error'] = False
        response_data['error_msg'] = ''
        return HttpResponse(json.dumps(response_data), mimetype="application/json")
      except ObjectDoesNotExist:
        response_data['error'] = True
        response_data['error_msg'] = 'User not logged in.'
        return HttpResponse(json.dumps(response_data), mimetype="application/json")

    if course == None and section != None:
      response_data['error'] = True
      response_data['error_msg'] = 'You must enter a course!'
      return HttpResponse(json.dumps(response_data), mimetype="application/json")
    elif course != None and section == None:
      response_data['error'] = True
      response_data['error_msg'] = 'You must enter a section!'
      return HttpResponse(json.dumps(response_data), mimetype="application/json")

    if section != None and len(section) != 4:
      if len(section) == 3:
        section = "0" + section
      else:
        response_data['error'] = True
        response_data['error_msg'] = 'That section ID is Invalid!'
        return HttpResponse(json.dumps(response_data), mimetype="application/json")

    try:
      resp = Course.objects.filter(name=course, section=section, user=User.objects.get(id = request.user.id))
    except ObjectDoesNotExist:
      response_data['error'] = True
      response_data['error_msg'] = 'That username does not exist!'
      return HttpResponse(json.dumps(response_data), mimetype="application/json")

    if len(resp) == 0:
      response_data['error'] = True
      response_data['error_msg'] = 'That class/section was not found!'
      return HttpResponse(json.dumps(response_data), mimetype="application/json")

    response_data['courses'] = []
    fill_table(response_data, resp)

    return HttpResponse(json.dumps(response_data), mimetype="application/json")

def fill_table(table, resp):
    for r in resp:
      course_info = {}
      course_info['name']         = r.name
      course_info['section']      = r.section
      course_info['build_code']   = r.build_code
      course_info['room_number']  = r.room_number
      course_info['start_time']   = r.start_time.strftime("%H:%M")
      course_info['end_time']     = r.end_time.strftime("%H:%M")
      course_info['section_days'] = []

      split_days(course_info['section_days'], r.section_days)

      course_info['user']         = r.user.username
      course_info['link']         = r.link
      course_info['tag']          = r.tag
      course_info['id']           = r.id
      table['courses'].append(course_info)

def split_days(table, section_days):
    for i in range(0, len(section_days)):
      if i+1 < len(section_days) and section_days[i+1].islower():
        table.append(section_days[i] + section_days[i+1])
        i += 2
      elif not section_days[i].islower():
        table.append(section_days[i])
