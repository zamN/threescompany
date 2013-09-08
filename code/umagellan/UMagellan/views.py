from bs4 import BeautifulSoup
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render_to_response, render
from django.template import RequestContext, loader
from UMagellan.models import Course, Spot
from bs4 import BeautifulSoup
import urllib2
# from UMagellan.models import Route
from UMagellan.forms import UserForm
from django.views.generic.base import View


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
                user = User.objects.get(id=request.user.id)
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
