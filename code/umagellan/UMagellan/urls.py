from django.conf.urls import patterns, include, url
from UMagellan.views import index, UserCreate, SetHome
from django.contrib.auth.decorators import login_required

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Load index page
    url(r'^$', index, name='home'),
    url(r'^add_course', 'UMagellan.views.add_course'),
    url(r'^get_course', 'UMagellan.views.get_course'),
    url(r'^delete_course/(?P<course_id>\d+)/', 'UMagellan.views.delete_course'),
    url(r'^delete_all_courses/$', 'UMagellan.views.delete_all_courses', name='delete_all_courses'),

    # Admin views
    url(r'^admin/', include(admin.site.urls)),

    # Course views
    url(r'^/course/create/$', 'django_cas.views.login', name = 'course_create_page'),
    url(r'^/course/edit/$', 'django_cas.views.login', name = 'course_edit_page'),
    url(r'^/course/delete/$', 'django_cas.views.login', name = 'course_delete_page'),
    
    # User views
    url(r'^login/$', 'django_cas.views.login', name = 'user_login_page'),
    url(r'^logout/$', 'django_cas.views.logout', name = 'user_logout_page'),
    url(r'^user/create/$', UserCreate.as_view(), name = 'user_create_page'),
    url(r'^user/sethome/$', 'UMagellan.views.SetHome', name = 'set_user_home'),
)
