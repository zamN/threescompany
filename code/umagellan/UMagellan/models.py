from django.db import models
from django.contrib.auth.models import User

# represents a class
class Course(models.Model):
    department = models.ForeignKey(User)
    number = models.IntegerField()
    section = models.IntegerField()
    building = models.TextField(max_length = 3) 
    room = models.IntegerField()
    user = models.ForeignKey(User, related_name = 'users_courses')
    
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