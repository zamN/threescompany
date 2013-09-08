from django.conf.urls import patterns, include, url
from UMagellan.views import index, UserCreate
from django.contrib.auth.decorators import login_required

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Load index page
    url(r'^$', index),
    url(r'^add_course', 'UMagellan.views.add_course'),

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
)
