from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# represents a class
class Course(models.Model):
    name = models.CharField(max_length=56)
    section = models.CharField(max_length=4)
    build_code = models.CharField(max_length=3)
    start_time = models.DateTimeField(blank=True)
    end_time = models.DateTimeField(blank=True)
    section_days = models.CharField(max_length=10)
    user = models.ForeignKey(User, related_name = 'users_courses')
    disc = models.BooleanField(default=False)
    link = models.CharField(max_length=1024)
    def __unicode__(self):
      return self.name

    
# # the route that the user will take from start_location to end_location
# class Route(models.Model):
#     start = models.ForeignKey(Course, related_name = 'class_start_location')
#     end = models.ForeignKey(Course, related_name = 'class_end_location')
#     user = models.ForeignKey(User)
    
# represents a point of interest
class Spot(models.Model):
    name = models.TextField()
    lat = models.DecimalField(max_digits=20, decimal_places=12)
    lon = models.DecimalField(max_digits=20, decimal_places=12)
    user = models.ForeignKey(User, related_name = 'users_spots')
